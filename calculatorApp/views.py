import os
import io
from msilib import Table

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from docx import Document
import pandas as pd
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from fontTools.ttLib import TTFont
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, TableStyle
from spire.xls import Workbook
from xhtml2pdf import pisa

from calculatorApp import calculator1, resultToExcel1
from calculatorApp.calculator1 import Calculator1


@csrf_exempt
def calculate_fact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data = {key: int(value) for key, value in data.items()}
            print("Фактические расчеты - данные:", data)
            calculator = Calculator1(data)
            results = calculator.calculate()
            excel = resultToExcel1.fact(results)
            html_content = convert_to_html(excel)
            context = {'html_content': html_content}
            return JsonResponse(context)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат данных'}, status=400)
        except Exception as e:
            print(f"Ошибка: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)


@csrf_exempt
def calculate_plan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data = {key: int(value) for key, value in data.items()}
            print("Плановые расчеты - данные:", data)
            calculator = Calculator1(data)
            results = calculator.calculate()
            excel = resultToExcel1.plan(results)
            html_content = convert_to_html(excel)
            context = {'html_content': html_content}
            return JsonResponse(context)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат данных'}, status=400)
        except Exception as e:
            print(f"Ошибка: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)


def calculator_view(request, calculator_name):
    return render(request, f'calculator{calculator_name}.html')


def convert_to_html(workbook):
    sheet = workbook.active
    html = "<table style='width: 100%; border-collapse: collapse;'>\n"
    for row in sheet.iter_rows():
        html += "  <tr>\n"
        for cell in row:
            if cell.value is not None:
                value = cell.value
            else:
                # Если это объединенная ячейка, найдем первую ячейку в диапазоне
                value = ""
                for merged_range in sheet.merged_cells.ranges:
                    if cell.coordinate in merged_range:
                        top_left_cell = sheet[merged_range.coord.split(":")[0]]
                        value = top_left_cell.value
                        break
            html += f"    <td style='border: 1px solid #ddd; padding: 8px;'>{value}</td>\n"
        html += "  </tr>\n"
    html += "</table>"
    return html


@csrf_exempt
def export_excel(request):
    try:
        print("Raw request body:", request.body.decode('utf-8'))
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return HttpResponse(f'JSONDecodeError: {str(e)}', status=400)

    data = {key: int(value) for key, value in data.items()}
    print("Плановые расчеты - данные:", data)
    calculator = Calculator1(data)
    results = calculator.calculate()

    # Создаем экземпляр ExcelTemplateFiller и заполняем данные
    excel = resultToExcel1.fact_plan(results)
    file_format = request.GET.get('format', 'xlsx')

    if file_format == 'xlsx':
        buffer = io.BytesIO()
        excel.save(buffer)
        buffer.seek(0)
        response = HttpResponse(buffer,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="file.xlsx"'
        return response


    elif file_format == 'pdf':
        # Читаем данные из Excel
        wb = excel
        sheet = wb.active

        # Создаем PDF
        pdf_output = io.BytesIO()
        c = canvas.Canvas(pdf_output, pagesize=letter)
        pdfmetrics.registerFont(TTFont('static/font/FreeSans.ttf', 'FreeSans'))
        c.setFont('FreeSans', 12)
        width, height = letter

        # Начальная позиция для рисования таблицы
        x_offset = 30
        y_offset = height - 40
        row_height = 20
        col_width = 100

        # Рисуем заголовки таблицы
        for col_num, cell in enumerate(sheet[1], start=1):
            c.drawString(x_offset + (col_num - 1) * col_width, y_offset, str(cell.value))

        # Рисуем данные таблицы
        y_offset -= row_height
        for row in sheet.iter_rows(min_row=2, values_only=True):
            for col_num, cell in enumerate(row, start=1):
                c.drawString(x_offset + (col_num - 1) * col_width, y_offset, str(cell) if cell is not None else "")
            y_offset -= row_height

        c.save()

        pdf_output.seek(0)
        response = HttpResponse(pdf_output, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="file.pdf"'
        return response


    elif file_format == 'doc':
        # Преобразуем Excel в Word
        doc = Document()
        doc.add_heading('Exported Table', level=1)

        sheet = excel.active
        table = doc.add_table(rows=1, cols=sheet.max_column)
        table.style = 'Table Grid'

        # Добавляем заголовки
        hdr_cells = table.rows[0].cells
        for i, cell in enumerate(sheet[1]):
            hdr_cells[i].text = str(cell.value)

        # Добавляем строки
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_cells = table.add_row().cells
            for i, cell in enumerate(row):
                row_cells[i].text = str(cell) if cell is not None else ""

        # Форматируем документ
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.style.font.size = Pt(10)
                    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        doc_output = io.BytesIO()
        doc.save(doc_output)
        doc_output.seek(0)

        response = HttpResponse(doc_output,
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="file.docx"'
        return response

    return HttpResponse(status=400)
