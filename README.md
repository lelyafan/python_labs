# Лабораторная работа №7
## test_json_csv
```python
import sys
import os

os.chdir("C:/Users/lazar/Desktop/python_labs")
sys.path.insert(0, os.getcwd())

import pytest
import csv
import json
from pathlib import Path
from json_csv import json_to_csv, csv_to_json


def test_json_to_csv_roundtrip(tmp_path: Path):
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"
    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    json_to_csv(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert {"name", "age"} <= set(rows[0].keys())


def test_csv_to_json_roundtrip(tmp_path: Path):
    src = tmp_path / "people.csv"
    dst = tmp_path / "people.json"
    data = [
        {"name": "Alice", "age": "22"},
        {"name": "Bob", "age": "25"},
    ]
    with open(src, "w", newline="", encoding="utf-8") as f:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    csv_to_json(str(src), str(dst))
    with dst.open(encoding="utf-8") as f:
        rows = json.load(f)
    assert len(rows) == 2


@pytest.mark.parametrize(
    "function, input_file, error",
    [
        (json_to_csv, "people.json", ValueError),
    ],
)
def test_error_handling(function, input_file, error, tmp_path: Path):
    file_path = tmp_path / input_file
    file_path.write_text("Error???", encoding="utf-8")
    dst = tmp_path / "people.csv"
    f = json_to_csv if function is json_to_csv else csv_to_json
    with pytest.raises(error):
        f(str(file_path), str(dst))
```

## test_text
```python
import sys
import pytest

sys.path.append("C:/Users/lazar/Desktop/python_labs")

from text_stats import normalize, tokenize, count_freq, top_n


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
        ("", ""),
        ("   ", ""),
    ],
)
def test_normalize(source, expected):
    assert normalize(source) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("привет мир", ["привет", "мир"]),
        ("hello world test", ["hello", "world", "test"]),
        ("", []),
        ("   ", []),
        ("знаки, препинания! тест.", ["знаки", "препинания", "тест"]),
    ],
)
def test_tokenize(text, expected):
    assert tokenize(text) == expected


def test_count_freq_basic():
    tokens = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    result = count_freq(tokens)
    expected = {"apple": 3, "banana": 2, "cherry": 1}
    assert result == expected


def test_count_freq_empty():
    assert count_freq([]) == {}


def test_top_n_basic():
    freq = {"apple": 5, "banana": 3, "cherry": 7, "date": 1}
    result = top_n(freq, 2)
    expected = [("cherry", 7), ("apple", 5)]
    assert result == expected


def test_top_n_tie_breaker():
    freq = {"banana": 3, "apple": 3, "cherry": 3}
    result = top_n(freq, 3)
    expected = [("apple", 3), ("banana", 3), ("cherry", 3)]
    assert result == expected


def test_top_n_empty():
    assert top_n({}, 5) == []


def test_full_pipeline():
    text = "Привет мир! Привет всем. Мир прекрасен."
    normalized = normalize(text)
    tokens = tokenize(normalized)
    freq = count_freq(tokens)
    top_words = top_n(freq, 2)

    assert normalized == "привет мир! привет всем. мир прекрасен."
    assert tokens == [
        "привет",
        "мир",
        "привет",
        "всем",
        "мир",
        "прекрасен",
    ]
    assert freq == {"привет": 2, "мир": 2, "всем": 1, "прекрасен": 1}
    assert top_words == [("мир", 2), ("привет", 2)]
```
## результат
![результат](./images/lab07/testik.png)


# Лабораторная работа №8
## Models
```python
dataclasses import dataclass
from datetime import date, datetime


DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    @staticmethod
    def _validate_birthdate(value: str) -> date:
        try:
            return datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(
                f"Некорректный формат даты '{value}'. Ожидается {DATE_FORMAT}"
            )

    @staticmethod
    def _validate_gpa(value: float) -> float:
        try:
            gpa_value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Средний балл должен быть числом")

        if not 0 <= gpa_value <= 5:
            raise ValueError("Средний балл должен быть в диапазоне от 0 до 5")
        return gpa_value

    def __post_init__(self) -> None:
        self._birthdate_dt = self._validate_birthdate(self.birthdate)
        self.gpa = self._validate_gpa(self.gpa)

    def age(self) -> int:
        today = date.today()
        years = today.year - self._birthdate_dt.year
        if (today.month, today.day) < (
            self._birthdate_dt.month,
            self._birthdate_dt.day,
        ):
            years -= 1
        return years

    def to_dict(self):
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            fio=data["fio"],
            birthdate=data["birthdate"],
            group=data["group"],
            gpa=data["gpa"],
        )

    # @classmethod
    # def from_dict(data):
    #     return Student(
    #         fio=data["fio"],
    #         birthdate=data["birthdate"],
    #         group=data["group"],
    #         gpa=data["gpa"],
    #     )

    def __str__(self) -> str:
        return f"{self.fio} ({self.group}), {self.age()} лет, GPA {self.gpa:.2f}"
```
## SerSialize
```python
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
```
## стиль
![стиль](./images/lab08/blackk.png)

![](./images/lab08/result.png)

# Лабораторная работа №1

## Задание 1
![Приветствие](./images/lab01/01.png)

## Задание 2
![Вещественные числа](./images/lab01/02.png)

## Задание 3
![Скидки](./images/lab01/03.png)

## Задание 4
![ЧЧ:ММ делала как целочисленное деление на 60 и остаток от деления на 60](./images/lab01/04.png)

## Задание 5
![Средний код, но работает хорошо](./images/lab01/05.png)


# Лабораторная работа №2
## Задание A

```python
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        return ValueError
    return(min(nums), max(nums))
print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
print(min_max([]))
print(min_max([1.5, 2, 2.0, -3.1]))
```
![min_max](./images/lab02/min_max.png)
```python
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(set(nums))
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
```
![unique_sorted](./images/lab02/unique_sorted.png)
```python
def flatten(mat: list[list | tuple]) -> list:
    result = []
    for r in mat:
        if not isinstance(r, (list, tuple)):
            return TypeError
        result.extend(r)
    return result
print(flatten([[1,2], [3,4]]))
print(flatten([[1,2], (3, 4, 5)]))
print(flatten([[1], [], [2, 3]]))
print(flatten([[1, 2], "ab"]))
```
![flatten](./images/lab02/flatten.png)
![тест](./images/lab02/ITOG1.png)

## Задание B

```python
def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    row_length = len(mat[0])
    for i, row in enumerate(mat):
        if len(row) != row_length:
            return ValueError
    result = []
    for cl in range(len(mat[0])):
        new_row = []
        for row in range(len(mat)):
            new_row.append(mat[row][cl])
        result.append(new_row)
    return result
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
print(transpose([[1, 2], [3]]))
```
![transpose](./images/lab02/transpose.png)
```python
def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    row_length = len(mat[0])
    for i, row in enumerate(mat):
        if len(row) != row_length:
            return ValueError
    result = []
    for row in mat:
        result.append(sum(row))
    return result
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
print(row_sums([[1, 2], [3]]))
```
![row_sums](./images/lab02/row_sums.png)
```python
def col_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    row_length = len(mat[0])
    for i, row in enumerate(mat):
        if len(row) != row_length:
            return ValueError
    result = []
    for col in range(len(mat[0])):
        col_sum = 0
        for row in range(len(mat)):
            col_sum += mat[row][col]
        result.append(col_sum)
    return result
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
print(col_sums([[1, 2], [3]]))
```
![col_sums](./images/lab02/col_sums.png)
![тест](./images/lab02/ITOG2.png)

## Задание C
```python
def format_record(rec: tuple[str, str, float]) -> str:
    fio, gr, gpa = rec
    fio2 = ' '.join(fio.split()).split()
    fam = fio2[0]

    ini = []
    for i in range(1, len(fio2)):
        if i <= 2:
            ini.append(f'{fio2[i][0]}.')
    res = f'{fam} {' '.join(ini)}, гр. {gr}, GPA {gpa:.2f}'
    return res
t = ("Иванов Иван Иванович", "BIVT-25", 4.6)
print(format_record(t))
```
![format_record](./images/lab02/fio.png)
![тест](./images/lab02/ITOG3.png)

# Лабораторная работа №3
## Задание A
``` python
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold == True:
        text = text.casefold()
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    text = ' '.join(text.split())
    text = text.strip()
    return text
print(normalize("ПрИвЕт\nМИр\t"))
print(normalize("ёжик, Ёлка"))
print(normalize("Hello\r\nWorld"))
print(normalize("  двойные   пробелы  "))
```
![norm](./images/lab03/normalize.png)

``` python
import re

def tokenize(text: str) -> list[str]:
    t = r'[\w]+(?:-[\w]+)*'
    l = re.findall(t, text, re.UNICODE)
    return l
print(tokenize("привет мир"))
print(tokenize("hello,world!!!"))
print(tokenize("по-настоящему круто"))
print(tokenize("2025 год"))
print(tokenize("emoji 😀 не слово"))
```
![token](./images/lab03/token.png)

``` python
def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}
    for i in tokens:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    items = []
    for word in freq:
        count = freq[word]
        items.append((word, count))
    items.sort(key=lambda i: (-i[1], i[0]))
    return items[:n]

print(count_freq(["a","b","a","c","b","a"]))
print(count_freq(["bb","aa","bb","aa","cc"]))
print(top_n(count_freq(["a","b","a","c","b","a"])))
print(top_n(count_freq(["bb","aa","bb","aa","cc"])))
```
![count_top](./images/lab03/count_top.png)
![ИТОГИ](./images/lab03/test.png)

## Задание B
``` python
import sys
import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    if casefold:
        text = text.casefold()
    text = ' '.join(text.split())
    text = text.strip()
    return text

def tokenize(text: str) -> list[str]:
    t = r'[\w]+(?:-[\w]+)*'
    l = re.findall(t, text, re.UNICODE)
    return l

def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}
    for i in tokens:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    items = []
    for word in freq:
        count = freq[word]
        items.append((word, count))
    items.sort(key=lambda i: (-i[1], i[0]))
    return items[:n]

a =  "Привет, мир! Привет!!!"

nt = normalize(a)
allwords = tokenize(nt)
uw = count_freq(allwords)
top = top_n(uw, 5)

print(f'Всего слов: {len(allwords)}')
print(f"Уникальных слов: {len(uw)}")
print("Топ-5:")
for y in top:
    print(y[0] + ': ' + str(y[1]))
```
![ИТОГИ](./images/lab03/text.png)


# Лабораторная работа #4
## Задание A
``` python
from pathlib import Path
from csv import writer
from text_stats import *

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    p = path
    with open(p, 'r', encoding=encoding) as f:
        temp = f.read()
        if not temp.strip():
            raise ValueError('FileNotFoundError')
        if encoding != "utf-8":
            raise ValueError('UnicodeDecodeError')
    return temp
print(read_text("C:/Users/lazar/Desktop/python_labs/lib/meow.txt"))

def write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None) -> None:
    with open(path, 'w', newline="", encoding='utf-8') as file:
        w= writer(file)
        if (header != None): w.writerows(header)
        w.writerows(rows)
print(count_freq(tokenize(normalize(read_text("C:/Users/lazar/Desktop/python_labs/lib/meow.txt")))).items())
```
## Задание B
``` python
from pathlib import Path
import csv
import argparse
from text_stats import normalize, tokenize, count_freq
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../lib'))

def read_csv_report(csv_file: str) -> None:
    input_path = Path(csv_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Ошибка: файл {csv_file} не существует")

    with open(input_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        word_counts = {}
        total_words = 0
        
        for row in reader:
            if len(row) >= 2:
                word = row[0]
                count = int(row[1])
                word_counts[word] = count
                total_words += count

    unique_words = len(word_counts)
    
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
    
    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    for i, (word, count) in enumerate(sorted_words[:5], 1):
        print(f"{i}. {word}: {count}")

def generate_csv_report(input_file: str, output_file: str) -> None:
    """Генерирует CSV отчет из текстового файла"""
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Ошибка: файл {input_file} не существует")
    
    # Читаем текстовый файл
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if not text.strip():
        print("Пустой файл — создаю CSV только с заголовком.")
        # Создаем пустой CSV с заголовком
        output_path = Path(output_file)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['word', 'count'])
        return

    # Обрабатываем текст
    norm_text = normalize(text)
    tokens = tokenize(norm_text)
    freqs = count_freq(tokens)
    
    # Сохраняем результат в CSV
    output_path = Path(output_file)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'count'])  # заголовок
        for word, count in freqs.items():
            writer.writerow([word, count])
    
    print(f"Отчет сохранен в: {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Чтение отчета из CSV файла')
    parser.add_argument('--csv', dest='csv_file', default='data/check.csv', help='Путь к CSV файлу с отчетом')
    # создает аргумент ArgumentParser


    args = parser.parse_args()
    # разбивает аргументы, переданные скрипту при запуске
    
    try:
        read_csv_report(args.csv_file)
    except Exception as error:
        print(error)
        exit(1)
```

# Лабораторная работа #5
## Js0n->SCV
``` python
import json
import csv
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл в CSV."""
    if Path(json_path).suffix != '.json' or Path(csv_path).suffix != '.csv':
        raise TypeError("Неверное расширение файла")
    
    with open(json_path, encoding="utf-8") as f: 
        data = json.load(f)
    
    if not data or not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    
    # Собираем все уникальные ключи из всех объектов
    fieldnames = sorted({key for item in data for key in item.keys()})
    
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        # Заполняем отсутствующие поля пустыми строками
        for item in data:
            row = {field: item.get(field, '') for field in fieldnames}
            writer.writerow(row)

def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV в JSON (список словарей)."""
    if Path(csv_path).suffix != '.csv' or Path(json_path).suffix != '.json':
        raise TypeError("Неверное расширение файла")
    
    with open(csv_path, 'r', encoding='utf-8', newline='') as cf:
        reader = csv.DictReader(cf)
        lt_rows = list(reader)
        
    if not lt_rows:
        raise ValueError("CSV файл пуст или содержит только заголовок")
    
    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump(lt_rows, jf, ensure_ascii=False, indent=2)

json_to_csv('C:\Users\lazar\Desktop\python_labs\data\samples\people.json', 'C:\Users\lazar\Desktop\python_labs\data\out\people_from_json.csv')
csv_to_json('C:\Users\lazar\Desktop\python_labs\data\samples\people.csv', 'C:\Users\lazar\Desktop\python_labs\data\out\people_from_csv.json')
```

## csv->xlsx
```python
from openpyxl import Workbook
import csv
from pathlib import Path

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """Конвертирует CSV в XLSX."""
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    
    try:
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            if not rows:
                raise ValueError("CSV файл пуст")
            
            for row in rows:
                ws.append(row)
            
            # Автоширина колонок
            for column in ws.columns:
                if column:  # Проверяем что колонка не пустая
                    mx = max(len(str(cell.value)) for cell in column)
                    ws.column_dimensions[column[0].column_letter].width = max(mx + 2, 8)
        
        wb.save(xlsx_path)
        
    except csv.Error as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")
    
csv_to_xlsx('C:\Users\lazar\Desktop\python_labs\data\samples\people.csv', 'C:\Users\lazar\Desktop\python_labs\data\out\people.xlsx')
```

# Лабораторная работа #6
## cli_text.py
``` python
import argparse
from text_stats import tokenize, count_freq, top_n


def main():
    parser = argparse.ArgumentParser(description="CLI‑утилиты лабораторной №6")
    subparsers = parser.add_subparsers(dest="command")

    # подкоманда cat - вывод файла
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True, help="путь к файлу")
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    # подкоманда stats - анализ
    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", required=True, help="путь к файлу")
    stats_parser.add_argument("--top", type=int, default=5, help="топ слов")

    args = parser.parse_args()

    if args.command == "cat":
        try:
            with open(args.input, encoding="utf-8") as f:
                # нумеруем с 1 в формате номер: строка
                for i, line in enumerate(f, start=1):
                    if args.n:
                        print(f"{i}: {line.rstrip()}")
                    else:
                        print(line.rstrip())
        except FileNotFoundError:
            parser.error("файл не найден")
        except Exception as e:
            parser.error("ошибка при чтении файла")

    #
    elif args.command == "stats":
        try:
            with open(args.input, encoding="utf-8") as f:
                text = f.read()
            tokens = tokenize(text)
            freqs = count_freq(tokens)
            for word, count in top_n(freqs, args.top):
                print(f"{word}: {count}")
        except FileNotFoundError:
            parser.error(f"Файл '{args.input}' не найден")
        except Exception as e:
            parser.error(f"Ошибка при анализе файла: {e}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

## cli_convert.py
``` python
import argparse
from pathlib import Path
from json_csv import json_to_csv, csv_to_json
from csv_xlsx import csv_to_xlsx  

def main():
    parser = argparse.ArgumentParser(description="Конвертер данных между форматами")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды конвертации")

    # JSON → CSV
    json_to_csv_parser = subparsers.add_parser("json_to_csv", help="Конвертировать JSON в CSV")
    json_to_csv_parser.add_argument("--in", dest="input", required=True, help="Входной JSON файл")
    json_to_csv_parser.add_argument("--out", dest="output", required=True, help="Выходной CSV файл")

    # CSV → JSON
    csv_to_json_parser = subparsers.add_parser("csv_to_json", help="Конвертировать CSV в JSON")
    csv_to_json_parser.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    csv_to_json_parser.add_argument("--out", dest="output", required=True, help="Выходной JSON файл")

    # CSV → XLSX
    csv_to_xlsx_parser = subparsers.add_parser("csv_to_xlsx", help="Конвертировать CSV в XLSX")
    csv_to_xlsx_parser.add_argument("--in", dest="input", required=True, help="Входной CSV файл")
    csv_to_xlsx_parser.add_argument("--out", dest="output", required=True, help="Выходной XLSX файл")

    args = parser.parse_args()

    if args.command == "json_to_csv":
        json_to_csv(json_path=args.input, csv_path=args.output)

    elif args.command == "csv_to_json":
        csv_to_json(csv_path=args.input, json_path=args.output)

    elif args.command == "csv_to_xlsx":
        csv_to_xlsx(csv_path=args.input, xlsx_path=args.output)

if __name__ == "__main__":
    main()
```