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