"""Verify local links, executable examples, snapshot freshness, and stage behavior."""
import argparse
import ast
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from build_stages import ROOT, STAGES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='run all six standalone snapshot suites and demos')
    args = parser.parse_args()
    errors = []
    excerpts = 0
    for path in [ROOT / 'README.md', *sorted((ROOT / 'docs').rglob('*.md')),
                 *sorted((ROOT / 'examples/stages').glob('*/README.md'))]:
        content = path.read_text()
        prose = re.sub(r'```[^\n]*\n.*?```', '', content, flags=re.S)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', prose):
            if re.match(r'[a-zA-Z]+:', target) or target.startswith('#'):
                continue
            if not (path.parent / target.split('#', 1)[0]).exists():
                errors.append(f'{path.relative_to(ROOT)}: missing link {target}')
        for filename, snippet in re.findall(r'<!-- reference: ([^ ]+) -->\n```python\n(.*?)\n```', content, flags=re.S):
            source = ROOT / filename
            if not source.exists() or snippet.rstrip() != source.read_text().rstrip():
                errors.append(f'{path.relative_to(ROOT)}: stale excerpt from {filename}')
            excerpts += 1
        for snippet in re.findall(r'```python\n(.*?)\n```', content, flags=re.S):
            try:
                ast.parse(snippet)
            except SyntaxError as error:
                errors.append(f'{path.relative_to(ROOT)}: invalid example: {error}')
    check = subprocess.run([sys.executable, str(ROOT / 'tools/build_stages.py'), '--check'], capture_output=True, text=True)
    if check.returncode:
        errors.append(check.stdout + check.stderr)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'Documentation links, {excerpts} complete-file excerpts, Python examples, and snapshot freshness verified.')
    if args.full:
        for index, stage in enumerate(STAGES, 1):
            with tempfile.TemporaryDirectory() as directory:
                shutil.copytree(ROOT / 'examples/stages' / stage, directory, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache'))
                env = os.environ.copy()
                env['PYTHONPATH'] = directory
                env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
                tests = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=directory, env=env,
                                       text=True, capture_output=True, timeout=90)
                if tests.returncode:
                    print(tests.stdout + tests.stderr)
                    return 1
                requests = 'add 2 3\nsquare 3\npower 3 exponent=4\ndivide 1 0\nhistory\nclear\nhistory\nexit\n'
                if index >= 5:
                    requests = requests.replace('exit\n', 'stddev 10 20 30 40 50\ncsv stddev values.csv\nexit\n')
                demo = subprocess.run([sys.executable, '-m', 'calculator'], input=requests if index >= 4 else '',
                                      cwd=directory, env=env, capture_output=True, text=True, timeout=15)
                valid = demo.returncode == 0
                if index < 3:
                    valid = valid and demo.stdout.strip() == '5.0'
                elif index == 3:
                    valid = valid and demo.stdout.strip().splitlines() == ['5.0', '81.0']
                else:
                    valid = valid and all(text in demo.stdout for text in
                        ('Result: 5.0000', 'Result: 9.0000', 'Result: 81.0000', 'Error:', 'History cleared.', 'History is empty.', 'Goodbye!'))
                    if index >= 5:
                        valid = valid and demo.stdout.count('Result: 15.8114') == 2
                if not valid:
                    print(f'{stage}: demo failed\n{demo.stdout}\n{demo.stderr}')
                    return 1
                if index == 4:
                    scope = subprocess.run([sys.executable, '-c',
                        'from calculator.commands import HelpCommand; text=HelpCommand().execute(); assert "csv" not in text and "stddev" not in text'],
                        cwd=directory, env=env, capture_output=True, text=True)
                    if scope.returncode:
                        print(f'{stage}: help describes features before they are introduced.\n{scope.stderr}')
                        return 1
                print(f'{stage}: tests, demonstration, and stage scope verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
