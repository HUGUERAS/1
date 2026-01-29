# 🎯 Casos de Uso Específicos - Ativo Real + MCP

## Baseado nas funcionalidades **reais** que faltam no app atual

---

## 🔥 CASO 1: Dashboard do Topógrafo (Funcionalidade Faltante)

### **Problema Atual:**
[DashboardTopografo.tsx](../ativo-real/src/DashboardTopografo.tsx) mostra lista básica, mas falta:
- ❌ Filtros avançados
- ❌ Ordenação por múltiplos campos
- ❌ Métricas de produtividade
- ❌ Gráficos de progresso

### **Teste com MCP:**

```
Claude, simula dashboard completo do topógrafo "João Silva":

1. Lista projetos dele com estatísticas:
   - Em andamento: quantidade e % de progresso médio
   - Concluídos no mês: quantidade
   - Atrasados: quantidade e dias de atraso médio
   - Valor total em carteira (soma de projetos ativos)

2. Calcula métricas de produtividade:
   - Tempo médio de conclusão (dias)
   - Taxa de sucesso (100% assinado)
   - Receita gerada no mês
   - Projetos por tipo (desmembramento, CAR, etc)

3. Identifica ações urgentes:
   - Projetos sem atualização 10+ dias
   - Assinaturas faltantes (< 80%)
   - Pagamentos pendentes

4. Salva dashboard em C:\Dashboards\joao-silva-{data}.json

Me mostra resumo visual com números-chave.
```

**Resultado:** Você descobre **exatamente** quais KPIs colocar no dashboard React!

---

## 🔥 CASO 2: GlobalMap - Seleção de Lotes (Funcionalidade Faltante)

### **Problema Atual:**
[GlobalMap.tsx](../ativo-real/src/GlobalMap.tsx) só tem desenho básico, mas falta:
- ❌ Salvar polígonos desenhados
- ❌ Calcular área automaticamente
- ❌ Validar sobreposições
- ❌ Exportar para KML/GeoJSON

### **Teste com MCP:**

```
Claude, simula workflow de desenho de lote:

1. Cria arquivo GeoJSON simulando polígono desenhado no mapa:
   - Nome: "Lote 15 - Fazenda Boa Vista"
   - 6 vértices (coordenadas de Campinas-SP)
   - Salva em C:\Temp\lote-15-desenhado.geojson

2. Calcula automaticamente:
   - Área em hectares
   - Perímetro em metros
   - Centroide (lat/lon)
   - Coordenadas dos vértices em UTM

3. Valida geometria:
   - Polígono é fechado?
   - Tem auto-interseções?
   - Área mínima respeitada? (> 0.5ha)

4. Salva metadados no Cosmos DB:
   - Projeto: "Fazenda Boa Vista"
   - Lote: 15
   - Área: {calculada}
   - Arquivo: lote-15-desenhado.geojson
   - Status: "desenhado"

5. Gera relatório de validação

Me mostra se o lote passou em todas as validações.
```

**Resultado:** Você sabe **exatamente** quais validações implementar no OpenLayers!

---

## 🔥 CASO 3: Sistema de Status Inteligente (Funcionalidade Faltante)

### **Problema Atual:**
App tem status (`em_andamento`, `concluido`), mas falta:
- ❌ Transições de status automáticas
- ❌ Validações de pré-requisitos
- ❌ Notificações de mudança de status
- ❌ Histórico de status

### **Teste com MCP:**

```
Claude, testa máquina de estados do projeto:

1. Cria projeto "Teste Status Flow"

2. Simula transições de status com validações:

   a) "rascunho" → "em_andamento":
      - Valida: tem proprietário?
      - Valida: tem valor contratado?
      - Valida: tem topógrafo responsável?
      - Se OK: muda status + registra timestamp
      - Se ERRO: lista campos faltantes

   b) "em_andamento" → "aguardando_assinaturas":
      - Valida: tem arquivo topográfico?
      - Valida: tem vizinhos cadastrados?
      - Valida: área calculada?
      - Se OK: gera links de convite
      - Se ERRO: bloqueia transição

   c) "aguardando_assinaturas" → "protocolar":
      - Valida: 100% assinaturas obtidas?
      - Valida: pagamento >= 50%?
      - Se OK: prepara documentos
      - Se ERRO: mostra pendências

   d) "protocolar" → "concluido":
      - Valida: protocolo registrado?
      - Valida: pagamento 100%?
      - Se OK: fecha projeto + gera certificado
      - Se ERRO: lista documentos faltantes

3. Para cada transição, registra:
   - Data/hora
   - Usuário responsável
   - Status anterior e novo
   - Validações executadas
   - Erros encontrados

4. Salva máquina de estados em C:\Docs\status-flow.json

Me mostra diagrama de estados possíveis e transições válidas.
```

**Resultado:** Você tem **regras de negócio claras** para implementar no backend!

---

## 🔥 CASO 4: Onboarding de Vizinhos (Funcionalidade Faltante)

### **Problema Atual:**
Não existe fluxo de assinatura digital para vizinhos.

### **Teste com MCP:**

```
Claude, simula fluxo completo de assinatura de vizinho:

1. GERAÇÃO DE CONVITE:
   - Projeto: "Fazenda Teste Vizinho"
   - Vizinho: "Carlos Mendes"
   - Gera link único: https://ativo.real/assinar/{token}
   - Token expira em: 30 dias
   - Email/SMS enviado: (simulado)

2. ACESSO DO VIZINHO:
   - Vizinho abre link
   - Valida token (não expirado?)
   - Carrega dados do projeto:
     * Memorial descritivo
     * Mapa do lote
     * Coordenadas confrontantes
   - Mostra declaração a ser assinada

3. ASSINATURA:
   - Vizinho confirma dados pessoais
   - Aceita termos
   - "Assina" digitalmente (simula)
   - Registra:
     * IP do acesso
     * Data/hora
     * Geolocalização (se disponível)

4. PÓS-ASSINATURA:
   - Marca vizinho como "assinado" no Cosmos DB
   - Gera PDF do documento assinado
   - Envia cópia por email
   - Notifica topógrafo
   - Atualiza % de assinaturas do projeto

5. AUDITORIA:
   - Salva log completo em C:\Assinaturas\carlos-mendes-{timestamp}.json

Me mostra cada etapa do fluxo e possíveis erros.
```

**Resultado:** Você define **toda a UX** antes de criar as telas!

---

## 🔥 CASO 5: Sistema de Arquivos Versionados (Funcionalidade Faltante)

### **Problema Atual:**
Upload de arquivo sobrescreve o anterior, sem histórico.

### **Teste com MCP:**

```
Claude, simula versionamento de arquivos topográficos:

PROJETO: "Fazenda Versões"

1. UPLOAD VERSÃO 1:
   - Arquivo: fazenda-v1.kml
   - Data: 2026-01-10
   - Área: 18.5 ha
   - Vértices: 8
   - Salva como: C:\Arquivos\proj_123\v1_fazenda.kml
   - Registra no Cosmos DB:
     * versao: 1
     * arquivo: "v1_fazenda.kml"
     * hash: {MD5}
     * usuário: "João Silva"
     * motivo: "Levantamento inicial"

2. UPLOAD VERSÃO 2:
   - Arquivo: fazenda-v2.kml (área corrigida)
   - Data: 2026-01-15
   - Área: 18.7 ha (+0.2ha)
   - Vértices: 8 (coordenadas ajustadas)
   - Salva como: C:\Arquivos\proj_123\v2_fazenda.kml
   - Mantém v1 no histórico
   - Registra diferenças:
     * delta_area: +0.2ha
     * vertices_alterados: [1, 3, 5]
     * motivo: "Correção após vistoria"

3. UPLOAD VERSÃO 3:
   - Arquivo: fazenda-v3.kml (mudança maior)
   - Data: 2026-01-20
   - Área: 19.2 ha (+0.5ha vs v2)
   - Vértices: 10 (adicionou 2)
   - Alerta: mudança significativa (> 2%)
   - Requer aprovação do cliente
   - Status: "pendente_aprovacao"

4. HISTÓRICO:
   - Lista todas as versões
   - Permite comparar v1 vs v2 vs v3
   - Mostra evolução da área
   - Identifica quem fez cada mudança
   - Permite rollback para v1 ou v2 se necessário

5. VALIDAÇÃO:
   - Todas versões preservadas?
   - Hashes únicos?
   - Histórico completo?
   - Diferenças rastreadas?

Salva relatório de versionamento em:
C:\Historicos\fazenda-versoes-timeline.txt

Me mostra comparação visual entre versões.
```

**Resultado:** Você tem **sistema de versionamento completo** antes de implementar!

---

## 🔥 CASO 6: Precificação Inteligente (Funcionalidade Faltante)

### **Problema Atual:**
Não tem sugestão automática de preço baseada em histórico.

### **Teste com MCP:**

```
Claude, cria sistema de precificação inteligente:

1. ANÁLISE DE HISTÓRICO:
   - Lista TODOS os projetos concluídos do Cosmos DB
   - Extrai dados:
     * Tipo de projeto (desmembramento, CAR, geo)
     * Área (hectares)
     * Localização (cidade)
     * Valor cobrado
     * Complexidade (nº de vizinhos)
     * Tempo de conclusão (dias)

2. CÁLCULO DE MÉDIAS:
   - Valor médio por hectare, por tipo
   - Valor médio por vizinho
   - Ajuste por localização (capital vs interior)
   - Prêmio por complexidade

3. NOVO PROJETO (simulado):
   - Tipo: "desmembramento"
   - Área: 25 hectares
   - Local: "Campinas-SP" (interior)
   - Vizinhos: 6
   
   SUGESTÃO DE PREÇO:
   - Base (área): 25ha × R$ 800/ha = R$ 20.000
   - Complexidade (vizinhos): 6 × R$ 500 = R$ 3.000
   - Ajuste regional (Campinas): +10% = R$ 2.300
   - TOTAL SUGERIDO: R$ 25.300
   
   RANGE:
   - Mínimo (-15%): R$ 21.505
   - Recomendado: R$ 25.300
   - Máximo (+20%): R$ 30.360

4. COMPARAÇÃO:
   - Projetos similares (mesma região, área parecida)
   - Preço praticado por concorrentes (se disponível)
   - Taxa de conversão por faixa de preço

5. RECOMENDAÇÃO FINAL:
   "Com base em 47 projetos similares, recomendamos:
    R$ 25.300 (probabilidade de aceitação: 78%)"

Salva análise em C:\Precificacao\novo-projeto-analise.json

Me mostra lógica de cálculo detalhada.
```

**Resultado:** Você tem **algoritmo de pricing** validado antes de codificar!

---

## 🔥 CASO 7: Alertas de Conformidade INCRA/SIGEF (Funcionalidade Faltante)

### **Problema Atual:**
Não valida se projeto está conforme normas técnicas.

### **Teste com MCP:**

```
Claude, valida conformidade com normas INCRA/SIGEF:

PROJETO: "Fazenda Certificação"

1. VALIDAÇÕES TÉCNICAS:
   
   a) ÁREA:
      - Mínimo módulo rural respeitado? (depende da região)
      - Área declarada = área calculada? (tolerância: ±2%)
      - Área compatível com matrícula?
   
   b) COORDENADAS:
      - Sistema: SIRGAS 2000 (obrigatório)
      - Precisão: classe A? (±10cm)
      - Amarração: tem vértices homologados?
   
   c) MEMORIAL DESCRITIVO:
      - Azimutes calculados?
      - Distâncias conferem?
      - Área por coordenadas analíticas OK?
   
   d) CONFRONTANTES:
      - Todos identificados?
      - CPF/CNPJ válidos?
      - Assinaturas obtidas?

2. CHECKLIST SIGEF:
   - [ ] Vértices com precisão adequada
   - [ ] Sobreposição com outras parcelas verificada
   - [ ] Memorial descritivo completo
   - [ ] ART de responsabilidade técnica anexada
   - [ ] Certificado de cadastro atualizado

3. PONTOS DE ATENÇÃO:
   - Área próxima a APP (verificar 30m de rio)
   - Dentro de Terra Indígena? (consultar FUNAI)
   - Área de reserva legal averbada?

4. STATUS DE CONFORMIDADE:
   - APROVADO: pronto para protocolar
   - PENDENTE: lista de documentos faltantes
   - REPROVADO: problemas críticos encontrados

5. RELATÓRIO:
   Salva análise completa em:
   C:\Conformidade\fazenda-certificacao-sigef.txt

Me mostra score de conformidade (0-100%) e itens não conformes.
```

**Resultado:** Você tem **checklist automatizado** antes de submeter ao INCRA!

---

## 🔥 CASO 8: Integração com WhatsApp (Funcionalidade Faltante)

### **Problema Atual:**
Comunicação com vizinhos é manual (telefone/email).

### **Teste com MCP:**

```
Claude, simula envio de notificações via WhatsApp:

1. CADASTRO DE VIZINHO:
   - Nome: "José Silva"
   - Telefone: +55 11 98765-4321
   - Projeto: "Fazenda Notificações"

2. MENSAGENS PROGRAMADAS:

   a) CONVITE PARA ASSINATURA:
      "Olá José! Você foi identificado como confrontante do 
       imóvel Fazenda XYZ em Campinas-SP. 
       
       Por favor, acesse o link abaixo para revisar e assinar 
       o memorial descritivo:
       
       https://ativo.real/assinar/abc123xyz
       
       Link válido por 30 dias.
       
       Dúvidas? Ligue (11) 3333-4444
       
       Ativo Real - Topografia"

   b) LEMBRETE (7 dias depois se não assinou):
      "Olá José! Lembramos que você ainda não assinou o 
       documento do imóvel Fazenda XYZ.
       
       Acesse: https://ativo.real/assinar/abc123xyz
       
       Restam 23 dias para expirar."

   c) CONFIRMAÇÃO (após assinatura):
      "Obrigado José! Sua assinatura foi registrada com sucesso.
       
       Uma cópia do documento foi enviada para seu email.
       
       Protocolo: #ASS-2026-00123"

3. RASTREAMENTO:
   - Mensagem enviada: ✅ (2026-01-23 10:30)
   - Entregue: ✅ (2026-01-23 10:31)
   - Lida: ✅ (2026-01-23 11:15)
   - Link clicado: ✅ (2026-01-23 11:18)
   - Assinado: ✅ (2026-01-23 11:25)

4. ANALYTICS:
   - Taxa de abertura: 85%
   - Taxa de clique: 67%
   - Taxa de conversão: 52%
   - Tempo médio até assinatura: 3.2 dias

Salva log de mensagens em:
C:\Notificacoes\whatsapp-log-{projeto}.json

Me mostra templates de mensagens e métricas de engajamento.
```

**Resultado:** Você tem **workflow de comunicação** completo antes de integrar API!

---

## 🎯 RESUMO: O que MCP permite testar SEM CÓDIGO

| Funcionalidade | Teste com MCP | Tempo | Benefício |
|----------------|---------------|-------|-----------|
| Dashboard KPIs | ✅ Simular métricas | 10min | Define quais gráficos criar |
| Cálculo de áreas | ✅ Validar geometria | 5min | Testa OpenLayers antes de UI |
| Máquina de estados | ✅ Validar transições | 15min | Regras de negócio claras |
| Assinatura digital | ✅ Fluxo completo | 20min | Define toda UX antecipadamente |
| Versionamento | ✅ Histórico de mudanças | 15min | Sistema de backup robusto |
| Precificação | ✅ Algoritmo de pricing | 10min | Validação com dados reais |
| Conformidade SIGEF | ✅ Checklist automatizado | 15min | Zero erros no protocolo |
| WhatsApp | ✅ Templates e tracking | 10min | Workflow de comunicação |

**TOTAL:** ~1h30min de testes = **20+ horas de desenvolvimento economizadas**

---

## 💡 WORKFLOW RECOMENDADO

Para cada funcionalidade nova:

1. **Teste com MCP** (5-15min)
   - Valide lógica de negócio
   - Identifique edge cases
   - Defina estrutura de dados

2. **Documente** (5min)
   - Salve exemplos de entrada/saída
   - Registre regras de validação
   - Liste campos obrigatórios

3. **Implemente UI** (1-2h)
   - Com confiança (lógica já validada)
   - Sem retrabalho
   - Menos bugs

4. **Integre backend** (30min)
   - Estruturas já definidas
   - Validações já testadas
   - Zero surpresas

**Resultado:** Features implementadas **3x mais rápido** com **90% menos bugs**! 🚀

---

**🎯 Use MCP como seu "laboratório de features" antes de codar!**
