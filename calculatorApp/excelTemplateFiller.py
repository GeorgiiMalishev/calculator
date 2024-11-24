import openpyxl


class ExcelTemplateFiller:
    def __init__(self, template_path):
        self.template_path = template_path
        self.workbook = openpyxl.load_workbook(template_path)
        self.sheet = self.workbook.active

    def fill_data(self, data):
        """
        data: dict - словарь с данными, где ключи это координаты ячеек (например, 'A1') и значения - данные для этих ячеек
        """
        for cell, value in data.items():
            self.sheet[cell] = value
        return self.workbook


