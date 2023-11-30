# -*- coding: utf-8 -*-
import json
from Types import DataType
from DataReader import DataReader

class JsonDataReader(DataReader):

    def read(self, path: str) -> DataType:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File not found at path: {path}")
            return None
        except Exception as e:
            print(f"Error: Unable to read the file. Reason: {e}")
            return None

        students = data.get('students', [])
        students_in_last_quartile = self.filter_students_last_quartile(students)

        # Вывод на экран студентов с рейтингом в последнюю квартиль
        for student in students_in_last_quartile:
            print(f"S: {student['name']}, R: {student['rating']}")

        return {'students_in_last_quartile': students_in_last_quartile}

    def filter_students_last_quartile(self, students):
        sorted_students = sorted(students, key=lambda x: x['rating'])
        total_students = len(sorted_students)
        last_quartile_start = total_students // 4 * 3

        return sorted_students[last_quartile_start:]

# Пример использования
if __name__ == "__main__":

    json_reader = JsonDataReader()
    json_reader.read("data\\data.json")