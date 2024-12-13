import io
from docx import Document
from io import BytesIO

def fill_doc_template(template_path, data):
    """
    Заполняет шаблон DOC данными и сохраняет заполненный документ.

    Args:
        template_path (str): Путь к файлу шаблона DOC.
        data (dict): Словарь с данными для заполнения шаблона.
    """
    # Загружаем шаблон
    doc = Document(template_path)

    # Проходим по всем параграфам и заменяем плейсхолдеры
    for paragraph in doc.paragraphs:
        if not paragraph.runs:
            continue
            
        for key, value in data.items():
            placeholder = f'{key}'
            if placeholder in paragraph.text:
                # Ищем, в каком run находится плейсхолдер
                for run in paragraph.runs:
                    if placeholder in run.text:
                        # Заменяем текст в run, сохраняя форматирование
                        run.text = run.text.replace(placeholder, str(value))

    # Сохраняем заполненный документ
    doc_output = io.BytesIO()
    doc.save(doc_output)
    doc_output.seek(0)
    return doc_output


def fill_template_from_calculator1(data, template_path):
    """
    Заполняет шаблон DOC данными из словаря с результатами первого калькулятора и возвращает заполненный документ.

    Args:
        calculator (Calculator1): Объект калькулятора с результатами расчетов.
        template_path (str): Путь к файлу шаблона DOC.
        output_path (str): Путь для сохранения заполненного документа.
    """

    # Преобразуем данные в формат, ожидаемый шаблоном
    template_values = {
        'Q': data['Общее факт среднее кол-во файлов в месяц'],
        'W': data['День факт среднее кол-во файлов в месяц'],
        'E': data['Ночь/пр/вых факт среднее кол-во файлов в месяц'] + data['День/пр/вых факт среднее кол-во файлов в месяц'],
        'R': data['Факт кол-во машин 180 часов'],
        'T': data['Факт кол-во машин 168 часов'],
        'Y': data['Факт кол-во машин 79 часов'],
        'U': data['Факт кол-во машин 180 часов'],
        'P': data['День факт нагрузка в %'],
        'A': data['Факт нехватка машин 180 часов'],
        'S': data['Факт нехватка машин 168 часов'],
        'D': data['Факт нехватка машин 79 часов'],
        'F': data['Факт нехватка машин 180 часов'],
        'G': data['Общее кол-во новых пользователей (УЗ)'],
        'H': data['Ср колво файлов новых УЗ в месяц день'],
        'J': data['Ср колво файлов новых УЗ в месяц ночь/пр/вых'] + data['Ср колво файлов новых УЗ в месяц день/пр/вых'],
        'V': data['Ср колво файлов с учетом новых УЗ в месяц день'],
        'B': data['Ср колво файлов с учетом новых УЗ в месяц день/пр/вых'] + data['Ср колво файлов с учетом новых УЗ в месяц ночь/пр/вых'],
        'K': data['Планируемая нагрузка в % день'],
        'L': data['Планируемая нехватка машин 180 часов'],
        'Z': data['Планируемая нехватка машин 168 часов'],
        'X': data['Планируемая нехватка машин 79 часов'],
        'C': data['Планируемая нехватка машин 180 часов']
    }

    # Заполняем шаблон
    return fill_doc_template(template_path, template_values)
