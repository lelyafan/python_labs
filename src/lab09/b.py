import csv
from pathlib import Path
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from a import Student

class Group:
    def __init__(self, storage_path: str):
        self.path = Path("data/lab09") / storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with open(self.path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['fio', 'birthdate', 'group', 'gpa'])
                writer.writeheader()
    
    def _read_all(self) -> List[Dict[str, Any]]:
        rows = []
        with open(self.path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['gpa'] = float(row['gpa'])
                rows.append(row)
        return rows
    
    def _write_all(self, rows: List[Dict[str, Any]]): 
        with open(self.path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['fio', 'birthdate', 'group', 'gpa'])
            writer.writeheader()
            writer.writerows(rows)
    
    def list(self) -> List[Student]: 
        rows = self._read_all()
        students = []
        for row in rows:
            try:
                student = Student.from_dict(row)
                students.append(student)
            except ValueError as e:
                print(f"Ошибка валидации студента {row['fio']}: {e}")
        return students
    
    def add(self, student: Student):
        try:
            validated_student = Student(
                fio=student.fio,
                birthdate=student.birthdate,
                group=student.group,
                gpa=student.gpa
            )
        except ValueError as e:
            raise ValueError(f"Некорректные данные студента: {e}")
        
        with open(self.path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['fio', 'birthdate', 'group', 'gpa'])
            writer.writerow(validated_student.to_dict())
    
    def find(self, substr: str) -> List[Student]: 
        students = self.list()
        return [student for student in students if substr.lower() in student.fio.lower()]
    
    def remove(self, fio: str): 
        rows = self._read_all()
        updated_rows = [row for row in rows if row['fio'] != fio]
        if len(updated_rows) == len(rows):
            raise ValueError(f"Студент с ФИО '{fio}' не найден")
        self._write_all(updated_rows)
    
    def update(self, fio: str, **fields):
        rows = self._read_all()
        updated = False
        for row in rows:
            if row['fio'] == fio:
                for field, value in fields.items():
                    if field in ['fio', 'birthdate', 'group', 'gpa']:
                        row[field] = value
                updated = True
                try:
                    Student.from_dict(row)
                except ValueError as e:
                    raise ValueError(f"Некорректные данные после обновления: {e}")
        if not updated:
            raise ValueError(f"Студент с ФИО '{fio}' не найден")
        self._write_all(rows)
    
    def stats(self) -> Dict[str, Any]:
        students = self.list()
        if not students:
            return {
                "count": 0,
                "min_gpa": 0,
                "max_gpa": 0,
                "avg_gpa": 0,
                "groups": {},
                "top_5_students": []
            }
        
        gpas = [student.gpa for student in students]
        groups_stats = {}
        for student in students:
            groups_stats[student.group] = groups_stats.get(student.group, 0) + 1
        sorted_students = sorted(students, key=lambda s: s.gpa, reverse=True)
        top_5 = [{"fio": s.fio, "gpa": s.gpa} for s in sorted_students[:5]]
        return {
            "count": len(students),
            "min_gpa": min(gpas),
            "max_gpa": max(gpas),
            "avg_gpa": round(sum(gpas) / len(gpas), 2),
            "groups": groups_stats,
            "top_5_students": top_5
        }
    
    def exists(self, fio: str) -> bool:
        students = self.list()
        return any(student.fio == fio for student in students)

    def is_empty(self) -> bool:
        with open(self.path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return len(list(reader)) == 0
    
if __name__ == "__main__":

    group = Group("students.csv")

    if group.is_empty(): 
        students_to_add = [
            Student("Иванов Иван", "2000-05-15", "БИВТ-25-1", 4.5),
            Student("Иванов Петр", "2004-12-03", "БИВТ-25-2", 3.8),
            Student("Сидорова Анна", "1999-08-22", "БИВТ-25-1", 4.2),
            Student("Сидоров Алексей","2003-03-20","БИВТ-21-1",3.9),
            Student("Кузнецова Мария","2004-08-25","БИВТ-21-1",4.8),
            Student("Иванова Ольга", "2001-07-14", "БИВТ-21-1", 4.9)
        ]
        
        for student in students_to_add:
            group.add(student)
            print(f"    Добавлен: {student.fio}")
    else:
        print("Файл уже содержит данные")
    group.remove("Иванова Ольга")
    print(f"\nПосле удаления Ивановой, всего студентов: {len(group.list())}")
    print("Студенты:")
    for student in group.list():
        print(f"  {student}")
    
    print("\nПоиск по 'Иванов':")
    for student in group.find("Иванов"):
        print(f"  {student}")
    
    print("\nСтатистика:")
    stats = group.stats()
    for key, value in stats.items():
        if key == "top_5_students":
            print(f"  {key}:")
            for student in value:
                print(f"    {student['fio']} - GPA: {student['gpa']}")
        else:
            print(f"  {key}: {value}")
