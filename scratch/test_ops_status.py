import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import LiveProject

def main():
    print("--------------------------------------------------")
    print("Testing System Status Live Updates...")
    print("--------------------------------------------------")
    
    # Find Sentinel HUFP V7 LiveProject
    project = LiveProject.objects.filter(title__contains="Sentinel HUFP V7").first()
    if not project:
        print("Sentinel HUFP V7 LiveProject not found.")
        return
        
    print(f"Current status of '{project.title}': {project.system_status}")
    
    # Toggle it to Maintenance
    project.system_status = "Maintenance"
    project.save()
    print(f"Successfully toggled status of '{project.title}' to: {project.system_status}")

if __name__ == '__main__':
    main()
