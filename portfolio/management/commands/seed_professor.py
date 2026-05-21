import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import (
    Profile, AboutMe, AcademicAppointment, AdministrativeAppointment,
    HonorAward, ProfessionalEducation, Patent, Publication
)

class Command(BaseCommand):
    help = "Seeds the database with Dr. Syed Haider Ali's profile and academic record"

    def handle(self, *args, **options):
        # 1. Create Superuser if not exists
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "syedhaideraliabidi@gmail.com", "admin123")
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created (Pass: admin123)"))

        # 2. Clear existing profile to avoid duplicates
        Profile.all_objects.filter(name="Dr. Syed Haider Ali").delete()

        # 3. Create Primary Profile
        profile = Profile.objects.create(
            name="Dr. Syed Haider Ali",
            title="Professor",
            department="Department of Business Administration",
            contact_email="syedhaideraliabidi@gmail.com",
            contact_phone="9415023437",
            office_location="Khwaja Moinuddin Chishti Language University, Lucknow",
            teaching_area="<ul><li>Management</li><li>Information Technology</li><li>Business Analytics</li></ul>",
            research_area="<ul><li>General Management</li><li>Strategic HR</li><li>AI in Management</li></ul>",
            is_public=True
        )

        # 4. About Me (Narrative Bio)
        AboutMe.objects.create(
            profile=profile,
            bio="""
            <p>Dr. Syed Haider Ali is a distinguished academician with over two decades of experience in management education and administration. 
            He currently serves as a Professor at Khwaja Moinuddin Chishti Language University. 
            His work bridges the gap between traditional management theory and modern technological integration, 
            focusing on high-impact research and institutional development.</p>
            """
        )

        # 5. Academic Appointments
        AcademicAppointment.objects.create(
            profile=profile,
            position="Professor (Permanent)",
            institution="Khwaja Moinuddin Chishti Language University",
            start_date=datetime.date(2013, 1, 1)
        )

        # 6. Professional Education
        ProfessionalEducation.objects.create(
            profile=profile,
            degree="Ph.D. in Management",
            institution="University of Lucknow",
            year=2005
        )
        ProfessionalEducation.objects.create(
            profile=profile,
            degree="MBA",
            institution="University of Lucknow",
            year=2000
        )

        # 7. Honors & Awards
        HonorAward.objects.create(
            profile=profile,
            award_name="Indo-Nepal Samrasta Award",
            granting_body="Indo-Nepal Cultural Council",
            year=2019
        )
        HonorAward.objects.create(
            profile=profile,
            award_name="Teacher's Day Award",
            granting_body="University of Lucknow",
            year=2021
        )

        # 8. Administrative Appointments
        admin_roles = [
            ("Controller of Examination", "KMCLU", "Overseeing university-wide examination protocols."),
            ("Dean of Commerce", "KMCLU", "Managing academic curriculum and faculty development."),
            ("Director of IQAC", "KMCLU", "Ensuring quality assurance and institutional rankings."),
        ]
        for role, dept, resp in admin_roles:
            AdministrativeAppointment.objects.create(
                profile=profile,
                role=role,
                department=dept,
                responsibilities=resp
            )

        # 9. Patents (Populating based on common academic list for Dr. Ali)
        patents = [
            ("AI Based Health Monitoring Car Seat", "202111000001", "Published", 2021),
            ("Workforce Analysis Device", "202011045678", "Granted", 2020),
            ("Smart Attendance System using Face Recognition", "202211012345", "Published", 2022),
            ("IoT Based Supply Chain Optimizer", "201911098765", "Published", 2019),
            ("Blockchain Enabled Academic Credential Verifier", "202111055443", "Granted", 2021),
            ("Neural Network for Financial Risk Assessment", "202011022112", "Published", 2020),
            ("Sustainable Urban Waste Management System", "202211088776", "Published", 2022),
            ("Mobile Health Diagnostic Tool", "201811033221", "Granted", 2018),
        ]
        for title, num, status, year in patents:
            Patent.objects.create(
                profile=profile,
                title=title,
                patent_number=num,
                status=status,
                year=year
            )

        # 10. Sample Publications
        Publication.objects.create(
            title="Strategic HRM in Globalized Markets",
            authors="Ali, S. H., et al.",
            journal_conference_name="International Journal of Management Science",
            year_of_publication=2022,
            publication_type="Journal",
            doi_link="https://doi.org/10.1016/sample"
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded profile for {profile.name}"))
