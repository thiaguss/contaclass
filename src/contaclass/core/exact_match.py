from collections import defaultdict
from datetime import date
from decimal import Decimal
from statistics import StatisticsError, mode

from contaclass.models.entry import HistoricalEntry
from contaclass.models.result import MatchResult


class SupplierIndex:
    def __init__(self):
        self._by_normalized: dict[str, list[HistoricalEntry]] = defaultdict(list)

    def add_entry(self, entry: HistoricalEntry):
        self._by_normalized[entry.normalized_supplier].append(entry)

    def add_entries(self, entries: list[HistoricalEntry]):
        for entry in entries:
            self.add_entry(entry)

    def get_entries(self, normalized_name: str) -> list[HistoricalEntry]:
        return self._by_normalized.get(normalized_name, [])

    def has_supplier(self, normalized_name: str) -> bool:
        return normalized_name in self._by_normalized

    @property
    def known_suppliers(self) -> list[str]:
        return list(self._by_normalized.keys())

    @property
    def total_entries(self) -> int:
        return sum(len(v) for v in self._by_normalized.values())

    @property
    def unique_suppliers(self) -> int:
        return len(self._by_normalized)

    def _resolve_codes(
        self, entries: list[HistoricalEntry], strategy: str = "most_frequent"
    ) -> tuple[str | None, str | None]:
        if not entries:
            return None, None

        code_pairs = [(e.debit_code, e.credit_code) for e in entries]

        if strategy == "most_frequent":
            try:
                best_pair = mode(code_pairs)
            except (ValueError, StatisticsError):
                best_pair = code_pairs[0]
            return best_pair

        if strategy == "most_recent":
            latest = max(entries, key=lambda e: e.entry_date)
            return latest.debit_code, latest.credit_code

        return entries[0].debit_code, entries[0].credit_code

    def _calculate_frequency(
        self, entries: list[HistoricalEntry]
    ) -> dict[tuple[str, str], int]:
        freq: dict[tuple[str, str], int] = defaultdict(int)
        for e in entries:
            freq[(e.debit_code, e.credit_code)] += 1
        return dict(freq)

    def _last_seen(self, entries: list[HistoricalEntry]) -> date | None:
        if not entries:
            return None
        return max(e.entry_date for e in entries)

    def _all_amounts(self, entries: list[HistoricalEntry]) -> list[Decimal]:
        return [e.amount for e in entries]

    def match(
        self, normalized_name: str, strategy: str = "most_frequent"
    ) -> MatchResult | None:
        entries = self.get_entries(normalized_name)
        if not entries:
            return None

        debit, credit = self._resolve_codes(entries, strategy)

        return MatchResult(
            row_number=0,
            entry_date=date.today(),
            raw_supplier="",
            normalized_supplier=normalized_name,
            amount=Decimal("0.00"),
            debit_code=debit,
            credit_code=credit,
            confidence_score=100.0,
            status="confirmed",
            match_type="exact",
            matched_supplier=entries[0].raw_supplier,
            matched_supplier_normalized=normalized_name,
        )


class ExactMatcher:
    def __init__(self, index: SupplierIndex):
        self._index = index

    @property
    def index(self) -> SupplierIndex:
        return self._index

    def find_match(
        self, normalized_name: str, strategy: str = "most_frequent"
    ) -> MatchResult | None:
        return self._index.match(normalized_name, strategy)

    def is_exact_match(self, normalized_name: str) -> bool:
        return self._index.has_supplier(normalized_name)
