import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def count_prod_loc():
    excluded_dirs = {'node_modules', '.git', 'coverage', 'dist', 'venv', 'env', 'tests', '__pycache__'}
    total_loc = 0
    by_ext = {}
    file_count = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in excluded_dirs and 'test' not in d.lower() and 'generated' not in d.lower()]
        for f in files:
            p = Path(root) / f
            ext = p.suffix.lower()
            if ext in ('.py', '.ts', '.tsx', '.js', '.jsx'):
                if 'test' in f.lower():
                    continue
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                        lines = len(fp.readlines())
                        total_loc += lines
                        by_ext[ext] = by_ext.get(ext, 0) + lines
                        file_count += 1
                except Exception:
                    pass
    return total_loc, file_count, by_ext

if __name__ == '__main__':
    loc, count, by_ext = count_prod_loc()
    print(f"Current Prod LOC: {loc} across {count} files")
    print(f"By ext: {by_ext}")
