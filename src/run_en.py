# src/run_en.py
# Script para probar el parser en inglés desde consola

import sys
from src.en_parser import analyze_en_sentence


def main():
    if len(sys.argv) == 2:
        # una oración como argumento
        sentence = sys.argv[1]
        result = analyze_en_sentence(sentence)
        if result.ok:
            print("✔", result.message)
        else:
            print("✘ Invalid sentence.")
            print("  Detail:", result.message)

    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        # archivo: una oración por línea
        path = sys.argv[2]
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                sent = line.strip()
                if not sent:
                    continue
                result = analyze_en_sentence(sent)
                status = "OK" if result.ok else "ERROR"
                print(f"[{status}] {sent}")
                if not result.ok:
                    print("   ->", result.message)
    else:
        print("Usage:")
        print('  python -m src.run_en "the dog eats the apple"')
        print("  python -m src.run_en -f path/to/file.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
