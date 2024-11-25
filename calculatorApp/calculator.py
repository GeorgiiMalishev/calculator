from abc import ABC, abstractmethod
from typing import Dict


class Calculator(ABC):
    def __init__(self, input_data: Dict[str, float]):
        self.input_data = input_data

    @abstractmethod
    def calculate(self):
        """
        Абстрактный метод для вычисления формул на основе данных.
        Должен быть реализован в наследуемых классах.
        """
        pass
