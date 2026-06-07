from datetime import date
from decimal import Decimal

from contaclass.core.exact_match import ExactMatcher, SupplierIndex
from contaclass.core.fuzzy_match import FuzzyMatcher
from contaclass.core.normalizer import Normalizer
from contaclass.core.score import ScoreContext, ScoreEngine
from contaclass.models.entry import HistoricalEntry, NewEntry
from contaclass.models.result import (
    MatchResult,
    ProcessingBatchResult,
)


class Classifier:
    def __init__(
        self,
        normalizer: Normalizer | None = None,
        exact_matcher: ExactMatcher | None = None,
        fuzzy_matcher: FuzzyMatcher | None = None,
        score_engine: ScoreEngine | None = None,
        threshold: float = 70.0,
        code_strategy: str = "most_frequent",
    ):
        self.normalizer = normalizer or Normalizer()
        self.fuzzy_matcher = fuzzy_matcher or FuzzyMatcher()
        self.score_engine = score_engine or ScoreEngine()
        self.threshold = threshold
        self.code_strategy = code_strategy

        self._exact_matcher = exact_matcher
        self._index: SupplierIndex | None = None

    def build_index(self, historical_entries: list[HistoricalEntry]) -> SupplierIndex:
        idx = SupplierIndex()
        for entry in historical_entries:
            if not entry.normalized_supplier:
                entry.normalized_supplier = self.normalizer.normalize(entry.raw_supplier)
            idx.add_entry(entry)
        self._index = idx
        self._exact_matcher = ExactMatcher(idx)
        return idx

    @property
    def index(self) -> SupplierIndex | None:
        return self._index

    def classify_entry(
        self, entry: NewEntry, known_suppliers: list[str]
    ) -> MatchResult:
        normalized = self.normalizer.normalize(entry.raw_supplier)
        result = MatchResult(
            row_number=entry.row_number,
            entry_date=entry.entry_date,
            raw_supplier=entry.raw_supplier,
            normalized_supplier=normalized,
            amount=entry.amount,
            codigo_historico=entry.codigo_historico,
            codigo_matriz_filial=entry.codigo_matriz_filial,
            inicia_lote=entry.inicia_lote,
        )

        if not normalized:
            result.status = "not_found"
            return result

        if self._exact_matcher and self._exact_matcher.is_exact_match(normalized):
            match = self._exact_matcher.find_match(normalized, self.code_strategy)
            if match:
                result.debit_code = match.debit_code
                result.credit_code = match.credit_code
                result.confidence_score = 100.0
                result.status = "confirmed"
                result.match_type = "exact"
                result.matched_supplier = match.matched_supplier
                result.matched_supplier_normalized = normalized
                return result

        fuzzy_results = self.fuzzy_matcher.find_best_matches(
            normalized, known_suppliers, top_n=1, threshold=50.0
        )

        if fuzzy_results:
            best = fuzzy_results[0]
            base_score = best["score"]

            ctx = self._build_context(entry, best["name"])

            breakdown = self.score_engine.calculate(base_score, ctx)
            final_score = breakdown.final_score

            if final_score >= self.threshold:
                matched_entries = self._index.get_entries(best["name"])
                if matched_entries:
                    best_pair = self._resolve_best_pair(matched_entries)
                    result.debit_code = best_pair[0]
                    result.credit_code = best_pair[1]

            result.matched_supplier = best["name"]
            result.matched_supplier_normalized = best["name"]
            result.confidence_score = final_score
            result.status = self.score_engine.classify_status(final_score)
            result.match_type = "fuzzy"

            return result

        result.status = "not_found"
        return result

    def _build_context(self, entry: NewEntry, matched_normalized: str) -> ScoreContext:
        if not self._index:
            return ScoreContext()

        matched_entries = self._index.get_entries(matched_normalized)
        if not matched_entries:
            return ScoreContext()

        code_pairs = {(e.debit_code, e.credit_code) for e in matched_entries}
        unique_pairs = len(code_pairs)
        same_code_pair_always = unique_pairs == 1

        frequency = len(matched_entries)

        last_seen = max(e.entry_date for e in matched_entries)
        last_seen_days = (date.today() - last_seen).days

        historical_amounts = [e.amount for e in matched_entries]
        avg_amount = sum(historical_amounts, Decimal("0")) / len(historical_amounts)

        amount_diff = None
        if avg_amount > 0:
            diff_pct = float((entry.amount - avg_amount) / avg_amount * 100)
            amount_diff = round(diff_pct, 2)

        same_month = any(
            e.entry_date.month == entry.entry_date.month
            and e.entry_date.year != entry.entry_date.year
            for e in matched_entries
        )

        return ScoreContext(
            frequency=frequency,
            last_seen_days_ago=last_seen_days,
            same_code_pair_always=same_code_pair_always,
            unique_code_pairs_count=unique_pairs,
            amount_difference_pct=amount_diff,
            same_month_seasonal=same_month,
            entry_date=entry.entry_date,
            historical_amounts=historical_amounts,
        )

    def _resolve_best_pair(
        self, entries: list[HistoricalEntry]
    ) -> tuple[str | None, str | None]:
        if self.code_strategy == "most_recent":
            latest = max(entries, key=lambda e: e.entry_date)
            return latest.debit_code, latest.credit_code

        from collections import Counter

        pairs = Counter((e.debit_code, e.credit_code) for e in entries)
        return pairs.most_common(1)[0][0]

    def process(
        self,
        new_entries: list[NewEntry],
        historical_entries: list[HistoricalEntry] | None = None,
    ) -> ProcessingBatchResult:
        import time

        start = time.perf_counter()

        if historical_entries is not None:
            self.build_index(historical_entries)

        if not self._index:
            raise ValueError("Nenhum índice de histórico disponível. Forneça historical_entries ou chame build_index() primeiro.")

        known_suppliers = self._index.known_suppliers
        batch = ProcessingBatchResult()
        batch.total_entries = len(new_entries)

        for entry in new_entries:
            result = self.classify_entry(entry, known_suppliers)
            batch.entries.append(result)

        batch.confirmed_count = sum(
            1 for e in batch.entries if e.status == "confirmed"
        )
        batch.review_count = sum(
            1 for e in batch.entries if e.status == "review"
        )
        batch.not_found_count = sum(
            1 for e in batch.entries if e.status == "not_found"
        )
        batch.processing_time_ms = int((time.perf_counter() - start) * 1000)

        return batch
