"""Build six cumulative references, keeping early interfaces deliberately small.

The first two parts use fixed operands; Part 3 introduces variable arguments.
Use --check to verify snapshots without writing. Later parts reuse canonical code.
"""
import argparse
import ast
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
    paths = ['requirements.txt', 'pytest.ini', 'calculator/__init__.py', 'calculator/validation.py', 'calculator/history.py']
    if index >= 3:
        paths += ['calculator/operations.py', 'calculator/calculation.py', 'calculator/factory.py',
                  'tests/test_operations.py', 'tests/test_calculation.py', 'tests/test_factory.py']
    if index >= 4:
        paths += ['calculator/session.py', 'calculator/commands.py', 'calculator/cli.py',
                  'tests/test_commands.py', 'tests/test_cli.py', 'tests/test_history.py']
    if index >= 5:
        paths += ['values.csv', 'calculator/statistics.py', 'calculator/inputs.py', 'tests/test_statistics.py', 'tests/test_csv.py']
    if index >= 6:
        paths += ['calculator/sequence.py', 'tests/test_sequence.py', '.github/workflows/tests.yml']
    files = {path: (ROOT / path).read_text() for path in paths}
    if index <= 2:
        files.update({'calculator/operations.py': EARLY_OPERATIONS, 'calculator/calculation.py': EARLY_CALCULATION,
                      'tests/test_refactoring.py': EARLY_TESTS})
        if index == 2:
            files.update({'calculator/factory.py': EARLY_FACTORY, 'tests/test_factory.py': EARLY_FACTORY_TESTS})
    elif index < 5:
        before_statistics(files)
    if index == 1:
        demo = 'from calculator.calculation import Calculation\nfrom calculator.operations import Operations\nprint(Calculation(2, 3, Operations.add).get_result())\n'
    elif index == 2:
        demo = 'from calculator.factory import CalculationFactory\nprint(CalculationFactory.create("add", 2, 3).get_result())\n'
    elif index == 3:
        demo = 'from calculator.factory import CalculationFactory\nprint(CalculationFactory.create("add", 2, 3).get_result())\nprint(CalculationFactory.create("power", 3, exponent=4).get_result())\n'
    else:
        demo = (ROOT / 'calculator/__main__.py').read_text()
    files['calculator/__main__.py'] = demo
    files['README.md'] = f'''# Part {index}: {STAGES[index-1]}

This cumulative snapshot is a worked reference, not a starter. Read the matching
lesson under the course root's docs/lessons folder, then work in your own solution.

Run from this folder with the course environment already activated:

```bash
python -m calculator
python -m pytest -q
```

Parts 1–2 print 5.0. Part 3 prints 5.0 and 81.0. Parts 4–6 accept interactive
requests such as add 2 3, history, clear, and exit. Statistics and CSV begin in
Part 5. Part 6 adds a prepared-calculation sequence example and CI review.

These parts extend the completed OOP calculator. The first two interfaces use
two named operands; Part 3 deliberately changes them to flexible arguments.
'''
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    errors = []
    for index, name in enumerate(STAGES, 1):
        destination = ROOT / 'examples/stages' / name
        expected = stage_files(index)
        if args.check:
            actual = {str(path.relative_to(destination)): path.read_text() for path in destination.rglob('*')
                      if path.is_file() and '__pycache__' not in path.parts and '.pytest_cache' not in path.parts}
            for path in sorted(actual.keys() | expected.keys()):
                if actual.get(path) != expected.get(path):
                    errors.append(f'{name}/{path}: stale or missing; run tools/build_stages.py')
        else:
            for obsolete in destination.rglob('*'):
                if obsolete.is_file() and '__pycache__' not in obsolete.parts and '.pytest_cache' not in obsolete.parts and str(obsolete.relative_to(destination)) not in expected:
                    obsolete.unlink()
            for path, content in expected.items():
                target = destination / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
    print('\n'.join(errors) if errors else 'Six cumulative snapshots are current.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
