from typing import Dict, Any

from calculatorApp.formula import Formula


class Calculator1:
    def __init__(self, data: Dict[str, Any], formulas: Dict[str, Formula]):
        """
        :param data: словарь данных
        :param formulas: словарь формул, где ключ — это наименование результата, а значение — формула
        """
        self.data = data
        self.formulas = formulas

    def calculate(self) -> Dict[str, Any]:
        """
        Последовательно вычисляет все формулы, обновляя данные.
        """
        for result_key, formula in self.formulas.items():
            formula.evaluate(self.data, result_key)
        return self.data


if __name__ == "__main__":
    const_data = \
        {'Кол-во часов работы 180 часов': 11,
         'Кол-во часов работы 168 часов': 8,
         'Кол-во часов работы 79 часов': 4,
         'Кол-во часов работы 180 часов праздники/вых': 11,
         'Кол-во часов работы 180 часов ночь': 11,
         'Среднее кол-во дней 180 часов': 15,
         'Среднее кол-во дней 168 часов': 20,
         'Среднее кол-во дней 79 часов': 20,
         'Среднее кол-во дней 180 часов праздники/вых': 15,
         'Среднее кол-во дней 180 часов ночь': 15,
         'Максимальное кол-во файлов в день 180 часов': 58,
         'Максимальное кол-во файлов в день 168 часов': 43,
         'Максимальное кол-во файлов в день 79 часов': 21,
         'Максимальное кол-во файлов в день 180 часов праздники/вых': 78,
         'Максимальное кол-во файлов в день 180 часов ночь': 78,
         'Максимальное кол-во файлов в месяц 180 часов': 877,
         'Максимальное кол-во файлов в месяц 168 часов': 850,
         'Максимальное кол-во файлов в месяц 79 часов': 425,
         'Максимальное кол-во файлов в месяц 180 часов праздники/вых': 1169,
         'Максимальное кол-во файлов в месяц 180 часов ночь': 1169}

    input_data = \
        {
            'Общее факт среднее кол-во файлов в месяц': 10491,
            'Общее кол-во новых пользователей (УЗ)': 600,
            'День факт среднее кол-во файлов в месяц': 6539,
            'Ночь/пр/вых факт среднее кол-во файлов в месяц': 1143,
            'День/пр/вых факт среднее кол-во файлов в месяц': 833,
            'Факт кол-во машин 180 часов': 2,
            'Факт кол-во машин 168 часов': 4,
            'Факт кол-во машин 79 часов': 3,
            'Факт кол-во машин 180 часов ночь': 2,
            'Время обработки (мин) день': 8,
            'Время обработки (мин) ночь': 6,
            'Кол-во мин в часе': 50,
        }
    # Создаём формулы: ключ - наименование результата, значение - формула
    formulas = {
        'Факт максимальное кол-во файлов 180 часов': Formula('Факт кол-во машин 180 часов', '*', 'Максимальное кол-во файлов в месяц 180 часов'),
        'Факт максимальное кол-во файлов 168 часов': Formula('Факт кол-во машин 168 часов', '*', 'Максимальное кол-во файлов в месяц 168 часов'),
        'Факт максимальное кол-во файлов 79 часов': Formula('Факт кол-во машин 79 часов', '*', 'Максимальное кол-во файлов в месяц 79 часов'),
        'Факт максимальное кол-во файлов 180 часов праздники/вых': Formula('Факт кол-во машин 180 часов ночь','*', 'Максимальное кол-во файлов в месяц 180 часов праздники/вых'),
        'Факт максимальное кол-во файлов 180 часов ночь': Formula('Факт кол-во машин 180 часов ночь','*', 'Максимальное кол-во файлов в месяц 180 часов ночь'),
        'сумм1': Formula('Факт максимальное кол-во файлов 180 часов', '+', 'Факт максимальное кол-во файлов 168 часов'),
        'сумм2': Formula('сумм1', '+', 'Факт максимальное кол-во файлов 79 часов'),
        'День факт разница нагрузки': Formula('сумм2', '-', 'День факт среднее кол-во файлов в месяц'),
        'День/пр/вых факт разница нагрузки': Formula('Факт максимальное кол-во файлов 180 часов праздники/вых', '-', 'День/пр/вых факт среднее кол-во файлов в месяц'),
        'Ночь/пр/вых факт разница нагрузки': Formula('Факт максимальное кол-во файлов 180 часов ночь', '-', 'Ночь/пр/вых факт среднее кол-во файлов в месяц'),

    }

    data = {**const_data, **input_data}

    calculator = Calculator1(data, formulas)

    result_data = calculator.calculate()

    print(result_data)
