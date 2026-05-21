from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import (
    Profile, Publication, Course, ResearchProject, NewsAnnouncement, LiveProject, LocalResource, 
    SystemDeployment, LabPrototype, OpenSourceContribution, TechStackMetric, TerminalLog, PeerReference,
    KnowledgeAsset, SideVentureAsset
)

def index_view(request):
    """
    Unified Single-Page View Controller.
    """
    # 1. Identity Core
    profile = Profile.objects.first()

    # 2. Infrastructure Registry (Excluding Trashed/Private Nodes)
    deployments = SystemDeployment.objects.filter(is_public=True, is_deleted=False)

    # 3. Creative Lab Prototypes & Sandboxed Code
    lab_prototypes = LabPrototype.objects.filter(is_public=True)

    # 4. Open Source Contributions & Commits
    open_source = OpenSourceContribution.objects.filter(is_public=True)

    # 5. Technical Capability Weights
    stack_metrics = TechStackMetric.objects.all().order_by('order')


    # 6. Live DevOps Event Terminal Logs (Most recent 15 lines)
    system_logs = TerminalLog.objects.filter(is_public=True).order_by('-timestamp')[:15]

    # 7. Verified Peer Testimonials
    references = PeerReference.objects.filter(is_public=True)


    # Dynamic Section Ordering (Fallback compatibility)
    sections = [
        {'name': 'about', 'order': getattr(profile, 'order_about', 1) if profile else 1},
        {'name': 'publications', 'order': getattr(profile, 'order_academic', 2) if profile else 2},
        {'name': 'teaching', 'order': getattr(profile, 'order_education', 3) if profile else 3},
        {'name': 'news', 'order': getattr(profile, 'order_admin', 4) if profile else 4},
        {'name': 'patents', 'order': getattr(profile, 'order_patents', 5) if profile else 5},
    ]
    sections.sort(key=lambda x: x['order'])

    # 8. Knowledge Vault Assets (Public)
    knowledge_assets = KnowledgeAsset.objects.filter(is_public=True).order_by('order', '-created_at')
    certificates = knowledge_assets.filter(asset_type='CERTIFICATE')
    learning_modules = knowledge_assets.filter(asset_type='LEARNING_MODULE')

    # ========================================================
    # ASSEMBLE CONTEXT GRAPH
    # ========================================================
    context = {
        'profile': profile,
        'deployments': deployments,
        'lab_prototypes': lab_prototypes,
        'open_source': open_source,
        'stack_metrics': stack_metrics,
        'system_logs': reversed(system_logs),  # Keeps log chronology correct in console view
        'references': references,
        'sections': sections,
        'certificates': certificates,
        'learning_modules': learning_modules,
    }
    
    return render(request, 'portfolio/index.html', context)


# ──────────────────────────────────────────────────────────────────────────────
# Knowledge Vault — Secure Asset Fetch Endpoint
# ──────────────────────────────────────────────────────────────────────────────

def fetch_asset_view(request, asset_id: int):
    """
    Streams a KnowledgeAsset to the requester.

    Routes internally to LOCAL_DISK or GOOGLE_DRIVE based on the asset's
    storage_provider field. Public assets can be accessed by anyone.
    Private assets require an active authenticated session.

    GET /vault/asset/<asset_id>/
    """
    from portfolio.services.knowledge_vault import (
        fetch_knowledge_asset,
        KnowledgeAssetNotFound,
        KnowledgeAssetFetchError,
    )

    try:
        allow_private = request.user.is_authenticated
        return fetch_knowledge_asset(asset_id, allow_private=allow_private)

    except KnowledgeAssetNotFound as exc:
        return JsonResponse(
            {"error": "NOT_FOUND", "detail": str(exc)},
            status=404
        )

    except KnowledgeAssetFetchError as exc:
        return JsonResponse(
            {"error": "FETCH_ERROR", "detail": str(exc)},
            status=502
        )

    except Exception as exc:
        return JsonResponse(
            {"error": "INTERNAL_ERROR", "detail": "An unexpected error occurred."},
            status=500
        )

# ──────────────────────────────────────────────────────────────────────────────
# Side Ventures API Endpoint
# ──────────────────────────────────────────────────────────────────────────────
def side_ventures_api(request):
    """
    Returns a secure JSON payload of public SideVentureAsset objects.
    GET /api/side-ventures
    """
    assets = SideVentureAsset.objects.filter(is_public=True).order_by('order', '-timestamp')
    
    data = []
    for asset in assets:
        # Determine the file extension or footprint purely for telemetry display
        ext = ".BIN"
        if asset.file_type == 'PDF': ext = ".PDF"
        elif asset.file_type == 'DATASET': ext = ".JSON/.CSV"
        elif asset.file_type == 'IMAGE': ext = ".PNG/.JPG"
        elif asset.file_type == 'RAW_CODE': ext = ".PY/.JS"
        
        # Determine URI (either local relative path or Google Drive ID)
        final_uri = asset.uri
        if asset.storage_provider == 'LOCAL_DISK' and asset.upload:
            final_uri = asset.upload.url
            
        data.append({
            "id": str(asset.id),
            "title": asset.title,
            "category": asset.category,
            "fileType": asset.file_type,
            "storageProvider": asset.storage_provider,
            "uri": final_uri,
            "ext": ext,
            "timestamp": asset.timestamp.isoformat()
        })
        
    return JsonResponse({"ventures": data})
