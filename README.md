# ContaClass

Classificação contábil inteligente — do histórico ao lançamento em segundos.

Automatiza a classificação de lançamentos contábeis usando busca exata e fuzzy
matching, eliminando o retrabalho manual de consulta ao histórico.

---

## Fase 1 — Script CLI Python

### Funcionalidades

- **Leitura de arquivo histórico** (.xlsx / .xls) com múltiplas abas
- **Detecção automática** de colunas (Data, Débito, Crédito, Valor, Fornecedor)
- **Consolidação** e indexação dos lançamentos por fornecedor
- **Classificação automática** de novos lançamentos:
  - Correspondência exata → Confirmado
  - Correspondência fuzzy → Revisar (com score)
  - Sem correspondência → Não Encontrado
- **Exportação Excel colorido** (verde/amarelo/vermelho) + relatório

### Stack

| Tecnologia | Versão |
|-----------|--------|
| Python | 3.11+ |
| Click | 8.x |
| OpenPyXL | 3.x |
| Pandas | 2.x |
| RapidFuzz | 3.x |

### Instalação

```bash
pip install contaclass
```

### Uso

```bash
# Processamento completo
contaclass --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx

# Threshold personalizado
contaclass --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx --threshold 65

# Listar abas do histórico
contaclass --historico hist.xlsx --listar-abas
```

---

## Roadmap

| Fase | Período | Entrega |
|------|---------|---------|
| 1 | Meses 1-2 | Script CLI Python |
| 2 | Meses 3-6 | Aplicação Web SaaS |
| 3 | Meses 7-9 | Aprendizado Contínuo |
| 4 | Meses 10-15 | IA de Classificação |
