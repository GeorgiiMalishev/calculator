from typing import Dict, Any


class Formula:
    def __init__(self, value1_key: str, operation: str, value2_key: str = None, constant: float = None):
        """
        Универсальный конструктор для двух случаев:
        1. Операция между двумя переменными (value1_key и value2_key).
        2. Операция между переменной (value1_key) и константой (constant).
        
        :param value1_key: ключ первого значения из словаря данных
        :param operation: знак операции (+, -, *, /)
        :param value2_key: ключ второго значения (если операция с двумя переменными)
        :param constant: константа, если операция с переменной и константой
        """
        self.value1_key = value1_key
        self.value2_key = value2_key
        self.constant = constant
        self.operation = operation

    def evaluate(self, data: Dict[str, Any], result_key: str) -> None:
        """
        Выполняет вычисление на основе значений из data и записывает результат по ключу result_key.
        Если значение не нулевое, используется оно, иначе используется константа.
        """
        value1 = data.get(self.value1_key, 0)

        # Если второй ключ задан, это операция между двумя значениями
        if self.value2_key:
            value2 = data.get(self.value2_key, 0)
        else:
            # Если второй ключ не задан, используем константу
            value2 = self.constant

        # Выполняем операцию
        if self.operation == '+':
            result = value1 + value2
        elif self.operation == '-':
            result = value1 - value2
        elif self.operation == '*':
            result = value1 * value2
        elif self.operation == '/':
            result = value1 / value2
        else:
            raise ValueError(f"Unsupported operation: {self.operation}")

        # Сохраняем результат в словарь
        data[result_key] = result
