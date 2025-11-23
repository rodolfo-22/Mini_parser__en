# src/en_parser.py
#
# Gramática:
#   S      -> NP VP
#   NP     -> DET N | PRON
#   VP     -> V OptObj
#   OptObj -> NP | ε
#
# Validaciones extra:
#   - Concordancia sujeto–verbo en número (SG / PL).
#   - Concordancia determinante–sustantivo en número.

from dataclasses import dataclass
from src.en_lexicon import Token, tokenize_sentence, LexicalError


class ParseError(Exception):
    pass


@dataclass
class ParseResult:
    ok: bool
    message: str


class RDEnParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0  # índice del token actual

    # --------- utilidades ---------

    def current(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def accept(self, expected_cat: str) -> Token:
        tok = self.current()
        if tok is None:
            raise ParseError(
                f"Expected {expected_cat}, but reached end of sentence. "
                f"Probably missing a {expected_cat} at the end."
            )

        if tok.cat != expected_cat:
            raise ParseError(
                f"Expected {expected_cat}, found {tok.cat} ('{tok.word}') at position {tok.pos}."
            )

        self.i += 1
        return tok

    # --------- reglas de la gramática ---------

    def parse(self) -> ParseResult:
        try:
            subj_num = self.S()  # símbolo inicial
            if self.current() is not None:
                tok = self.current()
                raise ParseError(
                    f"Extra input after a valid sentence: '{tok.word}' at position {tok.pos}."
                )
            return ParseResult(True, "Valid English sentence according to the grammar.")
        except (ParseError, LexicalError) as e:
            return ParseResult(False, str(e))

    def S(self) -> str:
        """
        S -> NP VP
        Devuelve el número del sujeto (SG/PL).
        """
        subj_num = self.NP()
        self.VP(expected_subj_num=subj_num)
        return subj_num

    def NP(self) -> str:
        """
        NP -> DET N | PRON
        Devuelve el número del sintagma nominal.
        """
        tok = self.current()
        if tok is None:
            raise ParseError("Expected a noun phrase (NP), but reached end of sentence.")

        if tok.cat == "PRON":
            pron = self.accept("PRON")
            # número del pronombre (he=SG, they=PL, etc.)
            return pron.num

        if tok.cat == "DET":
            det = self.accept("DET")
            noun = self.accept("N")

            # Concordancia DET–N en número
            if det.num != "ANY" and det.num != noun.num:
                raise ParseError(
                    f"Determiner–noun agreement error: determiner '{det.word}' "
                    f"({det.num}) with noun '{noun.word}' ({noun.num}) at position {noun.pos}."
                )

            return noun.num

        raise ParseError(
            f"Expected a determiner or pronoun to start NP, "
            f"found {tok.cat} ('{tok.word}') at position {tok.pos}."
        )

    def VP(self, expected_subj_num: str):
        """
        VP -> V OptObj
        Verifica concordancia sujeto–verbo en número.
        """
        verb = self.accept("V")

        # Concordancia sujeto–verbo
        if verb.num != expected_subj_num:
            raise ParseError(
                f"Subject–verb agreement error: subject is {expected_subj_num}, "
                f"but verb '{verb.word}' is {verb.num} (position {verb.pos})."
            )

        # Objeto opcional
        tok = self.current()
        if tok is not None and tok.cat in ("DET", "PRON"):
            self.NP()
        # Si no hay NP, producción ε (intransitivo)

# --------- Función de alto nivel ---------


def analyze_en_sentence(sentence: str) -> ParseResult:
    try:
        tokens = tokenize_sentence(sentence)
    except LexicalError as e:
        return ParseResult(False, f"Lexical error: {e}")

    parser = RDEnParser(tokens)
    return parser.parse()
