import os
import shutil
import datetime
import hashlib
import base64
from django.core.management.base import BaseCommand
from django.conf import settings
from cryptography.fernet import Fernet

class Command(BaseCommand):
    help = 'Creates an encrypted backup of the SQLite database'

    def handle(self, *args, **options):
        # 1. Setup paths
        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"db_backup_{timestamp}.enc"
        backup_path = os.path.join(backup_dir, backup_filename)

        self.stdout.write(f"Starting backup of {db_path}...")

        # 2. Generate encryption key from settings.CRYPTOGRAPHY_KEY
        # Fernet requires a 32-byte base64-encoded key
        key_source = settings.CRYPTOGRAPHY_KEY
        key = base64.urlsafe_b64encode(hashlib.sha256(key_source).digest())
        fernet = Fernet(key)

        try:
            # 3. Read DB content
            with open(db_path, 'rb') as f:
                data = f.read()

            # 4. Encrypt data
            encrypted_data = fernet.encrypt(data)

            # 5. Save encrypted backup
            with open(backup_path, 'wb') as f:
                f.write(encrypted_data)

            self.stdout.write(self.style.SUCCESS(f"Successfully created encrypted backup: {backup_path}"))
            
            # 6. Retention policy (keep last 7 days)
            # (Optional but good practice)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Backup failed: {str(e)}"))
