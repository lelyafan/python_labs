testcase1 = "ПрИвЕт\nМИр\t"
testcase2 = "ёжик, Ёлка"
testcase3 = "Hello\r\nWorld"
testcase4 = "  двойные   пробелы  "
import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if casefold:
        text = text.casefold()
    if yo2e:
        text = text.replace("ё", "e")
    return text


print(normalize(testcase1))
print(normalize(testcase2))
print(normalize(testcase3))
print(normalize(testcase4))


testcase2 = "hello,world!!!"
testcase3 = "по-настоящему круто"
testcase4 = "2025 год"
testcase5 = "emoji 😀 не слово"

import re


def tokenize(text: str) -> list[str]:
    shablon = r"\w+(?:-\w+)*"
    tockens = re.findall(shablon, normalize(text))
    return tockens


print(tokenize(testcase1))
print(tokenize(testcase2))
print(tokenize(testcase3))
print(tokenize(testcase4))
print(tokenize(testcase5))

testcase1 = ["a", "b", "a", "c", "b", "a"]
testcase2 = ["bb", "aa", "bb", "aa", "cc"]


def count_freq(tokens: list[str]) -> dict[str, int]:
    fdict = {}
    for token in tokens:
        if token in fdict:
            fdict[token] += 1
        else:
            fdict[token] = 1
    return fdict


def top_n(freq: dict[str, int], n: int = 2) -> list[tuple[str, int]]:
    items = list(freq.items())
    sorted_items = sorted(items, key=lambda x: (-x[1], x[0]))
    return sorted_items[:n]


print(count_freq(testcase1))
print(top_n(count_freq(testcase1)))
print(count_freq(testcase2))
print(top_n(count_freq(testcase2)))
