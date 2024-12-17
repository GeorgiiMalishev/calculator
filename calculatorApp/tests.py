from django.test import TestCase
import unittest

from calculatorApp.calculator1 import Calculator1

class TestCalculator1(unittest.TestCase):
    def setUp(self):
        # Входные данные из таблицы
        self.input_data = {
            'День факт среднее кол-во файлов в месяц': 6258,
            'День/пр/вых факт среднее кол-во файлов в месяц': 1619,
            'Ночь/пр/вых факт среднее кол-во файлов в месяц': 2913,
            'Факт кол-во машин 180 часов': 2,
            'Факт кол-во машин 168 часов': 4,
            'Факт кол-во машин 79 часов': 3,
            'Общее кол-во новых пользователей (УЗ)': 8300
        }
        self.calculator = Calculator1(self.input_data)

    def test_basic_calculations(self):
        results = self.calculator.calculate()
        print(results)
        # Проверяем основные расчёты
        self.assertEqual(results['Общее факт среднее кол-во файлов в месяц'], 10790)
        self.assertEqual(results['Факт максимальное кол-во файлов 180 часов'], 3606)
        self.assertEqual(results['Факт максимальное кол-во файлов 168 часов'], 3500)
        self.assertEqual(results['Факт максимальное кол-во файлов 79 часов'], 1314)
        self.assertEqual(results['Факт максимальное кол-во файлов 180 часов праздники/вых'], 3204)

    def test_load_percentages(self):
        results = self.calculator.calculate()
        
        # Проверяем процент нагрузки
        self.assertEqual(results['День факт нагрузка в %'], 74)
        self.assertEqual(results['День/пр/вых факт нагрузка в %'], 51)
        self.assertEqual(results['Ночь/пр/вых факт нагрузка в %'], 91)

    def test_machine_shortage(self):
        results = self.calculator.calculate()
        
        # Проверяем нехватку машин
        self.assertEqual(results['Факт нехватка машин 180 часов'], 1)
        self.assertEqual(results['Факт нехватка машин 168 часов'], 0)
        self.assertEqual(results['Факт нехватка машин 79 часов'], 0)
        self.assertEqual(results['Ночь/пр/вых факт нехватка машин'], 1)

    def test_load_differences(self):
        results = self.calculator.calculate()
        
        # Проверяем разницу нагрузки
        self.assertEqual(results['День факт разница нагрузки'], 2162)
        self.assertEqual(results['День/пр/вых факт разница нагрузки'], 1585)
        self.assertEqual(results['Ночь/пр/вых факт разница нагрузки'], 291)

    def test_planned_load_differences(self):
        results = self.calculator.calculate()
        
        # Проверяем планируемую разницу нагрузки
        self.assertEqual(results['Планируемая разница нагрузки день'], -1692)
        self.assertEqual(results['Планируемая разница нагрузки день/пр/вых'], -34)
        self.assertEqual(results['Планируемая разница нагрузки ночь/пр/вых'], -2622)
        
        # Проверяем планируемую нагрузку в процентах
        self.assertEqual(results['Планируемая нагрузка в % день'], 116)
        self.assertEqual(results['Планируемая нагрузка в % день/пр/вых'], 101)
        self.assertEqual(results['Планируемая нагрузка в % ночь/пр/вых'], 182)

    def test_planned_machine_shortage(self):
        results = self.calculator.calculate()
        
        # Проверяем планируемую нехватку машин
        self.assertEqual(results['Планируемая нехватка машин 180 часов'], 3)
        self.assertEqual(results['Планируемая нехватка машин 168 часов'], 4)
        self.assertEqual(results['Планируемая нехватка машин 79 часов'], 0)
        self.assertEqual(results['Планируемая нехватка машин пр/вых'], 3)

    def test_planned_file_counts(self):
        results = self.calculator.calculate()
        
        # Проверяем среднее количество файлов с учетом новых УЗ
        self.assertEqual(results['Ср колво файлов с учетом новых УЗ в месяц день'], 12516)
        self.assertEqual(results['Ср колво файлов с учетом новых УЗ в месяц день/пр/вых'], 3238)
        self.assertEqual(results['Ср колво файлов с учетом новых УЗ в месяц ночь/пр/вых'], 5826)
        
        # Проверяем распределение новых УЗ по времени работы
        self.assertEqual(results['Ср колво файлов новых УЗ в месяц день'], 6258)
        self.assertEqual(results['Ср колво файлов новых УЗ в месяц день/пр/вых'], 1619)
        self.assertEqual(results['Ср колво файлов новых УЗ в месяц ночь/пр/вых'], 2913)

    def test_planned_maximum_files(self):
        results = self.calculator.calculate()
        
        # Проверяем плановые максимальные значения
        self.assertEqual(results['(план)Факт максимальное кол-во файлов 180 часов'], 6010)
        self.assertEqual(results['Факт максимальное кол-во файлов 168 часов'], 3500)
        self.assertEqual(results['Факт максимальное кол-во файлов 79 часов'], 1314)
        
        # Проверяем суммарные показатели
        self.assertEqual(results['сумм R4:R6'], 10824)

    def test_planned_machine_count(self):
        results = self.calculator.calculate()
        
        # Проверяем плановое количество машин
        self.assertEqual(results['(план)Факт кол-во машин 180 часов'], 5)
        self.assertEqual(results['Факт кол-во машин 168 часов'], 4)
        self.assertEqual(results['Факт кол-во машин 79 часов'], 3)

if __name__ == '__main__':
    unittest.main()
