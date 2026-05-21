import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import LabPrototype, OpenSourceContribution, TechStackMetric, TerminalLog, PeerReference

def seed_elite_data():
    # Clear existing
    LabPrototype.objects.all().delete()
    OpenSourceContribution.objects.all().delete()
    TechStackMetric.objects.all().delete()
    TerminalLog.objects.all().delete()
    PeerReference.objects.all().delete()

    # 1. LabPrototype
    LabPrototype.objects.create(
        title="AEGIS Judge-Jury Audit Engine (v7.4-alpha)",
        runtime_environment="Python 3.11 // PyTorch",
        mathematical_core="V_audit validation calculus incorporating muck-factor and gridlock parameters.",
        is_public=True
    )
    
    # 2. OpenSourceContribution
    OpenSourceContribution.objects.create(
        repository_name="django-unfold",
        pull_request_url="https://github.com/unfoldadmin/django-unfold",
        impact_summary="Optimized client-side state caching layer, reducing redundant SQL lookups by 35% on dashboard rendering paths.",
        lines_optimized=450,
        is_public=True
    )
    
    # 3. TechStackMetric
    TechStackMetric.objects.create(
        technology_name="PyTorch & Physics-Informed ML",
        category="AIML_FRAME",
        verified_use_cases="Deployed in HUFP Mumbai Transit Gridlock predictors and threat curves.",
        order=1
    )
    
    # 4. TerminalLog
    TerminalLog.objects.create(
        log_level="SUCCESS",
        message="Sentinel V7 Security Core handshake established cleanly across node clusters.",
        is_public=True
    )
    TerminalLog.objects.create(
        log_level="INFO",
        message="Core controller sync thread initialized successfully.",
        is_public=True
    )
    
    # 5. PeerReference
    PeerReference.objects.create(
        referee_name="Dr. Sarah Chen",
        organization_or_title="Principal Architect, AEGIS Infrastructure",
        verification_hash="a3b8d9c2e0f41a87b6d5e4a3b8d9c2e0f41a87b6d5e4a3b8d9c2e0f41a87b6d5",
        statement="Abdullah's work on Sentinel V7 telemetry pipelines sets a new standard for mission-critical environmental engineering.",
        is_public=True
    )

    print("Successfully seeded all 5 Elite Systems & Models!")

if __name__ == "__main__":
    seed_elite_data()
