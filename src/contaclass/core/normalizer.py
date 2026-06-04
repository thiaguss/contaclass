import re
from unidecode import unidecode

DEFAULT_PREFIXES = [
    "PIX", "PGTO", "PAGAMENTO", "PAG", "TED", "DOC",
    "TRANSF", "TRANSFERENCIA", "DEBITO", "CREDITO",
    "COBRANCA", "BOLETO", "DEB AUT", "TARIFAS", "TARIFA",
]

DEFAULT_SUFFIXES = [
    "S.A.", "SA", "LTDA", "EIRELI", "ME", "EPP",
    "S/A", "CIA", "INDUSTRIA", "COMERCIO",
]

DEFAULT_REMOVE_TERMS = ["CNPJ", "CPF"]


class Normalizer:
    def __init__(
        self,
        prefixes: list[str] | None = None,
        suffixes: list[str] | None = None,
        remove_terms: list[str] | None = None,
    ):
        self.prefixes = sorted(prefixes or DEFAULT_PREFIXES, key=len, reverse=True)
        self.suffixes = sorted(suffixes or DEFAULT_SUFFIXES, key=len, reverse=True)
        self.remove_terms = remove_terms or DEFAULT_REMOVE_TERMS

    def normalize(self, name: str) -> str:
        if not name or not name.strip():
            return ""

        result = name.strip().upper()

        result = unidecode(result)

        result = re.sub(r'\b\d{1,2}[/\-]\d{2,4}\b', '', result)

        for term in self.remove_terms:
            pattern = re.compile(
                rf'\b{re.escape(term)}\b[\s\d\/\.\-]*', re.IGNORECASE
            )
            result = pattern.sub('', result)

        for suffix in self.suffixes:
            escaped = re.escape(suffix)
            pattern = re.compile(
                rf'(?:^|\s){escaped}\.?(\s|$)', re.IGNORECASE
            )
            result = pattern.sub(' ', result)

        changed = True
        while changed:
            changed = False
            for prefix in self.prefixes:
                upper_result = result.upper()
                upper_prefix = prefix.upper()
                if upper_result.startswith(upper_prefix):
                    rest = result[len(prefix):].lstrip()
                    if not rest or rest[0] in '-\u2013\u2014':
                        rest = rest.lstrip('-\u2013\u2014\u2015').strip()
                    result = rest
                    changed = True
                    break

        result = re.sub(r'[^A-Z0-9\s]', ' ', result)

        result = re.sub(r'\s+', ' ', result).strip()

        return result

    def is_empty_after_normalization(self, name: str) -> bool:
        return len(self.normalize(name)) == 0
