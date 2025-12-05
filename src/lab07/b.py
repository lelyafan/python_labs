import csv
import json
from pathlib import Path
import pytest
from json_csv import json_to_csv, csv_to_json


def test_json_to_csv_roundtrip(tmp_path: Path):
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"

    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    # пишем JSON-файл
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # конвертация JSON -> CSV
    json_to_csv(str(src), str(dst))

    # читаем CSV обратно
    with dst.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    # количество записей
    assert len(rows) == 2
    # набор заголовков/ключей
    assert {"name", "age"} <= set(rows[0].keys())
    # значения (age может быть строкой — это ок для CSV)
    assert rows[0]["name"] == "Alice"
    assert rows[1]["name"] == "Bob"


def test_csv_to_json_roundtrip(tmp_path: Path):
    src = tmp_path / "people.csv"
    dst = tmp_path / "people.json"

    fieldnames = ["name", "age"]
    rows = [
        {"name": "Alice", "age": "22"},
        {"name": "Bob", "age": "25"},
    ]

    # пишем CSV-файл
    with src.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # конвертация CSV -> JSON
    csv_to_json(str(src), str(dst))

    # читаем JSON обратно
    text = dst.read_text(encoding="utf-8")
    data = json.loads(text)

    # это должен быть список словарей
    assert isinstance(data, list)
    assert len(data) == 2
    # набор ключей
    assert {"name", "age"} <= set(data[0].keys())
    # значения (возраст может быть либо строкой, либо числом — нормализуем через int)
    assert data[0]["name"] == "Alice"
    assert int(data[0]["age"]) == 22
    assert data[1]["name"] == "Bob"
    assert int(data[1]["age"]) == 25


# ---------- Негативные сценарии ----------


def test_json_to_csv_empty_file(tmp_path: Path):
    src = tmp_path / "empty.json"
    dst = tmp_path / "out.csv"

    # пустой файл
    src.write_text("", encoding="utf-8")

    # по заданию: пустой/некорректный файл -> ValueError
    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_json_to_csv_invalid_json(tmp_path: Path):
    src = tmp_path / "bad.json"
    dst = tmp_path / "out.csv"

    # заведомо некорректный JSON
    src.write_text("НЕ json", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_csv_to_json_empty_file(tmp_path: Path):
    src = tmp_path / "empty.csv"
    dst = tmp_path / "out.json"

    # пустой CSV
    src.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


@pytest.mark.parametrize(
    "func, src_name, dst_name",
    [
        (json_to_csv, "missing.json", "out.csv"),
        (csv_to_json, "missing.csv", "out.json"),
    ],
)
def test_conversion_missing_file(tmp_path: Path, func, src_name: str, dst_name: str):
    # файл-источник не существует
    src = tmp_path / src_name  # не создаём
    dst = tmp_path / dst_name

    with pytest.raises(FileNotFoundError):
        func(str(src), str(dst))
