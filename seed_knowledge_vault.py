import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import KnowledgeAsset

def seed_knowledge_vault():
    # Flush existing to avoid duplicates
    KnowledgeAsset.objects.all().delete()

    assets = [
        # --- CERTIFICATES ---
        {
            "title": "Letter of Appreciation // AI Kit Demonstration",
            "asset_type": "CERTIFICATE",
            "storage_provider": "GOOGLE_DRIVE",
            "uri": "1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W",
            "metadata": {
                "issuer": "Dr. A.P.J. Abdul Kalam AI Lab Inauguration",
                "issued_date": "2025-09-15",
                "classification": "AWARD",
                "verification_method": "SHA-256 SYSTEM DIRECT"
            },
            "order": 1,
            "is_public": True
        },
        {
            "title": "Team Leader Distinction // 'The Aegis' (Team ID 75864)",
            "asset_type": "CERTIFICATE",
            "storage_provider": "GOOGLE_DRIVE",
            "uri": "1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W",
            "metadata": {
                "issuer": "Smart India Hackathon 2025",
                "issued_date": "2025-12-20",
                "classification": "MILESTONE",
                "verification_method": "SHA-256 SYSTEM DIRECT"
            },
            "order": 2,
            "is_public": True
        },
        {
            "title": "'Carbon Smart' Sustainability Certification",
            "asset_type": "CERTIFICATE",
            "storage_provider": "GOOGLE_DRIVE",
            "uri": "1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W",
            "metadata": {
                "issuer": "Infosys Springboard Sustainability Initiative",
                "issued_date": "2025-10-05",
                "classification": "CERTIFICATION",
                "verification_method": "SHA-256 SYSTEM DIRECT"
            },
            "order": 3,
            "is_public": True
        },
        {
            "title": "First Prize // Nagar Stariya Vigyan Mela (City Science Fair)",
            "asset_type": "CERTIFICATE",
            "storage_provider": "GOOGLE_DRIVE",
            "uri": "1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W",
            "metadata": {
                "issuer": "Lucknow Municipal Science Registry",
                "issued_date": "2017-11-10",
                "classification": "AWARD",
                "verification_method": "SHA-256 SYSTEM DIRECT"
            },
            "order": 4,
            "is_public": True
        },
        # --- LEARNING MODULES ---
        {
            "title": "River Water Pollution Detection System using ML",
            "asset_type": "LEARNING_MODULE",
            "storage_provider": "GOOGLE_DRIVE",
            "uri": "1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W",
            "metadata": {
                "platform": "R&D Sandbox",
                "core_concept_approaches": (
                    "• Approach A: The 'Micro-Level' (IoT & Sensors)\n"
                    "  Focus: Chemical/physical water properties via floating sensor matrices streaming directly to cloud layers. Optimal for detecting invisible industrial dumping.\n\n"
                    "• Approach B: The 'Macro-Level' (Computer Vision)\n"
                    "  Focus: Visible physical debris and surface anomalies via drone, CCTV, or Sentinel-2 satellite imagery to map floating plastic arrays and algal blooms.\n\n"
                    "• Approach C: The Hybrid System\n"
                    "  Focus: Comprehensive spatial monitoring merging real-time sensor streams with computer vision validation loops."
                ),
                "key_parameters": (
                    "• Sensor Array Matrices: Tracking pH levels (industrial runoff spikes), Turbidity (suspended solids), Dissolved Oxygen (low DO = critical pollution indicators), Temperature (thermal power plant runoff), and Total Dissolved Solids (TDS/heavy metals).\n\n"
                    "• Computer Vision Frameworks: Real-time image processing mapping floating plastics/debris patches, rainbow oil sheens, and eutrophication/algae discoloration boundaries."
                ),
                "ml_architectures": (
                    "• Time-Series & Anomaly Profiling: Implements Isolation Forests and Autoencoders for unsupervised anomaly profiling. Employs Random Forest / XGBoost for safety classification alongside LSTMs and GRUs for predictive 24-hour forecasting arrays.\n\n"
                    "• Convolutional Computer Vision: Deploys YOLOv8 / EfficientDet models for high-speed object bounding boxes around floating plastics, combined with U-Net / Mask R-CNN architectures for pixel-perfect semantic segmentation tracking."
                ),
                "system_architecture_layers": (
                    "• Layer 1: Edge Computing Node\n"
                    "  Hardware: ESP32 or LoRaWAN transmitters paired with DS18B20 temperature arrays and analog turbidity nodes. Raspberry Pi 4 run loops execute edge-optimized TFLite models natively.\n\n"
                    "• Layer 2: Network Carrier Protocol\n"
                    "  Transmission via lightweight MQTT protocols directly over unstable river networks into localized InfluxDB time-series arrays and AWS S3 object storage structures.\n\n"
                    "• Layer 3: Central Inference Brain\n"
                    "  FastAPI infrastructure engine loads serialized model footprints (.h5/.pkl) to compute low-latency inference parameters from incoming streaming JSON bodies.\n\n"
                    "• Layer 4: Tactical Control Console\n"
                    "  Built using a responsive mapping dashboard displaying live telemetry positions, historical data trends, and automated alerting arrays via Twilio pipelines."
                ),
                "implementation_mvp_steps": (
                    "1. Data Acquisition: Parsing public historical data repositories alongside custom hardware simulation datasets.\n"
                    "2. Exploratory Analysis: Evaluating mathematical correlations between Dissolved Oxygen, temperature fluxes, and chemical spikes.\n"
                    "3. Model Optimization: Ingesting and training Random Forest classifiers to predict accurate Water Quality Index (WQI) scores above an 85% validation threshold.\n"
                    "4. Web Deployment: Provisioning an administrative control desk where field parameters can be evaluated manually or parsed straight from telemetry endpoints."
                ),
                "advanced_features": (
                    "• Upstream Source Tracing: Utilizing fluid mechanics flow data models to mathematically backtrack and isolate upstream illegal chemical discharge origins.\n"
                    "• Hydrological Digital Twin: Creating an integrated 3D virtual environment mapping active river tracks that adapts its visual states dynamically via operational streaming parameters.\n"
                    "• Citizen Validation Engine: Crowdsourced mobile ingestion portals enabling users to upload geotagged images, cross-verifying satellite and sensor boundaries instantly."
                )
            },
            "order": 1,
            "is_public": True
        }
    ]

    for item in assets:
        KnowledgeAsset.objects.create(
            title=item["title"],
            asset_type=item["asset_type"],
            storage_provider=item["storage_provider"],
            uri=item["uri"],
            metadata=item["metadata"],
            order=item["order"],
            is_public=item["is_public"]
        )

    print(f"Successfully seeded {len(assets)} items into the Knowledge Vault.")

if __name__ == '__main__':
    seed_knowledge_vault()
