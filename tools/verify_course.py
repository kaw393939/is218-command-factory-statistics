"""Check links, complete-file excerpts, and optionally all six worked snapshots."""
import argparse
import ast
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
STAGES = ["01-statistics", "02-command", "03-csv", "04-factory", "05-repl", "06-ci"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


def resolve(branch):
    for ref in (branch, "origin/" + branch):
        if subprocess.run(["git", "rev-parse", "--verify", ref], cwd=ROOT, capture_output=True).returncode == 0:
            return ref
    raise RuntimeError(f"Missing {branch}; fetch all branches before verifying")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="also run every worked stage in an isolated temporary folder")
    args = parser.parse_args()
    errors = []
    excerpts = 0
    for path in [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]:
        content = path.read_text()
        prose = re.sub(r"```[^\n]*\n.*?```", "", content, flags=re.S)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose):
            if re.match(r"[a-zA-Z]+:", target) or target.startswith("#"):
                continue
            local = (path.parent / target.split("#", 1)[0]).resolve()
            if not local.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing relative link {target}")
        for branch, filename, snippet in re.findall(r"<!-- reference: ([^:]+):([^ ]+) -->\n```[^\n]*\n(.*?)\n```", content, flags=re.S):
            expected = git("show", resolve(branch) + ":" + filename).rstrip()
            if snippet.rstrip() != expected:
                errors.append(f"{path.relative_to(ROOT)}: excerpt differs from {branch}:{filename}")
            excerpts += 1
        for snippet in re.findall(r"```python\n(.*?)\n```", content, flags=re.S):
            try:
                ast.parse(snippet)
            except SyntaxError as error:
                errors.append(f"{path.relative_to(ROOT)}: invalid Python snippet: {error}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Documentation links and {excerpts} complete-file excerpts verified; Python examples parse.")
    if args.full:
        for index, stage in enumerate(STAGES, start=1):
            ref = resolve("learn/" + stage)
            with tempfile.TemporaryDirectory() as directory:
                archive = subprocess.check_output(["git", "archive", ref], cwd=ROOT)
                with tarfile.open(fileobj=io.BytesIO(archive)) as files:
                    # Only instructor-owned, tracked course snapshots are extracted.
                    files.extractall(directory, filter="data")
                env = os.environ.copy()
                env["PYTHONPATH"] = directory
                tests = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=directory, env=env, text=True, capture_output=True, timeout=90)
                if tests.returncode:
                    print(tests.stdout + tests.stderr)
                    return 1
                inputs = "manual\n10 20 30 40 50\ncsv\nexit\n" if index >= 5 else ""
                demo = subprocess.run([sys.executable, "-m", "calculator"], input=inputs, cwd=directory, env=env, text=True, capture_output=True, timeout=15)
                if demo.returncode or (index >= 5 and demo.stdout.count("Standard deviation: 15.8114") != 2):
                    print(f"{ref}: demonstration failed\n{demo.stdout}\n{demo.stderr}")
                    return 1
                if index < 5 and abs(float(demo.stdout.strip()) - 15.811388300841896) > 1e-9:
                    print(f"{ref}: unexpected demonstration result {demo.stdout}")
                    return 1
                print(f"{stage}: {tests.stdout.strip().splitlines()[-1]}; demonstration verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
