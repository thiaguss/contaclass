# ContaClass — PRD: Sistema de Automação de Classificação Contábil

**Versão:** 1.0  
**Data:** Junho de 2026  
**Classificação:** Confidencial  
**Autores:** Equipe de Produto · ContaClass  
**Status:** Aprovado para Desenvolvimento

---

## Sumário

1. Visão Geral do Produto
2. Problema
3. Solução
4. Personas
5. Fluxo Atual (AS IS)
6. Fluxo Futuro (TO BE)
7. Requisitos Funcionais
8. Requisitos Não Funcionais
9. Casos de Uso
10. Regras de Negócio
11. Arquitetura Técnica
12. Modelagem de Dados
13. Estrutura do Banco de Dados
14. API Design
15. Estratégia de Similaridade
16. Estratégia de Confiança
17. Roadmap
18. MVP
19. Critérios de Aceite
20. Wireframes Textuais
21. Riscos
22. Possíveis Diferenciais Competitivos
23. Estimativa de Complexidade
24. Estratégia de Monetização SaaS
25. Integrações Futuras com ERPs

---

# 1. Visão Geral do Produto

## 1.1 Identidade do Produto

**Nome do Produto:** ContaClass  
**Tagline:** *"Classificação contábil inteligente, do histórico ao lançamento em segundos."*  
**Categoria:** Automação de Processos Contábeis / FinTech B2B  
**Público-Alvo Primário:** Escritórios de contabilidade de pequeno e médio porte (PME)  
**Público-Alvo Secundário:** Departamentos financeiros internos de empresas  

## 1.2 Declaração de Visão

Tornar o ContaClass a ferramenta padrão de automação de classificação contábil para escritórios de contabilidade brasileiros, eliminando o retrabalho manual, reduzindo erros humanos e possibilitando que contadores dediquem seu tempo a atividades de maior valor intelectual e estratégico.

## 1.3 Proposta de Valor

O ContaClass automatiza em segundos o que hoje um colaborador leva minutos ou horas para realizar: consultar o histórico de lançamentos, identificar o fornecedor, buscar os códigos de débito e crédito corretos e montar a planilha final classificada. Com engine de inteligência artificial e aprendizado contínuo, o sistema se torna mais preciso quanto mais é utilizado.

## 1.4 Objetivos Estratégicos

- Reduzir em pelo menos 80% o tempo gasto em classificação manual de lançamentos
- Atingir taxa de acerto automático superior a 90% nos fornecedores recorrentes
- Tornar-se plataforma SaaS recorrente para escritórios de contabilidade no Brasil
- Construir base de dados de inteligência contábil proprietária como moat competitivo

---

# 2. Problema

## 2.1 Contexto Operacional

Nos escritórios de contabilidade, uma das atividades mais repetitivas e operacionais é a classificação contábil de lançamentos bancários. A cada período fiscal (semanal, quinzenal ou mensal), o colaborador responsável recebe dois arquivos:

1. Um arquivo Excel histórico com lançamentos já classificados de períodos anteriores, frequentemente dividido em múltiplas abas (uma por banco ou conta)
2. Um arquivo Excel novo contendo apenas data, valor e fornecedor — sem nenhuma classificação

O colaborador então precisa, para cada linha do arquivo novo, abrir o histórico, localizar o mesmo fornecedor, copiar os códigos de débito e crédito, e preencher a planilha manualmente. Esse processo se repete dezenas a centenas de vezes por cliente, por mês.

## 2.2 Quantificação do Problema

Considerando um escritório de contabilidade de porte médio com:

- 20 clientes ativos
- Média de 80 lançamentos mensais por cliente = 1.600 lançamentos/mês
- Tempo médio por lançamento (busca + cópia + ajuste) = 2 minutos
- **Total: 3.200 minutos/mês = 53 horas/mês perdidas em classificação manual**

Para um colaborador com custo total de R$ 4.000/mês, o custo por hora é R$ 25. Logo:

- **Custo mensal do processo manual: R$ 1.333/mês por escritório**
- **Custo anual: R$ 16.000/ano por escritório**

## 2.3 Problemas Identificados

**P01 — Alta repetição manual:** A grande maioria dos fornecedores são recorrentes e possuem sempre os mesmos códigos. Ainda assim, o colaborador precisa buscá-los individualmente a cada ciclo.

**P02 — Variação de nomenclatura:** O mesmo fornecedor pode aparecer com nomes diferentes nos extratos bancários. Exemplos reais observados:

- VIVO / TELEFONICA BRASIL / VIVO EMPRESAS / CLARO SERV / NET SERV
- CEMIG / CEMIG DISTRIBUICAO / ENERGISA / EQUATORIAL ENERGIA
- BB FINANCIAMENTOS / BANCO DO BRASIL SA / BB CREDITO

**P03 — Erro humano:** Classificações erradas geram retrabalho futuro, inconsistência no balancete e possíveis problemas fiscais.

**P04 — Escalabilidade limitada:** Quanto mais clientes o escritório atende, maior a carga operacional — sem automação, o crescimento exige contratação proporcional.

**P05 — Perda de contexto histórico:** Quando um colaborador sai da empresa, o conhecimento acumulado sobre fornecedores e classificações vai junto.

**P06 — Ausência de rastreabilidade:** Não há log de quem classificou, quando e com qual critério — dificultando auditorias internas.

## 2.4 Impacto no Negócio

- Tempo improdutivo dos colaboradores mais experientes
- Risco de inconsistência fiscal entre períodos
- Baixa escalabilidade operacional do escritório
- Dificuldade de crescer a carteira sem aumentar custos operacionais

---

# 3. Solução

## 3.1 Visão da Solução

O ContaClass é um sistema que ingere o arquivo histórico de lançamentos classificados do cliente, constrói uma base interna de conhecimento por fornecedor, e ao receber um novo arquivo de lançamentos, classifica automaticamente cada linha utilizando três camadas de inteligência:

1. **Correspondência exata:** Busca idêntica do nome do fornecedor no histórico
2. **Correspondência fuzzy:** Algoritmo de similaridade de strings para variações de nomenclatura
3. **Inteligência artificial:** Modelo treinado com padrões de fornecedor, valor, frequência e categoria contábil (Fase 4)

## 3.2 Como Funciona (Resumo Funcional)

**Passo 1:** Usuário faz upload do arquivo Excel histórico (múltiplas abas/bancos)  
**Passo 2:** Sistema consolida todos os lançamentos e indexa por fornecedor  
**Passo 3:** Usuário faz upload do arquivo novo (apenas data, valor, fornecedor)  
**Passo 4:** Sistema processa cada linha:  

- Se encontrar correspondência exata → classifica como "Confirmado" (verde)
- Se encontrar similaridade ≥ 70% → classifica como "Revisar" (amarelo) com score
- Se não encontrar → marca como "Não Encontrado" (vermelho)

**Passo 5:** Sistema exporta Excel completo colorido + relatório de confiança  
**Passo 6:** Usuário revisa apenas os itens amarelos e vermelhos (minoria)

## 3.3 Benefícios Mensuráveis

| Benefício | Situação Atual | Com ContaClass |
|-----------|---------------|----------------|
| Tempo de classificação | 2 min/lançamento | < 5 seg/lançamento |
| Taxa de erro humano | 3-5% | < 0,5% |
| Lançamentos revisados manualmente | 100% | 5-15% (apenas dúvidas) |
| Escalabilidade | Linear com headcount | Desacoplada do headcount |
| Consistência histórica | Depende da memória do colaborador | 100% baseada em dados |

---

# 4. Personas

## 4.1 Persona 1 — Auxiliar/Analista Contábil Operacional

**Nome fictício:** Carla, 27 anos  
**Cargo:** Auxiliar Contábil  
**Empresa:** Escritório de contabilidade com 15 clientes  

**Contexto:** Carla passa boa parte do dia em atividades repetitivas de classificação. Tem experiência básica com Excel e está familiarizada com os sistemas contábeis da empresa. Sente frustração com tarefas mecânicas e tem vontade de aprender atividades de maior valor.

**Dores:**
- Perde horas por dia fazendo classificações que poderiam ser automáticas
- Fica ansiosa com o risco de errar a classificação de um fornecedor desconhecido
- Precisa interromper o fluxo constantemente para consultar o histórico
- Quando um cliente manda um extrato diferente do padrão, não sabe como proceder

**Objetivos com o ContaClass:**
- Terminar as classificações em minutos ao invés de horas
- Ter segurança de que as classificações estão corretas
- Poder revisar apenas os casos duvidosos

**Nível de Proficiência Técnica:** Médio (Excel, sistemas web básicos)

---

## 4.2 Persona 2 — Contador Sênior / Supervisor

**Nome fictício:** Rodrigo, 38 anos  
**Cargo:** Contador Sênior / Supervisor de Equipe  
**Empresa:** Escritório com 3 colaboradores e 25 clientes  

**Contexto:** Rodrigo é o responsável técnico pelas classificações e pela qualidade do trabalho. Supervisa a equipe e faz a conferência final das planilhas antes de importar no sistema contábil. Tem visão do negócio e preocupação com crescimento.

**Dores:**
- Tem que revisar tudo que a equipe faz porque os erros chegam na fase final
- Não consegue crescer sua carteira de clientes sem contratar mais pessoas
- Perde tempo valioso em conferência de itens óbvios
- Quando um colaborador sai, ele perde o conhecimento acumulado sobre os clientes

**Objetivos com o ContaClass:**
- Ter confiança de que 90%+ dos lançamentos estão corretos automaticamente
- Poder crescer a carteira sem aumentar headcount na mesma proporção
- Ter rastreabilidade de quem classificou o quê e quando
- Focar seu tempo em consultoria e análise, não em conferência operacional

**Nível de Proficiência Técnica:** Médio-alto (Excel avançado, sistemas contábeis)

---

## 4.3 Persona 3 — Sócio/Gestor do Escritório

**Nome fictício:** Fernanda, 45 anos  
**Cargo:** Sócia-Gestora  
**Empresa:** Escritório contábil com 8 colaboradores e 60 clientes  

**Contexto:** Fernanda administra o escritório e toma decisões de investimento em tecnologia. Foca em eficiência operacional, satisfação dos clientes e rentabilidade. Avalia ferramentas com base em ROI claro.

**Dores:**
- Custo operacional crescente que corrói a margem do escritório
- Dificuldade de precificar adequadamente por falta de visibilidade do tempo gasto
- Clientes que reclamam de erros nas classificações
- Dependência de pessoas-chave que concentram conhecimento

**Objetivos com o ContaClass:**
- Reduzir custo operacional sem demitir colaboradores (realocar para atividades de valor)
- Ter dashboards de produtividade e erros
- Poder oferecer serviço mais rápido e confiável aos clientes
- Reduzir o risco operacional pela concentração de conhecimento em pessoas

**Nível de Proficiência Técnica:** Baixo-médio (prefere relatórios e dashboards)

---

## 4.4 Persona 4 — Controller / Analista Financeiro (Cliente Final)

**Nome fictício:** Paulo, 35 anos  
**Cargo:** Controller em empresa de médio porte  
**Empresa:** Indústria com departamento financeiro interno  

**Contexto:** Paulo gerencia o processo de classificação contábil internamente, sem terceirizar para escritório. Busca ferramentas para ganhar eficiência no fechamento mensal.

**Dores:**
- Fechamento mensal é sempre corrido e com muito trabalho manual
- Tem que treinar constantemente novos analistas nas regras de classificação
- Erros de classificação causam retrabalho no fechamento e ajustes no balancete

---

# 5. Fluxo Atual (AS IS)

## 5.1 Diagrama do Fluxo Atual

```
[Cliente] → Envia extrato bancário (Excel/PDF/CSV)
     ↓
[Colaborador] → Recebe arquivo com: Data | Valor | Fornecedor
     ↓
[Colaborador] → Abre arquivo histórico Excel (múltiplas abas)
     ↓
[Colaborador] → Para cada linha do arquivo novo:
   ├── Lê o nome do fornecedor
   ├── Vai até a aba correspondente do banco no histórico
   ├── Usa Ctrl+F para buscar o fornecedor
   ├── Se encontrar → copia Cod Débito e Cod Crédito
   ├── Se NÃO encontrar → pesquisa em outras abas
   ├── Se ainda não encontrar → consulta supervisor ou plano de contas
   ├── Preenche a linha na nova planilha
   └── Ajusta data e valor
     ↓
[Colaborador] → Revisa a planilha completa
     ↓
[Supervisor] → Confere a planilha
     ↓
[Colaborador] → Importa no sistema contábil (ex: Domínio, Alterdata, Questor)
```

## 5.2 Análise de Tempo por Etapa

| Etapa | Tempo Médio | Percentual do Total |
|-------|------------|---------------------|
| Abertura dos arquivos e organização | 5 min | 5% |
| Busca manual de cada fornecedor | 90 min (para 80 lançamentos) | 60% |
| Preenchimento das colunas | 30 min | 20% |
| Revisão própria | 15 min | 10% |
| Revisão do supervisor | 10 min | 7% |
| Ajustes pós-revisão | 5 min | 3% |
| **Total por cliente/mês** | **~155 min** | 100% |

## 5.3 Pontos de Falha Identificados

- **FH01:** Fornecedor não encontrado no histórico → classificação incorreta ou omitida
- **FH02:** Nome diferente do fornecedor → colaborador não reconhece como o mesmo
- **FH03:** Erro de digitação ao copiar os códigos → erro silencioso difícil de detectar
- **FH04:** Abas do histórico desatualizadas → classificação baseada em dado obsoleto
- **FH05:** Acúmulo de lançamentos por atraso → pressa aumenta a taxa de erro
- **FH06:** Dependência de pessoa-chave com conhecimento tácito

---

# 6. Fluxo Futuro (TO BE)

## 6.1 Diagrama do Fluxo com ContaClass

```
[Cliente] → Envia extrato bancário
     ↓
[Colaborador] → Acessa ContaClass
     ↓
[Sistema] → Upload do histórico (Fase Inicial: por cliente)
     │       OU recupera histórico já processado anteriormente
     ↓
[ContaClass] → Processa e indexa todas as abas automaticamente
     ↓
[Colaborador] → Upload do arquivo novo (Data | Valor | Fornecedor)
     ↓
[ContaClass] → Processa cada linha automaticamente:
   ├── Busca exata → "Confirmado" (verde) → preenche Débito e Crédito
   ├── Busca fuzzy (score ≥ 70%) → "Revisar" (amarelo) → preenche com sugestão
   └── Não encontrado → "Não Encontrado" (vermelho) → aguarda input manual
     ↓
[ContaClass] → Gera Excel classificado com cores + relatório de confiança
     ↓
[Colaborador] → Revisa APENAS itens amarelos e vermelhos (5-15%)
     ↓
[ContaClass] → Aprende com as correções manuais (Fase 3)
     ↓
[Colaborador] → Exporta planilha final e importa no sistema contábil
```

## 6.2 Comparativo AS IS vs TO BE

| Dimensão | AS IS | TO BE |
|----------|-------|-------|
| Tempo total por cliente/mês | ~155 min | ~20 min |
| % lançamentos revisados manualmente | 100% | 5-15% |
| Taxa de erro estimada | 3-5% | < 0,5% |
| Dependência de pessoa-chave | Alta | Baixa |
| Rastreabilidade | Nenhuma | Total |
| Aprendizado institucional | Pessoal/informal | Sistemático/digital |
| Escalabilidade | Linear | Exponencial |

## 6.3 Benefício Financeiro Estimado por Escritório

| Perfil do Escritório | Economia Mensal (h) | Economia Anual (R$) |
|---------------------|--------------------|--------------------|
| Pequeno (10 clientes) | ~22 h | R$ 6.600 |
| Médio (30 clientes) | ~65 h | R$ 19.500 |
| Grande (80 clientes) | ~170 h | R$ 51.000 |

*Custo por hora = R$ 25. Economia sobre 75% do tempo de classificação.*

---

# 7. Requisitos Funcionais

## RF01 — Upload de Arquivo Histórico

**Descrição:** O sistema deve permitir que o usuário faça upload de um arquivo Excel (.xlsx, .xls) contendo os lançamentos históricos já classificados.

**Critérios:**
- Aceitar arquivos nos formatos .xlsx e .xls
- Tamanho máximo por arquivo: 50 MB (Fase 1: 10 MB)
- Exibir progresso de upload em tempo real
- Validar se o arquivo é um Excel válido antes de processar
- Exibir mensagem de erro clara se o formato for inválido

**Prioridade:** Must Have

---

## RF02 — Leitura Automática de Múltiplas Abas

**Descrição:** O sistema deve detectar e ler automaticamente todas as abas do Excel histórico, sem necessidade de configuração manual.

**Critérios:**
- Listar todas as abas encontradas com nome e número de linhas
- Ler cada aba independentemente
- Identificar automaticamente qual coluna é Data, Cod Débito, Cod Crédito, Valor e Fornecedor (por nome ou posição)
- Permitir mapeamento manual de colunas caso a detecção automática falhe
- Ignorar abas vazias ou com menos de 2 linhas

**Prioridade:** Must Have

---

## RF03 — Consolidação de Lançamentos Históricos

**Descrição:** Após a leitura de todas as abas, o sistema deve consolidar todos os lançamentos em uma base interna única, indexada por fornecedor.

**Critérios:**
- Consolidar dados de todas as abas em uma estrutura única
- Indexar por nome do fornecedor (normalizado: uppercase, sem acentos, sem espaços duplos)
- Manter a origem (qual aba/banco) como metadado
- Exibir resumo: total de lançamentos consolidados, fornecedores únicos, período coberto
- Persistir a base no banco de dados vinculada ao cliente

**Prioridade:** Must Have

---

## RF04 — Upload de Planilha Nova

**Descrição:** O sistema deve permitir upload da planilha nova contendo apenas Data, Valor e Fornecedor.

**Critérios:**
- Aceitar .xlsx, .xls e .csv
- Detectar automaticamente as colunas de Data, Valor e Fornecedor
- Exibir preview das primeiras 10 linhas antes de processar
- Confirmar ou corrigir mapeamento de colunas antes do processamento
- Validar que todas as linhas possuem data e valor preenchidos

**Prioridade:** Must Have

---

## RF05 — Busca Exata de Fornecedor

**Descrição:** Para cada fornecedor da planilha nova, o sistema deve realizar busca exata no histórico consolidado.

**Critérios:**
- Comparação case-insensitive e sem acentos
- Remover caracteres especiais para comparação (ex: ponto, hífen)
- Se encontrar correspondência exata → atribuir Score 100%
- Preencher automaticamente Cod Débito e Cod Crédito
- Marcar status como "Confirmado"

**Prioridade:** Must Have

---

## RF06 — Preenchimento Automático de Débito e Crédito

**Descrição:** Quando houver correspondência (exata ou fuzzy com score ≥ configurável), o sistema deve preencher automaticamente os campos Cod Débito e Cod Crédito.

**Critérios:**
- Para correspondência exata: preencher sem questionamento
- Para fuzzy match: preencher com código mais frequente do fornecedor similar
- Quando houver múltiplos códigos para o mesmo fornecedor no histórico: usar o mais recente ou o mais frequente (configurável)
- Registrar qual entrada histórica foi usada como referência

**Prioridade:** Must Have

---

## RF07 — Busca por Similaridade (Fuzzy Matching)

**Descrição:** Para fornecedores não encontrados por busca exata, o sistema deve aplicar algoritmo de fuzzy matching para identificar correspondências parciais.

**Critérios:**
- Algoritmo primário: RapidFuzz / Levenshtein Distance
- Algoritmo complementar: Token Sort Ratio (para variações na ordem das palavras)
- Algoritmo complementar: Partial Ratio (para substrings)
- Score resultante: média ponderada dos algoritmos
- Threshold mínimo para sugestão: 50% (configurável pelo usuário)
- Exibir as 3 principais correspondências com seus scores
- Aplicar pré-processamento: uppercase, remoção de acentos, remoção de termos genéricos (S.A., LTDA, EIRELI, ME, EPP)

**Prioridade:** Must Have

---

## RF08 — Score de Confiança

**Descrição:** O sistema deve calcular e exibir um score de confiança (0-100%) para cada classificação.

**Critérios:**
- Score 100%: correspondência exata
- Score 70-99%: fuzzy match com alta similaridade
- Score 50-69%: fuzzy match com similaridade moderada
- Score < 50%: não sugerido (marcado como "Não Encontrado")
- O score deve ser exibido como porcentagem na planilha exportada e na interface
- Score pode considerar múltiplos fatores (ver Seção 16)

**Prioridade:** Must Have

---

## RF09 — Coluna de Status

**Descrição:** O sistema deve adicionar uma coluna "Status" na planilha de saída.

**Critérios:**
- "Confirmado" → correspondência exata (Score = 100%)
- "Revisar" → correspondência fuzzy (Score 50-99%)
- "Não Encontrado" → sem correspondência (Score < 50%)
- A coluna deve conter também o score numérico
- Deve ser possível filtrar por status na interface web

**Prioridade:** Must Have

---

## RF10 — Colorização Automática do Excel Exportado

**Descrição:** O arquivo Excel exportado deve ter colorização automática por status.

**Critérios:**
- Verde (#C6EFCE / texto #276221): Status "Confirmado"
- Amarelo (#FFEB9C / texto #9C6500): Status "Revisar"
- Vermelho (#FFC7CE / texto #9C0006): Status "Não Encontrado"
- Colorização aplicada na linha inteira (não apenas na célula de status)
- Compatível com Excel, LibreOffice e Google Sheets

**Prioridade:** Must Have

---

## RF11 — Exportação do Excel Final

**Descrição:** O sistema deve exportar o Excel final com toda a estrutura esperada, pronto para importação ou conferência.

**Critérios:**
- Colunas: Data | Cod Débito | Cod Crédito | Valor | Fornecedor | Status | Score | Sugestão Fuzzy
- Manter formatação de data original
- Manter formatação de valores monetários (R$ com 2 casas decimais)
- Nome do arquivo sugerido: `[NomeCliente]_classificado_[AAAA-MM]_[timestamp].xlsx`
- Incluir aba de "Resumo" com estatísticas do processamento
- Download direto pelo browser (Fase 2)

**Prioridade:** Must Have

---

## RF12 — Cadastro de Clientes (Fase 2)

**Descrição:** O sistema deve permitir o cadastro e gestão de múltiplos clientes por escritório contábil.

**Prioridade:** Should Have (Fase 2)

---

## RF13 — Aprendizado por Correção (Fase 3)

**Descrição:** Quando o usuário corrigir uma classificação sugerida, o sistema deve registrar a correção e utilizá-la em processamentos futuros.

**Prioridade:** Should Have (Fase 3)

---

## RF14 — Sugestão por IA (Fase 4)

**Descrição:** Modelo de IA que sugere classificação baseado em padrões multimodais (fornecedor, valor, frequência, sazonalidade, categoria).

**Prioridade:** Nice to Have (Fase 4)

---

# 8. Requisitos Não Funcionais

## RNF01 — Performance

- Processamento de 100 lançamentos em menos de 10 segundos
- Processamento de 1.000 lançamentos em menos de 60 segundos
- Upload de arquivo de até 10MB deve completar em menos de 5 segundos (conexão padrão)
- Tempo de resposta da API < 500ms para endpoints de leitura
- Tempo de resposta da API < 3s para endpoints de processamento

## RNF02 — Disponibilidade

- SLA de 99,5% de disponibilidade (máximo 3,6 horas de downtime/mês)
- Janela de manutenção programada: domingos 02h-04h (horário de Brasília)
- Health check endpoint disponível para monitoramento externo

## RNF03 — Segurança

- Autenticação via JWT com expiração em 8 horas
- Refresh token com expiração em 30 dias
- HTTPS obrigatório em todas as comunicações
- Dados de clientes isolados por tenant (multi-tenant seguro)
- Arquivos enviados armazenados em bucket privado com URL temporária (presigned URL)
- Arquivos excluídos após 30 dias ou conforme política do usuário
- Conformidade com LGPD: dados processados apenas para a finalidade declarada
- Log de auditoria para todas as ações de processamento

## RNF04 — Escalabilidade

- Arquitetura stateless para escalar horizontalmente
- Processamento assíncrono para arquivos grandes (filas)
- Suporte a pelo menos 100 usuários simultâneos (Fase 2)

## RNF05 — Usabilidade

- Interface responsiva para desktop e tablet (mínimo 1024px)
- Fluxo completo (upload → exportar) em no máximo 5 cliques
- Mensagens de erro em linguagem humana (sem códigos técnicos)
- Tutorial de onboarding com 3 passos para novo usuário
- Suporte a idioma: Português Brasileiro (pt-BR)

## RNF06 — Manutenibilidade

- Cobertura de testes unitários ≥ 80%
- Documentação da API via OpenAPI/Swagger
- Código versionado em Git com conventional commits
- CI/CD automatizado com deploy em staging antes de produção

## RNF07 — Compatibilidade

- Excel: .xlsx e .xls (versões 2007 em diante)
- CSV: UTF-8 e ISO-8859-1 (Latin-1)
- Browsers suportados: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- Sistema operacional (Fase 1): Windows 10+, macOS 10.15+, Ubuntu 20.04+

## RNF08 — Confiabilidade

- Zero perda de dados em caso de falha durante processamento (transações atômicas)
- Processamentos falhos devem ser reexecutáveis sem efeitos colaterais
- Logs de erro persistidos por 90 dias

---

# 9. Casos de Uso

## UC01 — Processar Planilha de Novos Lançamentos

**Ator Principal:** Auxiliar/Analista Contábil  
**Pré-condição:** Usuário autenticado; histórico do cliente já carregado no sistema  

**Fluxo Principal:**
1. Usuário acessa a tela de processamento
2. Seleciona o cliente
3. Faz upload do arquivo novo
4. Sistema detecta colunas automaticamente
5. Usuário confirma o mapeamento
6. Sistema processa e exibe resultado em tempo real
7. Usuário visualiza tabela com status por linha
8. Usuário faz download do Excel classificado

**Fluxo Alternativo A — Mapeamento manual de colunas:**  
4a. Sistema não detecta colunas com confiança  
4b. Exibe interface de mapeamento manual  
4c. Usuário seleciona qual coluna é Data, Valor e Fornecedor  
4d. Retorna ao passo 5

**Fluxo Alternativo B — Histórico não carregado:**  
2b. Sistema alerta que não há histórico para o cliente selecionado  
2c. Usuário faz upload do histórico antes de continuar

---

## UC02 — Carregar Histórico de Lançamentos

**Ator Principal:** Auxiliar/Analista Contábil  
**Pré-condição:** Cliente já cadastrado no sistema  

**Fluxo Principal:**
1. Usuário acessa a gestão do cliente
2. Seleciona "Carregar Histórico"
3. Faz upload do arquivo Excel histórico
4. Sistema lista as abas encontradas
5. Usuário confirma as abas a serem processadas (todas por padrão)
6. Sistema processa e exibe resumo: N abas, X lançamentos, Y fornecedores únicos
7. Histórico disponível para processamento

---

## UC03 — Revisar e Corrigir Classificações

**Ator Principal:** Auxiliar/Analista Contábil ou Supervisor  
**Pré-condição:** Processamento concluído com itens "Revisar" ou "Não Encontrado"  

**Fluxo Principal:**
1. Usuário acessa a tela de resultados
2. Filtra por status "Revisar" e/ou "Não Encontrado"
3. Para cada item, visualiza a sugestão do sistema
4. Aceita a sugestão (score amarelo) OU
5. Corrige manualmente digitando os códigos corretos
6. Sistema registra a correção no banco de aprendizado (Fase 3)
7. Usuário exporta planilha após revisão

---

## UC04 — Configurar Regras de Similaridade

**Ator Principal:** Supervisor/Gestor  
**Pré-condição:** Usuário com perfil de administrador  

**Fluxo Principal:**
1. Usuário acessa configurações do escritório
2. Navega até "Regras de Classificação"
3. Ajusta threshold mínimo de score para sugestão automática (padrão: 70%)
4. Define política para múltiplos códigos: "mais recente" ou "mais frequente"
5. Configura termos a ignorar na normalização (ex: "PGTO", "PIX", "TED")
6. Salva configurações
7. As próximas classificações usam as novas regras

---

## UC05 — Visualizar Relatório de Produtividade (Fase 2)

**Ator Principal:** Gestor/Sócio  
**Pré-condição:** Pelo menos 30 dias de uso do sistema  

**Fluxo Principal:**
1. Gestor acessa o dashboard
2. Visualiza: total de lançamentos processados, taxa de automação, taxa de revisão manual
3. Compara desempenho por colaborador, por cliente, por período
4. Exporta relatório em PDF ou Excel

---

# 10. Regras de Negócio

## RN01 — Normalização de Nomes

Antes de qualquer busca, os nomes de fornecedores devem ser normalizados:
- Converter para maiúsculas (UPPERCASE)
- Remover acentos (á→a, ê→e, etc.)
- Remover caracteres especiais exceto letras, números e espaço
- Substituir múltiplos espaços por um único espaço
- Remover termos genéricos de sufixo: S.A., SA, LTDA, EIRELI, ME, EPP, CNPJ, CPF
- Remover prefixos genéricos de transação: PGTO, PIX, TED, DOC, TRANSF, PAG

**Exemplo:**  
Entrada: "Pagamento PIX - TELEFONICA BRASIL S.A."  
Normalizado: "TELEFONICA BRASIL"

## RN02 — Critério de Desempate em Múltiplos Códigos

Quando um fornecedor possui mais de um par (Cod Débito, Cod Crédito) no histórico:
- Regra padrão: usar o par mais frequente
- Regra alternativa (configurável): usar o par mais recente
- Quando há empate de frequência: usar o mais recente
- Registrar no log quando houve desempate

## RN03 — Threshold de Confiança para Preenchimento Automático

- Score ≥ 100%: preenche automaticamente, marca como "Confirmado"
- Score ≥ 70% e < 100%: preenche com sugestão, marca como "Revisar"
- Score < 70% (threshold padrão): não preenche, marca como "Não Encontrado"
- O threshold de 70% é o padrão configurável pelo escritório

## RN04 — Unicidade do Processamento

- Cada arquivo novo processado gera um "lote" único com ID, data/hora, usuário e cliente
- Reprocessar o mesmo arquivo gera um novo lote separado (não sobrescreve)
- O usuário pode visualizar histórico de todos os lotes

## RN05 — Isolamento por Tenant

- Dados de clientes de um escritório nunca são acessíveis por outro escritório
- O histórico de um cliente é estritamente privado ao escritório que o carregou
- Não há compartilhamento de base de fornecedores entre tenants (diferente da Fase 4, onde modelos globais poderão ser treinados com dados anonimizados)

## RN06 — Versionamento de Histórico

- Cada upload de histórico cria uma nova versão, não sobrescreve a anterior
- O sistema usa o histórico mais recente por padrão
- O usuário pode reverter para uma versão anterior

## RN07 — Auditoria Obrigatória

- Todo processamento deve ser registrado com: timestamp, usuário, arquivo processado, número de linhas, taxa de automação, tempo de processamento
- Correções manuais devem registrar: usuário que corrigiu, timestamp, código anterior, código novo

## RN08 — Dados Financeiros

- Valores monetários devem ser tratados como Decimal com 2 casas (nunca float)
- Datas devem ser armazenadas em formato ISO 8601 (YYYY-MM-DD) internamente
- Exibição de data no formato brasileiro (DD/MM/YYYY) na interface

---

# 11. Arquitetura Técnica

## 11.1 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUÁRIO (Browser)                        │
│                    Next.js Frontend (Fase 2)                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTPS / REST / WebSocket
┌───────────────────────────▼─────────────────────────────────────┐
│                    API Gateway / Load Balancer                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    FastAPI Backend (Fase 2)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Auth Service │  │ Upload Svc   │  │  Classification Svc  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Export Svc   │  │ Audit Svc    │  │   Learning Svc (F3)  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└──────┬────────────────────┬────────────────────┬────────────────┘
       │                    │                    │
┌──────▼──────┐   ┌─────────▼──────┐   ┌────────▼───────┐
│ PostgreSQL  │   │ Redis Cache    │   │ S3-Compatible  │
│ (Dados)     │   │ (Sessão/Fila)  │   │ Storage        │
└─────────────┘   └────────────────┘   └────────────────┘
```

## 11.2 Stack Tecnológico

### Fase 1 — Script Local

| Componente | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Runtime | Python 3.11+ | Ecossistema rico para dados e NLP |
| Leitura Excel | OpenPyXL + Pandas | Padrão industria para manipulação Excel |
| Fuzzy Matching | RapidFuzz | Mais rápido que FuzzyWuzzy, mesma API |
| Exportação Excel | OpenPyXL | Suporte nativo a cores e formatação |
| CLI | Click | Interface de linha de comando elegante |

### Fase 2 — Aplicação Web

| Componente | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Frontend | Next.js 14+ (App Router) | SSR, performance, ecossistema React |
| UI Components | Tailwind CSS + shadcn/ui | Produtividade e consistência visual |
| Backend | FastAPI (Python 3.11+) | Performance assíncrona, OpenAPI nativo |
| ORM | SQLAlchemy 2.0 + Alembic | Migrations, type safety |
| Banco de Dados | PostgreSQL 15+ | ACID, JSON support, performance |
| Cache | Redis 7+ | Sessões, filas de processamento |
| Storage | MinIO (self-hosted) / AWS S3 | Armazenamento de arquivos |
| Autenticação | JWT + bcrypt | Padrão seguro e stateless |
| Task Queue | Celery + Redis | Processamento assíncrono de arquivos |
| Containerização | Docker + Docker Compose | Portabilidade e deploy simplificado |

### Fase 3 — Aprendizado

| Componente | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Armazenamento de correções | PostgreSQL (tabela de feedback) | ACID, relacionamento com processamentos |
| Re-treinamento | Python scripts + scikit-learn | Pipeline simples para ajuste de regras |

### Fase 4 — IA

| Componente | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Modelo Base | Sentence Transformers (BERT) | Embeddings semânticos para fornecedores |
| Fine-tuning | Python + HuggingFace | Adaptação ao domínio contábil |
| Serving | FastAPI + ONNX Runtime | Inferência rápida em produção |
| Armazenamento de Vetores | pgvector (extensão PostgreSQL) | Busca por similaridade vetorial |

## 11.3 Padrões de Design

- **API:** RESTful com versionamento (/api/v1/)
- **Autenticação:** Bearer Token (JWT)
- **Comunicação em tempo real:** WebSocket para progresso de processamento
- **Tratamento de erros:** RFC 7807 (Problem Details for HTTP APIs)
- **Logs:** Estruturado em JSON (compatible com ELK Stack)
- **Multi-tenancy:** Row-Level Security no PostgreSQL

---

# 12. Modelagem de Dados

## 12.1 Diagrama Conceitual

```
Escritório (1) ──────< (N) Usuário
Escritório (1) ──────< (N) Cliente
Cliente (1) ──────────< (N) HistóricoVersão
HistóricoVersão (1) ──< (N) LançamentoHistórico
LançamentoHistórico (N) >──< (1) Fornecedor
Fornecedor (N) >──────< (N) ParCodigoContabil
Cliente (1) ──────────< (N) Lote
Lote (1) ──────────────< (N) LançamentoProcessado
LançamentoProcessado (N) >──< (1) Fornecedor
Usuário (1) ──────────< (N) Correção
Correção (N) >──────────< (1) LançamentoProcessado
```

## 12.2 Entidades Principais

### Escritório (Office)
Representa o escritório de contabilidade (tenant principal)

### Cliente (Client)
Empresa cliente do escritório, para quem as classificações são realizadas

### Fornecedor (Supplier)
Entidade que aparece nos lançamentos bancários (ex: VIVO, EQUATORIAL)

### ParCodigoContábil (AccountingCodePair)
Combinação de Código Débito + Código Crédito associada a um fornecedor

### HistóricoVersão (HistoryVersion)
Uma versão do arquivo histórico carregado para um cliente

### LançamentoHistórico (HistoricalEntry)
Linha individual de um arquivo histórico (já classificado)

### Lote (ProcessingBatch)
Um processamento de arquivo novo — agrupa todos os lançamentos processados naquele momento

### LançamentoProcessado (ProcessedEntry)
Linha do arquivo novo após processamento, com status e score

### Correção (Correction)
Registro de correção manual feita pelo usuário (base do aprendizado)

---

# 13. Estrutura do Banco de Dados

## 13.1 DDL Completo

```sql
-- ================================================================
-- SCHEMA: contaclass
-- ================================================================

CREATE SCHEMA IF NOT EXISTS contaclass;
SET search_path TO contaclass;

-- ================================================================
-- TABELA: offices (escritórios — tenants)
-- ================================================================
CREATE TABLE offices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(200) NOT NULL,
    cnpj            VARCHAR(14) UNIQUE,
    email           VARCHAR(200) NOT NULL UNIQUE,
    phone           VARCHAR(20),
    plan            VARCHAR(50) NOT NULL DEFAULT 'starter',
    plan_expires_at TIMESTAMP,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    settings        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ================================================================
-- TABELA: users
-- ================================================================
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id       UUID NOT NULL REFERENCES offices(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    email           VARCHAR(200) NOT NULL,
    password_hash   VARCHAR(200) NOT NULL,
    role            VARCHAR(50) NOT NULL DEFAULT 'analyst',
    is_active       BOOLEAN NOT NULL DEFAULT true,
    last_login_at   TIMESTAMP,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(office_id, email)
);

-- ================================================================
-- TABELA: clients
-- ================================================================
CREATE TABLE clients (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id       UUID NOT NULL REFERENCES offices(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    cnpj            VARCHAR(14),
    code            VARCHAR(50),
    is_active       BOOLEAN NOT NULL DEFAULT true,
    notes           TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(office_id, cnpj)
);

-- ================================================================
-- TABELA: suppliers (fornecedores indexados)
-- ================================================================
CREATE TABLE suppliers (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id           UUID NOT NULL REFERENCES offices(id) ON DELETE CASCADE,
    client_id           UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    raw_name            VARCHAR(500) NOT NULL,
    normalized_name     VARCHAR(500) NOT NULL,
    category            VARCHAR(100),
    first_seen_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    last_seen_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    occurrence_count    INTEGER NOT NULL DEFAULT 1,
    UNIQUE(client_id, normalized_name)
);

CREATE INDEX idx_suppliers_normalized ON suppliers(client_id, normalized_name);
CREATE INDEX idx_suppliers_office ON suppliers(office_id);

-- ================================================================
-- TABELA: accounting_code_pairs
-- ================================================================
CREATE TABLE accounting_code_pairs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id     UUID NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
    debit_code      VARCHAR(50) NOT NULL,
    credit_code     VARCHAR(50) NOT NULL,
    frequency       INTEGER NOT NULL DEFAULT 1,
    last_used_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    is_preferred    BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_code_pairs_supplier ON accounting_code_pairs(supplier_id);

-- ================================================================
-- TABELA: history_versions
-- ================================================================
CREATE TABLE history_versions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id       UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    uploaded_by     UUID NOT NULL REFERENCES users(id),
    file_name       VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    file_path       VARCHAR(1000),
    tabs_found      JSONB NOT NULL DEFAULT '[]',
    total_entries   INTEGER NOT NULL DEFAULT 0,
    unique_suppliers INTEGER NOT NULL DEFAULT 0,
    period_start    DATE,
    period_end      DATE,
    status          VARCHAR(50) NOT NULL DEFAULT 'processing',
    error_message   TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    processed_at    TIMESTAMP,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ================================================================
-- TABELA: historical_entries (lançamentos do histórico)
-- ================================================================
CREATE TABLE historical_entries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    history_id      UUID NOT NULL REFERENCES history_versions(id) ON DELETE CASCADE,
    supplier_id     UUID REFERENCES suppliers(id),
    tab_name        VARCHAR(200),
    entry_date      DATE NOT NULL,
    raw_supplier    VARCHAR(500) NOT NULL,
    normalized_supplier VARCHAR(500) NOT NULL,
    debit_code      VARCHAR(50) NOT NULL,
    credit_code     VARCHAR(50) NOT NULL,
    amount          NUMERIC(15,2) NOT NULL,
    row_number      INTEGER,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_hist_entries_history ON historical_entries(history_id);
CREATE INDEX idx_hist_entries_supplier ON historical_entries(normalized_supplier);
CREATE INDEX idx_hist_entries_date ON historical_entries(entry_date);

-- ================================================================
-- TABELA: processing_batches (lotes de processamento)
-- ================================================================
CREATE TABLE processing_batches (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id           UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    processed_by        UUID NOT NULL REFERENCES users(id),
    history_version_id  UUID REFERENCES history_versions(id),
    file_name           VARCHAR(500) NOT NULL,
    file_path           VARCHAR(1000),
    output_file_path    VARCHAR(1000),
    total_entries       INTEGER NOT NULL DEFAULT 0,
    confirmed_count     INTEGER NOT NULL DEFAULT 0,
    review_count        INTEGER NOT NULL DEFAULT 0,
    not_found_count     INTEGER NOT NULL DEFAULT 0,
    automation_rate     NUMERIC(5,2),
    status              VARCHAR(50) NOT NULL DEFAULT 'pending',
    error_message       TEXT,
    processing_time_ms  INTEGER,
    reference_month     VARCHAR(7),
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMP
);

CREATE INDEX idx_batches_client ON processing_batches(client_id);
CREATE INDEX idx_batches_processed_by ON processing_batches(processed_by);

-- ================================================================
-- TABELA: processed_entries (lançamentos processados)
-- ================================================================
CREATE TABLE processed_entries (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_id            UUID NOT NULL REFERENCES processing_batches(id) ON DELETE CASCADE,
    supplier_id         UUID REFERENCES suppliers(id),
    row_number          INTEGER NOT NULL,
    entry_date          DATE NOT NULL,
    raw_supplier        VARCHAR(500) NOT NULL,
    normalized_supplier VARCHAR(500) NOT NULL,
    amount              NUMERIC(15,2) NOT NULL,
    suggested_debit     VARCHAR(50),
    suggested_credit    VARCHAR(50),
    final_debit         VARCHAR(50),
    final_credit        VARCHAR(50),
    match_type          VARCHAR(50),
    confidence_score    NUMERIC(5,2),
    matched_supplier    VARCHAR(500),
    status              VARCHAR(50) NOT NULL DEFAULT 'pending',
    is_corrected        BOOLEAN NOT NULL DEFAULT false,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_processed_batch ON processed_entries(batch_id);
CREATE INDEX idx_processed_status ON processed_entries(status);

-- ================================================================
-- TABELA: corrections (base de aprendizado — Fase 3)
-- ================================================================
CREATE TABLE corrections (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    processed_entry_id  UUID NOT NULL REFERENCES processed_entries(id),
    corrected_by        UUID NOT NULL REFERENCES users(id),
    original_supplier   VARCHAR(500),
    corrected_supplier  VARCHAR(500),
    original_debit      VARCHAR(50),
    corrected_debit     VARCHAR(50),
    original_credit     VARCHAR(50),
    corrected_credit    VARCHAR(50),
    original_status     VARCHAR(50),
    notes               TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ================================================================
-- TABELA: audit_logs
-- ================================================================
CREATE TABLE audit_logs (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    office_id   UUID REFERENCES offices(id),
    user_id     UUID REFERENCES users(id),
    action      VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id   UUID,
    metadata    JSONB,
    ip_address  INET,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_office ON audit_logs(office_id, created_at DESC);
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);
```

---

# 14. API Design

## 14.1 Convenções

- Base URL: `https://api.contaclass.com.br/api/v1`
- Autenticação: `Authorization: Bearer <token>`
- Content-Type: `application/json`
- Formato de erros: RFC 7807 (Problem Details)
- Paginação: `?page=1&page_size=50`

## 14.2 Endpoints de Autenticação

```
POST   /auth/login          → Autenticar usuário, retorna access_token + refresh_token
POST   /auth/refresh         → Renovar access_token
POST   /auth/logout          → Invalidar tokens
POST   /auth/forgot-password → Solicitar reset de senha
POST   /auth/reset-password  → Confirmar nova senha
```

## 14.3 Endpoints de Clientes

```
GET    /clients              → Listar clientes do escritório (paginado)
POST   /clients              → Criar novo cliente
GET    /clients/{id}         → Detalhes do cliente
PUT    /clients/{id}         → Atualizar dados do cliente
DELETE /clients/{id}         → Desativar cliente (soft delete)
GET    /clients/{id}/stats   → Estatísticas do cliente (lotes, taxa de automação)
```

## 14.4 Endpoints de Histórico

```
GET    /clients/{id}/history              → Listar versões de histórico
POST   /clients/{id}/history/upload       → Upload de arquivo histórico
GET    /clients/{id}/history/{version_id} → Detalhes da versão
DELETE /clients/{id}/history/{version_id} → Remover versão
GET    /clients/{id}/history/{version_id}/suppliers → Listar fornecedores indexados
```

**Exemplo de Request — Upload de Histórico:**
```
POST /clients/uuid-cliente/history/upload
Content-Type: multipart/form-data

file: <binário do Excel>
```

**Exemplo de Response:**
```json
{
  "id": "uuid-history-version",
  "status": "processing",
  "task_id": "celery-task-id",
  "estimated_time_seconds": 15
}
```

## 14.5 Endpoints de Processamento

```
POST   /batches                     → Criar lote (upload de arquivo novo)
GET    /batches/{id}                → Status + resultado do lote
GET    /batches/{id}/entries        → Listar entradas processadas (paginado, filtros)
PATCH  /batches/{id}/entries/{eid}  → Corrigir classificação de uma entrada
GET    /batches/{id}/export         → Download do Excel classificado
GET    /batches/{id}/summary        → Resumo estatístico do lote
```

**Exemplo de Request — Processar Lote:**
```
POST /batches
Content-Type: multipart/form-data

client_id: uuid-cliente
file: <binário do arquivo novo>
reference_month: 2026-06
```

**Exemplo de Response (após processamento):**
```json
{
  "id": "uuid-batch",
  "status": "completed",
  "total_entries": 85,
  "confirmed_count": 72,
  "review_count": 9,
  "not_found_count": 4,
  "automation_rate": 84.71,
  "processing_time_ms": 3240,
  "entries_url": "/batches/uuid-batch/entries",
  "export_url": "/batches/uuid-batch/export"
}
```

## 14.6 Endpoints de WebSocket (Progresso em Tempo Real)

```
WS /ws/batches/{batch_id}/progress
WS /ws/history/{version_id}/progress
```

**Payload de Progresso:**
```json
{
  "event": "progress",
  "processed": 45,
  "total": 85,
  "percentage": 52.9,
  "current_supplier": "TELEFONICA BRASIL"
}
```

## 14.7 Endpoints de Fornecedores e Aprendizado

```
GET    /suppliers                    → Listar fornecedores do escritório
GET    /suppliers/{id}              → Detalhes + histórico de classificações
PUT    /suppliers/{id}/preferred-codes → Definir par de códigos preferido
GET    /corrections                  → Listar correções realizadas
GET    /corrections/analytics        → Análise de padrões de correção
```

## 14.8 Endpoints Administrativos

```
GET    /offices/me            → Dados do escritório atual
PUT    /offices/me            → Atualizar dados
PUT    /offices/me/settings   → Atualizar configurações (thresholds, etc.)
GET    /offices/me/stats      → Dashboard de uso e produtividade
GET    /users                 → Listar usuários
POST   /users                 → Convidar novo usuário
PUT    /users/{id}/role       → Alterar perfil do usuário
```

---

# 15. Estratégia de Similaridade

## 15.1 Pipeline de Normalização

Antes de qualquer comparação, ambos os nomes (histórico e novo) passam pelo mesmo pipeline:

```
Entrada: "Pagamento PIX - TELEFONICA BRASIL S.A. 03/2026"

Passo 1 (Uppercase):      "PAGAMENTO PIX - TELEFONICA BRASIL S.A. 03/2026"
Passo 2 (Remove acentos): "PAGAMENTO PIX - TELEFONICA BRASIL S.A. 03/2026"
Passo 3 (Remove sufixos): "PAGAMENTO PIX - TELEFONICA BRASIL"
Passo 4 (Remove prefixos): "TELEFONICA BRASIL"
Passo 5 (Remove especiais): "TELEFONICA BRASIL"
Passo 6 (Collapse spaces): "TELEFONICA BRASIL"

Saída: "TELEFONICA BRASIL"
```

**Lista de termos removidos (expansível via configuração):**

Prefixos: PIX, PGTO, PAGAMENTO, PAG, TED, DOC, TRANSF, TRANSFERENCIA, DEBITO, CREDITO, COBRANCA, BOLETO, DEB AUT, TARIFAS, TARIFA

Sufixos: S.A., SA, LTDA, EIRELI, ME, EPP, CNPJ, CPF, S/A, CIA, INDUSTRIA, COMERCIO

## 15.2 Algoritmos de Similaridade

### Algoritmo 1 — Levenshtein Ratio (Peso: 35%)
Mede a distância de edição entre duas strings. Bom para erros de digitação e pequenas variações.

```
"VIVO" vs "VIVOO" → 88.9%
"EQUATORIAL" vs "EQUAT ORIAL" → 95.2%
```

### Algoritmo 2 — Token Sort Ratio (Peso: 35%)
Ordena os tokens antes de comparar. Bom para palavras em ordem diferente.

```
"BANCO DO BRASIL" vs "BRASIL BANCO" → 100%
"VIVO EMPRESAS" vs "EMPRESAS VIVO" → 100%
```

### Algoritmo 3 — Partial Ratio (Peso: 30%)
Busca a melhor substring. Bom para nomes que são substrings uns dos outros.

```
"VIVO" vs "TELEFONICA VIVO" → 100%
"NET" vs "NET SERVICOS" → 100%
```

### Score Final

```
Score = (Levenshtein × 0.35) + (TokenSort × 0.35) + (Partial × 0.30)
```

## 15.3 Estratégias Complementares (Fase 4)

### Similaridade Semântica por Categoria
Usar embeddings de linguagem para agrupar fornecedores por categoria:
- Telecomunicações: VIVO, CLARO, TIM, OI, NET, NEXTEL
- Energia Elétrica: CEMIG, COPEL, LIGHT, COELBA, CELPE, EQUATORIAL
- Água/Saneamento: SABESP, CAESB, COMPESA, CAERN

### Grafo de Fornecedores Relacionados
Se o usuário já corrigiu "NET → VIVO" uma vez, o sistema registra essa relação no grafo. Se encontrar "CLARO NET" no futuro, o grafo sugere buscar na categoria "Telecomunicações".

## 15.4 Casos Especiais

| Cenário | Tratamento |
|---------|-----------|
| Nome numérico puro | Busca por valor + data para sugestão |
| Nome com CNPJ embutido | Extrair CNPJ, buscar por CNPJ na base |
| Nome com data embutida | Remover data antes de normalizar |
| Nome com valor embutido | Remover valor antes de normalizar |
| String vazia após normalização | Marcar como "Não Encontrado" sem processar |

---

# 16. Estratégia de Confiança

## 16.1 Score Base (Similaridade)

O score base é o resultado do pipeline de fuzzy matching descrito na Seção 15.

## 16.2 Fatores de Ajuste do Score

O score base pode ser ajustado por fatores contextuais:

| Fator | Ajuste | Condição |
|-------|--------|----------|
| Frequência do par de códigos | +5% | Par de códigos usado >5 vezes no histórico |
| Recência | +3% | Último uso < 90 dias |
| Consistência | +7% | Fornecedor sempre usou o mesmo par de códigos |
| Valor similar | +3% | Valor difere menos de 10% da média histórica |
| Mês recorrente | +5% | Fornecedor aparece no mesmo mês em anos anteriores |
| Correção anterior | +10% | Usuário já corrigiu para este mapeamento antes |
| Inconsistência histórica | -10% | Fornecedor usou >3 pares de códigos diferentes |

## 16.3 Classificação Final do Score

| Score Final | Status | Cor | Ação do Sistema |
|-------------|--------|-----|-----------------|
| 100% | Confirmado | Verde | Preenche automaticamente, sem marcação |
| 85-99% | Confirmado com Aviso | Verde claro | Preenche, adiciona nota do score |
| 70-84% | Revisar | Amarelo | Preenche com sugestão, requer confirmação |
| 50-69% | Revisar (Baixa Confiança) | Laranja | Preenche com sugestão fraca, requer confirmação |
| < 50% | Não Encontrado | Vermelho | Não preenche, requer input manual |

## 16.4 Explicabilidade do Score

Para cada lançamento, o sistema deve ser capaz de explicar o score:

```json
{
  "entry": "NET SERVIÇOS",
  "matched_to": "VIVO",
  "final_score": 78.5,
  "score_breakdown": {
    "levenshtein": 45.0,
    "token_sort": 62.0,
    "partial_ratio": 85.0,
    "base_fuzzy_score": 62.75,
    "adjustments": [
      { "factor": "high_frequency", "delta": +5.0 },
      { "factor": "consistent_codes", "delta": +7.0 },
      { "factor": "recency", "delta": +3.0 }
    ],
    "final_score": 77.75
  }
}
```

---

# 17. Roadmap

## Fase 1 — Script Local Python (Meses 1-2)

**Objetivo:** Entregar valor imediato com mínima fricção de adoção

**Entregas:**
- Script Python CLI: `contaclass.py --historico arquivo_hist.xlsx --novo arquivo_novo.xlsx --saida resultado.xlsx`
- Leitura automática de todas as abas do histórico
- Engine de normalização de nomes
- Busca exata + fuzzy matching (RapidFuzz)
- Exportação Excel colorido com status e score
- Documentação de instalação e uso (README.md)
- Instalador Windows (.exe via PyInstaller)

**Critério de Sucesso:** Processar 100 lançamentos em < 10 segundos com ≥ 85% de taxa de automação em dados reais de teste

---

## Fase 2 — Aplicação Web (Meses 3-6)

**Objetivo:** Interface profissional, multi-usuário, multi-cliente, SaaS

**Entregas:**
- Backend FastAPI com toda a API documentada
- Frontend Next.js com fluxo completo
- Sistema de autenticação e multi-tenancy
- Gestão de clientes e histórico versionado
- Processamento assíncrono com progresso em tempo real
- Dashboard de produtividade básico
- Planos SaaS com billing (integração Stripe)
- Deploy em nuvem (AWS ou GCP) com CI/CD

**Critério de Sucesso:** 20 escritórios piloto usando ativamente, NPS ≥ 40

---

## Fase 3 — Aprendizado Contínuo (Meses 7-9)

**Objetivo:** Sistema que melhora automaticamente com o uso

**Entregas:**
- Interface de correção inline no resultado
- Registro estruturado de correções por usuário
- Pipeline de re-indexação de fornecedores com correções
- Relatório de "erros sistemáticos" (o sistema sempre erra para X fornecedor)
- Notificação ao usuário quando o sistema aprende um novo mapeamento
- Exportação do dicionário de fornecedores por cliente

**Critério de Sucesso:** Taxa de automação cresce pelo menos 5pp após 60 dias de uso com correções

---

## Fase 4 — IA de Classificação (Meses 10-15)

**Objetivo:** Inteligência artificial para casos não cobertos por regras

**Entregas:**
- Modelo de embeddings fine-tunado com dados contábeis brasileiros
- Classificação por categoria semântica (telecomunicações, energia, etc.)
- Sugestão baseada em padrão de valor + sazonalidade
- API de predição de categoria para novos fornecedores
- Feedback loop: modelo melhora com correções de todos os tenants (anonimizado)
- Dashboard de performance do modelo (precision, recall, F1)

**Critério de Sucesso:** Taxa de automação ≥ 95% em dataset de validação

---

## 17.1 Linha do Tempo Visual

```
Mês:  1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
      |─────────────|
      FASE 1 (Script)
                   |──────────────────────────|
                         FASE 2 (Web App)
                                              |──────────────|
                                                FASE 3 (Learn)
                                                              |──────────────────────|
                                                                   FASE 4 (IA)
```

---

# 18. MVP

## 18.1 Escopo do MVP (Fase 1)

O MVP é o script Python CLI que entrega o valor essencial sem necessidade de infraestrutura web.

**Incluído no MVP:**
- RF01: Upload de arquivo histórico (parâmetro CLI)
- RF02: Leitura automática de múltiplas abas
- RF03: Consolidação em base local (arquivo JSON/SQLite)
- RF04: Upload de planilha nova (parâmetro CLI)
- RF05: Busca exata de fornecedor
- RF06: Preenchimento automático de débito e crédito
- RF07: Busca por similaridade (fuzzy matching básico)
- RF08: Score de confiança simples
- RF09: Coluna de Status (Confirmado / Revisar / Não Encontrado)
- RF10: Colorização automática do Excel
- RF11: Exportação do Excel final

**Excluído do MVP (pós-MVP):**
- Interface web (Fase 2)
- Autenticação e multi-tenancy (Fase 2)
- Gestão de clientes (Fase 2)
- Aprendizado automático (Fase 3)
- IA (Fase 4)

## 18.2 Comandos do MVP

```bash
# Processamento completo
contaclass --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx

# Com threshold personalizado
contaclass --historico hist.xlsx --novo novo.xlsx --saida resultado.xlsx --threshold 65

# Apenas listar abas do histórico
contaclass --historico hist.xlsx --listar-abas

# Somente abas específicas
contaclass --historico hist.xlsx --novo novo.xlsx --abas "Banco do Brasil,Santander"
```

## 18.3 Critérios de Saída do MVP para Fase 2

- Pelo menos 5 escritórios testando ativamente o script
- Taxa de automação documentada ≥ 80% nos dados reais
- Feedbacks coletados de pelo menos 10 usuários
- Lista priorizada de features solicitadas pela comunidade de early adopters

---

# 19. Critérios de Aceite

## CA01 — Leitura do Histórico

- DADO que o usuário fornece um Excel com 3 abas e 200 linhas totais
- QUANDO o sistema processa o arquivo
- ENTÃO deve listar as 3 abas, exibir 200 lançamentos consolidados e identificar corretamente as colunas Data, Cod Débito, Cod Crédito, Valor e Fornecedor

## CA02 — Busca Exata

- DADO que o fornecedor "VIVO" está no histórico com códigos 503/101
- QUANDO o arquivo novo contém uma linha com fornecedor "VIVO"
- ENTÃO o sistema deve preencher Débito=503, Crédito=101, Status=Confirmado, Score=100%

## CA03 — Busca Fuzzy

- DADO que o fornecedor "VIVO" está no histórico com códigos 503/101
- QUANDO o arquivo novo contém "TELEFONICA BRASIL" (mesmo fornecedor, nome diferente)
- ENTÃO o sistema deve preencher Débito=503, Crédito=101, Status=Revisar, Score entre 65-95%

## CA04 — Não Encontrado

- DADO que o fornecedor "EMPRESA NOVA XYZ" não está no histórico
- QUANDO o arquivo novo contém esse fornecedor
- ENTÃO o sistema deve marcar Status=Não Encontrado, Score=0%, Débito e Crédito vazios

## CA05 — Colorização

- DADO que o processamento foi concluído com linhas Confirmado, Revisar e Não Encontrado
- QUANDO o usuário exporta o Excel
- ENTÃO as linhas devem estar coloridas: verde (Confirmado), amarelo (Revisar), vermelho (Não Encontrado)

## CA06 — Performance

- DADO um arquivo histórico com 500 lançamentos e um arquivo novo com 100 linhas
- QUANDO o usuário solicita o processamento
- ENTÃO deve completar em menos de 15 segundos

## CA07 — Normalização

- DADO que o histórico contém "VIVO" e o arquivo novo contém "Pagamento PIX - VIVO EMPRESAS S.A."
- QUANDO o sistema normaliza ambos os nomes
- ENTÃO deve identificar "VIVO" como match fuzzy de alta confiança (≥ 75%)

## CA08 — Múltiplos Códigos

- DADO que "EQUATORIAL" aparece 8 vezes no histórico, sendo 6 vezes com 504/101 e 2 vezes com 505/101
- QUANDO o sistema classifica um novo lançamento de EQUATORIAL
- ENTÃO deve usar os códigos 504/101 (mais frequentes) e registrar que houve desempate

---

# 20. Wireframes Textuais

## 20.1 Tela Principal — Dashboard

```
┌──────────────────────────────────────────────────────────────────┐
│  ContaClass                              [Rodrigo ▼]  [Sair]     │
├──────────────────────────────────────────────────────────────────┤
│  📊 Dashboard   |  👥 Clientes  |  📁 Lotes  |  ⚙️ Config       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BOM DIA, RODRIGO!                                               │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 1.240       │  │ 89,3%       │  │ 28          │             │
│  │ Lançamentos │  │ Automação   │  │ Clientes    │             │
│  │ este mês    │  │ este mês    │  │ ativos      │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  ATIVIDADE RECENTE                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 📄 Empresa ABC      85 lançamentos   91%   há 2h  [Ver]  │   │
│  │ 📄 Empresa XYZ      120 lançamentos  78%   hoje   [Ver]  │   │
│  │ 📄 Empresa DEF      60 lançamentos   100%  ontem  [Ver]  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  [+ NOVO PROCESSAMENTO]                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 20.2 Tela de Novo Processamento — Passo 1: Selecionar Cliente

```
┌──────────────────────────────────────────────────────────────────┐
│  NOVO PROCESSAMENTO                                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PASSO 1 DE 4                                                    │
│  ●────○────○────○                                                │
│  Cliente  Histórico  Arquivo  Resultado                          │
│                                                                  │
│  Selecione o cliente:                                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 🔍 Buscar cliente...                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ○  Empresa ABC Ltda         CNPJ: 00.000.000/0001-00    │   │
│  │ ○  Empresa XYZ S.A.         CNPJ: 11.111.111/0001-11    │   │
│  │ ○  Indústria DEF Eireli     CNPJ: 22.222.222/0001-22    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Mês de referência: [Junho 2026 ▼]                              │
│                                                                  │
│                              [Cancelar]  [Próximo →]            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 20.3 Tela de Resultado

```
┌──────────────────────────────────────────────────────────────────┐
│  RESULTADO — Empresa ABC — Junho/2026                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ 72 Confirmados  ⚠️ 9 Revisar  ❌ 4 Não Encontrados           │
│  ████████████████████████░░░░░░░░  85% automação                 │
│                                                                  │
│  Filtrar: [Todos ▼]  [Pesquisar fornecedor...]                  │
│                                                                  │
│  ┌───┬────────────┬──────────────────┬───────┬───────┬──────┐   │
│  │ # │ Data       │ Fornecedor       │ Déb.  │ Cré.  │Status│   │
│  ├───┼────────────┼──────────────────┼───────┼───────┼──────┤   │
│  │ 1 │ 01/06/2026 │ VIVO             │  503  │  101  │ ✅   │   │
│  │ 2 │ 02/06/2026 │ EQUATORIAL       │  504  │  101  │ ✅   │   │
│  │ 3 │ 03/06/2026 │ TELEFONICA BR... │  503  │  101  │ ⚠️78%│   │
│  │   │            │ → Sugestão: VIVO │       │       │      │   │
│  │ 4 │ 04/06/2026 │ EMPRESA NOVA XYZ │       │       │ ❌   │   │
│  └───┴────────────┴──────────────────┴───────┴───────┴──────┘   │
│                                                                  │
│  Para item ⚠️ ou ❌: [✓ Aceitar]  [✎ Corrigir manualmente]       │
│                                                                  │
│                    [⬇ Exportar Excel]  [Finalizar Lote]         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 20.4 Modal de Correção Manual

```
┌──────────────────────────────────────────┐
│  CORRIGIR CLASSIFICAÇÃO                  │
├──────────────────────────────────────────┤
│                                          │
│  Fornecedor: EMPRESA NOVA XYZ            │
│  Data: 04/06/2026   Valor: R$ 1.250,00   │
│                                          │
│  Código Débito:  [_______]               │
│  Código Crédito: [_______]               │
│                                          │
│  Vincular ao fornecedor existente?       │
│  [Selecionar fornecedor... ▼]            │
│  (Se vinculado, o sistema aprenderá)     │
│                                          │
│  Observação: [__________________________]│
│                                          │
│         [Cancelar]  [Salvar Correção]    │
└──────────────────────────────────────────┘
```

---

# 21. Riscos

## 21.1 Matriz de Riscos

| ID | Risco | Probabilidade | Impacto | Nível | Mitigação |
|----|-------|--------------|---------|-------|-----------|
| R01 | Taxa de automação abaixo do esperado em dados reais | Média | Alto | Alto | Testes com dados reais antes do lançamento; threshold configurável |
| R02 | Resistência à adoção por colaboradores | Alta | Médio | Médio-Alto | Onboarding simples; demonstrar economia de tempo com dados reais |
| R03 | Estrutura do Excel histórico muito heterogênea | Alta | Alto | Alto | Mapeamento manual de colunas como fallback obrigatório |
| R04 | Violação de dados sensíveis de clientes | Baixa | Muito Alto | Alto | LGPD compliance; dados isolados por tenant; auditoria |
| R05 | Dependência de bibliotecas Python descontinuadas | Baixa | Médio | Baixo | Pinning de versões; atualização periódica |
| R06 | Concorrente lança produto similar | Média | Alto | Alto | Velocidade de execução; moat de dados e aprendizado |
| R07 | Formato do arquivo histórico muda com atualizações do Excel | Baixa | Médio | Baixo | Suporte a múltiplas versões; testes de regressão |
| R08 | Score alto em match errado (falso positivo) | Média | Alto | Alto | Limite configurável; revisão humana obrigatória para score < 100% |
| R09 | Volume de dados muito grande (arquivo com 10k+ linhas) | Baixa | Médio | Baixo | Processamento assíncrono; filas; paginação |
| R10 | Churn elevado por percepção de produto complexo | Média | Alto | Alto | UX simplificada; tutorial de onboarding; suporte ativo |

## 21.2 Riscos Específicos do MVP (Fase 1)

| Risco | Mitigação |
|-------|-----------|
| Usuário não consegue instalar o Python | Gerar executável (.exe) com PyInstaller |
| Excel com encoding diferente (UTF-8 vs Latin-1) | Detecção automática de encoding com chardet |
| Arquivo sem cabeçalho padrão | Detecção por posição + fallback para seleção manual |
| Versão antiga do Excel (.xls) | Suporte via xlrd |

---

# 22. Possíveis Diferenciais Competitivos

## 22.1 Diferenciais do Produto

**D01 — Especialização no mercado contábil brasileiro**  
Ao contrário de soluções genéricas de automação (como Power Automate ou scripts Excel), o ContaClass é construído especificamente para o fluxo de trabalho e terminologia contábil brasileira, incluindo plano de contas brasileiro, formatos de data/valor nacionais e integração com ERPs nacionais.

**D02 — Motor de aprendizado baseado em uso**  
Cada correção manual do usuário torna o sistema mais inteligente. A base de conhecimento cresce com o uso, criando um ciclo virtuoso: quanto mais o escritório usa, maior a taxa de automação, maior o ROI.

**D03 — Propriedade e privacidade dos dados**  
O histórico de cada cliente permanece estritamente privado ao escritório. Não há compartilhamento de dados sensíveis entre tenants — apenas padrões anonimizados podem ser usados para treinar modelos globais (com opt-in explícito).

**D04 — Moat de dados**  
Com o tempo, o ContaClass acumula o maior banco de dados de mapeamentos fornecedor-código-contábil do Brasil. Esse ativo proprietário cria uma barreira competitiva crescente.

**D05 — Integração com ERPs nacionais**  
Exportação nativa nos formatos de importação dos principais sistemas contábeis brasileiros (Domínio, Alterdata, Questor, Totvs Protheus), eliminando a necessidade de manipulação manual pós-exportação.

**D06 — ROI Imediato e Mensurável**  
A proposta de valor é quantificável: o próprio sistema mostra "Você economizou X horas neste mês", tornando fácil justificar a assinatura.

**D07 — Adoção Progressiva**  
O usuário começa com o script gratuito (Fase 1), sem fricção de cadastro ou cobrança. A transição para o SaaS (Fase 2) é natural quando ele quer multi-usuário e histórico persistente.

## 22.2 Análise Competitiva

| Dimensão | ContaClass | Power Automate | Excel Manual | Outros ERPs |
|----------|-----------|---------------|-------------|-------------|
| Especialização contábil BR | ✅ Alta | ❌ Genérico | N/A | ⚠️ Parcial |
| Fuzzy matching de fornecedores | ✅ Nativo | ❌ Manual | ❌ Não | ⚠️ Limitado |
| Aprendizado contínuo | ✅ Fase 3 | ❌ Não | ❌ Não | ❌ Não |
| Facilidade de uso | ✅ Alta | ❌ Técnico | ⚠️ Médio | ⚠️ Médio |
| Custo mensal estimado | ✅ R$99-399 | ⚠️ R$800+ | ✅ Grátis | ❌ Alto |
| Integração com ERPs BR | ✅ Roadmap | ❌ Custom | ❌ Manual | ✅ Nativo |

---

# 23. Estimativa de Complexidade

## 23.1 Estimativa por Fase (Story Points / T-Shirt Size)

### Fase 1 — Script Python

| Funcionalidade | Complexidade | Esforço (dias) |
|---------------|-------------|----------------|
| Leitura de Excel (múltiplas abas) | P | 1 |
| Normalização de nomes | M | 2 |
| Engine de busca exata | P | 1 |
| Engine de fuzzy matching | M | 3 |
| Cálculo de score | M | 2 |
| Exportação Excel colorido | M | 2 |
| CLI com Click | P | 1 |
| Testes e ajustes | G | 4 |
| Documentação e empacotamento | M | 2 |
| **Total Fase 1** | | **~18 dias** |

### Fase 2 — Aplicação Web

| Funcionalidade | Complexidade | Esforço (dias) |
|---------------|-------------|----------------|
| Setup infraestrutura (Docker, CI/CD) | G | 5 |
| Backend auth + multi-tenancy | G | 8 |
| API de clientes e histórico | M | 5 |
| API de processamento + fila | G | 8 |
| WebSocket progresso real-time | M | 3 |
| API de exportação | M | 3 |
| Frontend: auth + onboarding | M | 5 |
| Frontend: gestão de clientes | M | 5 |
| Frontend: fluxo de processamento | G | 10 |
| Frontend: tela de resultados | G | 8 |
| Dashboard de produtividade | G | 5 |
| Billing (Stripe) | G | 5 |
| Testes E2E + QA | GG | 10 |
| **Total Fase 2** | | **~80 dias** |

### Fase 3 — Aprendizado

| Funcionalidade | Complexidade | Esforço (dias) |
|---------------|-------------|----------------|
| Interface de correção inline | M | 5 |
| Pipeline de aprendizado | G | 8 |
| Re-indexação automática | M | 4 |
| Relatório de análise de erros | M | 5 |
| **Total Fase 3** | | **~22 dias** |

### Fase 4 — IA

| Funcionalidade | Complexidade | Esforço (dias) |
|---------------|-------------|----------------|
| Coleta e preparação de dados | GG | 20 |
| Fine-tuning do modelo | GG | 25 |
| Integração pgvector | G | 8 |
| API de predição | G | 8 |
| Dashboard de performance | M | 5 |
| **Total Fase 4** | | **~66 dias** |

## 23.2 Equipe Mínima Recomendada

| Papel | Fase 1 | Fase 2 | Fase 3 | Fase 4 |
|-------|--------|--------|--------|--------|
| Python Dev (Backend/Data) | 1 | 1 | 1 | 1 |
| Full-Stack Dev (Frontend) | — | 1 | 1 | 1 |
| ML Engineer | — | — | — | 1 |
| Product Manager | 0,5 | 0,5 | 0,5 | 0,5 |
| Designer UX/UI | — | 0,5 | — | — |

---

# 24. Estratégia de Monetização SaaS

## 24.1 Modelo de Precificação

O ContaClass adota modelo **por escritório** (tenant) com limites baseados em clientes ativos e lançamentos processados mensalmente.

### Plano Starter — Gratuito

**Perfil:** Escritórios pequenos ou experimentando a plataforma

- Até 3 clientes ativos
- Até 500 lançamentos/mês
- 1 usuário
- Histórico: últimos 3 meses
- Sem suporte prioritário
- **R$ 0/mês**

---

### Plano Professional — R$ 149/mês

**Perfil:** Escritório de pequeno-médio porte

- Até 15 clientes ativos
- Até 3.000 lançamentos/mês
- Até 3 usuários
- Histórico ilimitado
- Exportação para formatos ERP (Domínio, Alterdata)
- Suporte via e-mail (48h)
- **R$ 149/mês (ou R$ 1.490/ano — 2 meses grátis)**

---

### Plano Business — R$ 299/mês

**Perfil:** Escritório de médio-grande porte

- Até 50 clientes ativos
- Até 15.000 lançamentos/mês
- Até 10 usuários
- Histórico ilimitado + backup
- Exportação para todos os ERPs suportados
- Dashboard de produtividade avançado
- API de integração
- Suporte via chat (24h)
- **R$ 299/mês (ou R$ 2.990/ano)**

---

### Plano Enterprise — Sob Consulta

**Perfil:** Grandes escritórios, redes de franquias contábeis, empresas com departamento financeiro interno

- Clientes ilimitados
- Lançamentos ilimitados
- Usuários ilimitados
- SSO (SAML/OAuth)
- SLA dedicado (99,9%)
- Treinamento personalizado
- Gerente de conta dedicado
- Deploy on-premise (opcional)
- **A partir de R$ 800/mês**

## 24.2 Estratégia de Aquisição

**Fase 1 (Script Gratuito):** Distribuição via GitHub, fóruns de contabilidade, grupos do WhatsApp de contadores. O script gratuito funciona como "freemium de topo de funil" — contadores que usam o script e se beneficiam são os leads mais qualificados para o SaaS.

**Fase 2 (SaaS):** 
- SEO para palavras-chave contábeis ("automação de lançamentos contábeis", "classificação contábil automática")
- Parcerias com associações de contadores (CRC, FENACON, Sescon)
- Programa de indicação: 1 mês grátis por indicação bem-sucedida
- Webinars e conteúdo educativo no YouTube e Instagram

## 24.3 Unit Economics Projetados

| Métrica | Ano 1 | Ano 2 | Ano 3 |
|---------|-------|-------|-------|
| Escritórios pagantes | 50 | 250 | 800 |
| Ticket médio (R$/mês) | R$ 180 | R$ 200 | R$ 220 |
| MRR | R$ 9.000 | R$ 50.000 | R$ 176.000 |
| ARR | R$ 108.000 | R$ 600.000 | R$ 2.112.000 |
| Churn mensal estimado | 4% | 3% | 2% |
| CAC estimado | R$ 400 | R$ 300 | R$ 250 |
| LTV estimado | R$ 4.500 | R$ 6.670 | R$ 11.000 |
| LTV/CAC | 11x | 22x | 44x |

## 24.4 Modelo de Expansão de Receita

- **Upsell:** Escritórios que crescem a carteira sobem de plano naturalmente
- **Add-ons:** Integrações com ERPs específicos (R$ 49/mês por integração adicional)
- **Serviços:** Migração de dados históricos, treinamento, configuração personalizada (receita de serviços, não recorrente)
- **Marketplace de Regras:** Escritórios podem vender/compartilhar suas regras de classificação para outros (comissão de 20%)

---

# 25. Integrações Futuras com ERPs e Sistemas Contábeis

## 25.1 ERPs Contábeis Nacionais (Prioritários)

### Domínio Sistemas (Thomson Reuters)
- **Status:** Prioritário (maior market share Brasil)
- **Tipo de integração:** Exportação em layout proprietário + futura API REST
- **Dados:** Lançamentos contábeis, plano de contas, cadastro de fornecedores
- **Benefício:** Importação direta sem manipulação manual

### Alterdata
- **Status:** Prioritário
- **Tipo de integração:** Exportação via layout TXT proprietário
- **Dados:** Lançamentos, contas, centros de custo

### Questor Sistemas
- **Status:** Alta prioridade (forte no Sul e Sudeste)
- **Tipo de integração:** API disponível mediante parceria
- **Dados:** Plano de contas, fornecedores, lançamentos

### Totvs Protheus
- **Status:** Médio prazo (foco em departamentos financeiros corporativos)
- **Tipo de integração:** REST API (TOTVS Fluig) + importação via planilha padrão
- **Dados:** Lançamentos, CTBC, fornecedores, projetos

### Nasajon
- **Status:** Médio prazo
- **Tipo de integração:** API REST disponível

## 25.2 Bancos e Open Finance

### Open Finance Brasil (BACEN)
- **Tipo:** Extração automática de extratos bancários via Open Finance
- **Benefício:** Eliminar a etapa de envio manual do arquivo pelo cliente
- **Status:** Roadmap Fase 3

### Bancos Principais
- Banco do Brasil (API)
- Itaú (Itaú Developers)
- Bradesco
- Santander
- Nubank Empresas
- C6 Bank Empresas

## 25.3 Integrações com Plataformas de Nota Fiscal

### SEFAZ (NF-e / NFS-e)
- Extração de dados de fornecedor e valor diretamente das NF-e
- Validação cruzada: a NF-e confirma que o lançamento corresponde a uma nota emitida
- CNPJ do emitente → identificação inequívoca do fornecedor

### Plataformas de gestão de NF-e
- NFe.io
- Focus NFe
- Tiny ERP

## 25.4 Integrações de Comunicação e Workflow

### Microsoft Teams / Slack
- Notificações de processamentos concluídos
- Alertas de lotes com alta taxa de "Não Encontrados"
- Relatório semanal de produtividade

### Google Workspace / Microsoft 365
- Salvamento direto em Google Drive / OneDrive
- Export para Google Sheets

## 25.5 Roadmap de Integrações

| Integração | Fase | Complexidade |
|-----------|------|-------------|
| Export layout Domínio | 2 | Média |
| Export layout Alterdata | 2 | Média |
| Export layout Questor | 2 | Média |
| Open Finance (extratos) | 3 | Alta |
| NF-e SEFAZ | 3 | Alta |
| Totvs Protheus API | 3 | Alta |
| Google Drive | 2 | Baixa |
| Microsoft 365 | 3 | Média |
| Slack/Teams notificações | 3 | Baixa |
| Nasajon API | 3 | Média |

---

# Apêndice A — Glossário

| Termo | Definição |
|-------|-----------|
| Lançamento Contábil | Registro de movimentação financeira com pelo menos um débito e um crédito |
| Código de Débito | Código da conta contábil debitada na operação |
| Código de Crédito | Código da conta contábil creditada na operação |
| Plano de Contas | Estrutura padronizada de contas contábeis de uma empresa |
| Fuzzy Matching | Técnica de comparação de strings por similaridade aproximada |
| Score de Confiança | Percentual que indica a certeza do sistema na classificação sugerida |
| Tenant | Escritório contábil como unidade isolada de dados no sistema multi-tenant |
| Normalização | Processo de padronização de strings para comparação (uppercase, remoção de acentos) |
| ERP | Enterprise Resource Planning — sistema integrado de gestão empresarial |
| LGPD | Lei Geral de Proteção de Dados (Lei nº 13.709/2018) |

---

# Apêndice B — Referências Técnicas

- **RapidFuzz:** https://github.com/maxbachmann/RapidFuzz
- **OpenPyXL:** https://openpyxl.readthedocs.io
- **FastAPI:** https://fastapi.tiangolo.com
- **Next.js:** https://nextjs.org
- **PostgreSQL RLS:** https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- **Open Finance Brasil:** https://openfinancebrasil.org.br
- **RFC 7807 (Problem Details):** https://tools.ietf.org/html/rfc7807
- **LGPD:** https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

---

*Documento gerado por: Equipe de Produto ContaClass*  
*Versão 1.0 — Junho de 2026*  
*Para dúvidas e contribuições: produto@contaclass.com.br*
