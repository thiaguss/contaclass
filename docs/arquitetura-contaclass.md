# Analise Arquitetural — ContaClass

**Versao do documento:** 1.0
**Referencia:** ContaClass_PRD_v1.0.md
**Data:** Junho de 2026

---

## 1. Estrutura de Pastas Proposta

```
contaclass/
├── src/
│   └── contaclass/
│       ├── __init__.py
│       ├── __main__.py          # Suporte a python -m contaclass
│       ├── cli.py               # Interface CLI (Click)
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── normalizer.py    # Pipeline de normalizacao (RN01)
│       │   ├── exact_match.py   # Busca exata + SupplierIndex (RF05)
│       │   ├── fuzzy_match.py   # 3 algoritmos RapidFuzz (RF07)
│       │   ├── score.py         # Motor de confianca + 7 fatores (RF08)
│       │   └── classifier.py    # Orquestrador do fluxo completo
│       │
│       ├── io/
│       │   ├── __init__.py
│       │   ├── excel_reader.py  # Leitura multi-aba + deteccao de colunas (RF01/RF02)
│       │   └── excel_writer.py  # Exportacao Excel colorido (RF10/RF11)
│       │
│       └── models/
│           ├── __init__.py
│           ├── entry.py         # HistoricalEntry, NewEntry
│           └── result.py        # MatchResult, ProcessingBatchResult
│
├── tests/
│   ├── __init__.py
│   ├── test_normalizer.py       # 24 testes
│   ├── test_exact_match.py      # 8 testes
│   ├── test_fuzzy_match.py      # 13 testes
│   ├── test_score.py            # 13 testes
│   ├── test_classifier.py       # 9 testes
│   ├── test_excel_reader.py     # 11 testes
│   ├── test_excel_writer.py     # 7 testes
│   └── test_cli.py              # 8 testes
│
├── data/
│   └── fixtures/
│
├── docs/
│   ├── guiadeusagem-fase1.md
│   └── arquitetura-contaclass.md
│
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## 2. Modulos do Sistema

### Modulo 1 — Normalizacao (core/normalizer.py)
**Responsabilidade:** Padronizar nomes de fornecedores antes de comparacao.

**Pipeline (RN01):**
1. Uppercase
2. Remocao de acentos (Unidecode)
3. Remocao de termos genericos (CNPJ, CPF + digitos)
4. Remocao de sufixos (S.A., LTDA, EIRELI, ME, EPP, S/A, CIA...)
5. Remocao de prefixos (PIX, PGTO, TED, DOC, TRANSF...)
6. Remocao de caracteres especiais
7. Colapsar espacos multiplos

**Entrada:** "Pagamento PIX - TELEFONICA BRASIL S.A."
**Saida:** "TELEFONICA BRASIL"

---

### Modulo 2 — Leitura Excel (io/excel_reader.py)
**Responsabilidade:** Ler, detectar colunas e consolidar dados de multiplas abas.

**Funcionalidades (RF01/RF02/RF03):**
- Leitura de arquivos .xlsx e .xls
- Deteccao automatica de colunas por aliases ou posicao
- Consolidacao em base indexada por fornecedor normalizado
- Ignorar abas vazias ou com < 2 linhas
- Preview das primeiras N linhas

---

### Modulo 3 — Busca Exata (core/exact_match.py)
**Responsabilidade:** Match identico de fornecedor normalizado.

**Funcionalidades (RF05):**
- SupplierIndex: indexa fornecedores por nome normalizado
- ExactMatcher: busca por correspondencia exata (Score = 100%)
- Resolucao de codigos por frequencia ou recencia (RN02)
- Suporte a multiplos pares de codigo por fornecedor

---

### Modulo 4 — Fuzzy Matching (core/fuzzy_match.py)
**Responsabilidade:** Similaridade aproximada entre nomes.

**Funcionalidades (RF07):**
- 3 algoritmos RapidFuzz ponderados:
  - Levenshtein Ratio (35%) — erros de digitacao
  - Token Sort Ratio (35%) — variacoes de ordem
  - Partial Ratio (30%) — substrings
- Threshold configuravel (padrao: 50%)
- Retorna top-N correspondencias com breakdown de scores

---

### Modulo 5 — Motor de Confianca (core/score.py)
**Responsabilidade:** Calcular e ajustar score de confianca.

**Funcionalidades (RF08/Secao 16):**
- Score base (fuzzy) + 7 fatores de ajuste contextuais:
  - Frequencia do par de codigos (+5%)
  - Recencia (+3%)
  - Consistencia (+7%)
  - Valor similar (+3%)
  - Mes recorrente (+5%)
  - Correcao anterior (+10%)
  - Inconsistencia (-10%)
- Classificacao por status: Confirmado (>=100%), Revisar (50-99%), Nao Encontrado (<50%)
- Breakdown explicavel (Secao 16.4)

---

### Modulo 6 — Classificador (core/classifier.py)
**Responsabilidade:** Orquestrar o fluxo completo de classificacao.

**Fluxo:**
1. Normalizar nome do fornecedor
2. Busca exata no indice -> se encontrado: Score=100%, Status="confirmed"
3. Busca fuzzy (top 1) -> calcular score com fatores contextuais
4. Se score >= threshold -> preencher codigos sugeridos, Status="review"
5. Se score < threshold -> Status="not_found"
6. Processar todas as linhas e retornar ProcessingBatchResult

---

### Modulo 7 — Exportacao Excel (io/excel_writer.py)
**Responsabilidade:** Gerar Excel classificado com cores e formatacao.

**Funcionalidades (RF10/RF11):**
- Aba "Classificacao" com linhas coloridas:
  - Verde (#C6EFCE): Confirmado
  - Amarelo (#FFEB9C): Revisar
  - Vermelho (#FFC7CE): Nao Encontrado
- Aba "Resumo" com estatisticas
- Colunas: #, Data, Fornecedor, Valor, Cod Debito, Cod Credito, Status, Score, Match, Sugestao Fuzzy
- Largura de colunas auto-ajustada

---

### Modulo 8 — CLI (cli.py)
**Responsabilidade:** Interface de linha de comando.

**Comandos (Fase 1):**
- contaclass processar — Processar arquivo novo com historico
- contaclass listar-abas — Listar abas do arquivo historico
- contaclass versao — Exibir versao

---

## 3. Fluxo do Sistema

### Fluxo Completo (Fase 1 — CLI)

```
Usuario executa contaclass CLI
        |
        v
Leitura do arquivo historico (ExcelReader)
        |
        v
Consolidacao no SupplierIndex
        |
        v
Leitura do arquivo novo (ExcelReader)
        |
        v
Para cada linha do arquivo novo:
  1. Normalizar fornecedor (Normalizer)
  2. Busca exata no SupplierIndex
     -> Encontrou? Score=100%, Confirmado
     -> Nao encontrou? Fuzzy
  3. Busca fuzzy (FuzzyMatcher)
  4. Calcular score final (ScoreEngine)
  5. Classificar: Confirmado, Revisar ou Nao Encontrado
        |
        v
Exportacao Excel colorido (ExcelWriter)
```

### Fluxo Futuro (Fase 2 — Web)

```
Browser (Next.js)
    |
    +--> FastAPI Backend
    |       Auth Service (JWT)
    |       Clients Service
    |       History Service
    |       Processing Service --> Celery Worker --> Classification Engine
    |       Export Service
    |       Audit Service
    |
    +--> PostgreSQL (dados)
    +--> Redis (cache + filas)
    +--> MinIO/S3 (arquivos)
    +--> WebSocket (progresso em tempo real)
```

---

## 4. Dependencias

### Fase 1 — Script CLI (Atual)

| Dependencia | Uso | Versao |
|---|---|---|
| python | Runtime | >= 3.11 |
| click | CLI framework | 8.x |
| openpyxl | Leitura/escrita Excel .xlsx | 3.x |
| xlrd | Leitura Excel .xls (legado) | 2.x |
| pandas | Manipulacao de dados tabulares | 2.x |
| rapidfuzz | Fuzzy matching | 3.x |
| unidecode | Remocao de acentos | 1.x |
| pytest | Testes unitarios | 8.x |
| pytest-cov | Cobertura de codigo | 5.x |

### Fase 2 — Aplicacao Web (Futuro)

| Dependencia | Uso | Versao |
|---|---|---|
| fastapi | API REST + WebSocket | 0.110+ |
| uvicorn | ASGI server | 0.29+ |
| sqlalchemy | ORM | 2.0 |
| alembic | Migrations | 1.x |
| psycopg2 | Driver PostgreSQL | 2.9 |
| redis | Cache + Celery broker | 5.x |
| celery | Task queue assincrona | 5.x |
| python-jose | JWT tokens | 3.x |
| passlib + bcrypt | Hash de senhas | — |
| boto3 / minio | S3-compatible storage | — |
| chardet | Deteccao de encoding | 5.x |
| next.js | Frontend React (App Router) | 14+ |
| tailwindcss | CSS utility-first | 3.x |
| shadcn/ui | Componentes UI | — |
| docker + docker-compose | Containerizacao | — |
| postgresql | Banco de dados | 15+ |
| redis | Cache + fila | 7+ |

### Fase 3 — Aprendizado (Futuro)

| Dependencia | Uso |
|---|---|
| scikit-learn | Re-treinamento de regras |

### Fase 4 — IA (Futuro)

| Dependencia | Uso |
|---|---|
| sentence-transformers | Embeddings semanticos |
| onnxruntime | Inferencia em producao |
| pgvector | Busca vetorial no PostgreSQL |
| huggingface-hub | Fine-tuning |

---

## 5. Ordem de Implementacao

### Fase 1 — Script CLI (Meses 1-2) CONCLUIDO

| # | Tarefa | Dias | Modulos |
|---|--------|------|---------|
| 1 | Setup do projeto | 0.5 | — |
| 2 | normalizer.py — Pipeline de normalizacao | 2 | Modulo 1 |
| 3 | excel_reader.py — Leitura multi-aba | 1 | Modulo 2 |
| 4 | entry.py / result.py — Modelos de dados | 0.5 | — |
| 5 | exact_match.py — Busca exata | 1 | Modulo 3 |
| 6 | fuzzy_match.py — 3 algoritmos ponderados | 3 | Modulo 4 |
| 7 | score.py — Motor de confianca | 2 | Modulo 5 |
| 8 | classifier.py — Orquestracao do fluxo | 1 | Modulo 6 |
| 9 | excel_writer.py — Exportacao colorida | 2 | Modulo 7 |
| 10 | cli.py — Interface Click | 1 | Modulo 8 |
| 11 | Testes unitarios (>=80% cobertura) | 4 | Todos |
| 12 | Documentacao + empacotamento | 2 | — |
| **Total** | | **~18 dias** | |

### Fase 2 — Aplicacao Web (Meses 3-6)

| # | Tarefa | Dias | Modulos |
|---|--------|------|---------|
| 13 | Setup Docker + CI/CD + Alembic | 5 | Infra |
| 14 | Models SQLAlchemy (9 tabelas) | 3 | Modelos |
| 15 | Auth service + JWT + bcrypt | 5 | Modulo 8 |
| 16 | Multi-tenancy middleware (RLS) | 3 | Modulo 9 |
| 17 | API clients (CRUD) | 3 | — |
| 18 | API history (upload + processamento async) | 5 | Modulo 10 |
| 19 | Celery tasks | 5 | Modulo 10 |
| 20 | API batches | 5 | Modulo 10 |
| 21 | WebSocket progresso | 3 | Modulo 10 |
| 22 | API exportacao | 3 | Modulo 7 |
| 23 | Audit service + middleware | 2 | Modulo 11 |
| 24 | Refactor core engine | 3 | Modulos 1-6 |
| 25 | Setup Next.js + shadcn/ui | 5 | — |
| 26 | Tela de login + onboarding | 3 | — |
| 27 | Dashboard | 3 | — |
| 28 | Gestao de clientes | 5 | — |
| 29 | Fluxo de processamento (4 passos) | 10 | — |
| 30 | Tela de resultados + correcao inline | 8 | — |
| 31 | Download Excel + filtros | 2 | — |
| 32 | Testes E2E + QA | 10 | Todos |
| 33 | Deploy staging + producao | 3 | Infra |
| 34 | Billing Stripe | 5 | — |
| **Total** | | **~80 dias** | |

### Fase 3 — Aprendizado (Meses 7-9)

| # | Tarefa | Dias | Modulos |
|---|--------|------|---------|
| 35 | Tabela corrections + API | 3 | Modulo 12 |
| 36 | Interface de correcao inline | 5 | Modulo 12 |
| 37 | Pipeline de re-indexacao | 4 | Modulo 12 |
| 38 | Analise de erros sistematicos | 5 | Modulo 12 |
| 39 | Notificacoes ao usuario | 3 | Modulo 12 |
| 40 | Exportacao do dicionario | 2 | Modulo 12 |
| **Total** | | **~22 dias** | |

### Fase 4 — IA (Meses 10-15)

| # | Tarefa | Dias | Modulos |
|---|--------|------|---------|
| 41 | Coleta e preparacao de dados | 20 | Modulo 13 |
| 42 | Fine-tuning Sentence Transformers | 25 | Modulo 13 |
| 43 | Integracao pgvector | 8 | Modulo 13 |
| 44 | API de predicao ONNX Runtime | 8 | Modulo 13 |
| 45 | Dashboard de performance | 5 | Modulo 13 |
| **Total** | | **~66 dias** | |

---

## 6. Dependencias entre Fases

```
Fase 1 (CLI) CONCLUIDO
     |
     |  Code reuse: normalizer, fuzzy, score,
     |  excel_engine refactorados para Fase 2
     v
Fase 2 (Web) ----------------+
     |                        |
     |  Dados acumulados:     |
     |  fornecedores, codigos,|
     |  correcoes             |
     v                        |
Fase 3 (Learning) -----------+
     |
     |  Pares fornecedor->codigo acumulados ->
     |  dataset de treino para embeddings
     v
Fase 4 (IA)
```

---

## 7. Requisitos Funcionais Implementados (Fase 1)

| RF | Descricao | Status |
|----|-----------|--------|
| RF01 | Upload de arquivo historico (.xlsx/.xls) | CONCLUIDO |
| RF02 | Leitura automatica de multiplas abas | CONCLUIDO |
| RF03 | Consolidacao de lancamentos historicos | CONCLUIDO |
| RF04 | Upload de planilha nova (.xlsx/.xls) | CONCLUIDO |
| RF05 | Busca exata de fornecedor | CONCLUIDO |
| RF06 | Preenchimento automatico de Debito e Credito | CONCLUIDO |
| RF07 | Busca por similaridade (fuzzy matching) | CONCLUIDO |
| RF08 | Score de confianca | CONCLUIDO |
| RF09 | Coluna de Status | CONCLUIDO |
| RF10 | Colorizacao automatica do Excel exportado | CONCLUIDO |
| RF11 | Exportacao do Excel final | CONCLUIDO |
| RF12 | Cadastro de clientes | Fase 2 |
| RF13 | Aprendizado por correcao | Fase 3 |
| RF14 | Sugestao por IA | Fase 4 |

---

## 8. Regras de Negocio Implementadas

| RN | Descricao | Status |
|----|-----------|--------|
| RN01 | Normalizacao de nomes | CONCLUIDO |
| RN02 | Criterio de desempate em multiplos codigos | CONCLUIDO |
| RN03 | Threshold de confianca para preenchimento | CONCLUIDO |
| RN04 | Unicidade do processamento | Fase 2 |
| RN05 | Isolamento por tenant | Fase 2 |
| RN06 | Versionamento de historico | Fase 2 |
| RN07 | Auditoria obrigatoria | Fase 2 |
| RN08 | Dados financeiros (Decimal, ISO 8601) | CONCLUIDO |

---

Documento gerado por: Equipe ContaClass
Analise arquitetural baseada no PRD v1.0
