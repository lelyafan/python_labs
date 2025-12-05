testcase1 = "ПрИвЕт\nМИр\t"
testcase2 = "ёжик, Ёлка"
testcase3 = "Hello\r\nWorld"
testcase4 = "  двойные   пробелы  "


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if not text:
        return ""
    text = re.sub(r"[^a-zA-Zа-яА-ЯёЁ\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if casefold:
        text = text.lower()
    if yo2e:
        text = text.replace("ё", "е")

    return text


# print(normalize(testcase1))
# print(normalize(testcase2))
# print(normalize(testcase3))
# print(normalize(testcase4))

testcase1 = "привет мир"
testcase2 = "hello,world!!!"
testcase3 = "по-настоящему круто"
testcase4 = "2025 год"
testcase5 = "emoji 😀 не слово"
import re


def tokenize(text: str) -> list[str]:
    shablon = r"\w+(?:-\w+)*"
    # ищет все по шаблону из норм текста
    tockens = re.findall(shablon, normalize(text))
    return tockens


# print(tokenize(testcase1))
# print(tokenize(testcase2))
# print(tokenize(testcase3))
# print(tokenize(testcase4))
# print(tokenize(testcase5))


testcase1 = ["a", "b", "a", "c", "b", "a"]
testcase2 = ["bb", "aa", "bb", "aa", "cc"]


# from collections import*
def count_freq(tokens: list[str]) -> dict[str, int]:
    fdict = {}
    # создаем словарь
    for token in tokens:
        # если в словаре есть например 'а' то счетчик "a" увеличивается
        if token in fdict:
            fdict[token] += 1
        else:
            fdict[token] = 1
    return fdict


# УЖЕ ПОСЛЕ СОЗДАНИЯ СЛОВАРЯ ИЗ ЭЛЕМЕНТОВ
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    # превращем в представление словаря в списке
    items = list(freq.items())

    # Сортируем сначала по убыванию частоты, потом по алф
    sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))

    # Возвращаем первые N элементов
    return sorted_items[:n]


# print(count_freq(testcase1))
# print(top_n(count_freq(testcase1)))
# print(count_freq(testcase2))
# print(top_n(count_freq(testcase2)))
