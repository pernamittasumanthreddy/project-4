#!/usr/bin/env python3
"""
Hospital Management System (HMS) — Member 6 Main Entry Point
Production runtime entry point for the Multi-Tenant Finance, Billing, Insurance, and Accounting Engine.
"""
import os
import sys
import subprocess

def get_python_interpreter(base_dir):
    # Check for local venv
    win_venv = os.path.join(base_dir, "venv", "Scripts", "python.exe")
    posix_venv = os.path.join(base_dir, "venv", "bin", "python")
    if os.path.exists(win_venv):
        return win_venv
    if os.path.exists(posix_venv):
        return posix_venv
    return sys.executable

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python main.py [options]")
        print("Options:")
        print("  --help, -h       Display this help message")
        print("  --migrate-only   Run database migrations and exit")
        print("  --seed-only      Seed financial master data and exit")
        print("  --port PORT      Custom port for backend server (default: 8000)")
        sys.exit(0)

    print("================================================================================")
    print("Hospital Management System (HMS) — Member 6 Finance & Accounting Suite")
    print("================================================================================")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    py_exec = get_python_interpreter(base_dir)
    manage_py = os.path.join(backend_dir, "manage.py")

    # Run database migrations
    print("[1/3] Checking and applying database migrations...")
    subprocess.run([py_exec, manage_py, "migrate"], check=False)

    if "--migrate-only" in sys.argv:
        print("Migrations complete.")
        sys.exit(0)

    # Seed master data if needed
    print("[2/3] Verifying master financial data & chart of accounts...")
    subprocess.run([py_exec, manage_py, "seed_finance_data"], check=False)

    if "--seed-only" in sys.argv:
        print("Seeding complete.")
        sys.exit(0)

    # Port parsing
    port = "8000"
    if "--port" in sys.argv:
        try:
            port = sys.argv[sys.argv.index("--port") + 1]
        except (IndexError, ValueError):
            port = "8000"

    # Start Django server
    print(f"[3/3] Launching Member 6 API server on http://127.0.0.1:{port}/ ...")
    subprocess.run([py_exec, manage_py, "runserver", f"0.0.0.0:{port}"])

if __name__ == "__main__":
    main()
