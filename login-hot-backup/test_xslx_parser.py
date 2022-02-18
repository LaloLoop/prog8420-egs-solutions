from unittest import TestCase

from cipher import DEFAULT_MAPPING
from xslxparser import XLSXParser


class TestXLSXParser(TestCase):

    def test_loads_xlsx_mapping(self):
        xlsx_path = "test_files/chyper-code.xlsx"

        parser = XLSXParser()

        mapping = parser.load(xlsx_path)

        for k, v in DEFAULT_MAPPING.items():
            self.assertTrue(k in mapping)
            self.assertEqual(v, DEFAULT_MAPPING[k])
