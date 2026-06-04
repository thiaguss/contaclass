# ContaClass

Classificação contábil inteligente — do histórico ao lançamento em segundos.

Automatiza a classificação de lançamentos contábeis usando busca exata e fuzzy
matching, eliminando o retrabalho manual de consulta ao histórico.

---

## Fase 1 — Script CLI Python

### Funcionalidades

- **Leitura de arquivo histórico** (.xlsx / .xls) com múltiplas abas
- **Detecção automática** de colunas por alias (Data, Débito, Crédito, Valor, Fornecedor)
- **Normalização** de nomes de fornecedores (uppercase, remoção de acentos, prefixos genéricos, sufixos)
- **Consolidação** e indexação dos lançamentos por fornecedor
- **Classificação automática** de novos lançamentos em 3 camadas:
  - Correspondência exata (Score 100% → Confirmado)
  - Correspondência fuzzy (Score 50-99% → Revisar) — 3 algoritmos RapidFuzz
  - Sem correspondência (< threshold → Não Encontrado)
- **Motor de confiança** com 7 fatores de ajuste contextuais
- **Exportação Excel colorido** (verde/amarelo/vermelho) + aba de resumo

### Stack

| Tecnologia | Uso |
|-----------|------|
| Python 3.11+ | Runtime |
| Click | CLI framework |
| OpenPyXL + Pandas | Leitura/escrita Excel |
| RapidFuzz | Fuzzy matching (3 algoritmos) |
| Unidecode | Remoção de acentos |

### Instalação

```bash
pip install contaclass
```

### Uso

```bash
# Processamento completo
contaclass processar --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx

# Threshold personalizado (padrão: 70)
contaclass processar --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx --threshold 65

# Listar abas do histórico
contaclass listar-abas --historico hist.xlsx

# Filtrar abas específicas do histórico
contaclass processar --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx --abas "Banco do Brasil,Santander"

# Estratégia de desempate: mais recente (padrão: mais frequente)
contaclass processar --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx --estrategia most_recent

# Exibir versão
contaclass versao
```

### Estrutura do Projeto

```
src/contaclass/
├── cli.py               # Interface CLI (Click)
├── core/
│   ├── normalizer.py    # Normalização de nomes (RN01)
│   ├── exact_match.py   # Busca exata (RF05)
│   ├── fuzzy_match.py   # Fuzzy matching (RF07)
│   ├── score.py         # Motor de confiança (RF08)
│   └── classifier.py    # Orquestrador do fluxo
├── io/
│   ├── excel_reader.py  # Leitura Excel multi-aba (RF01/RF02)
│   └── excel_writer.py  # Exportação Excel colorido (RF10/RF11)
└── models/
    ├── entry.py         # Dataclasses de entrada
    └── result.py        # Dataclasses de resultado
```

---

## Roadmap

| Fase | Período | Entrega | Status |
|------|---------|---------|--------|
| 1 | Meses 1-2 | Script CLI Python | ✅ Concluído |
| 2 | Meses 3-6 | Aplicação Web SaaS | 📅 Próximo |
| 3 | Meses 7-9 | Aprendizado Contínuo | ⏳ Futuro |
| 4 | Meses 10-15 | IA de Classificação | ⏳ Futuro |

---

## Licença

Propriedade ContaClass — confidencial.
