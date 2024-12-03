from calculator.settings import STATIC_ROOT
from calculatorApp.excelTemplateFiller import ExcelTemplateFiller


def fact(data):
    """
        Заполняет шаблон Excel для фактических данных.

        Этот метод заполняет шаблон Excel, основываясь на фактических данных и вычисленных результатах.

        Параметры:
            data (dict): Данные, полученные из калькулятора.

        Возвращает:
            excel_template_filler.fill_data: Заполненный шаблон Excel.
        """
    excel_template_filler = ExcelTemplateFiller(STATIC_ROOT + "/excelTemplates/factTemplate1.xlsx")
    compares = {
        "B3": "Факт максимальное кол-во файлов 180 часов",
        "B4": "Факт максимальное кол-во файлов 168 часов",
        "B5": "Факт максимальное кол-во файлов 79 часов",
        "B6": "Факт максимальное кол-во файлов 180 часов праздники/вых",
        "C3": "День факт разница нагрузки",
        "C6": "День/пр/вых факт разница нагрузки",
        "C7": "Ночь/пр/вых факт разница нагрузки",
        "D3": "День факт нагрузка в %",
        "D6": "День/пр/вых факт нагрузка в %",
        "D7": "Ночь/пр/вых факт нагрузка в %",
        "E3": "Факт нехватка машин 180 часов",
        "E4": "Факт нехватка машин 168 часов",
        "E5": "Факт нехватка машин 79 часов",
        "E6": "Ночь/пр/вых факт нехватка машин"
    }

    return excel_template_filler.fill_data(compare_data(compares, data))


def plan(data):
    """
        Заполняет шаблон Excel для планируемых данных.

        Этот метод заполняет шаблон Excel, основываясь на планируемых данных.

        Параметры:
            data (dict): Данные, полученные из калькулятора.

        Возвращает:
            excel_template_filler.fill_data: Заполненный шаблон Excel.
        """
    excel_template_filler = ExcelTemplateFiller(STATIC_ROOT + "/excelTemplates/planTemplate1.xlsx")
    compares = {
        "B3": "Ср колво файлов новых УЗ в месяц день",
        "B6": "Ср колво файлов новых УЗ в месяц день/пр/вых",
        "B7": "Ср колво файлов новых УЗ в месяц ночь/пр/вых",
        "C3": "Ср колво файлов с учетом новых УЗ в месяц день",
        "C6": "Ср колво файлов с учетом новых УЗ в месяц день/пр/вых",
        "C7": "Ср колво файлов с учетом новых УЗ в месяц ночь/пр/вых",
        "D3": "(план)Факт максимальное кол-во файлов 180 часов",
        "D4": "Факт максимальное кол-во файлов 168 часов",
        "D5": "Факт максимальное кол-во файлов 79 часов",
        "D6": "Факт максимальное кол-во файлов 180 часов праздники/вых",
        "E3": "Планируемая разница нагрузки день",
        "E6": "Планируемая разница нагрузки день/пр/вых",
        "E7": "Планируемая разница нагрузки ночь/пр/вых",
        "F3": "Планируемая нагрузка в % день",
        "F6": "Планируемая нагрузка в % день/пр/вых",
        "F7": "Планируемая нагрузка в % ночь/пр/вых",
        "G3": "Планируемая нехватка машин 180 часов",
        "G4": "Планируемая нехватка машин 168 часов",
        "G5": "Планируемая нехватка машин 79 часов",
        "G6": "Планируемая нехватка машин 180 часов",
    }

    return excel_template_filler.fill_data(compare_data(compares, data))


def compare_data(compares, data):
    """
        Сравнивает и выбирает данные для заполнения шаблона Excel.

        Этот метод используется для подготовки данных, которые будут вставлены в шаблон Excel.

        Параметры:
            compares (dict): Словарь с соответствиями ячеек и ключей данных.
            data (dict): Данные, полученные из калькулятора.

        Возвращает:
            dict: Подготовленные данные для заполнения шаблона.
        """
    result = {}
    for key, value in compares.items():
        result[key] = data[value]
    return result


def fact_plan(data):
    """
        Заполняет шаблон Excel для комбинированных данных (фактические и планируемые).

        Этот метод заполняет комбинированный шаблон Excel, который включает как фактические, так и планируемые данные.

        Параметры:
            data (dict): Данные, полученные из калькулятора.

        Возвращает:
            excel_template_filler.fill_data: Заполненный комбинированный шаблон Excel.
        """
    excel_template_filler = ExcelTemplateFiller(STATIC_ROOT + "/excelTemplates/fact_planTemplate1.xlsx")
    compares = {
        "B3": "Факт максимальное кол-во файлов 180 часов",
        "B4": "Факт максимальное кол-во файлов 168 часов",
        "B5": "Факт максимальное кол-во файлов 79 часов",
        "B6": "Факт максимальное кол-во файлов 180 часов праздники/вых",
        "C3": "День факт разница нагрузки",
        "C6": "День/пр/вых факт разница нагрузки",
        "C7": "Ночь/пр/вых факт разница нагрузки",
        "D3": "День факт нагрузка в %",
        "D6": "День/пр/вых факт нагрузка в %",
        "D7": "Ночь/пр/вых факт нагрузка в %",
        "E3": "Факт нехватка машин 180 часов",
        "E4": "Факт нехватка машин 168 часов",
        "E5": "Факт нехватка машин 79 часов",
        "E6": "Ночь/пр/вых факт нехватка машин",

        "F3": "Ср колво файлов новых УЗ в месяц день",
        "F6": "Ср колво файлов новых УЗ в месяц день/пр/вых",
        "F7": "Ср колво файлов новых УЗ в месяц ночь/пр/вых",
        "G3": "Ср колво файлов с учетом новых УЗ в месяц день",
        "G6": "Ср колво файлов с учетом новых УЗ в месяц день/пр/вых",
        "G7": "Ср колво файлов с учетом новых УЗ в месяц ночь/пр/вых",
        "H3": "(план)Факт максимальное кол-во файлов 180 часов",
        "H4": "Факт максимальное кол-во файлов 168 часов",
        "H5": "Факт максимальное кол-во файлов 79 часов",
        "H6": "Факт максимальное кол-во файлов 180 часов праздники/вых",
        "I3": "Планируемая разница нагрузки день",
        "I6": "Планируемая разница нагрузки день/пр/вых",
        "I7": "Планируемая разница нагрузки ночь/пр/вых",
        "J3": "Планируемая нагрузка в % день",
        "J6": "Планируемая нагрузка в % день/пр/вых",
        "J7": "Планируемая нагрузка в % ночь/пр/вых",
        "K3": "Планируемая нехватка машин 180 часов",
        "K4": "Планируемая нехватка машин 168 часов",
        "K5": "Планируемая нехватка машин 79 часов",
        "K6": "Планируемая нехватка машин 180 часов",
    }
    return excel_template_filler.fill_data(compare_data(compares, data))

