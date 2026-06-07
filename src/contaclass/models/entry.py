from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class HistoricalEntry:
    tab_name: str
    entry_date: date
    raw_supplier: str
    normalized_supplier: str
    debit_code: str
    credit_code: str
    amount: Decimal
    row_number: int | None = None
    codigo_historico: str | None = None
    codigo_matriz_filial: str | None = None
    inicia_lote: str | None = None


@dataclass
class NewEntry:
    row_number: int
    entry_date: date
    raw_supplier: str
    amount: Decimal
    codigo_historico: str | None = None
    codigo_matriz_filial: str | None = None
    inicia_lote: str | None = None
