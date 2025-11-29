# ==============================================================================
# ESPECIFICACIÓN DE LA GRAMÁTICA (Recursive Descent Parser)

# Símbolo Inicial (Lógica de control):
#   Program  -> S ( COMMA S )*

#   NOTA DE DISEÑO:
#   Esta regla permite que el parser procese una lista indefinida (infinita) de 
#   oraciones separadas por comas. La coma cumple una doble función:
#     1. Sintáctica: Separador gramatical entre oraciones.
#     2. Recuperación: Elemento de sincronización para el 'Modo Pánico'.

# Producciones Sintácticas:
#   1. S        -> NP VP

#   2. NP       -> PRON
#                | DET AdjList N PPList
#                | N PPList                 (Restricción: N debe permitir 'Bare Noun')

#   3. AdjList  -> ADJ AdjList | ε
#
#   4. PPList   -> PP PPList | ε

#   5. PP       -> PREP NP

#   6. VP       -> AuxList V VPBody

#   7. AuxList  -> AUX AuxList | ε

#   8. VPBody   -> NP PPList
#                | PPList
#                | ε

# Reglas Semánticas y de Validación:
#   - Concordancia de Número: Sujeto (NP) con Verbo (VP).
#   - Concordancia de Número: Determinante (DET) con Sustantivo (N).
#   - Restricción 'Bare Noun': Sustantivos singulares contables (SGC) requieren determinante.
#     Sustantivos Plurales (PL), Incontables (UNC) o Colectivos (COLL) pueden ir solos.

# Estrategia de Manejo de Errores:
#   - Modo Pánico (Panic Mode Recovery).
#   - Token de Sincronización: COMMA (,).
# ==============================================================================

from dataclasses import dataclass, field
from typing import List
from src.en_lexicon import Token, tokenize_sentence, LexicalError

class ParseError(Exception):
    """Excepción lanzada cuando ocurre un error de sintaxis o concordancia."""
    pass

@dataclass
class ParseResult:
    """Clase para encapsular el resultado del análisis sintáctico."""
    ok: bool
    messages: List[str] = field(default_factory=list)

class RDEnParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0  # Puntero al token actual

    # MÉTODOS DE UTILIDAD

    def current(self):
        """Devuelve el token actual o None si se ha llegado al final."""
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def accept(self, expected_cat: str) -> Token:
        """
        Verifica si el token actual coincide con la categoría esperada.
        Si coincide, avanza el puntero y devuelve el token.
        Si no, lanza ParseError.
        """
        tok = self.current()
        if tok is None:
            raise ParseError(
                f"Unexpected end of input. Expected category: {expected_cat}."
            )

        if tok.cat != expected_cat:
            raise ParseError(
                f"Expected {expected_cat}, found {tok.cat} ('{tok.word}') at position {tok.pos}."
            )

        self.i += 1
        return tok

    # LÓGICA DE RECUPERACIÓN DE ERRORES (MODO PÁNICO)
    
    def parse_panic_mode(self) -> ParseResult:
        """
        Método principal que orquesta el análisis.
        Implementa un bucle para procesar múltiples oraciones separadas por comas.
        Si ocurre un error, registra el mensaje y sincroniza hasta la siguiente coma.
        """
        errors = []
        parsed_any = False

        while self.current() is not None:
            try:
                # Verificación de sintaxis: Coma no esperada al inicio de una oración
                if self.current().cat == "COMMA":
                    raise ParseError(f"Unexpected comma found at start of sentence (position {self.current().pos}).")

                # Intentar analizar una oración completa (S)
                self.S() 
                parsed_any = True
                
                # Verificación de delimitador: Esperamos una coma o el fin del archivo
                curr = self.current()
                if curr is not None:
                    if curr.cat == "COMMA":
                        self.accept("COMMA")  # Consumir el separador y continuar
                    else:
                        raise ParseError(f"Expected ',' or End of Input, found '{curr.word}'")
            
            except ParseError as e:
                # REPORTE: Agregar el error a la lista
                errors.append(str(e))
                # RECUPERACIÓN: Invocar rutina de sincronización
                self.synchronize_panic()

        # Generación del resultado final
        if errors:
            return ParseResult(False, errors)
        elif not parsed_any:
            return ParseResult(False, ["No input provided."])
        
        return ParseResult(True, ["Parsing successful."])

    def synchronize_panic(self):
        """
        Rutina de Sincronización.
        Descarta tokens consecutivamente hasta encontrar el token de sincronización (COMMA)
        o alcanzar el final del flujo de entrada.
        """
        while self.current() is not None:
            token = self.current()
            if token.cat == "COMMA":
                self.i += 1  # Consumir la coma para reiniciar el análisis en estado limpio
                return
            self.i += 1  # Descartar token actual

    # REGLAS DE ANÁLISIS SINTÁCTICO (RECURSIVE DESCENT)

    def S(self) -> str:
        """
        Producción: S -> NP VP
        Retorna el número del sujeto (SG/PL) para validaciones futuras.
        """
        subj_num = self.NP()
        self.VP(expected_subj_num=subj_num)
        return subj_num

    def NP(self) -> str:
        """
        Producciones NP:
          1. NP -> PRON
          2. NP -> DET AdjList N PPList
          3. NP -> N PPList (Bare Noun)
        """
        tok = self.current()
        if tok is None:
            raise ParseError("Expected NP, found end of sentence.")

        # 1. Caso Pronombre
        if tok.cat == "PRON":
            pron = self.accept("PRON")
            return pron.num

        # 2. Caso Determinante + Sustantivo
        if tok.cat == "DET":
            det = self.accept("DET")
            self.AdjList()
            noun = self.accept("N")
            noun_num = self.noun_agreement(noun)

            # Validación: Concordancia Determinante-Sustantivo
            if det.num != "ANY" and det.num != noun_num:
                raise ParseError(
                    f"Agreement Error: Determiner '{det.word}' ({det.num}) mismatch with noun '{noun.word}' ({noun.num})."
                )

            self.PPList()
            return noun_num

        # 3. Caso Sustantivo sin Determinante (Bare Noun)
        if tok.cat == "N":
            noun = self.accept("N")
            # Validación: Solo ciertos tipos de sustantivos pueden ir sin determinante
            if not self.noun_allows_bare(noun):
                raise ParseError(
                    f"Grammar Error: Countable singular noun '{noun.word}' cannot appear without a determiner."
                )
            self.PPList()
            return self.noun_agreement(noun)

        raise ParseError(f"Expected DET, PRON or N to start NP, found {tok.cat} ('{tok.word}').")

    def AdjList(self):
        """Producción: AdjList -> ADJ AdjList | ε"""
        while self.current() is not None and self.current().cat == "ADJ":
            self.accept("ADJ")

    def PPList(self):
        """Producción: PPList -> PP PPList | ε"""
        while self.current() is not None and self.current().cat == "PREP":
            self.PP()

    def PP(self):
        """Producción: PP -> PREP NP"""
        self.accept("PREP")
        self.NP()

    def AuxList(self):
        """Producción: AuxList -> AUX AuxList | ε"""
        while self.current() is not None and self.current().cat == "AUX":
            self.accept("AUX")

    def VP(self, expected_subj_num: str):
        """
        Producción: VP -> AuxList V VPBody
        Realiza la validación de concordancia Sujeto-Verbo.
        """
        self.AuxList()
        verb = self.accept("V")

        # Validación: Concordancia Sujeto-Verbo
        if verb.num != expected_subj_num:
            raise ParseError(
                f"Subject–Verb Agreement Error: Subject is {expected_subj_num}, "
                f"but verb '{verb.word}' is {verb.num}."
            )

        self.VPBody()

    def VPBody(self):
        """
        Producción: VPBody -> NP PPList | PPList | ε
        Maneja objetos directos y complementos preposicionales.
        """
        tok = self.current()
        # Verificamos si el siguiente token inicia un NP (Objeto Directo)
        if tok is not None and tok.cat in ("DET", "PRON", "N"):
            self.NP()      # Consumir Objeto Directo
            self.PPList()  # Consumir complementos circunstanciales
        else:
            # Si no hay objeto directo, solo buscamos complementos
            self.PPList()

    # HELPERS DE VALIDACIÓN SEMÁNTICA

    def noun_agreement(self, noun: Token) -> str:
        """Determina el número gramatical efectivo del sustantivo."""
        if noun.num == "PL": return "PL"
        return "SG"

    def noun_allows_bare(self, noun: Token) -> bool:
        """
        Verifica si el sustantivo puede aparecer sin determinante.
        Permitido para: Plurales (PL), Incontables (UNC) y Colectivos (COLL).
        """
        return noun.num in ("PL", "UNC", "COLL")

# PUNTO DE ENTRADA PÚBLICO

def analyze_en_sentence(sentence: str) -> ParseResult:
    """
    Función principal para invocar el parser.
    1. Tokeniza la entrada.
    2. Inicializa el parser.
    3. Ejecuta el análisis con recuperación de errores.
    """
    try:
        tokens = tokenize_sentence(sentence)
    except LexicalError as e:
        # Los errores léxicos detienen el proceso inmediatamente.
        return ParseResult(False, [f"Lexical Error: {e}"])

    parser = RDEnParser(tokens)
    return parser.parse_panic_mode()