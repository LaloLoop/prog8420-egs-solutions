import itertools

from openpyxl import load_workbook


class XLSXParser:

    def load(self, path="chyper-code.xlsx"):
        wb = load_workbook(path, read_only=True)
        sheet = wb.active

        # Skip header
        mapping = {}
        for row_num in itertools.count(2):
            row_str = str(row_num)

            key = sheet['A' + row_str].value
            value = sheet['B' + row_str].value

            if key is None or value is None:
                break

            mapping[str(key)] = str(value)

        return mapping

