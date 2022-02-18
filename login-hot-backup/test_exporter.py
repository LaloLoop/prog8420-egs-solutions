import tempfile
from unittest import TestCase
from unittest.mock import patch

from exporter import DBExporter


class TestExporter(TestCase):

    def setUp(self) -> None:
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file_name = self.test_file.name

    @patch('exporter.DBRepository')
    def test_export(self, DBRepository):
        user_records = [
            (1, 'user1@test.com', 'ML5ZYJ544', 3),
            (2, 'user2@test.com', 'ML5ZY6LJ544', 10)
        ]
        users_gen = (u for u in user_records)
        mock_repo = DBRepository.return_value

        mock_repo.find_all.return_value = users_gen

        exporter = DBExporter()

        exporter.export(self.test_file_name)

        mock_repo.find_all.assert_called_once()

        with open(self.test_file_name, "r") as result_file:
            i = 0
            for line in result_file:
                for j, v in enumerate(line.replace("\n", "").split(",")):
                    self.assertEqual(str(user_records[i][j]), v)
                i += 1

            self.assertTrue(i > 0)