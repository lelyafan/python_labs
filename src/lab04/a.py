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
    p = Path(path)
    if p.suffix.lower() != ".csv":
        raise ValueError
    
    with open(path, 'w', newline="", encoding='utf-8') as file:
        w= writer(file)
        if (header != None): w.writerows(header)
        w.writerows(rows)
print(count_freq(tokenize(normalize(read_text("C:/Users/lazar/Desktop/python_labs/lib/meow.txt")))).items())