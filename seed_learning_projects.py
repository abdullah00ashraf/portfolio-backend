import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import LearningProject

def seed_learning_sandbox():
    # Clear existing entries in this category to maintain clean unique references
    LearningProject.objects.filter(title__icontains="River Water Pollution").delete()

    LearningProject.objects.create(
        title="River Water Pollution Detection System using ML",
        core_concept_approaches=(
            "• Approach A: The 'Micro-Level' (IoT & Sensors)\n"
            "  Focus: Chemical/physical water properties via floating sensor matrices streaming directly to cloud layers. Optimal for detecting invisible industrial dumping.\n\n"
            "• Approach B: The 'Macro-Level' (Computer Vision)\n"
            "  Focus: Visible physical debris and surface anomalies via drone, CCTV, or Sentinel-2 satellite imagery to map floating plastic arrays and algal blooms.\n\n"
            "• Approach C: The Hybrid System\n"
            "  Focus: Comprehensive spatial monitoring merging real-time sensor streams with computer vision validation loops."
        ),
        key_parameters=(
            "• Sensor Array Matrices: Tracking pH levels (industrial runoff spikes), Turbidity (suspended solids), Dissolved Oxygen (low DO = critical pollution indicators), Temperature (thermal power plant runoff), and Total Dissolved Solids (TDS/heavy metals).\n\n"
            "• Computer Vision Frameworks: Real-time image processing mapping floating plastics/debris patches, rainbow oil sheens, and eutrophication/algae discoloration boundaries."
        ),
        ml_architectures=(
            "• Time-Series & Anomaly Profiling: Implements Isolation Forests and Autoencoders for unsupervised anomaly profiling. Employs Random Forest / XGBoost for safety classification alongside LSTMs and GRUs for predictive 24-hour forecasting arrays.\n\n"
            "• Convolutional Computer Vision: Deploys YOLOv8 / EfficientDet models for high-speed object bounding boxes around floating plastics, combined with U-Net / Mask R-CNN architectures for pixel-perfect semantic segmentation tracking."
        ),
        system_architecture_layers=(
            "• Layer 1: Edge Computing Node\n"
            "  Hardware: ESP32 or LoRaWAN transmitters paired with DS18B20 temperature arrays and analog turbidity nodes. Raspberry Pi 4 run loops execute edge-optimized TFLite models natively.\n\n"
            "• Layer 2: Network Carrier Protocol\n"
            "  Transmission via lightweight MQTT protocols directly over unstable river networks into localized InfluxDB time-series arrays and AWS S3 object storage structures.\n\n"
            "• Layer 3: Central Inference Brain\n"
            "  FastAPI infrastructure engine loads serialized model footprints (.h5/.pkl) to compute low-latency inference parameters from incoming streaming JSON bodies.\n\n"
            "• Layer 4: Tactical Control Console\n"
            "  Built using a responsive mapping dashboard displaying live telemetry positions, historical data trends, and automated alerting arrays via Twilio pipelines."
        ),
        implementation_mvp_steps=(
            "1. Data Acquisition: Parsing public historical data repositories alongside custom hardware simulation datasets.\n"
            "2. Exploratory Analysis: Evaluating mathematical correlations between Dissolved Oxygen, temperature fluxes, and chemical spikes.\n"
            "3. Model Optimization: Ingesting and training Random Forest classifiers to predict accurate Water Quality Index (WQI) scores above an 85% validation threshold.\n"
            "4. Web Deployment: Provisioning an administrative control desk where field parameters can be evaluated manually or parsed straight from telemetry endpoints."
        ),
        advanced_features=(
            "• Upstream Source Tracing: Utilizing fluid mechanics flow data models to mathematically backtrack and isolate upstream illegal chemical discharge origins.\n"
            "• Hydrological Digital Twin: Creating an integrated 3D virtual environment mapping active river tracks that adapts its visual states dynamically via operational streaming parameters.\n"
            "• Citizen Validation Engine: Crowdsourced mobile ingestion portals enabling users to upload geotagged images, cross-verifying satellite and sensor boundaries instantly."
        ),
        order=1,
        drive_folder_id="1JoUaUR4j9KFPg_cDL0F0gn2lrTZcbC8W"  # Connected directly to your cloud data vault
    )

    print("Intellectual R&D Learning Blueprint ingested successfully.")

if __name__ == '__main__':
    seed_learning_sandbox()
