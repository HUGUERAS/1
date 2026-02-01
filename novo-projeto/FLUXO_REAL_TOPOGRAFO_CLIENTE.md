# 🗺️ ATIVO REAL - FLUXO REAL (TOPOGRAFO + CLIENTE)

**Data:** 31/01/2026
**Verdadeiro Diferencial:** Cliente desenha → Topógrafo gera carta de confrontação

---

## 🎯 O FLUXO (DO ZERO ATÉ CARTA DE CONFRONTAÇÃO)

### 1️⃣ CLIENTE DESENHA (App)
```
Cliente abre app → Vê mapa vazio
↓
Desenha sua propriedade no mapa (polígono)
↓
Sistema calcula:
  - Área em hectares
  - Perímetro em metros
  - Coordenadas dos vértices
↓
Cliente salva projeto: "Propriedade João Silva - SP"
```

### 2️⃣ SISTEMA BUSCA VIZINHOS (Backend)
```
Quando cliente salva, backend faz:
  - Query PostGIS: ST_Buffer + ST_Intersects
  - Busca geometrias que tocam a área do cliente
  - Retorna: Nome do vizinho, CPF, endereço, área
  
Exemplo:
┌─────────────────────┐
│   João Silva        │  ← Cliente
│ (desenhou agora)    │
├─────────────────────┤
│ Vizinho N: Maria    │  ← Detectado automaticamente
│ Vizinho S: Pedro    │  ← Detectado automaticamente
│ Vizinho L: SIGEF    │  ← Detectado automaticamente
└─────────────────────┘
```

### 3️⃣ TOPOGRAFO RECEBE PROJETO (App)
```
Topógrafo vê na dashboard:
┌─────────────────────────────────────┐
│ Novo Projeto: João Silva            │
│ Status: Aguardando análise           │
│ Área: 45.8 hectares                 │
│ Vizinhos: 3 identificados            │
│ Ação: [Ver Projeto]                 │
└─────────────────────────────────────┘

Clica em "Ver Projeto" e visualiza:
- Área do cliente (azul)
- Limites dos vizinhos (cinza)
- Tabela com dados dos vizinhos:
  • Nome
  • CPF / CNPJ
  • Matrícula SNCR
  • Distância do limite
  • Área de confrontação
```

### 4️⃣ TOPOGRAFO GERA CARTA DE CONFRONTAÇÃO (App)
```
Topógrafo clica: [Gerar Carta]

Sistema cria:
────────────────────────────────────────
CARTA DE CONFRONTAÇÃO
Propriedade: João Silva
Local: São Paulo - SP
Data: 31/01/2026

DESCRIÇÃO DOS LIMITES:
─────────────────────

LIMITE NORTE:
Confronta com propriedade de Maria Oliveira (CPF xxx)
Azimute: 45°23'12"
Distância: 523,45 m
Descrição: Do ponto P1 ao ponto P2

LIMITE SUL:
Confronta com SIGEF / Gleba Rio Claro
Azimute: 135°10'48"
Distância: 387,23 m
Descrição: Do ponto P2 ao ponto P3

LIMITE LESTE:
Confronta com propriedade de Pedro Santos (CPF yyy)
Azimute: 225°45'30"
Distância: 298,67 m
Descrição: Do ponto P3 ao ponto P4

LIMITE OESTE:
Confronta com via pública (Rua das Flores)
Azimute: 315°22'15"
Distância: 445,89 m
Descrição: Do ponto P4 ao ponto P1

TOTAL: 1.655,24 m de perímetro
────────────────────────────────────────
```

### 5️⃣ CLIENTE APROVA (App)
```
Cliente recebe notificação:
"Sua carta de confrontação está pronta!"

Abre app e vê:
- Mapa com sua área + vizinhos + limites
- Carta em PDF (pode baixar)
- [Aprovar] [Pedir alterações]

Se aprova:
  ✅ Projeto passa para "Validado"
  ✅ Topógrafo pode prosseguir (pagamento, INCRA, etc)

Se pede alteração:
  "Limite norte está errado - vizinha disse que..."
  ↓ Volta para topógrafo revisar
  ↓ Topógrafo ajusta no mapa
  ↓ Volta para cliente
  ↓ Loop até aprovação
```

---

## 🔧 O QUE PRECISA EXISTIR

### Frontend
```
✅ Página: Cliente desenha área
   └─ Mapa vazio
   └─ Ferramentas: desenhar polígono
   └─ Botão: Salvar projeto
   └─ Input: Nome do projeto

✅ Página: Topógrafo vê projetos
   └─ Lista de "Novos projetos"
   └─ Ver cliente + área + vizinhos
   └─ Botão: Gerar carta

✅ Página: Carta de confrontação
   └─ Visualizar em PDF
   └─ Mapa com anotações
   └─ Tabela de confrontações

✅ Página: Cliente aprova
   └─ Ver carta
   └─ Aprovar / Pedir ajustes
```

### Backend
```
✅ POST /projects
   └─ Cliente desenha → salva geometria

✅ GET /projects/{id}/neighbors
   └─ Busca vizinhos via PostGIS
   └─ Retorna dados dos vizinhos

✅ POST /confrontation-letter
   └─ Gera carta (texto estruturado)

✅ PUT /projects/{id}/approve
   └─ Cliente aprova carta

✅ PUT /projects/{id}/request-changes
   └─ Cliente pede ajustes
```

### Database
```
✅ Tabela: projects
   ├─ id
   ├─ client_id
   ├─ topographer_id (NULL até aceitar)
   ├─ geometria (PostGIS)
   ├─ status (rascunho, aguardando, validado)
   └─ created_at

✅ Tabela: neighbors (pré-carregada com SIGEF/INCRA)
   ├─ id
   ├─ name
   ├─ cpf_cnpj
   ├─ geometria
   ├─ registration_number
   └─ data_source (SIGEF / INCRA / CAR)

✅ Tabela: confrontations
   ├─ id
   ├─ project_id
   ├─ neighbor_id
   ├─ azimuth
   ├─ distance
   ├─ confrontation_type (norte, sul, leste, oeste)
   └─ description
```

---

## ⏱️ MVP MÍNIMO (Quanto tempo?)

### Se focar APENAS nisso:

1. **Cliente desenha + salva** (2h)
   - Mapa + draw tool
   - POST /projects com geometria
   - Salvar no banco

2. **Backend busca vizinhos** (2h)
   - Query PostGIS para detectar vizinhos
   - Retornar dados estruturados

3. **Topógrafo vê e gera carta** (2h)
   - Dashboard de projetos
   - Gerar carta (template + dados)
   - Visualizar PDF

4. **Cliente aprova** (1h)
   - Página de aprovação
   - Feedback loop

**Total: 7 horas de trabalho FOCADO**

---

## 🚀 DIFERENCIAL REAL

Vs. Topógrafo tradicional:
- ❌ Topógrafo liga pro cliente pedindo info (demora dias)
- ❌ Cliente manda WhatsApp com coordenadas confusas
- ❌ Topógrafo tira print de Google Earth
- ❌ Cliente não sabe se entendeu direito

Com Ativo Real:
- ✅ Cliente desenha E VISUALIZA (sabe exatamente)
- ✅ Topógrafo recebe dados estruturados (0 confusão)
- ✅ Vizinhos já estão identificados (economia de tempo)
- ✅ Cliente aprova ANTES de gerar documento oficial
- ✅ Histórico de versões (rastreabilidade)

---

## 💡 PRÓXIMO PASSO

Esse é o fluxo real?

Se SIM: posso criar o código agora (7h de trabalho limpo)
Se NÃO: me diz o que falta
