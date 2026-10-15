"""
Package and Validate TrainPlex Submission ZIP for HMS Project 4
Ensures .git directory is embedded, all 5 evaluation criteria are met,
and validates the archive in an isolated temporary sandbox.
"""

import os
import sys
import zipfile
import subprocess
import tempfile
import json
from pathlib import Path

BASE_DIR = Path(r"c:\Users\BABI\Desktop\AI")
DESKTOP_ZIP = Path(r"C:\Users\BABI\Desktop\project4_trainplex_submission.zip")
WORKSPACE_ZIP = BASE_DIR / "HMS_Project4_Submission_With_Git.zip"

EXCLUDE_DIRS = {
    'node_modules', 'dist', 'build', '__pycache__', '.pytest_cache',
    'coverage', '.venv', 'venv', 'env', '.next'
}

EXCLUDE_FILES = {
    'project4_trainplex_submission.zip',
    'HMS_Project4_Submission_With_Git.zip',
    'HMS_Member1_CorePlatform_Full.zip',
    'project4update.zip',
    '.coverage',
    'coverage.xml',
    'db.sqlite3-journal',
}

def package_archive(output_path: Path):
    print(f"\n[HMS Packaging] Creating submission archive with .git at: {output_path}...")
    file_count = 0
    git_file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            # Prune excluded directories (except .git)
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for f in files:
                if f in EXCLUDE_FILES or f.endswith('.pyc') or f.endswith('.zip'):
                    continue

                full_path = Path(root) / f
                rel_path = full_path.relative_to(BASE_DIR)

                zf.write(full_path, arcname=str(rel_path).replace('\\', '/'))
                file_count += 1
                total_uncompressed_bytes += full_path.stat().st_size
                if str(rel_path).replace('\\', '/').startswith('.git/'):
                    git_file_count += 1

    size_mb = output_path.stat().st_size / (1024 * 1024)
    raw_mb = total_uncompressed_bytes / (1024 * 1024)
    print(f"[HMS Packaging] Archive created:")
    print(f"  * Destination : {output_path}")
    print(f"  * Total Files : {file_count:,d} (including {git_file_count:,d} .git internal objects)")
    print(f"  * Raw Size    : {raw_mb:.2f} MB")
    print(f"  * Zip Size    : {size_mb:.2f} MB")
    return output_path

def validate_archive(zip_path: Path):
    print(f"\n=====================================================================")
    print(f"   VALIDATING SUBMISSION ARCHIVE IN ISOLATED SANDBOX: {zip_path.name}")
    print(f"=====================================================================")
    with tempfile.TemporaryDirectory() as tmpdir:
        sandbox_dir = Path(tmpdir)
        print("Extracting archive into temporary sandbox directory...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(sandbox_dir)

        # CHECK 1: Git Directory Detection
        git_dir = sandbox_dir / ".git"
        check1_passed = git_dir.is_dir()
        print(f"\n[Case 1/5] Git-based repository (.git directory found):")
        print(f"  Status   : {'PASS' if check1_passed else 'FAIL'}")
        print(f"  Details  : .git directory exists at root = {check1_passed}")

        # Git worktree test
        p_worktree = subprocess.run(
            ["git", "-C", str(sandbox_dir), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True
        )
        is_worktree = p_worktree.stdout.strip() == "true"
        print(f"  Worktree : is-inside-work-tree = {is_worktree}")

        # CHECK 2: Minimum 100 Meaningful Commits
        p_commits = subprocess.run(
            ["git", "-C", str(sandbox_dir), "rev-list", "--count", "HEAD"],
            capture_output=True, text=True
        )
        commit_count = int(p_commits.stdout.strip()) if p_commits.returncode == 0 else 0
        check2_passed = commit_count >= 100
        print(f"\n[Case 2/5] At least 100 meaningful commits:")
        print(f"  Status   : {'PASS' if check2_passed else 'FAIL'}")
        print(f"  Measured : {commit_count:,d} commits (required: 100)")

        # CHECK 3: Minimum 100 Pull Requests (Merge Commits)
        p_merges = subprocess.run(
            ["git", "-C", str(sandbox_dir), "rev-list", "--merges", "--count", "HEAD"],
            capture_output=True, text=True
        )
        merge_count = int(p_merges.stdout.strip()) if p_merges.returncode == 0 else 0

        p_prs = subprocess.run(
            ["git", "-C", str(sandbox_dir), "log", "--grep=Merge pull request", "--oneline"],
            capture_output=True, text=True
        )
        pr_grep_count = len([l for l in p_prs.stdout.splitlines() if l.strip()])
        check3_passed = merge_count >= 100 and pr_grep_count >= 100
        print(f"\n[Case 3/5] At least 100 meaningful pull requests (merge commits):")
        print(f"  Status   : {'PASS' if check3_passed else 'FAIL'}")
        print(f"  Measured : {merge_count:,d} merge commits, {pr_grep_count:,d} PR merges (required: 100)")

        # CHECK 4: At least 2 Distinct Collaborators (Commit Authors)
        p_authors = subprocess.run(
            ["git", "-C", str(sandbox_dir), "log", "--format=%an <%ae>"],
            capture_output=True, text=True
        )
        authors = sorted(list(set(l.strip() for l in p_authors.stdout.splitlines() if l.strip())))
        check4_passed = len(authors) >= 2
        print(f"\n[Case 4/5] At least 2 collaborators (distinct commit authors):")
        print(f"  Status   : {'PASS' if check4_passed else 'FAIL'}")
        print(f"  Measured : {len(authors)} distinct authors (required: 2)")
        for a in authors[:5]:
            print(f"    * {a}")

        # CHECK 5: Minimum 500,000+ Lines of Code (prod only, tests/generated excluded)
        ext_map = {'.py': 'Python', '.ts': 'TypeScript', '.tsx': 'TypeScript', '.js': 'JavaScript', '.jsx': 'JavaScript'}
        counts = {'Python': [0, 0], 'TypeScript': [0, 0], 'JavaScript': [0, 0]}
        
        for root, dirs, files in os.walk(sandbox_dir):
            # Exclude non-prod folders
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and d != '.git']
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in ext_map:
                    rel_p = str(Path(root, f).relative_to(sandbox_dir)).lower().replace('\\', '/')
                    if any(p in rel_p.split('/') for p in ['test', 'tests', 'spec', 'specs', 'migrations', 'fixtures', 'coverage']):
                        continue
                    fname = os.path.basename(rel_p)
                    if 'test' in fname or 'spec' in fname or fname.startswith('mock_') or 'generated' in fname or fname.endswith('.min.js'):
                        continue
                    lang = ext_map[ext]
                    try:
                        with open(Path(root, f), 'r', encoding='utf-8', errors='ignore') as fp:
                            lines_cnt = sum(1 for _ in fp)
                        counts[lang][0] += lines_cnt
                        counts[lang][1] += 1
                    except Exception:
                        pass

        total_prod_loc = sum(c[0] for c in counts.values())
        total_prod_files = sum(c[1] for c in counts.values())
        check5_passed = total_prod_loc >= 500000
        print(f"\n[Case 5/5] Minimum 500,000+ lines of code (prod only, tests excluded):")
        print(f"  Status   : {'PASS' if check5_passed else 'FAIL'}")
        print(f"  Measured : {total_prod_loc:,d} prod LOC across {total_prod_files:,d} files (required: 500,000)")
        for lang, (loc, fcount) in counts.items():
            print(f"    * {lang:12s}: {loc:,d} LOC across {fcount} files")

        all_passed = all([check1_passed, is_worktree, check2_passed, check3_passed, check4_passed, check5_passed])
        print(f"\n=====================================================================")
        print(f"   SANDBOX VERIFICATION RESULT: {'>>> ALL 5 CHECKS PASSED <<<' if all_passed else 'SOME CHECKS FAILED'}")
        print(f"=====================================================================\n")
        return all_passed

if __name__ == "__main__":
    os.makedirs(BASE_DIR / "scripts", exist_ok=True)
    package_archive(DESKTOP_ZIP)
    package_archive(WORKSPACE_ZIP)
    success = validate_archive(DESKTOP_ZIP)
    if not success:
        sys.exit(1)
