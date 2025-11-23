# src/en_lexicon.py
# Vocabulario reducido para inglés + tokenización

from dataclasses import dataclass

class LexicalError(Exception):
    pass


@dataclass
class Token:
    word: str   # palabra original
    cat: str    # categoría gramatical: DET, N, PRON, V
    num: str    # número: SG (singular), PL (plural), ANY
    pos: int    # posición en la oración (1,2,3,...)


# Léxico: palabra -> (categoría, número)
LEXICON = {
    # Determiners
    "the":   ("DET", "ANY"),
    "a":     ("DET", "SG"),
    "an":    ("DET", "SG"),
    "this":  ("DET", "SG"),
    "that":  ("DET", "SG"),
    "these": ("DET", "PL"),
    "those": ("DET", "PL"),

    # Nouns (singular / plural)
    "dog":      ("N", "SG"),
    "dogs":     ("N", "PL"),
    "cat":      ("N", "SG"),
    "cats":     ("N", "PL"),
    "student":  ("N", "SG"),
    "students": ("N", "PL"),
    "teacher":  ("N", "SG"),
    "teachers": ("N", "PL"),
    "boy":      ("N", "SG"),
    "boys":     ("N", "PL"),
    "girl":     ("N", "SG"),
    "girls":    ("N", "PL"),
    "apple":    ("N", "SG"),
    "apples":   ("N", "PL"),
    "book":     ("N", "SG"),
    "books":    ("N", "PL"),
    "car":      ("N", "SG"),
    "cars":     ("N", "PL"),

    # Pronouns (solo sujeto)
    "he":   ("PRON", "SG"),
    "she":  ("PRON", "SG"),
    "it":   ("PRON", "SG"),
    "they": ("PRON", "PL"),
    "we":   ("PRON", "PL"),

    # Verbs present simple (3rd sg / plural-base)
    "eats":   ("V", "SG"),
    "eat":    ("V", "PL"),
    "runs":   ("V", "SG"),
    "run":    ("V", "PL"),
    "likes":  ("V", "SG"),
    "like":   ("V", "PL"),
    "sees":   ("V", "SG"),
    "see":    ("V", "PL"),
    "reads":  ("V", "SG"),
    "read":   ("V", "PL"),
    "plays":  ("V", "SG"),
    "play":   ("V", "PL"),
    "drinks": ("V", "SG"),
    "drink":  ("V", "PL"),
    "opens":  ("V", "SG"),
    "open":   ("V", "PL"),
    "closes": ("V", "SG"),
    "close":  ("V", "PL"),
}


def tokenize_sentence(sentence: str):
    """
    Recibe una oración en inglés y devuelve una lista de Token.
    Lanza LexicalError si encuentra una palabra desconocida.
    Ignora signos simples de puntuación al final de la palabra.
    """
    words = sentence.strip().lower().split()
    tokens = []

    for i, w in enumerate(words, start=1):
        # quitar puntuación simple: .,!? al inicio y final
        clean = w.strip(".,!?")
        if not clean:
            continue # palabra vacía tras limpiar puntuación

        entry = LEXICON.get(clean)
        if entry is None:
            raise LexicalError(f"Unknown word '{clean}' at position {i}")

        cat, num = entry
        tokens.append(Token(word=clean, cat=cat, num=num, pos=i))

    return tokens
