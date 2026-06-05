from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal
from statistics import mean, stdev
from typing import Callable


@dataclass
class ScoreContext:
    frequency: int = 0
    last_seen_days_ago: int | None = None
    same_code_pair_always: bool = False
    unique_code_pairs_count: int = 1
    amount_difference_pct: float | None = None
    same_month_seasonal: bool = False
    has_prior_correction_to_this: bool = False
    entry_date: date | None = None
    historical_amounts: list[Decimal] = field(default_factory=list)


@dataclass
class Adjustment:
    factor: str
    delta: float


@dataclass
class ScoreBreakdown:
    levenshtein: float = 0.0
    token_sort: float = 0.0
    partial_ratio: float = 0.0
    base_fuzzy_score: float = 0.0
    adjustments: list[Adjustment] = field(default_factory=list)
    final_score: float = 0.0

    def to_dict(self) -> dict:
        return {
            "levenshtein": self.levenshtein,
            "token_sort": self.token_sort,
            "partial_ratio": self.partial_ratio,
            "base_fuzzy_score": self.base_fuzzy_score,
            "adjustments": [{"factor": a.factor, "delta": a.delta} for a in self.adjustments],
            "final_score": self.final_score,
        }


class ScoreEngine:
    ADJUSTMENTS: list[tuple[str, Callable[[ScoreContext], float], str]] = [
        ("high_frequency", lambda ctx: 5.0 if ctx.frequency > 5 else 0.0, "Par de códigos usado >5 vezes no histórico"),
        ("recency", lambda ctx: 3.0 if ctx.last_seen_days_ago is not None and ctx.last_seen_days_ago < 90 else 0.0, "Último uso < 90 dias"),
        ("consistent_codes", lambda ctx: 7.0 if ctx.same_code_pair_always else 0.0, "Fornecedor sempre usou o mesmo par de códigos"),
        ("similar_amount", lambda ctx: 3.0 if ctx.amount_difference_pct is not None and abs(ctx.amount_difference_pct) < 10.0 else 0.0, "Valor difere menos de 10% da média histórica"),
        ("seasonal_month", lambda ctx: 5.0 if ctx.same_month_seasonal else 0.0, "Fornecedor aparece no mesmo mês em anos anteriores"),
        ("prior_correction", lambda ctx: 10.0 if ctx.has_prior_correction_to_this else 0.0, "Usuário já corrigiu para este mapeamento antes"),
        ("inconsistency", lambda ctx: -10.0 if ctx.unique_code_pairs_count > 3 else 0.0, "Fornecedor usou >3 pares de códigos diferentes"),
    ]

    def calculate(self, base_score: float, context: ScoreContext) -> ScoreBreakdown:
        breakdown = ScoreBreakdown()
        breakdown.base_fuzzy_score = base_score
        breakdown.final_score = base_score

        for name, rule_fn, _desc in self.ADJUSTMENTS:
            delta = rule_fn(context)
            if delta != 0.0:
                breakdown.adjustments.append(Adjustment(factor=name, delta=delta))
                breakdown.final_score += delta

        breakdown.final_score = round(max(0.0, min(100.0, breakdown.final_score)), 2)

        return breakdown

    def classify_status(self, final_score: float) -> str:
        if final_score >= 100.0:
            return "confirmed"
        if final_score >= 50.0:
            return "review"
        return "not_found"

    def classify_color(self, final_score: float) -> str:
        if final_score >= 100.0:
            return "#C6EFCE"
        if final_score >= 50.0:
            return "#FFEB9C"
        return "#FFC7CE"

    def classify_text_color(self, final_score: float) -> str:
        if final_score >= 100.0:
            return "#276221"
        if final_score >= 50.0:
            return "#9C6500"
        return "#9C0006"
