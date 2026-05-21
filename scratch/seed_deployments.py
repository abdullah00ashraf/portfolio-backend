import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import SystemDeployment

def seed_deployments():
    # Clear existing
    SystemDeployment.objects.all().delete()
    
    # Create SENTINEL HUFP V7
    hufp = SystemDeployment.objects.create(
        name="SENTINEL HUFP V7",
        sub_title="Asynchronous Live Telemetry Ingestion Grid",
        status="LIVE",
        telemetry_metric="1,420 FLOWS/S",
        endpoint_url="http://127.0.0.1:8000/admin/",
        system_architecture="High-throughput physics-informed flood telemetry pipeline for citizen HUD. Integrates low-latency WebSocket protocols with resilient edge security layers.",
        is_public=True,
        is_deleted=False,
        order=1
    )
    print(f"Created SystemDeployment: {hufp.name}")

    # Create Project Salsette
    salsette = SystemDeployment.objects.create(
        name="Project Salsette",
        sub_title="WebGL Showcase Architecture",
        status="LIVE",
        telemetry_metric="99.9% UPTIME",
        endpoint_url="http://127.0.0.1:8000/",
        system_architecture="Glassmorphic responsive client showcase showcasing custom intelligence vaults and WebGL canvas overlays for elite portfolio displays.",
        is_public=True,
        is_deleted=False,
        order=2
    )
    print(f"Created SystemDeployment: {salsette.name}")

if __name__ == "__main__":
    seed_deployments()
