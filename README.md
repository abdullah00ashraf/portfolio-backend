# Portfolio Backend: Django Academic & Systems Ledger Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Framework: Django 5.2](https://img.shields.io/badge/Django-5.2-darkgreen.svg)](https://www.djangoproject.com/)
[![Database: SQLite / PostgreSQL](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-blue.svg)](https://docs.djangoproject.com/en/5.2/ref/databases/)
[![Admin: Django Unfold](https://img.shields.io/badge/Admin-Unfold%20Tailwind-purple.svg)](https://github.com/unfoldadmin/django-unfold)

**Portfolio Backend (academic_portal)** is a high-security Django web service and data ledger powering the **Abdullah Ashraf Systems Portfolio**.

It provides data persistence, cryptographic credential validation, technical milestone registries, and API endpoints for decoupled frontend clients (such as [`portfolio-frontend`](https://github.com/abdullah00ashraf/portfolio-frontend)).

---

## 1. Architecture & Core Subsystems

```mermaid
graph TD
    Client["Decoupled Frontend (React / Vite UI)"] -->|REST API / JSON| Django["Django 5 Core (academic_portal)"]
    
    subgraph Core_Models["Portfolio Domain Models (portfolio/models.py)"]
        Django --> Profile["Profile & Systems Identity"]
        Django --> Milestone["ValidationMilestone (Awards & Hackathons)"]
        Django --> Knowledge["KnowledgeVault (Papers & Research)"]
        Django --> Projects["LearningProjects & TechStack"]
    end

    subgraph Security_Layer["Security & Storage"]
        Django --> Crypto["AES Cryptography Provider"]
        Django --> Storage["Isolated Credentials Vault (Google Drive API)"]
        Django --> DB[("Database (SQLite / PostgreSQL)")]
    end

    Admin["Custom Admin Portal (Django Unfold)"] --> Django
```

---

## 2. Directory Structure

```
PROTOFOLIO/
├── academic_portal/           # Django project root & settings
│   ├── asgi.py
│   ├── settings.py            # Environment-driven settings & security configs
│   ├── urls.py                # Main URL router
│   └── wsgi.py
├── portfolio/                 # Primary portfolio application
│   ├── admin.py               # Tailored Django Unfold admin interfaces
│   ├── apps.py
│   ├── models.py              # Profile, ValidationMilestone, KnowledgeVault
│   └── views.py               # REST API endpoints & data serializations
├── credentials/               # Isolated credentials directory (.gitignore protected)
│   └── google_drive_key.json.example
├── seed_credentials.py        # Database seeding for awards and certifications
├── seed_developer.py          # Database seeding for full developer profile
├── seed_identity.py           # Database seeding for systems manifesto
├── seed_knowledge_vault.py    # Database seeding for research papers
├── requirements.txt           # Production dependencies
├── manage.py                  # Django management CLI
├── .env.example               # Environment template
└── README.md                  # Backend documentation
```

---

## 3. Quickstart & Installation

### Prerequisites
- Python >= 3.11
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abdullah00ashraf/portfolio-backend.git
   cd portfolio-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   ```bash
   cp .env.example .env
   # Customize .env with your local settings and SECRET_KEY
   ```

5. **Apply Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Seed Initial Database Ledger:**
   ```bash
   python seed_identity.py
   python seed_credentials.py
   python seed_developer.py
   python seed_knowledge_vault.py
   ```

7. **Create Superuser & Run Development Server:**
   ```bash
   python manage.py createsuperuser
   python manage.py runserver 8000
   ```
Access the custom Unfold admin dashboard at [http://localhost:8000/admin/](http://localhost:8000/admin/).

---

## 4. Configuration Reference

| Variable | Description |
| :--- | :--- |
| `SECRET_KEY` | Unique cryptographic salt used for Django session and token signing |
| `DEBUG` | Enable/disable detailed debug traces (`True` in development, `False` in production) |
| `ALLOWED_HOSTS` | Comma-delimited list of permitted domain names |
| `CRYPTOGRAPHY_KEY` | AES encryption key for securing private metadata fields |
| `GOOGLE_DRIVE_API_KEY` | API key for interacting with Google Drive credential attachments |

---

## 5. License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
