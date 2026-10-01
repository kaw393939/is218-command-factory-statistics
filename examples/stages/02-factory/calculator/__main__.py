from calculator.factory import CalculationFactory
print(CalculationFactory.create("add", 2, 3).get_result())
