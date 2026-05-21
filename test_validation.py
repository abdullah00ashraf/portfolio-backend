import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import Publication
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

fake_pdf = SimpleUploadedFile("fake.pdf", b"this is not a pdf file but just text", content_type="application/pdf")

pub = Publication(title='Fake', authors='Fake', journal_conference_name='Fake', year_of_publication=2024, abstract='Fake', pdf_file=fake_pdf)
try:
    pub.full_clean()
    print('Failed: Validation did not catch fake PDF')
except ValidationError as e:
    print('Success: Validation caught fake PDF', e)
