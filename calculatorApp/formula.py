from typing import Dict, Any, Callable, List


class Formula:
    def __init__(self, expression: Callable[..., float], keys: List[str]):
        """
        Конструктор, принимающий лямбда-выражение для выполнения произвольной операции с произвольным числом переменных.

        :param expression: Лямбда-выражение, определяющее операцию.
        :param keys: Список ключей для значений, которые будут переданы в лямбда-выражение.
        """
        self.expression = expression
        self.keys = keys

    def evaluate(self, data: Dict[str, Any], result_key: str) -> None:
        """
        Выполняет вычисление на основе лямбда-выражения и значений из data и сохраняет результат по ключу result_key.

        :param data: Словарь с данными для вычислений.
        :param result_key: Ключ для сохранения результата в словаре data.
        """
        # Извлекаем значения по ключам, если ключ не найден, подставляем 0
        values = [data.get(key) for key in self.keys]

        # Выполняем лямбда-выражение с полученными значениями
        result = self.expression(*values)

        # Сохраняем результат в словарь
        data[result_key] = result
