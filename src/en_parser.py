# Gramática:
# VERIFICAR ESTA GRAMATICA, NO ESTOY SEGURO SI ES LA ULTIMA ACTUALIZADA
#   S        -> NP VP
#
#   NP       -> PRON | DET AdjList N PPList | N PPList
#
#       AdjList  -> ADJ AdjList | ε
#       PPList   -> PP PPList | ε
#       PP       -> PREP NP
#
#   VP       -> AuxList V VPBody
#       AuxList  -> AUX AuxList | ε
#
#       VPBody   -> NP PPList | PPList | ε
#
#   - Solo cuando Noun ∈ {PL, UNC, COLL} pueden aparecer sin Determinante como NP.
#   - La verificación de sujeto–verbo se hace con SG/PL.
#   - Después del verbo se permiten:
#       V
#       V NP
#       V PP*
#       V NP PP*


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
        self.i = 0

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

    # Funciones para manejo de sustantivos
    def noun_agreement(self, noun: Token) -> str:
        """
        Indica si el nombre es Singular o Plural a partir del tipo de sustantivo:

          PL              -> "PL"
          SGC, UNC, COLL  -> "SG"
        """
        if noun.num == "PL":
            return "PL"
        # SGC Singular contable, UNC Incontable, COLL Colectivo
        return "SG"

    def noun_allows_bare(self, noun: Token) -> bool:
        """
        Devuelve True si el sustantivo puede aparecer sin determinante como NP.

        Permitimos:
          - Plurales:    PL        (Dogs bark.)
          - Incontables: UNC       (Water flows.)
          - Colectivos:  COLL      (Family goes...)
        No permitimos:
          - Singulares contables: SGC  (Book is on table) -> error
        """
        return noun.num in ("PL", "UNC", "COLL")

    
    # Reglas de la Gramática
    def parse(self) -> ParseResult:
        try:
            subj_num = self.S()  # Símbolo Inicial
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

    # --------- NP y sus partes ---------

    def NP(self) -> str:
        """
        NP -> PRON
            | DET AdjList N PPList
            | N PPList     (solo si N lo permite)
        Devuelve el número (SG/PL) del sintagma nominal para concordancia.
        """
        tok = self.current()
        if tok is None:
            raise ParseError("Expected a noun phrase (NP), but reached end of sentence.")

        # Caso PRON
        if tok.cat == "PRON":
            pron = self.accept("PRON")
            return pron.num

        # Caso DET AdjList N PPList
        if tok.cat == "DET":
            det = self.accept("DET")

            # Lista de adjetivos opcionales
            self.AdjList()

            # Sustantivo obligatorio
            noun = self.accept("N")
            noun_num = self.noun_agreement(noun)

            # Concordancia DET–N (en número lógico SG/PL)
            if det.num != "ANY" and det.num != noun_num:
                raise ParseError(
                    f"Determiner–noun agreement error: determiner '{det.word}' "
                    f"({det.num}) with noun '{noun.word}' ({noun.num}) at position {noun.pos}."
                )

            # Sintagmas preposicionales opcionales que modifican al nombre
            self.PPList()

            return noun_num

        # Caso N PPList (bare noun como sujeto/objeto)
        if tok.cat == "N":
            noun = self.accept("N")

            if not self.noun_allows_bare(noun):
                raise ParseError(
                    f"Singular count noun '{noun.word}' cannot appear bare as NP "
                    f"(position {noun.pos}); a determiner is required."
                )

            # Modificadores preposicionales opcionales
            self.PPList()

            return self.noun_agreement(noun)

        raise ParseError(
            f"Expected a determiner, pronoun or noun to start NP, "
            f"found {tok.cat} ('{tok.word}') at position {tok.pos}."
        )

    def AdjList(self):
        """
        AdjList -> ADJ AdjList | ε
        Consume cero o más adjetivos.
        """
        tok = self.current()
        while tok is not None and tok.cat == "ADJ":
            self.accept("ADJ")
            tok = self.current()

    def PPList(self):
        """
        PPList -> PP PPList | ε
        Consume cero o más sintagmas preposicionales.
        """
        tok = self.current()
        while tok is not None and tok.cat == "PREP":
            self.PP()
            tok = self.current()

    def PP(self):
        """
        PP -> PREP NP
        Sintagma preposicional: preposición + sintagma nominal.
        """
        self.accept("PREP")
        self.NP()

    # --------- VP y auxiliares ---------

    def AuxList(self):
        """
        AuxList -> AUX AuxList | ε
        Consume cero o más auxiliares (can, may, must).
        """
        tok = self.current()
        while tok is not None and tok.cat == "AUX":
            self.accept("AUX")
            tok = self.current()

    def VP(self, expected_subj_num: str):
        """
        VP -> AuxList V VPBody
        Verifica concordancia sujeto–verbo en número usando el V principal.
        """
        # Auxiliares modales opcionales: can, may, must, ...
        self.AuxList()

        # Verbo principal
        verb = self.accept("V")

        # Concordancia sujeto–verbo
        if verb.num != expected_subj_num:
            raise ParseError(
                f"Subject–verb agreement error: subject is {expected_subj_num}, "
                f"but verb '{verb.word}' is {verb.num} (position {verb.pos})."
            )

        # Cuerpo del VP: objeto directo opcional + PP(s) opcional(es)
        self.VPBody()

    def VPBody(self):
        """
        VPBody -> NP PPList
               | PPList
               | ε

        Implementado como:
          - Si viene NP: consumir NP y luego posible lista de PP.
          - Si no viene NP: consumir solo lista de PP (o nada).
        """
        tok = self.current()
        if tok is not None and tok.cat in ("DET", "PRON", "N"):
            # Objeto directo (NP)
            self.NP()
            # PPs como complemento del verbo (incluye IO tipo "to the boy")
            self.PPList()
        else:
            # Sin NP, pero pueden venir PPs (run in the park, talk to the students)
            self.PPList()


# Función análisis de la oración
def analyze_en_sentence(sentence: str) -> ParseResult:
    try:
        tokens = tokenize_sentence(sentence)
    except LexicalError as e:
        return ParseResult(False, f"Lexical error: {e}")

    parser = RDEnParser(tokens)
    return parser.parse()