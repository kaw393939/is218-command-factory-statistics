"""Verify assessment contracts, distinct transfer requirements, and grading.

Sibling references remain outside student starters. No network is required.
Automated behavior is 60 points; student tests and explanations require review.
"""
import argparse
import ast
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

COURSE = Path(__file__).resolve().parents[1]


def signatures(path):
    result = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.FunctionDef):
            result[node.name] = ast.dump(node.args)
        elif isinstance(node, ast.ClassDef):
            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    result[f'{node.name}.{method.name}'] = ast.dump(method.args)
    return result


def grade(grader_root, submission, expected=None):
    with tempfile.TemporaryDirectory() as directory:
        result = subprocess.run([sys.executable, str(grader_root / 'grading/grade.py'), str(submission)],
                                cwd=directory, capture_output=True, text=True, timeout=150)
        report = Path(directory) / 'grade-results.json'
        if not report.exists():
            raise RuntimeError(result.stdout + result.stderr)
        data = json.loads(report.read_text())
        score, maximum = data['score'], data['maximum']
        if maximum != 60 or data.get('manual_maximum') != 40:
            raise RuntimeError(f'{grader_root.name}: automated/manual grading weights changed.')
        if data.get('diagnostic') or len(data['checks']) != 12 or result.returncode != (0 if score == maximum else 1):
            raise RuntimeError(result.stdout + result.stderr)
        if expected is not None and score != expected:
            raise RuntimeError(f'{submission.name}: expected {expected}, got {score}\n{result.stdout}\n{result.stderr}')
        return score


def check_documentation(root):
    for path in [root / 'README.md', root / 'MANUAL_REVIEW.md', *sorted((root / 'docs').rglob('*.md'))]:
        text = path.read_text()
        prose = re.sub(r'```[^\n]*\n.*?```', '', text, flags=re.S)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', prose):
            if not re.match(r'[a-zA-Z]+:', target) and not target.startswith('#'):
                if not (path.parent / target.split('#', 1)[0]).exists():
                    raise RuntimeError(f'{path}: broken local link {target}')
        for snippet in re.findall(r'```python\n(.*?)\n```', text, flags=re.S):
            ast.parse(snippet)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-root', type=Path, default=COURSE.parent)
    parser.add_argument('--mutations', action='store_true', help='prove relevant broken adaptations lose points')
    args = parser.parse_args()
    roots = {name: args.workspace_root / name for name in (
        'is218-statistics-practice', 'is218-statistics-exam',
        'is218-statistics-practice-solution', 'is218-statistics-instructor')}
    for root in roots.values():
        if not root.exists():
            raise RuntimeError(f'Missing checkout: {root}; pass --workspace-root if needed.')
        rubric = json.loads((root / 'grading/rubric.json').read_text())
        names = [name for category in rubric for name in category['tests']]
        test_names = {node.name for node in ast.parse((root / 'tests/test_acceptance.py').read_text()).body
                      if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}
        if len(names) != 12 or len(set(names)) != 12 or set(names) != test_names:
            raise RuntimeError(f'{root.name}: rubric must map twelve distinct named checks (60 points).')
        check_documentation(root)
    practice = roots['is218-statistics-practice']
    solution = roots['is218-statistics-practice-solution']
    exam = roots['is218-statistics-exam']
    instructor = roots['is218-statistics-instructor']
    for starter, reference, initial in ((practice, solution, 5), (exam, instructor, 10)):
        if (starter / 'tests/test_acceptance.py').read_bytes() != (reference / 'tests/test_acceptance.py').read_bytes():
            raise RuntimeError(f'{starter.name}: starter and reference acceptance checks differ.')
        if (starter / 'grading/rubric.json').read_bytes() != (reference / 'grading/rubric.json').read_bytes():
            raise RuntimeError(f'{starter.name}: starter and reference rubric differ.')
        for path in (starter / 'calculator').glob('*.py'):
            if signatures(path) != signatures(reference / 'calculator' / path.name):
                raise RuntimeError(f'{starter.name}/{path.name}: starter/reference signature mismatch.')
        print(f'{starter.name}: starter {grade(starter, starter, initial)}/60 (expected incomplete).')
        print(f'{reference.name}: reference {grade(starter, reference, 60)}/60.')
    for target, submission in ((practice, COURSE), (exam, COURSE), (exam, solution)):
        score = grade(target, submission)
        if score == 60:
            raise RuntimeError(f'{target.name}: unchanged {submission.name} passes the adaptation assessment.')
        print(f'Copy check: {submission.name} → {target.name}: {score}/60; new requirements remain unmet.')
    print('Published rubric mappings, API signatures, documentation, and distinct transfer requirements verified.')
    if args.mutations:
        mutations = (
            ('practice records failures', practice, solution, 'session.py',
             '        result = calculation.get_result()',
             '        self._history.add(calculation, 0.0)\n        result = calculation.get_result()'),
            ('practice scales before adding offset', practice, solution, 'operations.py',
             'return (value + offset) * scale', 'return value * scale + offset'),
            ('batch stops after a failed row', exam, instructor, 'commands.py',
             '                failed += 1', '                failed += 1\n                break'),
            ('exam exposes mutable failures', exam, instructor, 'session.py',
             'return list(self._failures)', 'return self._failures'),
        )
        for label, grader_root, reference, filename, before, after in mutations:
            with tempfile.TemporaryDirectory() as directory:
                candidate = Path(directory) / 'candidate'
                shutil.copytree(reference / 'calculator', candidate / 'calculator',
                                ignore=shutil.ignore_patterns('__pycache__'))
                path = candidate / 'calculator' / filename
                original = path.read_text()
                if before not in original:
                    raise RuntimeError(f'Mutation needs updating: {label}')
                path.write_text(original.replace(before, after))
                score = grade(grader_root, candidate)
                if score == 60:
                    raise RuntimeError(f'Checks missed mutation: {label}')
                print(f'Mutation detected: {label} ({score}/60).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
