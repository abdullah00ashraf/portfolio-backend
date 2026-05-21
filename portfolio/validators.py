import magic
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_is_pdf(file):
    # Read the first 2048 bytes
    initial_pos = file.tell()
    file.seek(0)
    file_data = file.read(2048)
    file.seek(initial_pos)

    # Use python-magic to get MIME type
    mime_type = magic.from_buffer(file_data, mime=True)

    if mime_type != 'application/pdf':
        raise ValidationError(
            _("Unsupported file type. Only PDF files are allowed. Detected: %(mime_type)s"),
            params={'mime_type': mime_type},
        )

def validate_is_video(file):
    # Read the first 2048 bytes
    initial_pos = file.tell()
    file.seek(0)
    file_data = file.read(2048)
    file.seek(initial_pos)

    # Use python-magic to get MIME type
    mime_type = magic.from_buffer(file_data, mime=True)

    allowed_mimetypes = ['video/mp4', 'video/quicktime', 'video/x-m4v']
    if mime_type not in allowed_mimetypes:
        raise ValidationError(
            _("Unsupported file type. Only MP4 and MOV videos are allowed. Detected: %(mime_type)s"),
            params={'mime_type': mime_type},
        )
