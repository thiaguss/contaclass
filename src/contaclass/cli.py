import sys
from pathlib import Path

import click

from contaclass.core.classifier import Classifier
from contaclass.core.normalizer import Normalizer
from contaclass.io.excel_reader import ExcelReader
from contaclass.io.excel_writer import ExcelWriter


@click.group()
def main():
    pass


@main.command()
@click.option("--historico", "-h", required=True, help="Caminho do arquivo Excel histórico (.xlsx)")
@click.option("--novo", "-n", required=True, help="Caminho do arquivo Excel novo (.xlsx)")
@click.option("--saida", "-s", required=True, help="Caminho para salvar o Excel classificado")
@click.option("--threshold", "-t", default=70.0, type=float, help="Threshold mínimo de score (padrão: 70)")
@click.option("--abas", "-a", default=None, help="Filtrar abas do histórico (separadas por vírgula)")
@click.option("--estrategia", "-e", default="most_frequent", type=click.Choice(["most_frequent", "most_recent"]),
              help="Estratégia para múltiplos códigos")
@click.option("--preview", is_flag=True, help="Exibir preview do arquivo novo antes de processar")
def processar(historico, novo, saida, threshold, abas, estrategia, preview):
    """Processa um arquivo novo usando o histórico e exporta o resultado."""
    hist_path = Path(historico)
    novo_path = Path(novo)
    saida_path = Path(saida)

    if not hist_path.exists():
        click.echo(f"Erro: Arquivo histórico não encontrado: {hist_path}", err=True)
        sys.exit(1)
    if not novo_path.exists():
        click.echo(f"Erro: Arquivo novo não encontrado: {novo_path}", err=True)
        sys.exit(1)

    tab_filter = abas.split(",") if abas else None

    click.echo("📂 Lendo histórico...")
    reader = ExcelReader(hist_path)
    historical_entries = reader.read_historical(tab_filter=tab_filter)
    click.echo(f"   → {len(historical_entries)} lançamentos históricos encontrados")

    if preview:
        click.echo("\n📋 Preview do arquivo novo:")
        preview_data = ExcelReader(novo_path).preview_new(n_rows=10)
        for i, row in enumerate(preview_data, 1):
            click.echo(f"   {i:3d}. {row['entry_date']:12s} {row['amount']:>10s}  {row['supplier']}")
        if not click.confirm("\n   Confirmar mapeamento e continuar?"):
            click.echo("Processamento cancelado.")
            sys.exit(0)

    click.echo("📂 Lendo arquivo novo...")
    new_entries = ExcelReader(novo_path).read_new()
    click.echo(f"   → {len(new_entries)} lançamentos a classificar")

    click.echo("\n⚙️  Classificando...")
    classifier = Classifier(threshold=threshold, code_strategy=estrategia)
    batch = classifier.process(
        new_entries=new_entries,
        historical_entries=historical_entries,
    )

    click.echo(f"\n📊 Resultado:")
    click.echo(f"   ✅ Confirmados:    {batch.confirmed_count}")
    click.echo(f"   ⚠️  Revisar:       {batch.review_count}")
    click.echo(f"   ❌ Não Encontrados: {batch.not_found_count}")
    click.echo(f"   📈 Automação:      {batch.automation_rate:.1f}%")
    click.echo(f"   ⏱️  Tempo:         {batch.processing_time_ms}ms")

    click.echo(f"\n💾 Exportando Excel...")
    writer = ExcelWriter(threshold=threshold)
    writer.write(
        batch=batch,
        output_path=saida_path,
        client_name=saida_path.stem,
    )
    click.echo(f"   → {saida_path.resolve()}")


@main.command()
@click.option("--historico", "-h", required=True, help="Caminho do arquivo Excel histórico (.xlsx)")
def listar_abas(historico):
    """Lista as abas encontradas no arquivo histórico."""
    hist_path = Path(historico)
    if not hist_path.exists():
        click.echo(f"Erro: Arquivo não encontrado: {hist_path}", err=True)
        sys.exit(1)

    reader = ExcelReader(hist_path)
    tabs = reader.list_tabs()
    click.echo(f"Abas encontradas em {historico}:")
    for tab in tabs:
        click.echo(f"   📄 {tab['name']} ({tab['rows']} linhas)")


@main.command()
def versao():
    """Exibe a versão do ContaClass."""
    from importlib.metadata import version
    try:
        v = version("contaclass")
    except Exception:
        v = "0.1.0"
    click.echo(f"ContaClass v{v}")
