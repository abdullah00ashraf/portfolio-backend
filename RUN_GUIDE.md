# Running the Academic Portal

This guide provides step-by-step instructions for running both the Django backend and the React frontend.

## 1. Prerequisites
- **Python 3.11+**
- **Node.js & npm**
- **Virtual Environment**: All dependencies are installed in the `venv` directory. **Always use the virtual environment to avoid "Module Not Found" errors.**

---

## 2. Running the Backend (Django)

### Step 1: Activate the Virtual Environment
Open your terminal (PowerShell or CMD) in the `c:\PROTOFOLIO` directory and run:

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
.\venv\Scripts\activate.bat
```

### Step 2: Database Setup & Migrations
Ensure your database is up to date with the latest Profile system changes:
```bash
python manage.py migrate
```

### Step 3: Start the Server
```bash
python manage.py runserver
```
The backend will be available at `http://127.0.0.1:8000/`.

---

## 3. Running the Frontend (React & esbuild)

The frontend is a specialized component (like the Liquid Footer) that is bundled and served by Django.

### Step 1: Navigate to Frontend
```bash
cd frontend
```

### Step 2: Install Dependencies (If not already done)
```bash
npm install
```

### Step 3: Build the Bundle
This command compiles the React code into a single Javascript file that Django can serve:
```bash
npm run build
```
The output is automatically saved to `static/portfolio/js/footer.bundle.js`.

---

## 4. Production Assets (Performance Check)

Since we implemented **Django Compressor**, you might need to run the following if you want to test the production minification locally:

```bash
python manage.py collectstatic --noinput
python manage.py compress
```

## 5. Troubleshooting

### "ModuleNotFoundError: No module named 'unfold'"
This happens when you run `python manage.py` without activating the virtual environment. Always ensure `(venv)` is visible in your terminal prompt, or run commands directly using the venv path:
```bash
.\venv\Scripts\python.exe manage.py runserver
```

### Admin Access
- **URL**: `http://127.0.0.1:8000/admin/`
- Use your superuser credentials to access the "Power Profile" controls.
