from portfolio.models import Publication, Course, ResearchProject, NewsAnnouncement

def dashboard_callback(request, context):
    context.update({
        "total_publications": Publication.objects.count(),
        "total_courses": Course.objects.count(),
        "active_projects": ResearchProject.objects.filter(status='Active').count(),
        "total_news": NewsAnnouncement.objects.count(),
        # Recycle Bin Stats
        "deleted_count": (
            Publication.all_objects.filter(is_deleted=True).count() + 
            Course.all_objects.filter(is_deleted=True).count() + 
            ResearchProject.all_objects.filter(is_deleted=True).count() + 
            NewsAnnouncement.all_objects.filter(is_deleted=True).count()
        ),
    })
    return context
