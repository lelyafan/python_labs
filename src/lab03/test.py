def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold == True:
        text = text.casefold()
    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
    text = " ".join(text.split())
    text = text.strip()
    return text


print(normalize("ПрИвЕт\nМИр\t"))
print(normalize("ёжик, Ёлка"))
print(normalize("Hello\r\nWorld"))
print(normalize("  двойные   пробелы  "))

import re


def tokenize(text: str) -> list[str]:
    t = r"[\w]+(?:-[\w]+)*"
    l = re.findall(t, text, re.UNICODE)
    return l


print(tokenize("привет мир"))
print(tokenize("hello,world!!!"))
print(tokenize("по-настоящему круто"))
print(tokenize("2025 год"))
print(tokenize("emoji 😀 не слово"))


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


print(count_freq(["a", "b", "a", "c", "b", "a"]))
print(count_freq(["bb", "aa", "bb", "aa", "cc"]))
print(top_n(count_freq(["a", "b", "a", "c", "b", "a"])))
print(top_n(count_freq(["bb", "aa", "bb", "aa", "cc"])))
