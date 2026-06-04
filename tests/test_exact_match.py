from datetime import date
from decimal import Decimal

from contaclass.core.exact_match import ExactMatcher, SupplierIndex
from contaclass.models.entry import HistoricalEntry


def _entry(normalized, debit, credit, amount="100.00", raw=None, tab="default", row=1):
    return HistoricalEntry(
        tab_name=tab,
        entry_date=date(2026, 1, 15),
        raw_supplier=raw or normalized,
        normalized_supplier=normalized,
        debit_code=debit,
        credit_code=credit,
        amount=Decimal(amount),
        row_number=row,
    )


def test_exact_match_found():
    idx = SupplierIndex()
    idx.add_entry(_entry("VIVO", "503", "101"))
    matcher = ExactMatcher(idx)
    result = matcher.find_match("VIVO")
    assert result is not None
    assert result.confidence_score == 100.0
    assert result.status == "confirmed"
    assert result.match_type == "exact"
    assert result.debit_code == "503"
    assert result.credit_code == "101"


def test_exact_match_not_found():
    idx = SupplierIndex()
    idx.add_entry(_entry("VIVO", "503", "101"))
    matcher = ExactMatcher(idx)
    result = matcher.find_match("TIM")
    assert result is None


def test_is_exact_match():
    idx = SupplierIndex()
    idx.add_entry(_entry("VIVO", "503", "101"))
    matcher = ExactMatcher(idx)
    assert matcher.is_exact_match("VIVO")
    assert not matcher.is_exact_match("TIM")


def test_most_frequent_code_pair():
    idx = SupplierIndex()
    idx.add_entry(_entry("EQUATORIAL", "504", "101", amount="200.00", row=1))
    idx.add_entry(_entry("EQUATORIAL", "504", "101", amount="150.00", row=2))
    idx.add_entry(_entry("EQUATORIAL", "504", "101", amount="300.00", row=3))
    idx.add_entry(_entry("EQUATORIAL", "505", "101", amount="100.00", row=4))
    idx.add_entry(_entry("EQUATORIAL", "504", "101", amount="250.00", row=5))
    idx.add_entry(_entry("EQUATORIAL", "505", "101", amount="180.00", row=6))
    idx.add_entry(_entry("EQUATORIAL", "504", "101", amount="220.00", row=7))
    idx.add_entry(_entry("EQUATORIAL", "504", "101", amount="190.00", row=8))
    matcher = ExactMatcher(idx)
    result = matcher.find_match("EQUATORIAL", strategy="most_frequent")
    assert result is not None
    assert result.debit_code == "504"
    assert result.credit_code == "101"


def test_most_recent_code_pair():
    idx = SupplierIndex()
    idx.add_entry(HistoricalEntry(
        tab_name="default", entry_date=date(2025, 6, 1),
        raw_supplier="CEMIG", normalized_supplier="CEMIG",
        debit_code="504", credit_code="101", amount=Decimal("100.00"), row_number=1
    ))
    idx.add_entry(HistoricalEntry(
        tab_name="default", entry_date=date(2026, 5, 1),
        raw_supplier="CEMIG", normalized_supplier="CEMIG",
        debit_code="505", credit_code="102", amount=Decimal("200.00"), row_number=2
    ))
    matcher = ExactMatcher(idx)
    result = matcher.find_match("CEMIG", strategy="most_recent")
    assert result is not None
    assert result.debit_code == "505"
    assert result.credit_code == "102"


def test_empty_index():
    idx = SupplierIndex()
    matcher = ExactMatcher(idx)
    assert matcher.find_match("QUALQUER") is None
    assert matcher.is_exact_match("QUALQUER") is False


def test_index_properties():
    idx = SupplierIndex()
    idx.add_entry(_entry("VIVO", "503", "101"))
    idx.add_entry(_entry("TIM", "504", "102"))
    idx.add_entry(_entry("VIVO", "503", "101"))
    assert idx.total_entries == 3
    assert idx.unique_suppliers == 2
    assert "VIVO" in idx.known_suppliers
    assert "TIM" in idx.known_suppliers


def test_add_entries_bulk():
    entries = [
        _entry("VIVO", "503", "101"),
        _entry("TIM", "504", "102"),
    ]
    idx = SupplierIndex()
    idx.add_entries(entries)
    assert idx.total_entries == 2
    assert idx.unique_suppliers == 2
