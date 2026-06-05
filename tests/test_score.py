from contaclass.core.score import ScoreEngine, ScoreContext


def test_exact_match_score():
    engine = ScoreEngine()
    ctx = ScoreContext()
    result = engine.calculate(100.0, ctx)
    assert result.final_score == 100.0


def test_below_threshold_not_found():
    engine = ScoreEngine()
    ctx = ScoreContext()
    result = engine.calculate(30.0, ctx)
    assert result.final_score == 30.0


def test_high_frequency_adjustment():
    engine = ScoreEngine()
    ctx = ScoreContext(frequency=10)
    result = engine.calculate(80.0, ctx)
    assert result.final_score == 85.0


def test_recency_adjustment():
    engine = ScoreEngine()
    ctx = ScoreContext(last_seen_days_ago=30)
    result = engine.calculate(80.0, ctx)
    assert result.final_score == 83.0


def test_no_recency_if_old():
    engine = ScoreEngine()
    ctx = ScoreContext(last_seen_days_ago=200)
    result = engine.calculate(80.0, ctx)
    assert result.final_score == 80.0


def test_consistent_codes_boost():
    engine = ScoreEngine()
    ctx = ScoreContext(same_code_pair_always=True)
    result = engine.calculate(80.0, ctx)
    assert result.final_score == 87.0


def test_inconsistency_penalty():
    engine = ScoreEngine()
    ctx = ScoreContext(unique_code_pairs_count=5)
    result = engine.calculate(80.0, ctx)
    assert result.final_score == 70.0


def test_multiple_adjustments():
    engine = ScoreEngine()
    ctx = ScoreContext(
        frequency=10,
        last_seen_days_ago=30,
        same_code_pair_always=True,
        unique_code_pairs_count=1,
    )
    result = engine.calculate(70.0, ctx)
    assert result.final_score == 85.0


def test_score_capped_at_100():
    engine = ScoreEngine()
    ctx = ScoreContext(
        frequency=10,
        last_seen_days_ago=30,
        same_code_pair_always=True,
        has_prior_correction_to_this=True,
    )
    result = engine.calculate(95.0, ctx)
    assert result.final_score <= 100.0


def test_classify_status():
    engine = ScoreEngine()
    assert engine.classify_status(100.0) == "confirmed"
    assert engine.classify_status(85.0) == "review"
    assert engine.classify_status(65.0) == "review"
    assert engine.classify_status(50.0) == "review"
    assert engine.classify_status(49.0) == "not_found"


def test_classify_color():
    engine = ScoreEngine()
    assert engine.classify_color(100.0) == "#C6EFCE"
    assert engine.classify_color(80.0) == "#FFEB9C"
    assert engine.classify_color(50.0) == "#FFEB9C"
    assert engine.classify_color(49.0) == "#FFC7CE"
    assert engine.classify_color(30.0) == "#FFC7CE"


def test_score_breakdown_structure():
    engine = ScoreEngine()
    ctx = ScoreContext(frequency=10, last_seen_days_ago=30, same_code_pair_always=True)
    result = engine.calculate(70.0, ctx)

    breakdown = result.to_dict()
    assert breakdown["base_fuzzy_score"] == 70.0
    assert len(breakdown["adjustments"]) == 3
    assert breakdown["final_score"] > 70.0


def test_prior_correction_boost():
    engine = ScoreEngine()
    ctx = ScoreContext(has_prior_correction_to_this=True)
    result = engine.calculate(70.0, ctx)
    assert result.final_score == 80.0
