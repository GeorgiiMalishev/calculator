from abc import ABC, abstractmethod
from typing import Dict, Any, List

from calculatorApp.formula import Formula


class Calculator(ABC):
    def __init__(self, data: Dict[str, float], formulas: List[Formula]):
        self.data = data
        self.formulas = formulas

    @abstractmethod
    def calculate(self):
        """
        Абстрактный метод для вычисления формул на основе данных.
        Должен быть реализован в наследуемых классах.
        """
        pass
