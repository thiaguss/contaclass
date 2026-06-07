from datetime import date
from decimal import Decimal

from contaclass.core.classifier import Classifier
from contaclass.models.entry import HistoricalEntry, NewEntry


def _ventry(normalized, debit, credit, amount="100.00", day=15, raw=None):
    return HistoricalEntry(
        tab_name="default",
        entry_date=date(2026, 1, day),
        raw_supplier=raw or normalized,
        normalized_supplier=normalized,
        debit_code=debit,
        credit_code=credit,
        amount=Decimal(amount),
        row_number=1,
    )


def _nentry(supplier, amount="150.00", day=20, row=1):
    return NewEntry(
        row_number=row,
        entry_date=date(2026, 2, day),
        raw_supplier=supplier,
        amount=Decimal(amount),
    )


def test_exact_match_classification():
    classifier = Classifier()
    classifier.build_index([
        _ventry("VIVO", "503", "101"),
    ])
    result = classifier.process([_nentry("VIVO")])
    assert result.total_entries == 1
    assert result.confirmed_count == 1
    assert result.entries[0].confidence_score == 100.0
    assert result.entries[0].debit_code == "503"
    assert result.entries[0].credit_code == "101"


def test_fuzzy_match_classification():
    classifier = Classifier(threshold=50.0)
    classifier.build_index([
        _ventry("TELEFONICA BRASIL", "503", "101"),
    ])
    result = classifier.process([_nentry("TELEFONICA")])
    assert result.total_entries == 1
    assert result.entries[0].status in ("review", "confirmed")
    assert result.entries[0].debit_code is not None


def test_not_found_classification():
    classifier = Classifier()
    classifier.build_index([
        _ventry("VIVO", "503", "101"),
    ])
    result = classifier.process([_nentry("FORNECEDOR DESCONHECIDO XYZ")])
    assert result.total_entries == 1
    assert result.not_found_count == 1
    assert result.entries[0].status == "not_found"
    assert result.entries[0].debit_code is None


def test_multiple_entries_mixed():
    classifier = Classifier(threshold=50.0)
    classifier.build_index([
        _ventry("VIVO", "503", "101"),
        _ventry("TIM", "504", "102"),
        _ventry("CLARO", "505", "103"),
    ])
    entries = [
        _nentry("VIVO", row=1),
        _nentry("TIM", row=2),
        _nentry("FORNECEDOR TOTALMENTE NOVO", row=3),
        _nentry("CLARO", row=4),
        _nentry("VIVO", row=5),
    ]
    result = classifier.process(entries)
    assert result.total_entries == 5
    assert result.confirmed_count >= 2
    assert result.not_found_count >= 1


def test_automation_rate():
    classifier = Classifier(threshold=50.0)
    classifier.build_index([
        _ventry("VIVO", "503", "101"),
        _ventry("TIM", "504", "102"),
    ])
    entries = [
        _nentry("VIVO", row=1),
        _nentry("DESCONHECIDO", row=2),
    ]
    result = classifier.process(entries)
    assert result.total_entries == 2
    assert result.automation_rate == 50.0


def test_normalization_integration():
    classifier = Classifier(threshold=50.0)
    classifier.build_index([
        _ventry("TELEFONICA BRASIL", "503", "101"),
    ])
    result = classifier.process([
        _nentry("Pagamento PIX - TELEFONICA BRASIL S.A."),
    ])
    assert result.entries[0].status != "not_found"
    assert result.entries[0].confidence_score > 0


def test_code_strategy_most_recent():
    classifier = Classifier(code_strategy="most_recent")
    classifier.build_index([
        HistoricalEntry("default", date(2025, 6, 1), "CEMIG", "CEMIG", "504", "101", Decimal("100"), 1),
        HistoricalEntry("default", date(2026, 5, 1), "CEMIG", "CEMIG", "505", "102", Decimal("200"), 2),
    ])
    result = classifier.process([_nentry("CEMIG")])
    assert result.entries[0].debit_code == "505"
    assert result.entries[0].credit_code == "102"


def test_empty_historical_raises():
    classifier = Classifier()
    try:
        classifier.process([_nentry("VIVO")])
        assert False, "Deveria ter lançado ValueError"
    except ValueError:
        pass


def test_classify_single_entry():
    classifier = Classifier()
    classifier.build_index([_ventry("VIVO", "503", "101")])
    entry = classifier.classify_entry(_nentry("VIVO"), classifier.index.known_suppliers)
    assert entry.status == "confirmed"
    assert entry.confidence_score == 100.0


def test_build_index_normalizes_empty_supplier():
    entry = HistoricalEntry(
        tab_name="default", entry_date=date(2026, 1, 1),
        raw_supplier="VIVO S.A.", normalized_supplier="",
        debit_code="503", credit_code="101", amount=Decimal("100.00"),
    )
    classifier = Classifier()
    classifier.build_index([entry])
    assert classifier.index.has_supplier("VIVO")


def test_fuzzy_match_sets_matched_supplier_below_threshold():
    classifier = Classifier(threshold=90.0)
    classifier.build_index([
        _ventry("TELEFONICA BRASIL", "503", "101"),
    ])
    entry = _nentry("TELEFONICA")
    result = classifier.classify_entry(entry, classifier.index.known_suppliers)
    assert result.status == "review"
    assert result.matched_supplier is not None
    assert result.debit_code is None


def test_extra_fields_propagated_from_new_entry_to_result():
    from datetime import date
    from decimal import Decimal
    from contaclass.models.entry import NewEntry

    classifier = Classifier(threshold=50.0)
    classifier.build_index([
        _ventry("VIVO", "503", "101"),
    ])
    entry = NewEntry(
        row_number=1,
        entry_date=date(2026, 2, 1),
        raw_supplier="VIVO",
        amount=Decimal("100.00"),
        codigo_historico="H001",
        codigo_matriz_filial="1",
        inicia_lote="S",
    )
    result = classifier.classify_entry(entry, classifier.index.known_suppliers)
    assert result.codigo_historico == "H001"
    assert result.codigo_matriz_filial == "1"
    assert result.inicia_lote == "S"
