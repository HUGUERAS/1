# ⚡ Comandos Prontos - Testar Features com MCP

**Copie e cole** estes comandos no **Claude Desktop** para testar funcionalidades faltantes.

---

## 💰 PAGAMENTOS

### Criar projeto com pagamentos
```
Claude, cria um projeto no Cosmos DB:
- Título: Fazenda Santa Rita
- Local: Campinas-SP
- Proprietário: Roberto Costa
- Valor total: R$ 28.000

Depois simula 2 pagamentos:
- R$ 10.000 via PIX (hoje)
- R$ 8.000 via Boleto (ontem)

Me mostra o saldo restante e status financeiro.
```

### Relatório de inadimplência
```
Claude, lista todos os projetos no Cosmos DB que:
- Têm valor pendente > R$ 5.000
- Não receberam pagamento nos últimos 30 dias

Ordena por valor pendente (maior primeiro) e salva em:
C:\Relatorios\inadimplentes-2026-01.txt
```

### Projeção de receita
```
Claude, analisa histórico de pagamentos de todos os projetos
e me dá projeção de receita para os próximos 3 meses
baseado na taxa média de conversão e tempo médio de pagamento.
```

---

## 👥 VIZINHOS/ENVOLVIDOS

### Cadastrar múltiplos vizinhos
```
Claude, para o projeto "Fazenda Boa Vista":

Adiciona estes vizinhos:
1. Maria Silva - (11) 98765-4321 - Confrontante Norte
2. João Santos - (11) 91234-5678 - Confrontante Sul  
3. Pedro Costa - (11) 99999-8888 - Confrontante Leste
4. Ana Oliveira - (11) 97777-6666 - Confrontante Oeste

Gera links de convite únicos para cada um e me mostra.
```

### Simular assinaturas
```
Claude, no projeto "Fazenda Boa Vista":

Marca como "assinado" os vizinhos:
- Maria Silva (assinado hoje às 10h)
- João Santos (assinado ontem às 15h)

Deixa os outros como "pendente" e me mostra:
- Percentual de assinaturas obtidas
- Quem ainda falta assinar
- Tempo médio para assinatura
```

### Dashboard de assinaturas
```
Claude, gera relatório de todos os projetos mostrando:
- Total de vizinhos cadastrados por projeto
- Percentual de assinaturas (0-100%)
- Projetos bloqueados (< 50% assinado)
- Projetos prontos para protocolo (100% assinado)

Salva em C:\Relatorios\assinaturas-dashboard.json
```

---

## 📁 ARQUIVOS TOPOGRÁFICOS

### Upload simulado de KML
```
Claude, simula upload de arquivo KML:

1. Cria arquivo KML de teste em C:\Temp\fazenda-modelo.kml
   com polígono de 5 vértices (coordenadas aproximadas de Campinas-SP)

2. Lê o arquivo e extrai:
   - Número de vértices
   - Coordenadas em WGS84
   - Área aproximada em hectares

3. Salva metadados no Cosmos DB (projeto: "Fazenda Modelo KML")
```

### Conversão KML → GeoJSON
```
Claude, pega todos os arquivos .kml da pasta:
C:\Projetos\arquivos-clientes\

Para cada arquivo:
1. Converte para GeoJSON
2. Calcula área
3. Valida se tem sobreposições
4. Salva resultado em C:\Projetos\convertidos\{nome}.geojson
5. Cria relatório de conversão

Me mostra resumo de quantos foram convertidos com sucesso.
```

### Análise de áreas
```
Claude, para todos os projetos no Cosmos DB que têm arquivo associado:

1. Lê cada arquivo GeoJSON/KML
2. Calcula área real
3. Compara com área declarada no projeto
4. Identifica discrepâncias > 5%

Salva relatório em C:\Relatorios\validacao-areas.txt
```

---

## 📊 RELATÓRIOS E DASHBOARDS

### Resumo executivo mensal
```
Claude, gera relatório executivo do mês de Janeiro/2026:

FINANCEIRO:
- Total contratado
- Total recebido  
- Ticket médio por projeto
- Taxa de conversão

OPERACIONAL:
- Projetos criados
- Projetos concluídos
- Tempo médio de conclusão
- Taxa de retrabalho

TOP 5:
- Clientes por valor
- Topógrafos por produtividade
- Tipos de projeto mais rentáveis

Salva em C:\Relatorios\executivo-2026-01.txt
```

### Dashboard de produtividade
```
Claude, analisa todos os projetos e me mostra:

Por TOPÓGRAFO:
- Quantos projetos ativos
- Tempo médio de conclusão
- Taxa de sucesso (100% assinado)
- Receita gerada

Por TIPO DE PROJETO:
- Quantidade
- Receita média
- Tempo médio
- Complexidade (nº de vizinhos)

Identifica gargalos e oportunidades de melhoria.
```

### Alerta de riscos
```
Claude, verifica projetos em risco:

CRITÉRIOS:
- Sem atualização há 20+ dias
- Menos de 50% de assinaturas e prazo < 15 dias
- Pagamento atrasado > 45 dias
- Arquivo topográfico com área divergente

Para cada projeto em risco:
- Severidade (crítico/alto/médio)
- Ações recomendadas
- Responsável para contatar

Salva em C:\Alertas\projetos-risco-2026-01-23.json
```

---

## 🔔 NOTIFICAÇÕES

### Alertas automáticos
```
Claude, configura sistema de alertas:

Verifica TODOS os projetos e gera notificações para:

1. URGENTE (crítico):
   - Pagamento atrasado 60+ dias
   - Prazo de entrega em 3 dias e < 70% concluído
   - Nenhuma assinatura obtida em 30+ dias

2. ATENÇÃO (alerta):
   - Pagamento atrasado 30-60 dias  
   - Sem atualização há 15+ dias
   - Faltam assinaturas e prazo < 10 dias

3. AVISO (info):
   - Projeto próximo de conclusão (90%+)
   - Pagamento recebido (última semana)
   - Nova assinatura obtida

Salva notificações em C:\Notificacoes\alertas-{data}.json
e me mostra resumo por severidade.
```

---

## 📝 HISTÓRICO E AUDITORIA

### Timeline de projeto
```
Claude, para o projeto "Fazenda Santa Clara":

Reconstrói timeline completo de eventos:
- Data de criação
- Todas alterações de status
- Cadastro de vizinhos (quando e quantos)
- Upload de arquivos (quais e quando)
- Assinaturas obtidas (quem e quando)
- Pagamentos recebidos (valor e método)

Apresenta em formato visual cronológico e salva em:
C:\Historicos\fazenda-santa-clara-timeline.txt
```

### Auditoria de mudanças
```
Claude, gera relatório de auditoria:

Para TODOS os projetos, rastreia:
- Quem criou (topógrafo)
- Quantas vezes status foi alterado
- Valores que mudaram (comparar valorTotal original vs atual)
- Arquivos que foram substituídos

Identifica anomalias:
- Projetos editados por múltiplos usuários
- Valores alterados sem justificativa
- Status voltou para trás (ex: concluído → em andamento)

Salva em C:\Auditoria\relatorio-mudancas-2026-01.txt
```

---

## 🤖 AUTOMAÇÕES AVANÇADAS

### Workflow completo automatizado
```
Claude, executa workflow completo de teste:

FASE 1 - SETUP:
1. Cria projeto "Teste Workflow Completo"
2. Valor: R$ 20.000
3. Cadastra 4 vizinhos com dados fictícios

FASE 2 - SIMULAÇÃO:
4. Simula 2 assinaturas (50%)
5. Registra pagamento de R$ 7.000 (35%)
6. Cria arquivo KML de teste
7. Calcula área (deve dar ~15ha)

FASE 3 - ANÁLISE:
8. Verifica se projeto está em dia
9. Identifica pendências
10. Calcula tempo estimado para conclusão

FASE 4 - RELATÓRIO:
11. Gera relatório completo do teste
12. Salva em C:\Testes\workflow-{timestamp}.json

Me mostra resumo de cada fase.
```

### Migração de dados
```
Claude, prepara migração do localStorage para Cosmos DB:

1. Lê estrutura de dados atual do localStorage 
   (analisa código em ativo-real/src/)

2. Identifica todos os campos usados:
   - Projetos
   - Usuários (topógrafos)
   - Configurações

3. Cria script de migração que:
   - Valida dados antes de migrar
   - Transforma formato se necessário
   - Cria backup antes de migrar
   - Testa inserção no Cosmos DB

4. Salva script em C:\Scripts\migracao-localstorage-cosmos.js

Me explica cada etapa da migração.
```

### Backup e restore
```
Claude, cria sistema de backup:

BACKUP:
1. Lista TODOS os projetos do Cosmos DB
2. Exporta para JSON com timestamp
3. Salva em C:\Backups\cosmos-backup-{data}.json
4. Compacta para .zip (se possível)

VALIDAÇÃO:
5. Verifica integridade do backup
6. Conta registros (deve bater com total do Cosmos DB)
7. Testa se JSON é válido

RESTORE (simulado):
8. Lê arquivo de backup
9. Mostra o que seria restaurado
10. Lista diferenças vs estado atual

Me mostra relatório de backup/restore.
```

---

## 🎯 COMANDOS DE VALIDAÇÃO

### Health check do sistema
```
Claude, executa health check completo:

1. COSMOS DB:
   - Conecta com sucesso?
   - Quantos projetos cadastrados?
   - Último projeto criado (quando?)

2. ESTRUTURA DE DADOS:
   - Todos projetos têm campos obrigatórios?
   - Algum valor inconsistente?
   - Datas inválidas?

3. INTEGRIDADE:
   - Projetos órfãos (sem topógrafo)
   - Pagamentos > valor total
   - Assinaturas > vizinhos cadastrados

Me mostra score de saúde (0-100%) e lista de problemas encontrados.
```

### Teste de carga
```
Claude, simula carga no sistema:

Cria 50 projetos de teste com dados realistas:
- Nomes variados (Fazenda, Loteamento, Sítio, etc)
- Locais diferentes (cidades do interior SP)
- Valores entre R$ 5.000 e R$ 50.000
- Status variados (30% em_andamento, 50% concluído, 20% pendente)

Para cada projeto, adiciona:
- 2-6 vizinhos (aleatório)
- 1-3 pagamentos (aleatório)
- 40-90% de assinaturas (aleatório)

Depois:
- Gera relatório de todos
- Testa busca por filtros
- Calcula performance

Me mostra tempo total e possíveis gargalos.
```

---

## 📖 DOCUMENTAÇÃO AUTOMÁTICA

### Gerar documentação de APIs
```
Claude, documenta todas as operações do MCP Cosmos DB:

Para cada ferramenta (create_project, list_projects, etc):

1. Nome da ferramenta
2. Parâmetros (obrigatórios e opcionais)
3. Exemplo de entrada (JSON)
4. Exemplo de saída (JSON)
5. Erros possíveis
6. Casos de uso

Salva em formato Markdown em:
C:\Docs\mcp-cosmos-db-api.md
```

---

## 🚀 INÍCIO RÁPIDO

**Comece com estes 3 comandos:**

### 1️⃣ Criar projeto de teste
```
Claude, cria projeto "Meu Primeiro Teste" em São Paulo-SP, 
proprietário João, valor R$ 10.000
```

### 2️⃣ Listar todos os projetos
```
Claude, lista todos os projetos do Cosmos DB
```

### 3️⃣ Gerar relatório
```
Claude, gera relatório resumido de todos os projetos
e salva em C:\Relatorios\resumo.txt
```

---

**💡 DICA:** Todos esses comandos funcionam **SEM ESCREVER CÓDIGO**!  
Claude usa os MCPs automaticamente para executar as operações.

**🎯 Resultado:** Você valida funcionalidades em **minutos** vs **horas** de desenvolvimento!
