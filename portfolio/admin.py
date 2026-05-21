from django.contrib import admin, messages
from django.utils import timezone
from unfold.admin import ModelAdmin
from unfold.decorators import action
from adminsortable2.admin import SortableAdminMixin
from import_export.admin import ImportExportModelAdmin
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Profile, AboutMe, AcademicAppointment, AdministrativeAppointment,
    HonorAward, OrganizationBoard, ProfessionalEducation, Patent,
    Publication, Course, ResearchProject, NewsAnnouncement, LiveProject, LocalResource,
    SystemDeployment, LabPrototype, OpenSourceContribution, TechStackMetric, TerminalLog, PeerReference,
    AssetAttachment, KnowledgeAsset, SideVentureAsset
)

class AssetAttachmentInline(GenericTabularInline):
    model = AssetAttachment
    extra = 1
    classes = ('tab', 'compressed')
    fields = ('label', 'resource_type', 'local_file', 'drive_direct_url', 'is_active')

# --- Inlines ---

class AboutMeInline(admin.StackedInline):
    model = AboutMe
    extra = 1

class AcademicAppointmentInline(admin.StackedInline):
    model = AcademicAppointment
    extra = 1

class AdministrativeAppointmentInline(admin.StackedInline):
    model = AdministrativeAppointment
    extra = 1

class HonorAwardInline(admin.StackedInline):
    model = HonorAward
    extra = 1

class OrganizationBoardInline(admin.StackedInline):
    model = OrganizationBoard
    extra = 1

class ProfessionalEducationInline(admin.StackedInline):
    model = ProfessionalEducation
    extra = 1

# --- Base Soft Delete Admin ---

class BaseSoftDeleteAdmin(ModelAdmin):
    def get_queryset(self, request):
        return self.model.all_objects.all()

    def get_status_badge(self, obj):
        if obj.is_public:
            return mark_safe('<span style="background: #10b981; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 10px;">PUBLIC</span>')
        return mark_safe('<span style="background: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 10px;">PRIVATE</span>')
    get_status_badge.short_description = "Status"

    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.deleted_at = timezone.now()
        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(is_deleted=True, deleted_at=timezone.now())

    @admin.action(description="Restore selected items")
    def restore_items(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)
        self.message_user(request, f"Successfully restored {queryset.count()} items.")

    @admin.action(description="PERMANENTLY DELETE selected items")
    def permanent_delete(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"PERMANENTLY deleted {count} items.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.GET.get('is_deleted__exact') == '1':
            if 'permanent_delete' in actions:
                del actions['permanent_delete']
        return actions

# --- Main Admin Classes ---

class PatentInline(admin.StackedInline):
    model = Patent
    extra = 1
    classes = ['collapse']

@admin.action(description="Batch Flag Selected Elements as Public")
def make_public(modeladmin, request, queryset):
    queryset.update(is_public=True)

@admin.action(description="Batch Hide Selected Elements from Public Grid")
def make_private(modeladmin, request, queryset):
    queryset.update(is_public=False)

@admin.register(Profile)
class ProfileAdmin(BaseSoftDeleteAdmin):
    list_display = ('name', 'title', 'contact_email', 'get_status_badge', 'is_deleted')
    list_filter = ('is_public', 'is_deleted')
    compressed_fields = True
    icon = "person"
    
    fieldsets = (
        (None, {
            'fields': ('name', 'title', 'designation', 'department', 'contact_email', 'contact_phone', 'office_location', 'profile_image', 'cv_pdf', 'resume_json', 'portfolio_pdf', 'is_public')
        }),
        ('SYSTEMS IDENTITY CORE', {
            'fields': ('manifesto_statement', 'core_mindset_philosophy', 'immediate_system_goals', 'profile_signature_initial'),
        }),
        ('Expertise & Narrative', {
            'fields': ('teaching_area', 'research_area'),
        }),
        ('Adaptive Layout & Alignment', {
            'classes': ('tab',),
            'fields': (
                ('horizontal_alignment', 'media_position'),
            ),
        }),
        ('Section Visibility', {
            'classes': ('tab',),
            'fields': (
                ('is_about_visible', 'is_academic_visible'),
                ('is_admin_visible', 'is_honors_visible'),
                ('is_boards_visible', 'is_education_visible', 'is_patents_visible'),
            ),
        }),
        ('Section Ordering', {
            'classes': ('tab',),
            'fields': (
                ('order_about', 'order_academic'),
                ('order_admin', 'order_honors'),
                ('order_boards', 'order_education', 'order_patents'),
            ),
        }),
    )

    inlines = [
        AboutMeInline, AcademicAppointmentInline, AdministrativeAppointmentInline,
        HonorAwardInline, OrganizationBoardInline, ProfessionalEducationInline, PatentInline
    ]
    actions = ['export_profile_json', 'restore_items', 'permanent_delete']
    
    @admin.action(description="Export Profile to JSON")
    def export_profile_json(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Please select only one profile to export.", level='ERROR')
            return
        
        obj = queryset.first()
        data = {
            "profile": {
                "name": obj.name,
                "title": obj.title,
                "department": obj.department,
                "contact_email": obj.contact_email,
                "office_location": obj.office_location,
            },
            "about": list(obj.about_sections.values('bio', 'is_public')),
            "academic_appointments": list(obj.academic_appointments.values('position', 'institution', 'start_date', 'end_date', 'is_public')),
            "admin_appointments": list(obj.admin_appointments.values('role', 'department', 'responsibilities', 'is_public')),
            "honors_awards": list(obj.honors_awards.values('award_name', 'granting_body', 'year', 'is_public')),
            "org_boards": list(obj.org_boards.values('org_name', 'role', 'committee_type', 'is_public')),
            "education": list(obj.education.values('degree', 'institution', 'specialization', 'is_public')),
        }
        
        response = HttpResponse(
            json.dumps(data, cls=DjangoJSONEncoder, indent=4),
            content_type="application/json"
        )
        response['Content-Disposition'] = f'attachment; filename=profile_{obj.name.lower().replace(" ", "_")}.json'
        return response

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(SystemDeployment)
class SystemDeploymentAdmin(BaseSoftDeleteAdmin):
    list_display = ('name', 'status', 'telemetry_metric', 'display_system_state', 'has_cloud_binding')
    list_filter = ('status', 'auto_sync_assets', 'is_deleted')
    search_fields = ('name', 'sub_title')
    icon = "router"
    inlines = [AssetAttachmentInline]
    
    actions = [make_public, make_private, 'bulk_soft_delete', 'bulk_restore_systems']

    def has_cloud_binding(self, obj):
        return "📁 CONNECTED" if obj.drive_folder_id else "✖ DISCONNECTED"
    has_cloud_binding.short_description = "Cloud Synchronization"

    fieldsets = (
        ('IDENTITY MATRIX', {
            'fields': ('name', 'sub_title', 'status', 'order')
        }),
        ('TECHNICAL PARAMETERS', {
            'fields': ('endpoint_url', 'telemetry_metric', 'system_architecture', 'is_public', 'is_deleted')
        }),
        ('GOOGLE CLOUD BINDING CONFIGURATION', {
            'classes': ('tab',),
            'fields': ('drive_folder_id', 'auto_sync_assets'),
            'description': 'Input your secure Google Drive Folder string to automatically feed directory content streams directly to this component.'
        }),
    )

    def display_system_state(self, obj):
        if obj.is_deleted:
            return "🗑 IN TRASH"
        return "🟢 ACTIVE"
    display_system_state.short_description = "Infrastructure Lifecycle"

    @action(description="Move selected systems to Recycle Bin", url_path="soft-delete")
    def bulk_soft_delete(self, request, queryset):
        count = 0
        for obj in queryset:
            obj.soft_delete()
            count += 1
        self.message_user(
            request, 
            f"Successfully shifted {count} deployment arrays into the Recycle Bin.", 
            messages.WARNING
        )

    @action(description="Restore selected systems to Active Grid", url_path="restore")
    def bulk_restore_systems(self, request, queryset):
        count = 0
        for obj in queryset:
            obj.restore()
            count += 1
        self.message_user(
            request, 
            f"Successfully restored {count} systems back to production pipeline channels.", 
            messages.SUCCESS
        )

@admin.register(LiveProject)
class LiveProjectAdmin(BaseSoftDeleteAdmin):
    list_display = ('title', 'system_status', 'uptime_percentage', 'display_system_state')
    list_filter = ('system_status', 'is_deleted')
    search_fields = ('title',)
    icon = "analytics"

    actions = [make_public, make_private, 'bulk_soft_delete', 'bulk_restore_systems']

    def display_system_state(self, obj):
        if obj.is_deleted:
            return "🗑 IN TRASH"
        return "🟢 ACTIVE"
    display_system_state.short_description = "Infrastructure Lifecycle"

    @action(description="Move selected systems to Recycle Bin", url_path="soft-delete")
    def bulk_soft_delete(self, request, queryset):
        count = 0
        for obj in queryset:
            obj.soft_delete()
            count += 1
        self.message_user(
            request, 
            f"Successfully shifted {count} deployment arrays into the Recycle Bin.", 
            messages.WARNING
        )

    @action(description="Restore selected systems to Active Grid", url_path="restore")
    def bulk_restore_systems(self, request, queryset):
        count = 0
        for obj in queryset:
            obj.restore()
            count += 1
        self.message_user(
            request, 
            f"Successfully restored {count} systems back to production pipeline channels.", 
            messages.SUCCESS
        )

@admin.register(LabPrototype)
class LabPrototypeAdmin(ModelAdmin):
    list_display = ('title', 'runtime_environment', 'drive_folder_id', 'is_public')
    actions = [make_public, make_private]
    icon = "biotech"
    
    fieldsets = (
        ('CORE DATA', {'fields': ('title', 'runtime_environment', 'mathematical_core', 'is_public')}),
        ('CLOUD ATTACHMENT', {'fields': ('drive_folder_id', 'auto_sync_assets')}),
    )

@admin.register(OpenSourceContribution)
class OpenSourceContributionAdmin(ModelAdmin):
    list_display = ('repository_name', 'lines_optimized', 'is_public')
    actions = [make_public, make_private]
    icon = "git_branch"

@admin.register(TechStackMetric)
class TechStackMetricAdmin(ModelAdmin):
    list_display = ('technology_name', 'category', 'order', 'is_public')
    list_filter = ('category',)
    actions = [make_public, make_private]
    icon = "layers"

@admin.register(TerminalLog)
class TerminalLogAdmin(ModelAdmin):
    list_display = ('timestamp', 'log_level', 'message', 'is_public')
    list_filter = ('log_level', 'is_public')
    actions = [make_public, make_private]
    icon = "terminal"

@admin.register(PeerReference)
class PeerReferenceAdmin(ModelAdmin):
    list_display = ('referee_name', 'organization_or_title', 'is_public')
    list_filter = ('is_public',)
    actions = [make_public, make_private, 'approve_references']
    icon = "verified_user"

    @admin.action(description="Approve selected peer references for public view")
    def approve_references(self, request, queryset):
        queryset.update(is_public=True)

@admin.register(LocalResource)
class LocalResourceAdmin(BaseSoftDeleteAdmin):
    list_display = ('title', 'resource_type', 'last_synced')
    actions = [make_public, make_private]
    icon = "analytics"


# ────────────────────────────────────────────────────────────
# KNOWLEDGE VAULT ADMIN PANEL
# ────────────────────────────────────────────────────────────

class AssetTypeFilter(admin.SimpleListFilter):
    """
    Custom filter that powers the Knowledge Vault sidebar links.
    Sidebar links use  ?asset_type=CERTIFICATE  /  ?asset_type=LEARNING_MODULE
    which this filter intercepts and applies as a queryset constraint.
    """
    title = 'Asset Type'
    parameter_name = 'asset_type'

    def lookups(self, request, model_admin):
        return KnowledgeAsset.ASSET_TYPE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(asset_type=self.value())
        return queryset


@admin.register(KnowledgeAsset)
class KnowledgeAssetAdmin(ModelAdmin):
    """
    Full-featured admin panel for the Knowledge Vault.

    Sidebar navigation links filter by asset_type so
    'Certificates' and 'Learning Modules' each open a
    pre-filtered list automatically.
    """
    list_display  = ('title', 'asset_type_badge', 'storage_badge', 'issuer_display', 'is_public', 'order')
    list_editable = ('order', 'is_public')
    list_filter   = (AssetTypeFilter, 'storage_provider', 'is_public')
    search_fields = ('title', 'metadata')
    ordering      = ('order', '-created_at')
    icon          = "school"  # Material symbol shown in the sidebar

    actions = [make_public, make_private, 'preview_asset_action']

    fieldsets = (
        ('VAULT IDENTITY', {
            'fields': ('title', 'asset_type', 'order', 'is_public')
        }),
        ('STORAGE CONFIGURATION', {
            'description': (
                '<strong style="color:#f59e0b">LOCAL_DISK</strong>: '
                'Upload via the file field below, or enter an absolute server path in URI. '
                '<strong style="color:#8b5cf6">GOOGLE_DRIVE</strong>: '
                'Enter the Drive File ID in the URI field (no full URL — just the ID string).'
            ),
            'fields': ('storage_provider', 'local_file', 'uri'),
        }),
        ('METADATA PAYLOAD', {
            'classes': ('tab',),
            'description': 'Free-form JSON. Keys: issuer, issued_date, expiry, tags, platform, hours, chapters…',
            'fields': ('metadata',),
        }),
    )

    # ── Display helpers ───────────────────────────────────────────────

    def asset_type_badge(self, obj):
        colour = '#8b5cf6' if obj.asset_type == 'CERTIFICATE' else '#06b6d4'
        label  = obj.get_asset_type_display()
        return mark_safe(
            f'<span style="background:{colour};color:#fff;padding:2px 8px;'
            f'border-radius:4px;font-size:10px;font-weight:700;font-family:monospace">'
            f'{label}</span>'
        )
    asset_type_badge.short_description = 'Type'

    def storage_badge(self, obj):
        if obj.storage_provider == 'LOCAL_DISK':
            colour, label = '#10b981', 'LOCAL'
        else:
            colour, label = '#f59e0b', 'DRIVE'
        return mark_safe(
            f'<span style="background:{colour};color:#000;padding:2px 8px;'
            f'border-radius:4px;font-size:10px;font-weight:700;font-family:monospace">'
            f'{label}</span>'
        )
    storage_badge.short_description = 'Storage'

    def issuer_display(self, obj):
        return obj.metadata.get('issuer', '—')
    issuer_display.short_description = 'Issuer'

    # ── Actions ──────────────────────────────────────────────────

    @admin.action(description="Generate secure fetch links for selected assets")
    def preview_asset_action(self, request, queryset):
        links = []
        for asset in queryset:
            url = f"/vault/asset/{asset.pk}/"
            links.append(
                f'<a href="{url}" target="_blank" style="color:#8b5cf6">'
                f'⇗ {asset.title}</a>'
            )
        self.message_user(
            request,
            mark_safe(
                '<strong>Secure Fetch Links:</strong><br>' +
                '<br>'.join(links)
            )
        )


@admin.register(SideVentureAsset)
class SideVentureAssetAdmin(ModelAdmin):
    list_display = ('title', 'category_badge', 'storage_badge', 'file_type', 'is_public', 'timestamp')
    list_filter = ('category', 'storage_provider', 'file_type', 'is_public')
    search_fields = ('title',)
    icon = "cases"

    fieldsets = (
        ('ASSET IDENTITY', {
            'fields': ('title', 'category', 'file_type', 'order', 'is_public')
        }),
        ('UPLOAD BIFURCATION ENGINE', {
            'description': 'Upload your asset here. If GOOGLE_DRIVE is selected, it will be piped directly to cloud storage and a Drive ID will be returned.',
            'fields': ('storage_provider', 'upload', 'uri')
        })
    )

    def category_badge(self, obj):
        colour = '#ffb000' if obj.category == 'SIDE_VENTURE' else '#06b6d4'
        return mark_safe(f'<span style="color:{colour};font-weight:bold;">{obj.get_category_display()}</span>')
    category_badge.short_description = "Category"

    def storage_badge(self, obj):
        colour = '#10b981' if obj.storage_provider == 'LOCAL_DISK' else '#f59e0b'
        return mark_safe(f'<span style="background:{colour};color:#000;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;">{obj.get_storage_provider_display()}</span>')
    storage_badge.short_description = "Storage"

    def save_model(self, request, obj, form, change):
        if obj.upload and obj.storage_provider == 'GOOGLE_DRIVE':
            from portfolio.utils.google_drive import GoogleDriveEngine
            drive_engine = GoogleDriveEngine()
            
            # Use the in-memory/temporary file for upload
            file_id = drive_engine.upload_file(
                file_obj=obj.upload.file,
                filename=obj.upload.name,
                mime_type=obj.upload.content_type
            )
            
            if file_id:
                obj.uri = file_id
                # Remove the file from being saved locally
                obj.upload = None
                messages.success(request, f"Successfully piped to Google Drive. ID: {file_id}")
            else:
                messages.error(request, "Failed to upload to Google Drive.")
        elif obj.upload and obj.storage_provider == 'LOCAL_DISK':
            # It will be saved automatically by Django. Just ensure uri points to it if needed
            # We can set uri to the name or path in post-save, or just leave uri blank and use obj.upload.url in frontend
            pass

        super().save_model(request, obj, form, change)
