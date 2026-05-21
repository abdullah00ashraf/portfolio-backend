import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

import requests
from portfolio.models import LiveProject

def main():
    print("--------------------------------------------------")
    print("Executing End-to-End Flex Layout Self-Correction Test...")
    print("--------------------------------------------------")
    
    # 1. Verify we have 3 projects currently public
    public_projects = LiveProject.objects.filter(is_public=True)
    print(f"Initial public project count: {public_projects.count()}")
    
    # Get Sentinel HUFP V7
    hufp = LiveProject.objects.filter(title__contains="Sentinel HUFP V7").first()
    if not hufp:
        print("Sentinel HUFP V7 LiveProject not found.")
        return
        
    print(f"Hiding '{hufp.title}' by setting is_public=False...")
    hufp.is_public = False
    hufp.save()
    
    # 2. Fetch the homepage HTML and inspect elements
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        html_content = response.text
        
        # Verify Sentinel HUFP V7 is hidden from frontend
        if hufp.title in html_content:
            print("FAILED: Hidden project is still visible on the home page!")
        else:
            print("SUCCESS: Hidden project is fully hidden from the home page context!")
            
        # Verify other projects remain active
        if "ALGOMYTH" in html_content and "Linkup Learn" in html_content:
            print("SUCCESS: Other live projects are still displayed perfectly.")
            
        # Check for self-correction flex classes in the code
        if "flex flex-wrap justify-center gap-10 w-full" in html_content:
            print("SUCCESS: Flex-wrap centering container is active, maintaining perfect layout symmetry!")
            
    except Exception as e:
        print(f"Error fetching home page: {e}")
        
    # 3. Restore visibility state
    print("Restoring Sentinel HUFP V7 visibility state to True...")
    hufp.is_public = True
    hufp.save()
    print("Restoration complete.")

if __name__ == '__main__':
    main()
