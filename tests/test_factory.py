import pytest
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
