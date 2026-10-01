"""Generate the six cumulative lesson programs and verify their Git branches.

The first two parts use fixed operands; Part 3 introduces flexible arguments.
Use --output-dir for materialization files or --check to validate published refs.
Neither mode edits Git refs or tracked files in the teaching checkout.
"""
import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('01-refactoring', '02-factory', '03-flexible-inputs', '04-commands', '05-statistics-csv', '06-transfer')

EARLY_OPERATIONS = '''"""Static math has no instance state."""


class Operations:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        return a / b
'''
EARLY_CALCULATION = '''"""Store two operands and a callable; run math only in get_result."""
from math import isfinite
from calculator.validation import numeric_values


class Calculation:
    def __init__(self, a, b, operation):
        numbers = numeric_values([a, b])
        self.a = numbers[0]
        self.b = numbers[1]
        self.operation = operation

    def get_result(self):
        result = float(self.operation(self.a, self.b))
        if not isfinite(result):
            raise ValueError("Result is outside the supported range.")
        return result
'''
EARLY_FACTORY = '''"""A factory centralizes construction; it does not execute math."""
from calculator.calculation import Calculation
from calculator.operations import Operations


class CalculationFactory:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
    }

    @staticmethod
    def create(name, a, b):
        name = name.strip().lower()
        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None
        return Calculation(a, b, operation)
'''
EARLY_TESTS = '''import pytest
from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.history import History


def test_math_without_an_instance():
    assert Operations.add(2, 3) == 5
    assert Operations.subtract(2, 3) == -1
    assert Operations.multiply(2, 3) == 6
    assert Operations.divide(7, 2) == pytest.approx(3.5)


def test_construction_does_not_call_math():
    calls = []
    def add(a, b):
        calls.append((a, b))
        return a + b
    calculation = Calculation("2", "3", add)
    assert calls == []
    assert calculation.get_result() == 5.0
    assert calls == [(2.0, 3.0)]


def test_history_copy_protects_membership():
    history = History()
    calculation = Calculation(2, 3, Operations.add)
    history.add(calculation, calculation.get_result())
    copy = history.get_history()
    copy.clear()
    assert len(history.get_history()) == 1


def test_execution_reports_zero_division():
    calculation = Calculation(1, 0, Operations.divide)
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()
'''
EARLY_FACTORY_TESTS = '''import pytest
from calculator.calculation import Calculation
from calculator.factory import CalculationFactory


def test_factory_constructs_selected_calculation():
    calculation = CalculationFactory.create(" ADD ", "2", "3")
    assert isinstance(calculation, Calculation)
    assert calculation.get_result() == 5.0


def test_factory_never_executes():
    calculation = CalculationFactory.create("divide", 1, 0)
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


def test_factory_reports_unknown_name():
    with pytest.raises(ValueError, match="Unknown operation"):
        CalculationFactory.create("other", 1, 2)
'''


def before_statistics(files):
    """Remove later collection/source features while retaining flexible math."""
    files['calculator/operations.py'] = files['calculator/operations.py'].replace(
        'from calculator.statistics import mean, standard_deviation\n', '').split('    @staticmethod\n    def mean')[0].rstrip() + '\n'
    files['calculator/factory.py'] = files['calculator/factory.py'].replace(
        '        "mean": Operations.mean,\n', '').replace('        "stddev": Operations.stddev,\n', '').replace(', "stddev": {"ddof"}', '')
    tree = ast.parse(files['tests/test_factory.py'])
    for node in ast.walk(tree):
        if isinstance(node, ast.List):
            node.elts = [item for item in node.elts if not (
                isinstance(item, ast.Tuple) and item.elts and isinstance(item.elts[0], ast.Constant)
                and item.elts[0].value in {'mean', 'stddev'})]
    files['tests/test_factory.py'] = ast.unparse(tree) + '\n'
    if 'calculator/cli.py' in files:
        files['calculator/commands.py'] = files['calculator/commands.py'].replace(
            '; sum/mean/stddev VALUES (stddev ddof=0/1); csv mean/stddev PATH', '; sum VALUES')
        files['calculator/cli.py'] = files['calculator/cli.py'].replace('import pandas as pd\n', '').replace('from calculator.inputs import read_csv_values\n', '')
        start = files['calculator/cli.py'].index('    if name == "csv":')
        end = files['calculator/cli.py'].index('    calculation =', start)
        files['calculator/cli.py'] = files['calculator/cli.py'][:start] + files['calculator/cli.py'][end:]
        files['calculator/cli.py'] = files['calculator/cli.py'].replace(
            'OverflowError,\n                pd.errors.ParserError, pd.errors.EmptyDataError', 'OverflowError')
        tree = ast.parse(files['tests/test_cli.py'])
        tree.body = [node for node in tree.body if not isinstance(node, ast.FunctionDef)
                     or node.name not in {'test_csv_and_manual_session', 'test_recovers_from_csv_failures'}]
        files['tests/test_cli.py'] = ast.unparse(tree) + '\n'


def stage_files(index):
    """Return deterministic application/test/dependency files for Part 1–6.

    Documentation and repository metadata are supplied when a branch is
    materialized. This function reads the canonical application on main and
    never writes files or changes Git refs.
    """
    if index not in range(1, len(STAGES) + 1):
        raise ValueError('Stage index must be between 1 and 6.')
    paths = ['pytest.ini', '.github/workflows/tests.yml', 'calculator/__init__.py',
             'calculator/validation.py', 'calculator/history.py']
    if index >= 3:
        paths += ['calculator/operations.py', 'calculator/calculation.py', 'calculator/factory.py',
                  'tests/test_operations.py', 'tests/test_calculation.py', 'tests/test_factory.py',
                  'tests/test_history.py']
    if index >= 4:
        paths += ['calculator/session.py', 'calculator/commands.py', 'calculator/cli.py',
                  'tests/test_commands.py', 'tests/test_cli.py']
    if index >= 5:
        paths += ['values.csv', 'calculator/statistics.py', 'calculator/inputs.py',
                  'tests/test_statistics.py', 'tests/test_csv.py']
    if index >= 6:
        paths += ['calculator/sequence.py', 'tests/test_sequence.py']
    files = {path: (ROOT / path).read_text() for path in paths}
    files['requirements.txt'] = ('pytest>=8.3,<9.0\n' if index < 5
                                 else 'pandas>=2.2,<3.0\npytest>=8.3,<9.0\n')
    if index <= 2:
        files.update({'calculator/operations.py': EARLY_OPERATIONS,
                      'calculator/calculation.py': EARLY_CALCULATION,
                      'tests/test_refactoring.py': EARLY_TESTS})
        if index == 2:
            files.update({'calculator/factory.py': EARLY_FACTORY,
                          'tests/test_factory.py': EARLY_FACTORY_TESTS})
    elif index < 5:
        before_statistics(files)
    if index == 3:
        # History is prerequisite knowledge. Session is introduced next part.
        tree = ast.parse(files['tests/test_history.py'])
        tree.body = [node for node in tree.body
                     if not (isinstance(node, ast.ImportFrom) and node.module == 'calculator.session')
                     and not (isinstance(node, ast.FunctionDef)
                              and node.name == 'test_sessions_have_independent_history')]
        files['tests/test_history.py'] = ast.unparse(tree) + '\n'
    if index == 1:
        demo = ('from calculator.calculation import Calculation\n'
                'from calculator.operations import Operations\n'
                'print(Calculation(2, 3, Operations.add).get_result())\n')
    elif index == 2:
        demo = ('from calculator.factory import CalculationFactory\n'
                'print(CalculationFactory.create("add", 2, 3).get_result())\n')
    elif index == 3:
        demo = ('from calculator.factory import CalculationFactory\n'
                'print(CalculationFactory.create("add", 2, 3).get_result())\n'
                'print(CalculationFactory.create("power", 3, exponent=4).get_result())\n')
    else:
        demo = (ROOT / 'calculator/__main__.py').read_text()
    files['calculator/__main__.py'] = demo
    return files


def git_command(*arguments):
    """Read Git metadata without changing branches, refs, or the working tree."""
    return subprocess.run(['git', '-C', str(ROOT), *arguments],
                          text=True, capture_output=True, check=False)


def resolve_stage_ref(stage):
    """Prefer a local learn branch, with origin's remote ref as CI fallback."""
    for ref in (f'refs/heads/learn/{stage}', f'refs/remotes/origin/learn/{stage}'):
        result = git_command('rev-parse', '--verify', f'{ref}^{{commit}}')
        if result.returncode == 0:
            return ref
    return None


def read_ref_file(ref, path):
    result = git_command('show', f'{ref}:{path}')
    if result.returncode:
        return None
    return result.stdout


def is_stage_source(path):
    python_source = (path.startswith(('calculator/', 'tests/'))
                     and path.endswith(('.py', '.pyi')))
    workflow_source = (path.startswith('.github/workflows/')
                       and path.endswith(('.yml', '.yaml')))
    return python_source or workflow_source


def check_branches():
    """Compare actual branches with generated programs and their parent chain."""
    errors = []
    refs = {}
    for index, stage in enumerate(STAGES, 1):
        ref = resolve_stage_ref(stage)
        if ref is None:
            errors.append(f'learn/{stage}: missing local/origin branch; fetch or materialize the learning branches.')
            continue
        refs[stage] = ref
        listing = git_command('ls-tree', '-r', '--name-only', ref)
        if listing.returncode:
            errors.append(f'learn/{stage}: could not read its tree: {listing.stderr.strip()}')
            continue
        actual_paths = set(listing.stdout.splitlines())
        expected = stage_files(index)
        for path, content in expected.items():
            if read_ref_file(ref, path) != content:
                errors.append(f'learn/{stage}/{path}: stale or missing generated content.')
        unexpected = {path for path in actual_paths if is_stage_source(path)} - expected.keys()
        for path in sorted(unexpected):
            errors.append(f'learn/{stage}/{path}: source belongs to a later part or is undeclared.')

    for previous, stage in zip(STAGES, STAGES[1:]):
        if previous not in refs or stage not in refs:
            continue
        previous_sha = git_command('rev-parse', refs[previous]).stdout.strip()
        parents = git_command('show', '-s', '--format=%P', refs[stage]).stdout.split()
        if parents != [previous_sha]:
            errors.append(f'learn/{stage}: its only parent must be the current learn/{previous} commit.')

    # The first lesson forks from main. Its base may precede later main updates.
    first = refs.get(STAGES[0])
    if first:
        parents = git_command('show', '-s', '--format=%P', first).stdout.split()
        main_ref = None
        for candidate in ('refs/heads/main', 'refs/remotes/origin/main'):
            if git_command('rev-parse', '--verify', candidate).returncode == 0:
                main_ref = candidate
                break
        if len(parents) != 1:
            errors.append(f'learn/{STAGES[0]}: expected one parent from main.')
        elif main_ref and git_command('merge-base', '--is-ancestor', parents[0], main_ref).returncode:
            errors.append(f'learn/{STAGES[0]}: its parent is not an ancestor of main.')
    return errors


def write_stages(output_dir):
    """Write fresh materialization directories outside this checkout."""
    destination = output_dir.resolve()
    checkout = ROOT.resolve()
    if destination == checkout or checkout in destination.parents:
        raise ValueError('--output-dir must be outside the teaching checkout; tracked files are never rewritten.')
    for stage in STAGES:
        target = destination / stage
        if target.exists() and (not target.is_dir() or any(target.iterdir())):
            raise ValueError(f'{target}: use a fresh or empty stage output directory.')
    for index, stage in enumerate(STAGES, 1):
        for relative, content in stage_files(index).items():
            target = destination / stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true',
                      help='check actual learn branches, generated files, scope, and sequential ancestry')
    mode.add_argument('--output-dir', type=Path,
                      help='write six fresh stage content directories outside this checkout; do not change Git')
    args = parser.parse_args()
    if args.check:
        errors = check_branches()
        print('\n'.join(errors) if errors else 'Six learning branches match their stage programs and sequential parent chain.')
        return 1 if errors else 0
    if args.output_dir:
        try:
            destination = write_stages(args.output_dir)
        except ValueError as error:
            parser.error(str(error))
        print(f'Wrote six stage content directories under {destination}; Git and the checkout are unchanged.')
        return 0
    parser.print_help()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
