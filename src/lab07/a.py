import pytest
from text import normalize, tokenize, count_freq, top_n


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
    ],
)
def test_normalize_basic(source, expected):
    assert normalize(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        ("привет мир", ["привет", "мир"]),  # обычный текст
        ("один два два", ["один", "два", "два"]),  # повторы
        ("", []),  # пустая строка
        ("   много   пробелов   ", ["много", "пробелов"]),  # лишние пробелы
    ],
)
def test_tokenize_basic(source, expected):
    tokens = tokenize(source)
    assert tokens == expected


def test_count_freq_and_top_n():
    # базовый и граничный сценарий сразу:
    # нормализуем текст, токенизируем, считаем частоты и берём top_n
    text = "Кот кот собака кот птица собака"
    norm = normalize(text)
    tokens = tokenize(norm)
    freq = count_freq(tokens)

    # частоты слов
    assert freq == {"кот": 3, "собака": 2, "птица": 1}

    # top_n по убыванию частоты
    top2 = top_n(freq, 2)
    assert top2 == [("кот", 3), ("собака", 2)]


def test_top_n_tie_breaker():
    # одинаковая частота -> сортировка по алфавиту
    freq = {"beta": 2, "alpha": 2, "gamma": 2}

    result = top_n(freq, 3)

    # ожидаем алфавитный порядок при равных значениях
    assert result == [
        ("alpha", 2),
        ("beta", 2),
        ("gamma", 2),
    ]
