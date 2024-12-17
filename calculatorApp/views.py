import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from calculatorApp import resultToExcel1
from calculatorApp.calculator1 import Calculator1
from calculatorApp.converter import *
from calculatorApp.docTemplateFiller import fill_template_from_calculator1


@csrf_exempt
def calculate_fact(request):
    """
    Обрабатывает POST-запросы для расчёта фактических данных.
    Принимает JSON-данные, обрабатывает их с помощью Calculator1 и возвращает результат в виде HTML.

    Параметры:
        request: Объект запроса Django, содержащий JSON-данные.

    Возвращает:
        JsonResponse с HTML-результатом или сообщением об ошибке.
    """
    if request.method == 'POST':
        try:
            #Загружаем данные и преобразуем в целочисленные значения
            data = json.loads(request.body)
            data = {key: int(value) for key, value in data.items()}
            # Проводим рассчеты
            calculator = Calculator1(data)
            results = calculator.calculate()
            #Преобразуем в excel
            excel = resultToExcel1.fact(results)
            # Преобразуем в html
            html_content = convert_to_html(excel)
            context = {'html_content': html_content}
            return JsonResponse(context)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат данных'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)


@csrf_exempt
def calculate_plan(request):
    """
    Обрабатывает POST-запросы для расчёта плановых данных.
    Принимает JSON-данные, обрабатывает их с помощью Calculator1 и возвращает результат в виде HTML.

    Параметры:
        request: Объект запроса Django, содержащий JSON-данные.

    Возвращает:
        JsonResponse с HTML-результатом или сообщением об ошибке.
    """
    if request.method == 'POST':
        try:
            # Загружаем данные и преобразуем в целочисленные значения
            data = json.loads(request.body)
            data = {key: int(value) for key, value in data.items()}
            # Проводим рассчеты если Общее кол-во новых пользователей (УЗ) больше 0
            calculator = Calculator1(data)
            if data['Общее кол-во новых пользователей (УЗ)'] < 1:
                return JsonResponse({'status': 'error', 'message': 'Для плановых расчетов поле "Кол-во новыхпользователей" не должно быть пустым или 0'}, status=400)
            results = calculator.calculate()
            # Преобразуем в excel
            excel = resultToExcel1.plan(results)
            # Преобразуем в html
            html_content = convert_to_html(excel)
            context = {'html_content': html_content}
            return JsonResponse(context)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат данных'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)


def calculator_view(request, calculator_name):
    """
    Рендерит HTML-страницу для заданного калькулятора.

    Параметры:
        request: Объект запроса Django.
        calculator_name: Имя калькулятора для отображения соответствующей страницы.

    Возвращает:
        HttpResponse с HTML-страницей.
    """
    return render(request, f'calculator{calculator_name}.html')


@csrf_exempt
def export_file(request):
    """
    Экспортирует данные в файл формата Excel, PDF или Word.
    Формат задаётся параметром 'format' в GET-запросе (xlsx, pdf, doc).

    Параметры:
        request: Объект Django HttpRequest, содержащий JSON-данные и параметр 'format'.

    Возвращает:
        HttpResponse с файлом в выбранном формате или сообщение об ошибке.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return HttpResponse(f'JSONDecodeError: {str(e)}', status=400)

    data = {key: int(value) for key, value in data.items()}
    calculator = Calculator1(data)
    results = calculator.calculate()
    if data['Общее кол-во новых пользователей (УЗ)'] >= 1:
        excel = resultToExcel1.fact_plan(results)
    else:
        excel = resultToExcel1.fact(results)
    file_format = request.GET.get('format', 'xlsx')

    #Экспорт в excel
    if file_format == 'xlsx':
        buffer = io.BytesIO()
        excel.save(buffer)
        buffer.seek(0)
        response = HttpResponse(buffer,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="file.xlsx"'
        return response

    # Экспорт в pdf
    elif file_format == 'pdf':
        pdf = convert_excel_to_pdf(excel)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="from_excel.pdf"'
        response.write(pdf)
        return response

    # Экспорт в doc
    elif file_format == 'doc':
        doc = convert_excel_to_word(excel)
        response = HttpResponse(doc,
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="file.docx"'
        return response

    # Экспорт в шаблон
    elif file_format == 'docTemplate':
        doc = fill_template_from_calculator1(results, STATIC_ROOT + '/docTemplates/template1.docx')
        response = HttpResponse(doc,
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="file.docx"'
        return response

    return HttpResponse(status=400)
