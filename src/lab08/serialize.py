import json
from pathlib import Path

from models import Student

DATA_DIR = Path(__file__).parent.parent
students = [
    Student(
        fio="Иванов Иван Иванович", birthdate="2000-05-15", group="ИТ-101", gpa=4.5
    ),
    Student(
        fio="Петрова Анна Сергеевна", birthdate="2001-03-20", group="ИТ-101", gpa=4.8
    ),
    Student(
        fio="Сидоров Алексей Петрович", birthdate="1999-12-10", group="ФИ-201", gpa=3.9
    ),
]


def students_to_json(students, path: str | Path) -> None:
    output_path = Path(path)
    data = [student.to_dict() for student in students]
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


students_to_json(students, "src/lab08/students_output.json")


def students_from_json(path: str | Path):
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Файл не найден: {input_path}")
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Ожидается список студентов в JSON")
    return [Student.from_dict(item) for item in data]


students = students_from_json("src/lab08/students_output.json")
for student in students:
    print(student)
