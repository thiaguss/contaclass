from pathlib import Path

import openpyxl
import pytest
from click.testing import CliRunner

from contaclass.cli import main


@pytest.fixture
def hist_xlsx(tmp_path):
    path = tmp_path / "historico.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "BB"
    ws.append(["Data", "Cod Débito", "Cod Crédito", "Valor", "Fornecedor"])
    ws.append(["01/01/2026", "503", "101", 1500.00, "VIVO"])
    ws.append(["15/01/2026", "504", "102", 850.00, "CEMIG"])
    wb.save(path)
    wb.close()
    return path


@pytest.fixture
def novo_xlsx(tmp_path):
    path = tmp_path / "novo.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Data", "Valor", "Fornecedor"])
    ws.append(["01/02/2026", 1500.00, "VIVO"])
    ws.append(["05/02/2026", 900.00, "CEMIG"])
    ws.append(["10/02/2026", 500.00, "EMPRESA XYZ"])
    wb.save(path)
    wb.close()
    return path


def test_listar_abas(hist_xlsx):
    runner = CliRunner()
    result = runner.invoke(main, ["listar-abas", "--historico", str(hist_xlsx)])
    assert result.exit_code == 0
    assert "BB" in result.output


def test_processar_completo(hist_xlsx, novo_xlsx, tmp_path):
    saida = tmp_path / "resultado.xlsx"
    runner = CliRunner()
    result = runner.invoke(main, [
        "processar",
        "--historico", str(hist_xlsx),
        "--novo", str(novo_xlsx),
        "--saida", str(saida),
    ])
    assert result.exit_code == 0
    assert saida.exists()


def test_processar_threshold_personalizado(hist_xlsx, novo_xlsx, tmp_path):
    saida = tmp_path / "resultado.xlsx"
    runner = CliRunner()
    result = runner.invoke(main, [
        "processar",
        "--historico", str(hist_xlsx),
        "--novo", str(novo_xlsx),
        "--saida", str(saida),
        "--threshold", "50",
    ])
    assert result.exit_code == 0
    assert saida.exists()


def test_processar_historico_inexistente(novo_xlsx, tmp_path):
    saida = tmp_path / "resultado.xlsx"
    runner = CliRunner()
    result = runner.invoke(main, [
        "processar",
        "--historico", "nao_existe.xlsx",
        "--novo", str(novo_xlsx),
        "--saida", str(saida),
    ])
    assert result.exit_code != 0
    assert "Erro" in result.output


def test_processar_novo_inexistente(hist_xlsx, tmp_path):
    saida = tmp_path / "resultado.xlsx"
    runner = CliRunner()
    result = runner.invoke(main, [
        "processar",
        "--historico", str(hist_xlsx),
        "--novo", "nao_existe.xlsx",
        "--saida", str(saida),
    ])
    assert result.exit_code != 0
    assert "Erro" in result.output


def test_processar_com_abas(hist_xlsx, novo_xlsx, tmp_path):
    saida = tmp_path / "resultado.xlsx"
    runner = CliRunner()
    result = runner.invoke(main, [
        "processar",
        "--historico", str(hist_xlsx),
        "--novo", str(novo_xlsx),
        "--saida", str(saida),
        "--abas", "BB",
    ])
    assert result.exit_code == 0
    assert saida.exists()


def test_listar_abas_arquivo_inexistente():
    runner = CliRunner()
    result = runner.invoke(main, ["listar-abas", "--historico", "nao_existe.xlsx"])
    assert result.exit_code != 0
    assert "Erro" in result.output


def test_versao():
    runner = CliRunner()
    result = runner.invoke(main, ["versao"])
    assert result.exit_code == 0
    assert "ContaClass" in result.output
