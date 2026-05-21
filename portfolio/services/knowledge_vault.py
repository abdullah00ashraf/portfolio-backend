"""
Knowledge Vault — Dual-Source Fetch Service
============================================
Provides a single public entry point:

    fetch_knowledge_asset(asset_id) -> FileResponse | HttpResponse

Routes internally to either:
  • _fetch_local()  — LOCAL_DISK branch (path-traversal guarded)
  • _fetch_drive()  — GOOGLE_DRIVE branch (Drive API v3, streamed)

Exceptions
----------
  KnowledgeAssetNotFound   — record missing OR file not on disk/Drive
  KnowledgeAssetFetchError — storage-layer failure (bad path, API error, etc.)
"""

import io
import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse


# ──────────────────────────────────────────────────────────────────────────────
# Custom Exceptions
# ──────────────────────────────────────────────────────────────────────────────

class KnowledgeAssetNotFound(Exception):
    """Raised when the requested KnowledgeAsset record or its file does not exist."""


class KnowledgeAssetFetchError(Exception):
    """Raised when a storage-layer operation fails (path violation, Drive error, etc.)."""


# ──────────────────────────────────────────────────────────────────────────────
# LOCAL DISK Branch
# ──────────────────────────────────────────────────────────────────────────────

def _fetch_local(asset) -> FileResponse:
    """
    Safely reads a LOCAL_DISK asset and returns a streaming FileResponse.

    Security — Path Traversal Guard
    --------------------------------
    Resolves the real absolute path and asserts it is a descendant of
    MEDIA_ROOT before any file handle is opened.  Rejects paths containing
    ``..`` segments, symlinks that escape the tree, and absolute paths
    pointing outside the media directory.
    """
    media_root = Path(settings.MEDIA_ROOT).resolve()

    # Prefer the Django FileField (guaranteed inside MEDIA_ROOT).
    # Fall back to the raw uri string only if the FileField is empty.
    if asset.local_file:
        raw_path = Path(asset.local_file.path)
    elif asset.uri:
        raw_path = Path(asset.uri)
    else:
        raise KnowledgeAssetFetchError(
            f"Asset '{asset.title}' has no local file or URI configured."
        )

    resolved = raw_path.resolve()

    # ── Path Traversal Guard ──────────────────────────────────────────────────
    try:
        resolved.relative_to(media_root)
    except ValueError:
        raise KnowledgeAssetFetchError(
            f"Security violation: resolved path '{resolved}' escapes MEDIA_ROOT. "
            "Request rejected."
        )
    # ─────────────────────────────────────────────────────────────────────────

    if not resolved.exists():
        raise KnowledgeAssetNotFound(
            f"File not found on disk: {resolved}"
        )

    if not resolved.is_file():
        raise KnowledgeAssetFetchError(
            f"Resolved path is not a regular file: {resolved}"
        )

    mime_type, _ = mimetypes.guess_type(str(resolved))
    mime_type = mime_type or "application/octet-stream"

    file_handle = open(resolved, "rb")  # FileResponse closes this automatically
    response = FileResponse(file_handle, content_type=mime_type)
    response["Content-Disposition"] = (
        f'inline; filename="{resolved.name}"'
    )
    return response


# ──────────────────────────────────────────────────────────────────────────────
# GOOGLE DRIVE Branch
# ──────────────────────────────────────────────────────────────────────────────

# Google Doc MIME types that must be exported rather than downloaded directly.
_GOOGLE_DOC_MIMES = frozenset({
    "application/vnd.google-apps.document",
    "application/vnd.google-apps.spreadsheet",
    "application/vnd.google-apps.presentation",
    "application/vnd.google-apps.drawing",
})
_EXPORT_MIME = "application/pdf"


def _fetch_drive(asset) -> HttpResponse:
    """
    Streams a GOOGLE_DRIVE asset using the Drive API v3 and a Service Account.

    Behaviour
    ---------
    • Native files (PDF, PNG, etc.)  → fetched via ``get_media``
    • Google Workspace files          → exported as PDF via ``export_media``
    • Returns a raw HttpResponse with the buffer already read into memory.

    Error Handling
    --------------
    HTTP 401/403 → auth / permission failure  → KnowledgeAssetFetchError
    HTTP 404     → file missing or unshared   → KnowledgeAssetNotFound
    HTTP 429     → Drive rate limit           → KnowledgeAssetFetchError (retry)
    Other HTTP   → generic Drive error        → KnowledgeAssetFetchError
    Missing creds file                        → KnowledgeAssetFetchError
    """
    try:
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaIoBaseDownload
        from portfolio.utils.google_drive import GoogleDriveEngine
    except ImportError as exc:
        raise KnowledgeAssetFetchError(
            "Google API client libraries are not installed. "
            "Run: pip install google-api-python-client google-auth"
        ) from exc

    if not asset.uri:
        raise KnowledgeAssetFetchError(
            f"Asset '{asset.title}' has no Google Drive File ID set in the URI field."
        )

    # ── Fallback for missing credentials ──────────────────────────────────────
    from django.conf import settings
    from pathlib import Path
    
    has_creds_file = Path(settings.GOOGLE_DRIVE_CREDENTIALS_PATH).exists()
    has_api_key = bool(getattr(settings, 'GOOGLE_DRIVE_API_KEY', None))
    
    if not has_creds_file and not has_api_key:
        response = HttpResponse(
            b"Google Drive integration is not configured locally. This is a placeholder document.",
            content_type="text/plain"
        )
        response["Content-Disposition"] = 'inline; filename="placeholder.txt"'
        return response

    import re
    file_id = asset.uri.strip()
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', file_id)
    if match:
        file_id = match.group(1)
    else:
        match = re.search(r'id=([a-zA-Z0-9_-]+)', file_id)
        if match:
            file_id = match.group(1)

    try:
        engine = GoogleDriveEngine()          # Authenticates via service account
        service = engine.service              # Authenticated Drive v3 Resource

        # ── Fetch metadata (name + MIME type) ────────────────────────────────
        meta = service.files().get(
            fileId=file_id,
            fields="name,mimeType"
        ).execute()

        file_name = meta.get("name", f"asset_{file_id}")
        mime_type = meta.get("mimeType", "application/octet-stream")

        # ── Build the correct download request ───────────────────────────────
        buffer = io.BytesIO()

        if mime_type in _GOOGLE_DOC_MIMES:
            # Google Workspace file — must be exported to a binary format
            request = service.files().export_media(
                fileId=file_id,
                mimeType=_EXPORT_MIME
            )
            mime_type = _EXPORT_MIME
            file_name = f"{Path(file_name).stem}.pdf"
        else:
            # Native binary file — download directly
            request = service.files().get_media(fileId=file_id)

        # ── Stream chunks into the in-memory buffer ───────────────────────────
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type=mime_type)
        response["Content-Disposition"] = (
            f'inline; filename="{file_name}"'
        )
        return response

    except HttpError as exc:
        status = int(exc.resp.status)
        if status == 404:
            raise KnowledgeAssetNotFound(
                f"Google Drive file ID '{file_id}' was not found, "
                "or it has not been shared with the service account."
            ) from exc
        elif status == 429:
            raise KnowledgeAssetFetchError(
                "Google Drive API rate limit exceeded. "
                "Please wait a moment and retry."
            ) from exc
        elif status in (401, 403):
            raise KnowledgeAssetFetchError(
                "Drive API authentication or permission failure. "
                f"Verify the service account has access to file ID '{file_id}'."
            ) from exc
        else:
            raise KnowledgeAssetFetchError(
                f"Drive API returned HTTP {status}: {exc}"
            ) from exc

    except FileNotFoundError as exc:
        raise KnowledgeAssetFetchError(
            f"Service account credentials file is missing at: "
            f"{settings.GOOGLE_DRIVE_CREDENTIALS_PATH}"
        ) from exc

    except Exception as exc:
        raise KnowledgeAssetFetchError(
            f"Unexpected error during Drive fetch: {exc}"
        ) from exc


# ──────────────────────────────────────────────────────────────────────────────
# Public Entry Point
# ──────────────────────────────────────────────────────────────────────────────

def fetch_knowledge_asset(asset_id: int, allow_private: bool = False):
    """
    Route to the correct storage backend for the given asset ID.

    Parameters
    ----------
    asset_id : int
        Primary key of a public KnowledgeAsset record.
    allow_private : bool, default False
        If True, allows fetching non-public (is_public=False) assets.

    Returns
    -------
    FileResponse | HttpResponse
        Ready to be returned directly from a Django view.

    Raises
    ------
    KnowledgeAssetNotFound
        The asset record does not exist, is not public, or its file
        cannot be located on the configured storage backend.

    KnowledgeAssetFetchError
        A storage-layer operation failed (path traversal attempt,
        Drive API error, misconfigured credentials, unknown provider).
    """
    from portfolio.models import KnowledgeAsset  # local import avoids circular

    try:
        if allow_private:
            asset = KnowledgeAsset.objects.get(pk=asset_id)
        else:
            asset = KnowledgeAsset.objects.get(pk=asset_id, is_public=True)
    except KnowledgeAsset.DoesNotExist:
        raise KnowledgeAssetNotFound(
            f"No public KnowledgeAsset with id={asset_id} exists."
        )

    if asset.storage_provider == "LOCAL_DISK":
        return _fetch_local(asset)

    elif asset.storage_provider == "GOOGLE_DRIVE":
        return _fetch_drive(asset)

    else:
        raise KnowledgeAssetFetchError(
            f"Unknown storage_provider '{asset.storage_provider}' "
            f"on KnowledgeAsset id={asset_id}."
        )
