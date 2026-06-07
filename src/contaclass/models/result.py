from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class MatchResult:
    row_number: int
    entry_date: date
    raw_supplier: str
    normalized_supplier: str
    amount: Decimal
    debit_code: str | None = None
    credit_code: str | None = None
    confidence_score: float = 0.0
    status: str = "pending"
    match_type: str | None = None
    matched_supplier: str | None = None
    matched_supplier_normalized: str | None = None
    is_corrected: bool = False
    codigo_historico: str | None = None
    codigo_matriz_filial: str | None = None
    inicia_lote: str | None = None


@dataclass
class ProcessingBatchResult:
    total_entries: int = 0
    confirmed_count: int = 0
    review_count: int = 0
    not_found_count: int = 0
    entries: list[MatchResult] = field(default_factory=list)
    processing_time_ms: int = 0

    @property
    def automation_rate(self) -> float:
        if self.total_entries == 0:
            return 0.0
        return round((self.confirmed_count / self.total_entries) * 100, 2)
