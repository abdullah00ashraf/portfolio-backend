import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academic_portal.settings')
django.setup()

from portfolio.models import TechStackMetric

def reseed_capability_matrix():
    # Flush existing metrics for a clean slate
    TechStackMetric.objects.all().delete()

    tech_components = [
        # ==========================================
        # 1. WEB & EDGE INFRASTRUCTURE (WEB_EDGE)
        # ==========================================
        {
            "name": "Vanilla JS (ES6+) & Glassmorphism UI",
            "category": "WEB_EDGE",
            "use_cases": "Zero-latency execution using pure async/await DOM manipulation. Styled with Tailwind CSS via CDN for rapid responsive scaling and 'Tesla Obsidian' glassmorphism.",
            "order": 1
        },
        {
            "name": "Hardware Interfacing APIs",
            "category": "WEB_EDGE",
            "use_cases": "Utilizes Geolocation API for live evacuation routing, Web Audio API for hardware-level SOS oscillators, and Vibration API for high-frequency visual strobe signaling.",
            "order": 2
        },
        {
            "name": "Leaflet.js Canvas & Spatial APIs",
            "category": "WEB_EDGE",
            "use_cases": "Operates Leaflet in preferCanvas mode to render 2,025 tactical nodes without DOM lag. Integrates OSRM for live evacuation route geometries and CartoDB/Esri Basemaps.",
            "order": 3
        },
        {
            "name": "FastAPI & Redis Edge Cache",
            "category": "WEB_EDGE",
            "use_cases": "Asynchronous backend gateway hosting low-latency REST endpoints via Uvicorn, with Redis acting as a state-tracking memory database for high-traffic payload routing.",
            "order": 4
        },

        # ==========================================
        # 2. ARTIFICIAL INTELLIGENCE & DATA (AI_CORE)
        # ==========================================
        {
            "name": "Hugging Face Ecosystem",
            "category": "AI_CORE",
            "use_cases": "Leverages Hugging Face Spaces for live Bi-LSTM neural inferences (managing 8-factor environmental tensors) and Datasets for ingesting sensor telemetry like rainfall and river discharge.",
            "order": 5
        },
        {
            "name": "PyTorch & Physics-Informed ML",
            "category": "AI_CORE",
            "use_cases": "Primary deep learning framework. Deploys an integrated Physics-Informed Neural Network (PINN) core to enforce thermodynamic mass balance and surface runoff laws.",
            "order": 6
        },
        {
            "name": "Deep Bi-LSTM & XAI Frameworks",
            "category": "AI_CORE",
            "use_cases": "Multi-layer Neural Core parsing time-series hydrology datasets bidirectionally. Integrates Explainable AI (XAI) to map raw inputs to model prediction confidence thresholds.",
            "order": 7
        },

        # ==========================================
        # 3. QUANTUM ENGINEERING (QUANTUM)
        # ==========================================
        {
            "name": "Post-Quantum Cryptography Bridge",
            "category": "QUANTUM",
            "use_cases": "Embedded via a web-client handshake bridge (ml_kem_bridge.js) using PQ-Kyber primitives to secure client-to-server networks against future post-quantum decryption threats.",
            "order": 8
        },

        # ==========================================
        # 4. SYSTEMS SECURITY (SECURITY)
        # ==========================================
        {
            "name": "Anti-Replay Middleware & HMAC",
            "category": "SECURITY",
            "use_cases": "Intercepts API packets to cross-examine incoming UUID tokens against a 60-second sliding window. Enforces HMAC-SHA256 message authentication codes directly against transactional bodies.",
            "order": 9
        },
        {
            "name": "PostgreSQL Vault & Memory Locks",
            "category": "SECURITY",
            "use_cases": "Conceptual multi-shard Master Vault utilizing AES-256 encryption. Operates OS Memory Locks (mlock) via ctypes to isolate Data Encryption Keys (DEKs) in RAM from swap files.",
            "order": 10
        },
    ]

    for item in tech_components:
        TechStackMetric.objects.create(
            technology_name=item["name"],
            category=item["category"],
            verified_use_cases=item["use_cases"],
            order=item["order"]
        )

    print(f"Successfully loaded {len(tech_components)} partitioned capabilities across Web, AI, Quantum, and Security domains.")

if __name__ == '__main__':
    reseed_capability_matrix()
