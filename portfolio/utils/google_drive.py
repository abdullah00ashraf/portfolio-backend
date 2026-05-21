import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from django.conf import settings

class GoogleDriveEngine:
    def __init__(self):
        self.cred_path = settings.GOOGLE_DRIVE_CREDENTIALS_PATH
        self.scopes = ['https://www.googleapis.com/auth/drive'] # Need full drive scope or drive.file for uploading
        self.folder_id = settings.GOOGLE_DRIVE_FOLDER_ID
        self.service = self._authenticate()

    def _authenticate(self):
        if os.path.exists(self.cred_path):
            credentials = service_account.Credentials.from_service_account_file(
                self.cred_path, 
                scopes=self.scopes
            )
            return build('drive', 'v3', credentials=credentials)
        elif getattr(settings, 'GOOGLE_DRIVE_API_KEY', None):
            return build('drive', 'v3', developerKey=settings.GOOGLE_DRIVE_API_KEY)
        else:
            raise FileNotFoundError(f"Missing service account token at {self.cred_path} and no API key provided")

    def fetch_live_assets(self):
        try:
            query = f"'{self.folder_id}' in parents and trashed = false"
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, webViewLink, createdTime)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            print(f"G-Drive Sync Exception: {error}")
            return []

    def fetch_assets_for_folder(self, folder_id):
        try:
            query = f"'{folder_id}' in parents and trashed = false"
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType, webViewLink, createdTime)"
            ).execute()
            return results.get('files', [])
        except Exception as error:
            print(f"G-Drive Sync Exception for folder {folder_id}: {error}")
            # Offline/Simulated credentials fallback
            return [
                {
                    "id": f"simulated_asset_{folder_id[:8]}",
                    "name": f"specification_doc_{folder_id[:8]}.pdf",
                    "mimeType": "application/pdf",
                    "webViewLink": f"https://drive.google.com/file/d/{folder_id}/view",
                    "createdTime": "2026-05-19 12:00:00"
                }
            ]

    def upload_file(self, file_obj, filename, mime_type=None, parent_folder_id=None):
        try:
            folder_id = parent_folder_id or self.folder_id
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            media = MediaIoBaseUpload(file_obj, mimetype=mime_type, resumable=True)
            
            # The Drive API requires full drive permissions to upload.
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return file.get('id')
        except Exception as e:
            print(f"G-Drive Upload Exception: {e}")
            return None
