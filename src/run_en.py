# src/run_en.py
import sys
from src.en_parser import analyze_en_sentence

def main():
    if len(sys.argv) < 2:
        print("Uso: python -m src.run_en \"frase\"")
        print("     python -m src.run_en -f archivo.txt")
        return

    # MODO ARCHIVO
    if sys.argv[1] == "-f" and len(sys.argv) == 3:
        path = sys.argv[2]
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    sent = line.strip()
                    if not sent: continue
                    
                    result = analyze_en_sentence(sent)
                    status = "OK" if result.ok else "ERROR"
                    print(f"[{status}] {sent}")
                    
                    if not result.ok:
                        for msg in result.messages:
                            print(f"   -> {msg}")
        except FileNotFoundError:
            print("Archivo no encontrado")
        return

    # MODO ORACIÓN SIMPLE
    sentence = sys.argv[1]
    result = analyze_en_sentence(sentence)

    if result.ok:
        print("✔ Parsing successful.")
    else:
        print("✘ Errors found:")
        for i, msg in enumerate(result.messages, 1):
            print(f"  {i}. {msg}")

if __name__ == "__main__":
    main()