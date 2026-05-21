from django.db import models
from tinymce.models import HTMLField
from django_cryptography.fields import encrypt
from django.utils import timezone
from .validators import validate_is_pdf, validate_is_video
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class InfrastructureQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

    def trashed(self):
        return self.filter(is_deleted=True)

    def order_index(self):
        return self.order_by('order')

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_public = models.BooleanField(default=True, verbose_name="Public Visibility")

    objects = InfrastructureQuerySet.as_manager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.is_public = False
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.is_public = True
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True

class Profile(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=255, default="Full Stack Developer & AI/ML Engineer", blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    office_location = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv_pdf = models.FileField(upload_to='cv/', blank=True, null=True, validators=[validate_is_pdf], verbose_name="Academic CV (PDF)")
    resume_json = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name="Resume Data (JSON)")
    portfolio_pdf = models.FileField(upload_to='portfolio_downloads/', blank=True, null=True, validators=[validate_is_pdf], verbose_name="Full Portfolio (PDF)")
    
    # Advanced Editorial Biography Fields
    manifesto_statement = models.TextField(
        blank=True, 
        null=True, 
        help_text="A high-end, single-sentence operational thesis framing your overall work."
    )
    core_mindset_philosophy = models.TextField(
        blank=True, 
        null=True, 
        help_text="Details your technical execution rules (e.g., performance tuning, heuristic optimization, security first)."
    )
    immediate_system_goals = models.TextField(
        blank=True, 
        null=True, 
        help_text="Bullet-pointed or structural breakdown of current active milestones."
    )
    
    # Luxury Media Assets
    profile_signature_initial = models.CharField(max_length=10, default="A", blank=True, null=True)

    # Pre-filled Rich Text Blocks
    teaching_area = HTMLField(blank=True, null=True, verbose_name="Teaching Area")
    research_area = HTMLField(blank=True, null=True, verbose_name="Research Area")

    # Section Visibility Toggles
    is_about_visible = models.BooleanField(default=True, verbose_name="Show 'About Me'")
    is_academic_visible = models.BooleanField(default=True, verbose_name="Show 'Academic Appointments'")
    is_admin_visible = models.BooleanField(default=True, verbose_name="Show 'Administrative Appointments'")
    is_honors_visible = models.BooleanField(default=True, verbose_name="Show 'Honors & Awards'")
    is_boards_visible = models.BooleanField(default=True, verbose_name="Show 'Organizations & Boards'")
    is_education_visible = models.BooleanField(default=True, verbose_name="Show 'Professional Education'")
    is_patents_visible = models.BooleanField(default=True, verbose_name="Show 'Patents'")

    # Adaptive Layout Logic
    ALIGNMENT_CHOICES = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ]
    MEDIA_POS_CHOICES = [
        ('left', 'Media Left'),
        ('right', 'Media Right'),
    ]
    horizontal_alignment = models.CharField(max_length=20, choices=ALIGNMENT_CHOICES, default='left', blank=True, null=True)
    media_position = models.CharField(max_length=20, choices=MEDIA_POS_CHOICES, default='left', blank=True, null=True)
    
    # Section Order
    order_about = models.PositiveIntegerField(default=1)
    order_academic = models.PositiveIntegerField(default=2)
    order_admin = models.PositiveIntegerField(default=3)
    order_honors = models.PositiveIntegerField(default=4)
    order_boards = models.PositiveIntegerField(default=5)
    order_education = models.PositiveIntegerField(default=6)
    order_patents = models.PositiveIntegerField(default=7)

    @property
    def public_about_section(self):
        return self.about_sections.filter(is_public=True, is_deleted=False).first()

    @property
    def public_patents(self):
        return self.patents.filter(is_public=True, is_deleted=False)

    def __str__(self):
        return self.name if self.name else "Unnamed Profile"

    class Meta:
        verbose_name = "Systems Identity Core"
        verbose_name_plural = "Systems Identity Cores"

class AboutMe(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='about_sections')
    bio = HTMLField(verbose_name="Narrative Bio", blank=True, null=True)
    intro_video = models.FileField(upload_to='videos/', blank=True, null=True, validators=[validate_is_video], verbose_name="Introduction Video (MP4/MOV)")
    
    class Meta:
        verbose_name = "About Me Section"
        verbose_name_plural = "About Me Sections"

class AcademicAppointment(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='academic_appointments')
    position = models.CharField(max_length=255, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if current")
    
    class Meta:
        verbose_name = "Academic Appointment"
        verbose_name_plural = "Academic Appointments"

class AdministrativeAppointment(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='admin_appointments')
    role = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Administrative Appointment"
        verbose_name_plural = "Administrative Appointments"

class HonorAward(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='honors_awards')
    award_name = models.CharField(max_length=255, blank=True, null=True)
    granting_body = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Honor & Award"
        verbose_name_plural = "Honors & Awards"

class OrganizationBoard(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='org_boards')
    org_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    committee_type = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Organization & Board"
        verbose_name_plural = "Organizations & Boards"

class ProfessionalEducation(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=255, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Professional Education"
        verbose_name_plural = "Professional Education"

class Patent(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='patents')
    title = models.CharField(max_length=500, blank=True, null=True)
    patent_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, help_text="Published/Granted")
    year = models.IntegerField(blank=True, null=True)
    link_or_file = models.FileField(upload_to='patents/', blank=True, null=True, help_text="Upload PDF or CV will link to DOI if URL is pasted below")
    url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Patent"
        verbose_name_plural = "Patents"

class Publication(BaseModel):
    PUB_TYPES = [
        ('Journal', 'Journal Article'),
        ('Conference', 'Conference Paper'),
        ('Book', 'Book/Chapter'),
    ]
    title = models.CharField(max_length=500, blank=True, null=True)
    authors = models.CharField(max_length=500, blank=True, null=True)
    journal_conference_name = models.CharField(max_length=300, blank=True, null=True)
    year_of_publication = models.IntegerField(blank=True, null=True)
    publication_type = models.CharField(max_length=20, choices=PUB_TYPES, default='Journal', blank=True, null=True)
    abstract = encrypt(HTMLField(blank=True, null=True))
    bibtex = models.TextField(blank=True, null=True, verbose_name="BibTeX Citation")
    doi_link = models.URLField(blank=True, null=True, verbose_name="DOI/Link")
    pdf_file = models.FileField(upload_to='publications/', blank=True, null=True, validators=[validate_is_pdf])

    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Untitled Publication"

    class Meta:
        ordering = ['order']

class Course(BaseModel):
    course_code = models.CharField(max_length=50, blank=True, null=True)
    course_title = models.CharField(max_length=200, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    syllabus = models.FileField(upload_to='syllabi/', blank=True, null=True)

    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.course_code} - {self.course_title}"

    class Meta:
        ordering = ['order']

class ResearchProject(BaseModel):
    project_title = models.CharField(max_length=300, blank=True, null=True)
    funding_agency = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active', blank=True, null=True)
    description = encrypt(HTMLField(blank=True, null=True))

    def __str__(self):
        return self.project_title

class NewsAnnouncement(BaseModel):
    headline = models.CharField(max_length=300, blank=True, null=True)
    content = HTMLField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.headline

class LiveProject(BaseModel):
    SYSTEM_STATUS_CHOICES = [
        ('OPERATIONAL', 'Operational'),
        ('MAINTENANCE', 'Maintenance'),
        ('OFFLINE', 'Offline'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    system_status = models.CharField(max_length=50, choices=SYSTEM_STATUS_CHOICES, default='OPERATIONAL')
    uptime_percentage = models.FloatField(default=99.9, blank=True, null=True)
    live_deployment_url = models.URLField(blank=True, null=True)
    github_sync_url = models.URLField(blank=True, null=True)
    active_api_requests = models.IntegerField(default=0, blank=True, null=True)
    drive_folder_link = models.URLField(blank=True, null=True)
    last_synced = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Live Project"

    class Meta:
        ordering = ['-last_synced']

class LocalResource(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    drive_file_id = models.CharField(max_length=255, blank=True, null=True)
    web_view_link = models.URLField(blank=True, null=True)
    resource_file = models.FileField(upload_to='resources/', blank=True, null=True, validators=[validate_is_pdf])
    resource_type = models.CharField(max_length=100, default="PDF")
    last_synced = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Resource"


class GoogleDriveBindModel(models.Model):
    """
    Abstract architecture mixed into portfolio models to allow 
    isolated section panels to link straight to cloud directories.
    """
    drive_folder_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text="Target Google Drive Folder ID (e.g., 1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W)"
    )
    auto_sync_assets = models.BooleanField(
        default=True, 
        help_text="If enabled, background cron tasks will systematically parse this folder."
    )

    class Meta:
        abstract = True


class SystemDeployment(BaseModel, GoogleDriveBindModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    telemetry_metric = models.CharField(max_length=255, blank=True, null=True)
    endpoint_url = models.URLField(blank=True, null=True)
    system_architecture = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, blank=True, null=True)
    asset_attachments = GenericRelation('AssetAttachment')

    def __str__(self):
        return self.name if self.name else "Unnamed System Deployment"

    class Meta:
        ordering = ['order']
        verbose_name = "System Deployment"
        verbose_name_plural = "System Deployments"


# ==========================================
# SYSTEM 1: WORKBENCH LAB PROTO TYPES
# ==========================================
class LabPrototype(GoogleDriveBindModel):
    """Tracks raw, un-deployed sandboxed files, R&D scripts, or experimental models."""
    title = models.CharField(max_length=255, blank=True, null=True)
    runtime_environment = models.CharField(max_length=100, default="Python 3.11 // PyTorch")
    notebook_or_file = models.FileField(upload_to='lab_sandbox/', blank=True, null=True)
    mathematical_core = models.TextField(blank=True, null=True, help_text="Formulas, optimization loss details, or algorithm logic")
    is_public = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Prototype"

# ==========================================
# SYSTEM 2: OPEN SOURCE CONTRIBUTION LEDGER
# ==========================================
class OpenSourceContribution(models.Model):
    """Tracks merged pull requests, structural issue fixes, or open-source repo tracking."""
    repository_name = models.CharField(max_length=255, blank=True, null=True)
    pull_request_url = models.URLField(blank=True, null=True)
    impact_summary = models.TextField(blank=True, null=True, help_text="What structural code did you optimize or refactor?")
    lines_optimized = models.IntegerField(default=0, blank=True, null=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.repository_name if self.repository_name else "Untitled Contribution"

# ==========================================
# SYSTEM 3: TECHNICAL STACK GRAPH & WEIGHTS
# ==========================================
class TechStackMetric(models.Model):
    # Updated Elite Domain Categories
    CATEGORY_CHOICES = [
        ('WEB_EDGE', 'Web & Edge Infrastructure'),
        ('AI_CORE', 'Artificial Intelligence & Data'),
        ('QUANTUM', 'Quantum Engineering'),
        ('SECURITY', 'Systems Security & Vaults'),
    ]
    technology_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='WEB_EDGE')
    verified_use_cases = models.TextField(help_text="Verified production use cases.", blank=True, null=True)
    order = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.technology_name if self.technology_name else "Untitled Stack Metric"

# ==========================================
# SYSTEM 4: SYSTEM ANNOUNCEMENTS & LOGS
# ==========================================
class TerminalLog(models.Model):
    """A minimal system log feed detailing certifications earned or major project milestones achieved."""
    timestamp = models.DateTimeField(auto_now_add=True)
    log_level = models.CharField(max_length=10, default="INFO") # INFO, SUCCESS, SECURITY
    message = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.log_level}] {self.message[:30]}..."

# ==========================================
# SYSTEM 5: DIGITAL GUESTBOOK / REFERENCE MATRIX
# ==========================================
class PeerReference(models.Model):
    """A clean panel for authenticated peer validations, project recommendations, or collaborator sign-offs."""
    referee_name = models.CharField(max_length=255, blank=True, null=True)
    organization_or_title = models.CharField(max_length=255, blank=True, null=True)
    verification_hash = models.CharField(max_length=64, blank=True, null=True, help_text="Optional secure validator hash")
    statement = models.TextField()
    is_public = models.BooleanField(default=False) # Requires manual dashboard approval first

    def __str__(self):
        return self.referee_name if self.referee_name else "Untitled Reference"


class LearningProject(GoogleDriveBindModel):
    """
    Manages high-fidelity R&D blueprints, algorithmic feasibility studies, 
    and conceptual end-to-end system designs.
    """
    title = models.CharField(max_length=255, blank=True, null=True)
    core_concept_approaches = models.TextField(blank=True, null=True, help_text="Detailed approach matrices (Micro, Macro, Hybrid).")
    key_parameters = models.TextField(blank=True, null=True, help_text="Sensor benchmarks and computer vision monitoring vectors.")
    ml_architectures = models.TextField(blank=True, null=True, help_text="Specific model structures (YOLOv8, Isolation Forest, LSTMs).")
    system_architecture_layers = models.TextField(blank=True, null=True, help_text="End-to-end operational pipeline stack loops.")
    implementation_mvp_steps = models.TextField(blank=True, null=True, help_text="Phased developmental execution directives.")
    advanced_features = models.TextField(blank=True, null=True, help_text="Advanced technical enhancements (Digital Twins, Source Tracing).")
    
    is_public = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    asset_attachments = GenericRelation('AssetAttachment')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "R&D Architecture Blueprint"
        verbose_name_plural = "R&D Architecture Blueprints"

    def __str__(self):
        return self.title or "Untitled Blueprint"


class AssetAttachment(models.Model):
    """
    Polymorphic Asset Broker: Attaches local uploads or permanent Google Drive 
    sharing strings to ANY section model dynamically.
    """
    RESOURCE_TYPES = [
        ('LOCAL', 'Local Disk Storage'),
        ('DRIVE', 'Google Drive Asset Link'),
    ]

    label = models.CharField(max_length=150, help_text="E.g., Production Blueprint PDF, JSON Configuration Schema")
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='LOCAL')
    
    # Local File Storage Field
    local_file = models.FileField(upload_to='section_assets/', blank=True, null=True, help_text="Upload directly to your server storage.")
    
    # Cloud Link Field
    drive_direct_url = models.URLField(blank=True, null=True, help_text="Drop the unrestricted sharing or download link from Google Drive.")

    # Generic Foreign Key Configuration to bind to any section model seamlessly
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "System Asset Attachment"
        verbose_name_plural = "System Asset Attachments"

    def get_download_url(self):
        """Resolves the safe download target depending on storage rules."""
        if self.resource_type == 'LOCAL' and self.local_file:
            return self.local_file.url
        return self.drive_direct_url or "#"


class ValidationMilestone(GoogleDriveBindModel):
    """
    Credentials & System Validations Ledger: Houses high-end technical
    certifications, awards, and cryptographic system validations.
    """
    VALIDATION_TYPES = [
        ('CERTIFICATION', 'Professional Certification'),
        ('AWARD', 'System Distinction / Award'),
        ('MILESTONE', 'Infrastructure Milestone'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True, help_text="E.g., Infosys 'Carbon Smart' Certification")
    issuing_authority = models.CharField(max_length=255, blank=True, null=True, help_text="E.g., Dr. A.P.J. Abdul Kalam AI Lab")
    classification = models.CharField(max_length=20, choices=VALIDATION_TYPES, default='CERTIFICATION')
    date_secured = models.DateField(blank=True, null=True)
    
    # Optional Local Media Field supporting PDF, JPG, PNG explicitly
    local_credential_file = models.FileField(
        upload_to='credentials_vault/', 
        blank=True, 
        null=True, 
        help_text="Upload certificate directly (PDF, JPG, PNG)."
    )
    
    is_public = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    asset_attachments = GenericRelation('AssetAttachment')

    class Meta:
        ordering = ['order', '-date_secured']
        verbose_name = "System Validation Milestone"
        verbose_name_plural = "System Validation Milestones"

    def __str__(self):
        return f"{self.title} // {self.issuing_authority}"


# ============================================================
# KNOWLEDGE VAULT — Unified Dual-Source Asset Registry
# ============================================================

class KnowledgeAsset(models.Model):
    """
    Unified schema for Certificates and Learning Module assets.

    Supports two independent storage backends:
      LOCAL_DISK   — file served from MEDIA_ROOT via the `local_file` FileField
                     or an absolute path stored in `uri`.
      GOOGLE_DRIVE — streamed live from Drive API v3 using the Drive File ID
                     stored in `uri`.

    The `metadata` JSONField is schema-free and can carry any auxiliary
    structured data (issuer, issue date, expiry, tags, module chapters, etc.).
    """

    ASSET_TYPE_CHOICES = [
        ('CERTIFICATE',    'Certificate'),
        ('LEARNING_MODULE', 'Learning Module'),
    ]

    STORAGE_PROVIDER_CHOICES = [
        ('LOCAL_DISK',    'Local Disk'),
        ('GOOGLE_DRIVE',  'Google Drive'),
    ]

    title = models.CharField(
        max_length=255,
        help_text="Human-readable asset name (e.g. 'AWS Solutions Architect – Associate')."
    )
    asset_type = models.CharField(
        max_length=20,
        choices=ASSET_TYPE_CHOICES,
        default='CERTIFICATE',
        db_index=True,
    )
    storage_provider = models.CharField(
        max_length=15,
        choices=STORAGE_PROVIDER_CHOICES,
        default='LOCAL_DISK',
        help_text="Where the underlying file lives."
    )
    uri = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text=(
            "LOCAL_DISK → absolute server path (must be inside MEDIA_ROOT). "
            "GOOGLE_DRIVE → Drive File ID (e.g. 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms)."
        )
    )
    local_file = models.FileField(
        upload_to='knowledge_vault/',
        blank=True,
        null=True,
        help_text="Upload the file directly. Takes precedence over URI for LOCAL_DISK assets."
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            'Free-form JSON payload. Examples: '
            '{"issuer": "Coursera", "issued_date": "2024-03", "tags": ["Python", "ML"]} '
            'or {"platform": "Udemy", "chapters": 42, "hours": 28.5}.'
        )
    )
    is_public = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Knowledge Asset"
        verbose_name_plural = "Knowledge Assets"
        indexes = [
            models.Index(fields=['asset_type', 'is_public']),
        ]

    def __str__(self):
        return f"[{self.get_asset_type_display()}] {self.title}"

    @property
    def is_drive_backed(self) -> bool:
        return self.storage_provider == 'GOOGLE_DRIVE'

    @property
    def issuer(self) -> str:
        """Convenience accessor for the most common metadata key."""
        return self.metadata.get('issuer', '—')

import uuid

class SideVentureAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    
    CATEGORY_CHOICES = [
        ('SIDE_VENTURE', 'Side Venture'),
        ('UNPUBLISHED_CONTENT', 'Unpublished Content'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='SIDE_VENTURE')
    
    FILE_TYPE_CHOICES = [
        ('PDF', 'PDF Document'),
        ('BINARY', 'Compiled Binary'),
        ('DATASET', 'Dataset / JSON / CSV'),
        ('IMAGE', 'Image Asset'),
        ('RAW_CODE', 'Raw Source Code'),
    ]
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='PDF')
    
    STORAGE_PROVIDER_CHOICES = [
        ('LOCAL_DISK', 'Local Disk'),
        ('GOOGLE_DRIVE', 'Google Drive'),
    ]
    storage_provider = models.CharField(max_length=20, choices=STORAGE_PROVIDER_CHOICES, default='LOCAL_DISK')
    
    uri = models.CharField(max_length=1024, blank=True, null=True, help_text="Generated automatically upon upload")
    
    upload = models.FileField(upload_to='ventures/', blank=True, null=True, help_text="Upload your asset here.")
    
    is_public = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-timestamp']
        verbose_name = "Side Venture & Unpublished Content"
        verbose_name_plural = "Side Ventures & Unpublished Content"

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"
