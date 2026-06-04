# Guia de Uso — ContaClass Fase 1

**Versão:** 0.1.0
**Última atualização:** Junho de 2026

---

## 1. Visão Geral

O ContaClass Fase 1 é um script CLI Python que classifica automaticamente lançamentos contábeis novos usando um arquivo histórico de referência. O sistema:

1. Lê um Excel histórico com lançamentos já classificados (múltiplas abas/bancos)
2. Lê um Excel novo com apenas Data, Valor e Fornecedor
3. Classifica cada linha usando busca exata e fuzzy matching
4. Exporta um Excel colorido com o resultado e uma aba de resumo

---

## 2. Pré-requisitos

| Requisito | Versão |
|-----------|--------|
| Python | 3.11 ou superior |
| pip | Última versão |
| Sistema operacional | Windows 10+, macOS 10.15+, Ubuntu 20.04+ |

---

## 3. Instalação

### 3.1 Instalação para uso (produção)

```bash
pip install contaclass
```

### 3.2 Instalação para desenvolvimento

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd ContaClass

# Criar ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Instalar em modo editável com dependências de teste
pip install -e ".[test]"

# Rodar os testes para validar
pytest tests/ -v
```

---

## 4. Comandos da CLI

### 4.1 Processar lançamentos

```bash
contaclass processar --historico <arquivo_hist.xlsx> --novo <arquivo_novo.xlsx> --saida <resultado.xlsx>
```

**Opções:**

| Opção | Abreviação | Padrão | Descrição |
|-------|-----------|--------|-----------|
| --historico | -h | obrigatório | Caminho do arquivo Excel histórico |
| --novo | -n | obrigatório | Caminho do arquivo Excel novo |
| --saida | -s | obrigatório | Caminho para salvar o resultado |
| --threshold | -t | 70 | Score mínimo para sugestão automática |
| --abas | -a | todas | Filtrar abas do histórico (separadas por vírgula) |
| --estrategia | -e | most_frequent | Desempate: most_frequent ou most_recent |
| --preview | - | False | Exibir preview antes de processar |

**Exemplos:**

```bash
# Processamento básico
contaclass processar -h historico.xlsx -n novo.xlsx -s resultado.xlsx

# Com threshold personalizado
contaclass processar -h historico.xlsx -n novo.xlsx -s resultado.xlsx -t 65

# Apenas abas específicas
contaclass processar -h historico.xlsx -n novo.xlsx -s resultado.xlsx -a "Banco do Brasil,Santander"

# Com estratégia de mais recente
contaclass processar -h historico.xlsx -n novo.xlsx -s resultado.xlsx -e most_recent

# Com preview interativo
contaclass processar -h historico.xlsx -n novo.xlsx -s resultado.xlsx --preview
```

### 4.2 Listar abas do histórico

```bash
contaclass listar-abas --historico <arquivo_hist.xlsx>
```

### 4.3 Exibir versão

```bash
contaclass versao
```

---

## 5. Formato dos Arquivos de Entrada

### 5.1 Arquivo Histórico

O arquivo histórico deve ser um Excel (.xlsx ou .xls) com pelo menos 5 colunas:

| Coluna | Descrição | Obrigatória |
|--------|-----------|:-----------:|
| Data | Data do lançamento | Sim |
| Cod Débito | Código da conta contábil de débito | Sim |
| Cod Crédito | Código da conta contábil de crédito | Sim |
| Valor | Valor monetário do lançamento | Sim |
| Fornecedor | Nome do fornecedor/beneficiário | Sim |

Detalhes:
- O arquivo pode ter múltiplas abas (uma por banco ou conta)
- Cada aba representa um banco/conta diferente
- O sistema detecta automaticamente as colunas pelos nomes dos cabeçalhos
- Abas vazias ou com menos de 2 linhas são ignoradas

Exemplo de estrutura:

```
+--------------+-----------+-------------+----------+----------------+
| Data         | Cod Débito| Cod Crédito | Valor    | Fornecedor     |
+--------------+-----------+-------------+----------+----------------+
| 01/01/2026   | 503       | 101         | 1500,00  | VIVO           |
| 15/01/2026   | 504       | 102         | 850,00   | CEMIG          |
| 20/01/2026   | 505       | 103         | 2200,00  | EQUATORIAL     |
+--------------+-----------+-------------+----------+----------------+
```

### 5.2 Arquivo Novo

O arquivo novo deve ser um Excel (.xlsx ou .xls) com pelo menos 3 colunas:

| Coluna | Descrição | Obrigatória |
|--------|-----------|:-----------:|
| Data | Data do lançamento | Sim |
| Valor | Valor monetário do lançamento | Sim |
| Fornecedor | Nome do fornecedor/beneficiário | Sim |

Exemplo de estrutura:

```
+--------------+----------+----------------+
| Data         | Valor    | Fornecedor     |
+--------------+----------+----------------+
| 01/02/2026   | 1500,00  | VIVO           |
| 05/02/2026   | 900,00   | CEMIG          |
| 10/02/2026   | 500,00   | EMPRESA NOVA   |
+--------------+----------+----------------+
```

---

## 6. Aliases de Colunas Reconhecidos

O sistema detecta automaticamente as colunas pelos seguintes nomes (case-insensitive):

**Data:** Data, Date, Dt, Lançamento, Lancamento

**Cod Débito:** Cod Débito, Cod Debito, Código Débito, Codigo Debito, Débito, Debito, CD

**Cod Crédito:** Cod Crédito, Cod Credito, Código Crédito, Codigo Credito, Crédito, Credito, CC

**Valor:** Valor, Value, Val, Vlr

**Fornecedor:** Fornecedor, Fornecedores, Favorecido, Beneficiário, Beneficiario, Descrição, Descricao, Desc, Nome, Histórico, Historico

> Dica: Se os cabeçalhos do seu Excel não forem reconhecidos, o sistema tenta inferir as colunas pela posição (1ª = Data, 2ª = Valor, 3ª = Fornecedor).

---

## 7. Workflow Passo a Passo

### 7.1 Preparar os arquivos

1. **Arquivo histórico:** exporte do seu sistema contábil os lançamentos já classificados de períodos anteriores. Certifique-se de que tem as colunas: Data, Cod Débito, Cod Crédito, Valor e Fornecedor.

2. **Arquivo novo:** exporte os lançamentos novos a serem classificados. Precisa ter apenas: Data, Valor e Fornecedor.

### 7.2 Listar abas (opcional)

```bash
contaclass listar-abas -h historico.xlsx
```

### 7.3 Processar

```bash
contaclass processar -h historico.xlsx -n novo.xlsx -s resultado.xlsx
```

### 7.4 Revisar o resultado

O sistema exibirá um resumo:

```
Resultado:
   Confirmados:    72
   Revisar:        9
   Nao Encontrados: 4
   Automacao:      84.7%
   Tempo:          3240ms
```

### 7.5 Abrir o Excel de resultado

O arquivo resultado.xlsx contém:

- **Aba "Classificacao":** todas as linhas com status colorido
  - Verde: Confirmado (match exato, Score 100%)
  - Amarelo: Revisar (fuzzy match, Score 50-99%)
  - Vermelho: Nao Encontrado (Score < threshold)
- **Aba "Resumo":** estatísticas do processamento (total, confirmados, revisar, taxa de automação, tempo)

### 7.6 Revisar itens amarelos e vermelhos

Abra o Excel e filtre por status "Revisar" e "Nao Encontrado". Esses são os únicos itens que precisam de intervenção manual — tipicamente 5-15% do total.

---

## 8. Opções de Configuração

### 8.1 Threshold de Confiança

Controla o score mínimo para que uma sugestão fuzzy seja aceita automaticamente.

| Threshold | Comportamento |
|-----------|---------------|
| 50 | Mais permissivo — aceita matches com score mais baixo |
| 70 (padrão) | Equilibrado — bom para a maioria dos casos |
| 85 | Mais rigoroso — menos falsos positivos |

```bash
contaclass processar -h hist.xlsx -n novo.xlsx -s res.xlsx -t 50
```

### 8.2 Estratégia de Desempate

Quando um fornecedor aparece no histórico com múltiplos pares de código:

| Estratégia | Comportamento |
|-----------|---------------|
| most_frequent (padrão) | Usa o par de códigos que aparece com mais frequência |
| most_recent | Usa o par de códigos do último lançamento registrado |

```bash
contaclass processar -h hist.xlsx -n novo.xlsx -s res.xlsx -e most_recent
```

### 8.3 Filtro de Abas

```bash
contaclass processar -h hist.xlsx -n novo.xlsx -s res.xlsx -a "Banco do Brasil,Santander"
```

---

## 9. Exemplo Prático

### Cenário

Um escritório de contabilidade precisa classificar 85 lançamentos do mês usando um histórico com 200 lançamentos em 2 abas.

### Execução

```bash
# Listar abas disponíveis
contaclass listar-abas -h historico.xlsx

# Processar
contaclass processar -h historico.xlsx -n lancamentos_novos.xlsx -s classificado.xlsx

# Ou com opções
contaclass processar -h historico.xlsx -n lancamentos_novos.xlsx -s classificado.xlsx -t 65 -a "Banco do Brasil,Santander"
```

### Resultado Esperado

```
Resultado:
   Confirmados:    72
   Revisar:        9
   Nao Encontrados: 4
   Automacao:      84.7%
   Tempo:          3240ms
```

---

## 10. Solução de Problemas

| Erro | Causa | Solução |
|------|-------|---------|
| Arquivo não encontrado | Caminho incorreto | Verifique o caminho completo do arquivo |
| Nenhum lançamento lido | Cabeçalhos não reconhecidos | Verifique os nomes das colunas ou use listar-abas |
| Não foi possível interpretar a data | Formato não suportado | Use: DD/MM/AAAA, AAAA-MM-DD ou MM/DD/AAAA |
| Não foi possível interpretar o valor | Formato inválido | Use vírgula como decimal (1500,00) ou ponto (1500.00) |
| Taxa de automação muito baixa | Histórico insuficiente | Verifique se o histórico está completo; abaixe o threshold |
| Muitos falsos positivos | Threshold muito baixo | Aumente o threshold (ex: de 70 para 85) |

---

## 11. Limitações da Fase 1

- Sem persistência: os dados não são salvos entre execuções
- Sem autenticação: qualquer pessoa com acesso ao terminal pode usar
- Sem interface web: apenas CLI
- Sem aprendizado: o sistema não melhora com correções (Fase 3)
- Sem IA: apenas regras e fuzzy matching (Fase 4)
- Tamanho limite: arquivos até 10 MB (expandível na Fase 2)

---

Documento gerado por: Equipe ContaClass
Fase 1 — v0.1.0
