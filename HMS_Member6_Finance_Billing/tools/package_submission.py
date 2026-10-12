import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_PARTS = {
    'node_modules',
    'venv',
    'env',
    'dist',
    '.pytest_cache',
    '__pycache__',
}

def should_exclude(rel_path: Path) -> bool:
    parts = set(rel_path.parts)
    # Exclude if any part matches excluded directory names
    if any(p in EXCLUDED_PARTS for p in parts):
        return True
    # Exclude compiled python bytecode
    if rel_path.suffix in ('.pyc', '.pyo', '.pyd'):
        return True
    # Exclude other zip archives
    if rel_path.suffix == '.zip':
        return True
    return False

def package_zip(dest_zip_path: Path):
    print(f"Creating zip archive at: {dest_zip_path}...")
    total_files = 0
    total_bytes = 0
    has_git = False
    
    dest_zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(dest_zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(ROOT):
            # Prune excluded dirs in-place to avoid walking huge node_modules or venv
            dirs[:] = [d for d in dirs if d not in EXCLUDED_PARTS]
            
            for f in files:
                full_path = Path(root) / f
                rel_path = full_path.relative_to(ROOT)
                
                if should_exclude(rel_path):
                    continue
                
                # Check if .git is captured
                if '.git' in rel_path.parts:
                    has_git = True
                
                zf.write(full_path, arcname=str(rel_path))
                total_files += 1
                total_bytes += full_path.stat().st_size

    zip_size_mb = dest_zip_path.stat().st_size / (1024 * 1024)
    print(f"Zip created successfully!")
    print(f"  - Files packaged: {total_files}")
    print(f"  - Uncompressed size: {total_bytes / (1024 * 1024):.2f} MB")
    print(f"  - Archive size: {zip_size_mb:.2f} MB")
    print(f"  - .git included: {has_git}")
    return has_git

def verify_zip(zip_path: Path):
    print(f"\nVerifying archive: {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()
        git_entries = [n for n in names if n.startswith('.git/')]
        print(f"  - Total entries in zip: {len(names)}")
        print(f"  - .git entries found: {len(git_entries)}")
        if '.git/HEAD' in names:
            print("  - CONFIRMED: .git/HEAD is present in archive root!")
        else:
            raise RuntimeError(".git/HEAD missing from archive root!")
            
        # Check prod files
        has_main_py = 'main.py' in names
        has_backend = any(n.startswith('backend/') for n in names)
        has_frontend = any(n.startswith('frontend/src/') for n in names)
        print(f"  - main.py present: {has_main_py}")
        print(f"  - backend present: {has_backend}")
        print(f"  - frontend present: {has_frontend}")
        
        # Check no .env committed/present
        env_files = [n for n in names if n == '.env' or n.startswith('.env.') or (n.endswith('.env') and n != 'example.env')]
        print(f"  - Sensitive .env files found: {env_files}")
        if env_files:
            raise RuntimeError(f"Found sensitive .env files: {env_files}")

if __name__ == '__main__':
    dest_paths = [
        ROOT / "HMS_Member6_Finance_Billing.zip",
        Path("C:/Users/pedha/OneDrive/Desktop/HMS_Member6_Finance_Billing.zip"),
    ]
    if Path("C:/Users/pedha/Desktop").exists():
        dest_paths.append(Path("C:/Users/pedha/Desktop/HMS_Member6_Finance_Billing.zip"))
        
    for p in dest_paths:
        try:
            package_zip(p)
            verify_zip(p)
        except Exception as e:
            print(f"Error packaging to {p}: {e}")
