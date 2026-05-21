import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import Profile

def seed_systems_identity():
    # Update or create the singular master profile row
    profile, created = Profile.objects.get_or_create(id=1)
    
    profile.name = "Abdullah Ashraf"
    profile.designation = "Full Stack & AI/ML Systems Engineer"
    profile.contact_email = "abdullah.ashraf55780@gmail.com"
    
    profile.manifesto_statement = (
        "Architecting robust full-stack software systems and predictive machine learning matrices "
        "engineered to solve complex municipal, humanitarian, and infrastructure challenges."
    )
    
    profile.core_mindset_philosophy = (
        "Engineering from scratch demands an uncompromised balance between algorithmic complexity, data security, "
        "and clean runtime execution. My approach relies heavily on heuristic optimization, neural network architectures, "
        "and modular full-stack code scaffolding to transition theoretical models into live, high-uptime platforms. "
        "I build systems to be secure at the database level using industry-standard primitives, ensuring every data flow "
        "is built for high performance and continuous stress handling."
    )
    
    profile.immediate_system_goals = (
        "• Production Optimization: Scaling SENTINEL HUFP V7 to establish resilient flood intelligence matrices and river water pollution detection frameworks for the Lucknow Division.\n"
        "• Predictive Pipeline Prototyping: Staging the computational infrastructure for Project Salsette to bridge regional telemetry streams with automated alert models.\n"
        "• Core Optimization R&D: Advancing heuristic code generation utilities via the ALGOMYTH logic engine to automate complex software optimization passes seamlessly."
    )
    
    profile.profile_signature_initial = "A"
    profile.save()
    
    print("Master Systems Identity successfully ingested into production context.")

if __name__ == '__main__':
    seed_systems_identity()
