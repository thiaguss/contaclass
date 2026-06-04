from rapidfuzz import fuzz, utils


class FuzzyMatcher:
    def __init__(
        self,
        levenshtein_weight: float = 0.35,
        token_sort_weight: float = 0.35,
        partial_weight: float = 0.30,
        default_threshold: float = 50.0,
    ):
        self.levenshtein_weight = levenshtein_weight
        self.token_sort_weight = token_sort_weight
        self.partial_weight = partial_weight
        self.default_threshold = default_threshold

    def compare(self, name_a: str, name_b: str) -> float:
        if not name_a or not name_b:
            return 0.0

        lev_score = fuzz.ratio(name_a, name_b, processor=utils.default_process)
        token_sort_score = fuzz.token_sort_ratio(name_a, name_b, processor=utils.default_process)
        partial_score = fuzz.partial_ratio(name_a, name_b, processor=utils.default_process)

        weighted = (
            lev_score * self.levenshtein_weight
            + token_sort_score * self.token_sort_weight
            + partial_score * self.partial_weight
        )

        return round(weighted, 2)

    def find_best_matches(
        self,
        name: str,
        candidates: list[str],
        top_n: int = 3,
        threshold: float | None = None,
    ) -> list[dict]:
        if not name or not candidates:
            return []

        threshold = threshold if threshold is not None else self.default_threshold

        scored = []
        for candidate in candidates:
            score = self.compare(name, candidate)
            if score >= threshold:
                scored.append({
                    "name": candidate,
                    "score": score,
                    "levenshtein": round(
                        fuzz.ratio(name, candidate, processor=utils.default_process), 2
                    ),
                    "token_sort": round(
                        fuzz.token_sort_ratio(name, candidate, processor=utils.default_process), 2
                    ),
                    "partial": round(
                        fuzz.partial_ratio(name, candidate, processor=utils.default_process), 2
                    ),
                })

        scored.sort(key=lambda x: x["score"], reverse=True)

        return scored[:top_n]
