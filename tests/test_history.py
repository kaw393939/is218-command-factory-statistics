import pytest
from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.history import History

def test_history_copy_protects_collection_membership():
    history = History()
    calculation = Calculation([2, 3], Operations.add)
    history.add(calculation, 5.0)
    snapshot = history.get_history()
    snapshot.clear()
    assert history.get_history() == [(calculation, 5.0)]

def test_history_objects_are_shared_by_the_shallow_copy():
    history = History()
    calculation = Calculation([2, 3], Operations.add)
    history.add(calculation, 5.0)
    snapshot = history.get_history()
    assert snapshot[0][0] is calculation

def test_history_rejects_non_calculations():
    with pytest.raises(TypeError):
        History().add('add 2 3', 5)
