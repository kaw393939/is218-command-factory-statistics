import pytest
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
