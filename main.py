#!/usr/bin/env python3
"""
Hospital Management System (HMS) Enterprise Platform Entry Point.
Executes database migrations and launches the Django REST API service.
"""

import os
import sys
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")

    print("=" * 70)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM (HMS) ENTERPRISE PLATFORM")
    print("=" * 70)
    print("Starting Django REST Framework backend on http://127.0.0.1:8000...")
    print("Interactive API Docs available at http://127.0.0.1:8000/api/docs/")
    print("=" * 70)

    # Set Django settings module if needed
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hms_core.settings")

    manage_py = os.path.join(backend_dir, "manage.py")
    if not os.path.exists(manage_py):
        manage_py = os.path.join(base_dir, "manage.py")

    cmd = [sys.executable, manage_py, "runserver", "127.0.0.1:8000"]
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nHMS Service gracefully stopped.")
    except Exception as exc:
        print(f"Error launching HMS platform: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
