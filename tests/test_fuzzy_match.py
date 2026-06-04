from contaclass.core.fuzzy_match import FuzzyMatcher


def test_exact_match_returns_100():
    fm = FuzzyMatcher()
    assert fm.compare("VIVO", "VIVO") == 100.0


def test_levenshtein_typo():
    fm = FuzzyMatcher()
    score = fm.compare("VIVO", "VIVOO")
    assert 80.0 <= score < 100.0


def test_token_sort_via_breakdown():
    fm = FuzzyMatcher()
    results = fm.find_best_matches("BANCO DO BRASIL", ["BRASIL BANCO DO"], top_n=1)
    assert len(results) == 1
    assert results[0]["token_sort"] == 100.0


def test_token_sort_vivo():
    fm = FuzzyMatcher()
    results = fm.find_best_matches("VIVO EMPRESAS", ["EMPRESAS VIVO"], top_n=1)
    assert len(results) == 1
    assert results[0]["token_sort"] == 100.0


def test_partial_ratio_substring():
    fm = FuzzyMatcher()
    results = fm.find_best_matches("VIVO", ["TELEFONICA VIVO"], top_n=1)
    assert len(results) == 1
    assert results[0]["partial"] == 100.0


def test_partial_ratio_net():
    fm = FuzzyMatcher()
    results = fm.find_best_matches("NET", ["NET SERVICOS"], top_n=1)
    assert len(results) == 1
    assert results[0]["partial"] == 100.0


def test_telefonica_vs_vivo_weighted():
    fm = FuzzyMatcher()
    score = fm.compare("TELEFONICA BRASIL", "VIVO")
    assert score > 0


def test_find_best_matches_top3():
    fm = FuzzyMatcher()
    candidates = ["VIVO", "TIM", "CLARO", "OI", "NET"]
    results = fm.find_best_matches("VIVO", candidates, top_n=3)
    assert len(results) <= 3
    assert results[0]["name"] == "VIVO"
    assert results[0]["score"] == 100.0


def test_threshold_filter():
    fm = FuzzyMatcher()
    candidates = ["VIVO", "EMPRESA COMPLETAMENTE DIFERENTE"]
    results = fm.find_best_matches("VIVO", candidates, top_n=3, threshold=80.0)
    assert len(results) == 1
    assert results[0]["name"] == "VIVO"


def test_empty_candidates():
    fm = FuzzyMatcher()
    assert fm.find_best_matches("VIVO", []) == []


def test_empty_name():
    fm = FuzzyMatcher()
    assert fm.find_best_matches("", ["VIVO"]) == []


def test_score_breakdown_all_keys():
    fm = FuzzyMatcher()
    results = fm.find_best_matches("VIVO EMPRESAS", ["EMPRESAS VIVO"], top_n=1)
    assert len(results) == 1
    r = results[0]
    assert "levenshtein" in r
    assert "token_sort" in r
    assert "partial" in r
    assert r["token_sort"] == 100.0


def test_weighted_score_is_average():
    fm = FuzzyMatcher()
    results = fm.find_best_matches("BANCO DO BRASIL", ["BRASIL BANCO DO"], top_n=1)
    r = results[0]
    expected = round(r["levenshtein"] * 0.35 + r["token_sort"] * 0.35 + r["partial"] * 0.30, 2)
    assert r["score"] == expected
