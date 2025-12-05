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
