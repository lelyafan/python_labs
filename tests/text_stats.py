import sys
import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
    if casefold:
        text = text.casefold()
    text = " ".join(text.split())
    text = text.strip()
    return text


def tokenize(text: str) -> list[str]:
    t = r"[\w]+(?:-[\w]+)*"
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


a = "Привет, мир! Привет!!!"

nt = normalize(a)
allwords = tokenize(nt)
uw = count_freq(allwords)
top = top_n(uw, 5)

print(f"Всего слов: {len(allwords)}")
print(f"Уникальных слов: {len(uw)}")
print("Топ-5:")
for y in top:
    print(y[0] + ": " + str(y[1]))
