# Vocabulario reducido para inglés + tokenización
from dataclasses import dataclass

class LexicalError(Exception):
    pass

@dataclass
class Token:
    word: str   # Palabra original
    cat: str    # Categoría gramatical: DET, N, PRON, V, ADJ, PREP, AUX
    num: str    # Singular SG, Plural PL, ANY, Singular Contable SGC, No Contable UNC, Colectivo COLL
    pos: int    # Posición en la oración (1,2,3,...)


LEXICON = {
    # Elemento de sincronizacion
    ",":     ("COMMA", "ANY"),

    # Determinantes
    "the":   ("DET", "ANY"),
    "a":     ("DET", "SG"),
    "an":    ("DET", "SG"),
    "this":  ("DET", "SG"),
    "that":  ("DET", "SG"),
    "these": ("DET", "PL"),
    "those": ("DET", "PL"),

    # Pronombres
    "i":     ("PRON", "PL"),
    "you":   ("PRON", "PL"),
    "we":    ("PRON", "PL"),
    "they":  ("PRON", "PL"),
    "he":    ("PRON", "SG"),
    "she":   ("PRON", "SG"),
    "it":    ("PRON", "SG"),

    # Nombres | Clasificados por singular, plural, contable, no contable, etc
    "time":      ("N", "UNC"),
    "year":      ("N", "SGC"),
    "people":    ("N", "PL"),
    "day":       ("N", "SGC"),
    "man":       ("N", "SGC"),
    "men":       ("N", "PL"),
    "woman":     ("N", "SGC"),
    "women":     ("N", "PL"),
    "child":     ("N", "SGC"),
    "children":  ("N", "PL"),
    "world":     ("N", "SGC"),
    "school":    ("N", "SGC"),
    "state":     ("N", "SGC"),
    "family":    ("N", "COLL"),
    "student":   ("N", "SGC"),
    "students":  ("N", "PL"),
    "group":     ("N", "COLL"),
    "country":   ("N", "SGC"),
    "problem":   ("N", "SGC"),
    "hand":      ("N", "SGC"),
    "part":      ("N", "SGC"),
    "place":     ("N", "SGC"),
    "case":      ("N", "SGC"),
    "company":   ("N", "SGC"),
    "system":    ("N", "SGC"),
    "program":   ("N", "SGC"),
    "question":  ("N", "SGC"),
    "work":      ("N", "UNC"),
    "number":    ("N", "SGC"),
    "night":     ("N", "SGC"),
    "home":      ("N", "SGC"),
    "room":      ("N", "SGC"),
    "fact":      ("N", "SGC"),
    "water":     ("N", "UNC"),
    "car":       ("N", "SGC"),
    "cars":      ("N", "PL"),
    "house":     ("N", "SGC"),
    "houses":    ("N", "PL"),
    "friend":    ("N", "SGC"),
    "friends":   ("N", "PL"),
    "father":    ("N", "SGC"),
    "mother":    ("N", "SGC"),
    "boy":       ("N", "SGC"),
    "boys":      ("N", "PL"),
    "girl":      ("N", "SGC"),
    "girls":     ("N", "PL"),
    "apple":     ("N", "SGC"),
    "apples":    ("N", "PL"),
    "book":      ("N", "SGC"),
    "books":     ("N", "PL"),
    "city":      ("N", "SGC"),
    "cities":    ("N", "PL"),
    "job":       ("N", "SGC"),
    "jobs":      ("N", "PL"),
    "money":     ("N", "UNC"),
    "story":     ("N", "SGC"),
    "stories":   ("N", "PL"),
    "childhood": ("N", "UNC"),
    "food":      ("N", "UNC"),
    "door":      ("N", "SGC"),
    "table":     ("N", "SGC"),
    "dog":      ("N", "SGC"),
    "cat":      ("N", "SGC"),
    "student":  ("N", "SGC"),
    "teacher":  ("N", "SGC"),
    "apple":    ("N", "SGC"),
    "book":     ("N", "SGC"),
    "ball":     ("N", "SGC"),   
    "car":      ("N", "SGC"),
    "boy":      ("N", "SGC"),
    "girl":     ("N", "SGC"),
    "dogs":     ("N", "PL"),
    "cats":     ("N", "PL"),
    "students": ("N", "PL"),
    "teachers": ("N", "PL"),
    "apples":   ("N", "PL"),
    "books":    ("N", "PL"),
    "cars":     ("N", "PL"),
    "boys":     ("N", "PL"),
    "girls":    ("N", "PL"),

    # Verbos en presente simple

    # be (irregular, presente)
    "am":   ("V", "PL"),
    "are":  ("V", "PL"),
    "is":   ("V", "SG"),

    # have
    "have": ("V", "PL"),
    "has":  ("V", "SG"),

    # do
    "do":   ("V", "PL"),
    "does": ("V", "SG"),

    "read":   ("V", "PL"), "reads":  ("V", "SG"),
    "drink":  ("V", "PL"), "drinks": ("V", "SG"),
    "go":   ("V", "PL"), "goes": ("V", "SG"),
    "say":  ("V", "PL"), "says": ("V", "SG"),
    "get":  ("V", "PL"), "gets": ("V", "SG"),
    "make": ("V", "PL"), "makes":("V", "SG"),
    "know": ("V", "PL"), "knows":("V", "SG"),
    "think": ("V", "PL"), "thinks":("V", "SG"),
    "take":  ("V", "PL"), "takes": ("V", "SG"),
    "see":   ("V", "PL"), "sees":  ("V", "SG"),
    "come":  ("V", "PL"), "comes": ("V", "SG"),
    "want":  ("V", "PL"), "wants": ("V", "SG"),
    "use":   ("V", "PL"), "uses":  ("V", "SG"),
    "find":  ("V", "PL"), "finds": ("V", "SG"),
    "give":  ("V", "PL"), "gives": ("V", "SG"),
    "tell":  ("V", "PL"), "tells": ("V", "SG"),
    "work":  ("V", "PL"), "works": ("V", "SG"),
    "call":  ("V", "PL"), "calls": ("V", "SG"),
    "try":   ("V", "PL"), "tries": ("V", "SG"),
    "ask":   ("V", "PL"), "asks":  ("V", "SG"),
    "need":  ("V", "PL"), "needs": ("V", "SG"),
    "feel":  ("V", "PL"), "feels": ("V", "SG"),
    "become":  ("V", "PL"), "becomes": ("V", "SG"),
    "leave": ("V", "PL"), "leaves":("V", "SG"),
    "put":  ("V", "PL"), "puts": ("V", "SG"),
    "mean":  ("V", "PL"), "means": ("V", "SG"),
    "keep":  ("V", "PL"), "keeps": ("V", "SG"),
    "let":   ("V", "PL"), "lets":  ("V", "SG"),
    "begin":  ("V", "PL"), "begins": ("V", "SG"),
    "seem":  ("V", "PL"), "seems": ("V", "SG"),
    "help":  ("V", "PL"), "helps": ("V", "SG"),
    "talk":  ("V", "PL"), "talks": ("V", "SG"),
    "turn":  ("V", "PL"), "turns": ("V", "SG"),
    "start": ("V", "PL"), "starts":("V", "SG"),
    "show":  ("V", "PL"), "shows": ("V", "SG"),
    "hear":  ("V", "PL"), "hears": ("V", "SG"),
    "play":  ("V", "PL"), "plays": ("V", "SG"),
    "run":   ("V", "PL"), "runs":  ("V", "SG"),
    "move":  ("V", "PL"), "moves": ("V", "SG"),
    "like":  ("V", "PL"), "likes": ("V", "SG"),
    "live":  ("V", "PL"), "lives": ("V", "SG"),
    "believe": ("V", "PL"), "believes":("V", "SG"),
    "hold":  ("V", "PL"), "holds": ("V", "SG"),
    "bring": ("V", "PL"), "brings":("V", "SG"),
    "happen": ("V", "PL"), "happens":("V", "SG"),
    "write": ("V", "PL"), "writes":("V", "SG"),
    "provide": ("V", "PL"), "provides":("V", "SG"),
    "sit":   ("V", "PL"), "sits":  ("V", "SG"),
    "stand": ("V", "PL"), "stands":("V", "SG"),
    "lose":  ("V", "PL"), "loses": ("V", "SG"),
    "pay":   ("V", "PL"), "pays":  ("V", "SG"),
    "meet":  ("V", "PL"), "meets": ("V", "SG"),
    "include": ("V", "PL"), "includes":("V", "SG"),
    "continue": ("V", "PL"), "continues":("V", "SG"),
    "learn": ("V", "PL"), "learns":("V", "SG"),
    "change": ("V", "PL"), "changes":("V", "SG"),
    "understand": ("V", "PL"), "understands":("V", "SG"),
    "watch": ("V", "PL"), "watches":("V", "SG"),
    "stop":  ("V", "PL"), "stops": ("V", "SG"),
    "create": ("V", "PL"), "creates":("V", "SG"),
    "eat":    ("V", "PL"), "eats":   ("V", "SG"),

    # Auxiliares| modales, presente simple
    "can":  ("AUX", "ANY"),
    "may":  ("AUX", "ANY"),
    "must": ("AUX", "ANY"),

    # Adjetivos
    "other":     ("ADJ", "ANY"), "new":       ("ADJ", "ANY"),
    "good":      ("ADJ", "ANY"), "high":      ("ADJ", "ANY"),
    "old":       ("ADJ", "ANY"), "great":     ("ADJ", "ANY"),
    "big":       ("ADJ", "ANY"), "small":     ("ADJ", "ANY"),
    "large":     ("ADJ", "ANY"), "young":     ("ADJ", "ANY"),
    "different": ("ADJ", "ANY"), "long":      ("ADJ", "ANY"),
    "little":    ("ADJ", "ANY"), "important": ("ADJ", "ANY"),
    "bad":       ("ADJ", "ANY"), "right":     ("ADJ", "ANY"),
    "early":     ("ADJ", "ANY"), "able":      ("ADJ", "ANY"),
    "happy":     ("ADJ", "ANY"), "sad":       ("ADJ", "ANY"),
    "black":     ("ADJ", "ANY"), "white":     ("ADJ", "ANY"),
    "real":      ("ADJ", "ANY"), "best":      ("ADJ", "ANY"),
    "public":    ("ADJ", "ANY"), "sure":      ("ADJ", "ANY"),
    "low":       ("ADJ", "ANY"), "local":     ("ADJ", "ANY"),
    "late":      ("ADJ", "ANY"), "human":     ("ADJ", "ANY"),
    "strong":    ("ADJ", "ANY"), "weak":      ("ADJ", "ANY"),
    "beautiful": ("ADJ", "ANY"), "ugly":      ("ADJ", "ANY"),
    "easy":      ("ADJ", "ANY"), "difficult": ("ADJ", "ANY"),
    "hot":       ("ADJ", "ANY"), "cold":      ("ADJ", "ANY"),
    "fast":      ("ADJ", "ANY"), "slow":      ("ADJ", "ANY"),
    "busy":      ("ADJ", "ANY"), "free":      ("ADJ", "ANY"),
    "clean":     ("ADJ", "ANY"), "dirty":     ("ADJ", "ANY"),
    "full":      ("ADJ", "ANY"), "empty":     ("ADJ", "ANY"),

    # Preposiciones
    "in":    ("PREP", "ANY"), "on":    ("PREP", "ANY"),
    "under": ("PREP", "ANY"), "with":  ("PREP", "ANY"),
    "near":  ("PREP", "ANY"), "from":  ("PREP", "ANY"),
    "to":    ("PREP", "ANY"), "at":    ("PREP", "ANY"),
    "for":   ("PREP", "ANY"),
}

def tokenize_sentence(sentence: str):
    """
    Recibe una oración en inglés y devuelve lista de Tokens.
    Llama a LexicalError si encuentra una palabra desconocida.
    """
    # Separar comas para que sean tokens independientes
    processed_sentence = sentence.replace(",", " , ")
    words = processed_sentence.strip().lower().split()
    tokens = []

    for i, w in enumerate(words, start=1):
        # Quitamos puntuación simple excepto la coma
        clean = w.strip(".!?")
        if not clean:
            continue # Palabra vacía tras limpiar la puntuación

        entry = LEXICON.get(clean)
        if entry is None:
            raise LexicalError(f"Unknown word '{clean}' at position {i}")

        cat, num = entry
        tokens.append(Token(word=clean, cat=cat, num=num, pos=i))

    return tokens