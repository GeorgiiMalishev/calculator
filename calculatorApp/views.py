import math
from django.http import JsonResponse, HttpResponse
#from .export_utils import export_to_excel, export_to_pdf, export_to_word
from django.shortcuts import render

# Выбор калькулятора (калькулятор 1, 2 или 3)
def calculate(request):
    if request.method == 'POST':
        calculator_type = request.POST.get('calculator_type')  # тип калькулятора
        operation_type = request.POST.get('operation_type')  # "Факт" или "План"

        # Получаем данные из формы
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        num3 = float(request.POST.get('num3'))

        result = None

        # Логика для калькулятора 1
        if calculator_type == '1':
            if operation_type == 'fact':
                result = calculate_fact_1(num1, num2, num3)
            else:
                result = calculate_plan_1(num1, num2, num3)


# Пример расчета для калькулятора 1
def calculate_fact_1(num1, num2, num3):
    # Логика расчета для "Факт" калькулятора 1
    result = (num1 + num2) * num3
    return result


def calculate_plan_1(num1, num2, num3):
    # Логика расчета для "План" калькулятора 1
    result = (num1 * num2) - num3
    return result

def calculator_view(request):
    return render(request, 'calculator.html')
# Логика расчета для калькуляторов 2 и 3 аналогична
