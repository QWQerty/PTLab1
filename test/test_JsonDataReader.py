import unittest
from unittest.mock import mock_open, patch
from JsonDataReader import JsonDataReader


class TestJsonDataReader(unittest.TestCase):

    def setUp(self):
        self.json_reader = JsonDataReader()

    def test_read_successful(self):
        # Мокаем open для имитации успешного чтения файла
        with patch("builtins.open", mock_open(
         read_data='{"students": [{"name": "Александра", "rating": 90}]}')):
            result = self.json_reader.read("fake_path.json")

        expected_result = {'students_in_last_quartile':
                           [{'name': 'Александра', 'rating': 90}]}
        self.assertEqual(result, expected_result)

    def test_read_file_not_found(self):
        # Мокаем open для имитации ошибки FileNotFoundError
        with patch("builtins.open",
                   side_effect=FileNotFoundError("File not found")):
            result = self.json_reader.read("nonexistent_file.json")

        self.assertIsNone(result)

    def test_read_file_read_error(self):
        # Мокаем open для имитации ошибки при чтении файла
        with patch("builtins.open",
                   side_effect=Exception("Unable to read file")):
            result = self.json_reader.read("fake_path.json")

        self.assertIsNone(result)

    def test_filter_students_last_quartile(self):
        students = [
            {"name": "Александра", "rating": 90},
            {"name": "Игорь", "rating": 85},
            {"name": "Елена", "rating": 95},
            {"name": "Дмитрий", "rating": 88},
            {"name": "Никита", "rating": 92},
        ]

        result = self.json_reader.filter_students_last_quartile(students)

        expected_result = [
            {"name": "Дмитрий", "rating": 88},
            {"name": "Александра", "rating": 90},
            {"name": "Никита", "rating": 92},
            {"name": "Елена", "rating": 95},
        ]

        # Сравнить наборы словарей
        self.assertEqual(set(map(frozenset, result)),
                         set(map(frozenset, expected_result)))


if __name__ == "__main__":
    unittest.main()
