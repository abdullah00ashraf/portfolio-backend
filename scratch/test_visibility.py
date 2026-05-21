import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import Publication

def main():
    print("--------------------------------------------------")
    print("Testing Public/Private Visibility Toggle...")
    print("--------------------------------------------------")
    
    # Let's find Sentinel HUFP V7 publication
    pub = Publication.objects.filter(title__contains="Sentinel HUFP V7").first()
    if not pub:
        print("Sentinel HUFP V7 publication not found.")
        return
        
    print(f"Current visibility of '{pub.title}': is_public = {pub.is_public}")
    
    # Toggle it to Private
    pub.is_public = False
    pub.save()
    print(f"Set visibility of '{pub.title}' to PRIVATE (is_public = False).")

if __name__ == '__main__':
    main()
