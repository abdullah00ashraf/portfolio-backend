import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import ValidationMilestone

def seed_credentials_vault():
    # Flush existing indicators to clear any legacy structural conflicts
    ValidationMilestone.objects.all().delete()

    milestones = [
        {
            "title": "Letter of Appreciation // AI Kit Demonstration",
            "authority": "Dr. A.P.J. Abdul Kalam AI Lab Inauguration",
            "type": "AWARD",
            "date": date(2025, 9, 15),
            "order": 1
        },
        {
            "title": "Team Leader Distinction // 'The Aegis' (Team ID 75864)",
            "authority": "Smart India Hackathon 2025",
            "type": "MILESTONE",
            "date": date(2025, 12, 20),
            "order": 2
        },
        {
            "title": "'Carbon Smart' Sustainability Certification",
            "authority": "Infosys Springboard Sustainability Initiative",
            "type": "CERTIFICATION",
            "date": date(2025, 10, 5),
            "order": 3
        },
        {
            "title": "First Prize // Nagar Stariya Vigyan Mela (City Science Fair)",
            "authority": "Lucknow Municipal Science Registry",
            "type": "AWARD",
            "date": date(2017, 11, 10),
            "order": 4
        }
    ]

    for m in milestones:
        ValidationMilestone.objects.create(
            title=m["title"],
            issuing_authority=m["authority"],
            classification=m["type"],
            date_secured=m["date"],
            order=m["order"],
            drive_folder_id="1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W"  # Dynamic cloud binding
        )

    print(f"Successfully populated {len(milestones)} cryptographic credentials into the active ledger.")

if __name__ == '__main__':
    seed_credentials_vault()
