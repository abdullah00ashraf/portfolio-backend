import os
import django
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from django.core.management import call_command
from portfolio.models import (
    Profile, AboutMe, AcademicAppointment, AdministrativeAppointment,
    HonorAward, OrganizationBoard, ProfessionalEducation, Patent,
    Publication, Course, ResearchProject, NewsAnnouncement
)

# Mock binary file bytes that satisfy python-magic MIME-type checks
PNG_BYTES = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82`'
PDF_BYTES = b'%PDF-1.4\n' + b'\x00' * 2000
MP4_BYTES = b'\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00mp42isom\x00\x00\x00\x08free' + b'\x00' * 2000
JSON_BYTES = b'{"name": "Abdullah Ashraf", "role": "Full Stack & AI/ML Developer"}'

def main():
    print("--------------------------------------------------")
    print("Starting Developer Profile Ingestion Script...")
    print("--------------------------------------------------")

    # Double check database is flushed
    print("[1/9] Verifying database status...")
    if Profile.objects.exists():
        print("Database not empty. Running flush sequence...")
        call_command('flush', interactive=False)
        print("Database flushed successfully.")
    else:
        print("Database is clean and ready.")

    print("\n[2/9] Creating Main Developer Profile...")
    profile = Profile(
        name="Abdullah Ashraf",
        title="Full Stack & AI/ML Developer",
        department="Computer Science & Engineering (CSE)",
        contact_email="abdullah.ashraf55780@gmail.com",
        office_location="Lucknow, Uttar Pradesh, India",
        teaching_area="<ul><li>Advanced Python & Django Frameworks</li><li>Automated Code Generation & CI/CD</li><li>Full Stack Web Development & System Architecture</li></ul>",
        research_area="<ul><li>Municipal Flood Prediction & Hydrological Machine Learning Models</li><li>Automated Code Optimization & Code Scaffolding Engines</li><li>Decentralized Application Security</li></ul>",
        horizontal_alignment="left",
        media_position="left",
        is_about_visible=True,
        is_academic_visible=True,
        is_admin_visible=True,
        is_honors_visible=True,
        is_boards_visible=True,
        is_education_visible=True,
        is_patents_visible=True,
        order_about=1,
        order_academic=2,
        order_education=3,
        order_admin=4,
        order_patents=5
    )
    
    # Save mock files with correct signatures to satisfy model validations
    profile.profile_image.save("abdullah_ashraf.png", ContentFile(PNG_BYTES), save=False)
    profile.cv_pdf.save("abdullah_cv.pdf", ContentFile(PDF_BYTES), save=False)
    profile.resume_json.save("resume_data.json", ContentFile(JSON_BYTES), save=False)
    profile.portfolio_pdf.save("full_portfolio.pdf", ContentFile(PDF_BYTES), save=False)
    profile.save()
    print(f"Created Profile: {profile.name} (PID: {profile.id})")

    print("\n[3/9] Creating About Me narrative section...")
    about = AboutMe(
        profile=profile,
        bio="<p>Full Stack Developer specializing in building robust AI/ML systems and responsive web applications. Deep interest in municipal infrastructure optimization, flood intelligence modeling, and historical preservation tech. Experienced across the complete lifecycle of product prototyping from scratch to secure cloud deployment.</p>"
    )
    about.intro_video.save("intro_video.mp4", ContentFile(MP4_BYTES), save=False)
    about.save()
    print("Created AboutMe Narrative & Video Ingestion.")

    print("\n[4/9] Ingesting Professional Education...")
    edu = ProfessionalEducation(
        profile=profile,
        degree="Bachelor of Technology (B.Tech)",
        institution="Khwaja Moinuddin Chishti Language University (KMCLU), Lucknow",
        specialization="Computer Science & Engineering (CSE) with a specialization in Artificial Intelligence & Machine Learning (AI/ML)",
        year=2026
    )
    edu.save()
    print(f"Created Education Record: {edu.degree} in {edu.specialization}")

    print("\n[5/9] Ingesting Leadership & Administrative Assignments...")
    admin_role1 = AdministrativeAppointment(
        profile=profile,
        role="Team Leader — The Aegis (Team ID 75864)",
        department="Smart India Hackathon 2025",
        responsibilities="Led the design and development of dynamic mapping and cloud predictive infrastructure to tackle critical civic flood planning and warning challenge statements."
    )
    admin_role1.save()
    
    admin_role2 = AdministrativeAppointment(
        profile=profile,
        role="Level 1 Local Guide & Contributor",
        department="Municipal Mapping Infrastructure, Lucknow",
        responsibilities="Contributed geographic data, mapping local roads, water bodies, and points of interest to support municipal planning and crowd-sourced geographic resources."
    )
    admin_role2.save()
    print(f"Ingested {AdministrativeAppointment.objects.count()} assignments successfully.")

    print("\n[6/9] Ingesting Honors, Awards & Milestones...")
    awards = [
        HonorAward(
            profile=profile,
            award_name="Letter of Appreciation for AI Kit Demonstration",
            granting_body="Dr. A.P.J. Abdul Kalam AI Lab Inauguration",
            year=2025
        ),
        HonorAward(
            profile=profile,
            award_name="\"Carbon Smart\" Sustainability Certification",
            granting_body="Infosys Springboard Sustainability Initiative",
            year=2025
        ),
        HonorAward(
            profile=profile,
            award_name="Registered Competitor",
            granting_body="GATE 2026 Examination",
            year=2026
        )
    ]
    for aw in awards:
        aw.save()
    print(f"Ingested {HonorAward.objects.count()} honors and milestones successfully.")

    print("\n[7/9] Creating Key Projects & Systems (Mapped to Research & Archive)...")
    
    # 7.1 Mapped to Research Projects
    projects = [
        ResearchProject(
            project_title="Sentinel HUFP V7 (Flood Intelligence & Impact Platform)",
            funding_agency="Municipal Infrastructure & Humanitarian Standards",
            duration="2025 - Present",
            status="Active",
            description="<p>A river water pollution detection and flood forecasting matrix engineered using machine learning frameworks from scratch. Designed to support municipal infrastructure and humanitarian standards.</p>"
        ),
        ResearchProject(
            project_title="ALGOMYTH (The Algorithm Generator)",
            funding_agency="Internal R&D",
            duration="2025",
            status="Completed",
            description="<p>An automated code scaffolding engine engineered for algorithmic optimization and system asset generation.</p>"
        ),
        ResearchProject(
            project_title="Linkup Learn v1.0",
            funding_agency="Self-Funded",
            duration="2024",
            status="Completed",
            description="<p>A web-based interactive learning environment tailored to dynamic educational delivery and resource mapping.</p>"
        ),
        ResearchProject(
            project_title="Zerodha Clone Major Project",
            funding_agency="Personal Portfolio",
            duration="2024",
            status="Completed",
            description="<p>High-fidelity frontend cloning and asset mapping of the popular trading interface architecture.</p>"
        )
    ]
    for pr in projects:
        pr.save()
    
    # 7.2 Mapped to Publications (Archive)
    pubs = [
        Publication(
            title="Sentinel HUFP V7: A Machine Learning Framework for Real-time Flood Intelligence and Water Pollution Detection",
            authors="Abdullah Ashraf",
            journal_conference_name="International Journal of Flood Intelligence and Municipal Engineering",
            year_of_publication=2025,
            publication_type="Journal",
            abstract="<p>A river water pollution detection and flood forecasting matrix engineered using machine learning frameworks from scratch. Designed to support municipal infrastructure and humanitarian standards.</p>",
            doi_link="https://doi.org/10.1016/sample-hufp",
            order=1
        ),
        Publication(
            title="ALGOMYTH: Automated Code Scaffolding for High-Performance Algorithmic Optimization",
            authors="Abdullah Ashraf",
            journal_conference_name="Conference on Algorithm Generation and Optimization Engines",
            year_of_publication=2025,
            publication_type="Conference",
            abstract="<p>An automated code scaffolding engine engineered for algorithmic optimization and system asset generation.</p>",
            doi_link="https://doi.org/10.1145/sample-algomyth",
            order=2
        ),
        Publication(
            title="Linkup Learn: Architecting Interactive Web Environments for Dynamic Educational Delivery",
            authors="Abdullah Ashraf",
            journal_conference_name="IEEE Transactions on Education and Digital Pedagogies",
            year_of_publication=2024,
            publication_type="Journal",
            abstract="<p>A web-based interactive learning environment tailored to dynamic educational delivery and resource mapping.</p>",
            doi_link="https://doi.org/10.1109/sample-linkup",
            order=3
        ),
        Publication(
            title="Zerodha Clone: Engineering High-Fidelity Client Architectures for Modern Financial Portals",
            authors="Abdullah Ashraf",
            journal_conference_name="Journal of Software Engineering and Frontend Cloning",
            year_of_publication=2024,
            publication_type="Journal",
            abstract="<p>High-fidelity frontend cloning and asset mapping of the popular trading interface architecture.</p>",
            doi_link="https://doi.org/10.5555/sample-zerodha",
            order=4
        )
    ]
    for pb in pubs:
        pb.pdf_file.save("sample_pub.pdf", ContentFile(PDF_BYTES), save=False)
        pb.save()
    
    print(f"Created {ResearchProject.objects.count()} active research projects.")
    print(f"Created {Publication.objects.count()} archive publication entries.")

    print("\n[8/9] Ingesting Innovation Patents & Pedagogy Courses...")
    patent = Patent(
        profile=profile,
        title="System and Method for Real-time Municipal Flood Inundation Prediction and Hydraulic Analysis",
        patent_number="202511099887",
        status="Published",
        year=2025,
        url="https://patents.google.com/patent/sample-flood-aegis"
    )
    patent.link_or_file.save("patent_flood_prediction.pdf", ContentFile(PDF_BYTES), save=False)
    patent.save()
    print("Ingested Innovation Patent.")

    courses = [
        Course(
            course_code="CS-401",
            course_title="Advanced Artificial Intelligence & Machine Learning",
            semester="Fall 2025",
            description="Covers advanced deep learning, convolutional networks, transformers, and hydrological intelligence forecasting models built from scratch.",
            order=1
        ),
        Course(
            course_code="CS-302",
            course_title="Automated Code Generation & Compiler Optimization",
            semester="Spring 2025",
            description="Explores automated scaffolding, algorithmic generation architectures, compiler pipelines, and code pattern analysis.",
            order=2
        ),
        Course(
            course_code="CS-205",
            course_title="Full Stack Web Engineering & Cloud Deployment Architectures",
            semester="Fall 2024",
            description="Bridges the gap between responsive vanilla frontends, Django REST backends, real-time WebSockets, and secure microservices.",
            order=3
        )
    ]
    for cs in courses:
        cs.syllabus.save("course_syllabus.pdf", ContentFile(PDF_BYTES), save=False)
        cs.save()
    print(f"Ingested {Course.objects.count()} pedagogy courses.")

    print("\n[9/9] Ingesting Bulletin News & Announcements...")
    news = [
        NewsAnnouncement(
            headline="Team Aegis Led by Abdullah Ashraf Competes at SIH 2025",
            content="<p>Leading Team Aegis (Team ID 75864) at the Smart India Hackathon 2025, tackling complex municipal infrastructure and civic challenge statements with automated software architectures.</p>",
            date="2025-10-15",
            is_active=True
        ),
        NewsAnnouncement(
            headline="Geographic Infrastructure Mapping for Lucknow Smart City",
            content="<p>Contributing as a Level 1 Local Guide and geographic data contributor to map urban roads, water bodies, and public spaces in Lucknow, aiding municipal mapping and flood planning.</p>",
            date="2025-06-20",
            is_active=True
        )
    ]
    for nw in news:
        nw.save()
    print(f"Ingested {NewsAnnouncement.objects.count()} bulletin articles successfully.")

    print("--------------------------------------------------")
    print("Developer Profile Ingestion Complete! Zero Errors.")
    print("--------------------------------------------------")

if __name__ == '__main__':
    main()
