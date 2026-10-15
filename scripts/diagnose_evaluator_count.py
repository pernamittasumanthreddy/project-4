import subprocess
import os

files = subprocess.check_output(['git', 'ls-files'], text=True).splitlines()
print(f"Total files in git: {len(files)}")

ext_map = {'.py': 'Python', '.ts': 'TypeScript', '.tsx': 'TypeScript', '.js': 'JavaScript', '.jsx': 'JavaScript'}

def evaluate(filter_name, exclude_filter_fn):
    counted_files = []
    py_lines = 0
    ts_lines = 0
    js_lines = 0
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ext_map:
            if exclude_filter_fn(f):
                continue
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
                    lines = sum(1 for _ in fp)
                if ext == '.py':
                    py_lines += lines
                elif ext in ['.ts', '.tsx']:
                    ts_lines += lines
                elif ext in ['.js', '.jsx']:
                    js_lines += lines
                counted_files.append((f, lines))
            except Exception:
                pass
    tot = py_lines + ts_lines + js_lines
    print(f"\nFilter: {filter_name}")
    print(f"  Counted files: {len(counted_files)}")
    print(f"  Total LOC: {tot:,d}")
    print(f"  Python: {py_lines:,d}")
    print(f"  TypeScript: {ts_lines:,d}")
    print(f"  JavaScript: {js_lines:,d}")
    return len(counted_files), tot

# Standard test/generated filter
evaluate("Standard filter (test, spec, mock, generated)", 
    lambda f: any(k in f.lower().replace('\\', '/') for k in ['/test', '/tests', '/spec', '/specs', 'mock_', 'generated', '.min.js', '/migrations/']) or 'test_' in os.path.basename(f) or '_test.' in os.path.basename(f)
)

# What if HMS_Member6_Finance_Billing is excluded or included?
evaluate("Excluding tests only (path contains 'test')",
    lambda f: 'test' in f.lower() or 'spec' in f.lower() or 'generated' in f.lower() or '.min.js' in f.lower()
)

evaluate("Excluding tests + fixtures + docs",
    lambda f: any(k in f.lower() for k in ['test', 'spec', 'fixture', 'doc', 'generated', '.min.js', 'migration'])
)
