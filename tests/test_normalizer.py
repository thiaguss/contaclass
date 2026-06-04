from contaclass.core.normalizer import Normalizer


def test_uppercase_conversion():
    n = Normalizer()
    assert n.normalize("Vivo Empresas") == "VIVO EMPRESAS"


def test_remove_accents():
    n = Normalizer()
    assert n.normalize("TELEFÔNICA BRASIL") == "TELEFONICA BRASIL"


def test_remove_suffix_ltda():
    n = Normalizer()
    assert n.normalize("EMPRESA EXEMPLO LTDA") == "EMPRESA EXEMPLO"


def test_remove_suffix_sa():
    n = Normalizer()
    assert n.normalize("TELEFONICA BRASIL S.A.") == "TELEFONICA BRASIL"


def test_remove_suffix_eireli():
    n = Normalizer()
    assert n.normalize("CONSULTORIA ABC EIRELI") == "CONSULTORIA ABC"


def test_remove_suffix_me():
    n = Normalizer()
    assert n.normalize("PADARIA DOIS IRMAOS ME") == "PADARIA DOIS IRMAOS"


def test_remove_prefix_pix():
    n = Normalizer()
    assert n.normalize("PIX - TELEFONICA BRASIL") == "TELEFONICA BRASIL"


def test_remove_prefix_pagamento():
    n = Normalizer()
    assert n.normalize("Pagamento PIX - VIVO EMPRESAS S.A.") == "VIVO EMPRESAS"


def test_remove_prefix_ted():
    n = Normalizer()
    assert n.normalize("TED BANCO DO BRASIL") == "BANCO DO BRASIL"


def test_remove_special_characters():
    n = Normalizer()
    assert n.normalize("VIVO S.A. (EMPRESA)") == "VIVO EMPRESA"


def test_collapse_spaces():
    n = Normalizer()
    assert n.normalize("VIVO   EMPRESAS  S.A.") == "VIVO EMPRESAS"


def test_full_pipeline():
    n = Normalizer()
    result = n.normalize("Pagamento PIX - TELEFONICA BRASIL S.A.")
    assert result == "TELEFONICA BRASIL"


def test_empty_string():
    n = Normalizer()
    assert n.normalize("") == ""
    assert n.normalize("   ") == ""


def test_name_with_cnpj():
    n = Normalizer()
    result = n.normalize("EMPRESA EXEMPLO CNPJ 00.000.000/0001-00")
    assert "CNPJ" not in result


def test_name_with_date():
    n = Normalizer()
    result = n.normalize("FATURA VIVO 03/2026")
    assert result == "FATURA VIVO"


def test_is_empty_after_normalization():
    n = Normalizer()
    assert n.is_empty_after_normalization("PIX")
    assert not n.is_empty_after_normalization("VIVO")


def test_numeric_value_embedded():
    n = Normalizer()
    result = n.normalize("BOLETO 001234 R$ 150,00")
    assert "R$" not in result


def test_multiple_suffixes():
    n = Normalizer()
    result = n.normalize("EMPRESA EXEMPLO LTDA ME")
    assert "LTDA" not in result
    assert "ME" not in result


def test_prefix_with_hyphen():
    n = Normalizer()
    assert n.normalize("TED - BANCO DO BRASIL") == "BANCO DO BRASIL"
    assert n.normalize("PIX - VIVO EMPRESAS") == "VIVO EMPRESAS"


def test_sa_in_middle():
    n = Normalizer()
    assert n.normalize("VIVO S.A. (EMPRESA)") == "VIVO EMPRESA"


def test_normalize_preserves_relevant_numbers():
    n = Normalizer()
    result = n.normalize("AGUA 123 LTDA")
    assert result == "AGUA 123"


def test_multiple_prefixes():
    n = Normalizer()
    result = n.normalize("Pagamento PIX VIVO EMPRESAS")
    assert result == "VIVO EMPRESAS"


def test_raw_name_with_slash():
    n = Normalizer()
    assert n.normalize("SABESP S/A") == "SABESP"


def test_raw_name_case_variations():
    n = Normalizer()
    assert n.normalize("vivo empresa ltda") == "VIVO EMPRESA"
    assert n.normalize("Vivo Empresa Ltda") == "VIVO EMPRESA"
