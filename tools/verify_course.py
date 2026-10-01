"""Check textbook examples and the six cumulative learning branches.

Without flags, checks use deterministic stage programs and need no learning refs.
--branches adds branch freshness/ancestry; --full also executes actual Git trees.
"""
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
from urllib.parse import unquote

from build_stages import (ROOT, STAGES, check_branches, read_ref_file,
                          resolve_stage_ref, stage_files)

EXPECTED_EXCERPTS = 5
REFERENCE_PATTERN = re.compile(
    r'<!-- reference: ([^\s]+) -->\s*```python\n(.*?)\n```', re.S)
PYTHON_PATTERN = re.compile(r'```python\n(.*?)\n```', re.S)


def reference_source(reference, use_branches=False):
    """Resolve a learn/STAGE/path marker against generated or actual stage code."""
    pieces = reference.split('/', 2)
    if len(pieces) != 3 or pieces[0] != 'learn' or pieces[1] not in STAGES:
        return None
    _, stage, path = pieces
    if use_branches:
        ref = resolve_stage_ref(stage)
        return read_ref_file(ref, path) if ref else None
    index = STAGES.index(stage) + 1
    return stage_files(index).get(path)


def documentation_files(directory):
    paths = [directory / 'README.md'] if (directory / 'README.md').exists() else []
    return paths + sorted((directory / 'docs').rglob('*.md'))


def check_documentation(directory, *, use_branches=False, required_excerpts=None):
    """Validate local links, complete-file markers, and Python snippet syntax."""
    errors = []
    excerpts = 0
    for path in documentation_files(directory):
        content = path.read_text()
        relative = path.relative_to(directory)
        prose = re.sub(r'```[^\n]*\n.*?```', '', content, flags=re.S)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', prose):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            if not (path.parent / target).exists():
                errors.append(f'{relative}: missing local link {target}')
        for reference, snippet in REFERENCE_PATTERN.findall(content):
            source = reference_source(reference, use_branches=use_branches)
            if source is None or snippet.rstrip() != source.rstrip():
                errors.append(f'{relative}: stale or missing complete-file excerpt from {reference}')
            excerpts += 1
        for snippet in PYTHON_PATTERN.findall(content):
            try:
                ast.parse(snippet)
            except SyntaxError as error:
                errors.append(f'{relative}: invalid Python example: {error}')
    if required_excerpts is not None and excerpts != required_excerpts:
        errors.append(f'Textbook requires {required_excerpts} marked complete-file excerpts; found {excerpts}.')
    return errors, excerpts


def check_stage_scope(index, files):
    """Keep dependency and import scope consistent with the conceptual sequence."""
    errors = []
    stage = STAGES[index - 1]
    required = ('pytest>=8.3,<9.0\n' if index < 5
                else 'pandas>=2.2,<3.0\npytest>=8.3,<9.0\n')
    if files.get('requirements.txt') != required:
        errors.append(f'{stage}: requirements must introduce pandas only in Part 5.')
    later_modules = set()
    if index < 2:
        later_modules.add('calculator.factory')
    if index < 4:
        later_modules.update({'calculator.commands', 'calculator.cli', 'calculator.session'})
    if index < 5:
        later_modules.update({'calculator.statistics', 'calculator.inputs', 'pandas'})
    if index < 6:
        later_modules.add('calculator.sequence')
    for path, source in files.items():
        if not path.endswith('.py'):
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError as error:
            errors.append(f'{stage}/{path}: invalid Python: {error}')
            continue
        for node in ast.walk(tree):
            imports = []
            if isinstance(node, ast.Import):
                imports = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports = [node.module]
            if any(module in later_modules or
                   any(module.startswith(later + '.') for later in later_modules)
                   for module in imports):
                errors.append(f'{stage}/{path}: imports a feature before its teaching part.')
    return errors


def generated_source_checks():
    errors = []
    for index in range(1, len(STAGES) + 1):
        errors.extend(check_stage_scope(index, stage_files(index)))
    return errors


def materialize_ref(ref, directory):
    """Extract the actual committed tree to a temporary directory for execution."""
    archive = subprocess.run(['git', '-C', str(ROOT), 'archive', '--format=tar', ref],
                             capture_output=True, check=False)
    if archive.returncode:
        raise ValueError(archive.stderr.decode(errors='replace').strip())
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode='r:') as tree:
        # Git trees contain no repository metadata. The data filter also rejects
        # unsafe archive paths; this works on supported patched Python releases.
        tree.extractall(directory, filter='data')


def run_stage(index):
    stage = STAGES[index - 1]
    ref = resolve_stage_ref(stage)
    if ref is None:
        return [f'learn/{stage}: missing branch for full verification.']
    with tempfile.TemporaryDirectory(prefix=f'course-{stage}-') as directory:
        folder = Path(directory)
        try:
            materialize_ref(ref, directory)
        except (ValueError, tarfile.TarError) as error:
            return [f'learn/{stage}: cannot materialize branch: {error}']
        errors, _ = check_documentation(folder, use_branches=True)
        actual_sources = {str(path.relative_to(folder)): path.read_text()
                          for path in folder.rglob('*.py')}
        requirements = folder / 'requirements.txt'
        if requirements.exists():
            actual_sources['requirements.txt'] = requirements.read_text()
        errors.extend(check_stage_scope(index, actual_sources))
        if errors:
            return [f'learn/{stage}: {error}' for error in errors]
        env = os.environ.copy()
        env['PYTHONPATH'] = directory
        env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
        try:
            tests = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=directory,
                                   env=env, text=True, capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            return [f'learn/{stage}: tests exceeded 90 seconds.']
        if tests.returncode:
            return [f'learn/{stage}: tests failed.\n{tests.stdout}{tests.stderr}']
        requests = ('add 2 3\nsquare 3\npower 3 exponent=4\ndivide 1 0\n'
                    'history\nclear\nhistory\nexit\n')
        if index >= 5:
            requests = requests.replace('exit\n',
                                        'stddev 10 20 30 40 50\ncsv stddev values.csv\nexit\n')
        try:
            demo = subprocess.run([sys.executable, '-m', 'calculator'],
                                  input=requests if index >= 4 else '', cwd=directory,
                                  env=env, capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired:
            return [f'learn/{stage}: demonstration exceeded 15 seconds.']
        valid = demo.returncode == 0
        if index < 3:
            valid = valid and demo.stdout.strip() == '5.0'
        elif index == 3:
            valid = valid and demo.stdout.strip().splitlines() == ['5.0', '81.0']
        else:
            valid = valid and all(text in demo.stdout for text in
                ('Result: 5.0000', 'Result: 9.0000', 'Result: 81.0000', 'Error:',
                 'History cleared.', 'History is empty.', 'Goodbye!'))
            if index >= 5:
                valid = valid and demo.stdout.count('Result: 15.8114') == 2
        if not valid:
            return [f'learn/{stage}: demonstration failed.\n{demo.stdout}\n{demo.stderr}']
        if index == 4:
            scope = subprocess.run([sys.executable, '-c',
                'from calculator.commands import HelpCommand; '
                'text=HelpCommand().execute(); '
                'assert "csv" not in text and "stddev" not in text and "mean" not in text'],
                cwd=directory, env=env, capture_output=True, text=True, timeout=15)
            if scope.returncode:
                return [f'learn/{stage}: help introduces statistics/CSV too early.\n{scope.stderr}']
        print(f'learn/{stage}: committed documentation, tests, demonstration, and stage scope verified.')
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--branches', action='store_true',
                        help='also validate actual local/origin learn refs and their sequential ancestry')
    parser.add_argument('--full', action='store_true',
                        help='check branches and run each actual committed tree in a temporary directory')
    args = parser.parse_args()
    errors, excerpts = check_documentation(ROOT, required_excerpts=EXPECTED_EXCERPTS)
    errors.extend(generated_source_checks())
    if args.branches or args.full:
        errors.extend(check_branches())
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'Textbook links, {excerpts} complete-file excerpts, Python examples, and six generated stage scopes verified.')
    if args.branches or args.full:
        print('Six actual learning branches match generated programs and sequential ancestry.')
    if args.full:
        for index in range(1, len(STAGES) + 1):
            errors = run_stage(index)
            if errors:
                print('\n'.join(errors))
                return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
