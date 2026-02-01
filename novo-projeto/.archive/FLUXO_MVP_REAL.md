# 🎯 ATIVO REAL - FLUXO COMPLETO REAL

**MVP Focado:** Cliente por link único + múltiplos clientes por trabalho + Topógrafo gerencia tudo

---

## 1️⃣ CLIENTE (LINK ÚNICO)

### Entrada
```
Cliente recebe: ativoreal.com/projeto/abc123def456

Clica → Landing page com:
├─ Logo + branding
├─ Formulário de login (email/CPF + senha)
└─ Opção: "Primeira vez? Cadastre-se"
```

### Dashboard do Cliente
```
Após login, acessa PÁGINA ÚNICA com:

┌─────────────────────────────────────────────────┐
│                 SEU PROJETO                     │
├─────────────────────────────────────────────────┤
│                                                 │
│  📋 INFORMAÇÕES CADASTRAIS (Editável)           │
│  ├─ Nome completo                               │
│  ├─ CPF                                          │
│  ├─ Email                                        │
│  ├─ Telefone                                     │
│  ├─ Endereço (cidade, estado, CEP)              │
│  ├─ Área estimada (hectares)                    │
│  └─ Descrição da propriedade                    │
│                                                 │
│  🗺️ VISUALIZAÇÃO DA ÁREA (Mapa Preview)        │
│  ├─ Cliente desenha polígono                    │
│  ├─ Sistema mostra área calculada               │
│  └─ Não é documento oficial, só referência      │
│                                                 │
│  📄 CONTRATO                                    │
│  ├─ [Visualizar PDF]                            │
│  ├─ [Baixar]                                    │
│  └─ [Assinar digitalmente] (se implementado)   │
│                                                 │
│  💳 FORMAS DE PAGAMENTO                         │
│  ├─ Valor total: R$ 2.500                       │
│  ├─ Pago: R$ 0                                  │
│  ├─ Pendente: R$ 2.500                          │
│  └─ [Pagar com PIX/Cartão/Boleto]              │
│                                                 │
│  📁 IMPORTAR/EXPORTAR                           │
│  ├─ [Importar KML/GeoJSON]                      │
│  ├─ [Exportar dados em PDF]                     │
│  ├─ [Exportar dados em Excel]                   │
│  └─ [Exportar dados em GeoJSON]                 │
│                                                 │
│  📊 ACOMPANHAMENTO DO TRABALHO                  │
│  ├─ Status: Aguardando levantamento em campo   │
│  ├─ Topógrafo: João Silva                      │
│  ├─ Última atualização: 30/01/2026 14:30       │
│  ├─ Histórico:                                 │
│  │  ├─ [✅] 29/01 - Projeto criado             │
│  │  ├─ [⏳] 30/01 - Levantamento agendado      │
│  │  └─ [⏳] 31/01 - Análise de vizinhos        │
│  └─ Previsão de conclusão: 15/02/2026          │
│                                                 │
│  💬 MENSAGENS COM TOPÓGRAFO (Chat)              │
│  ├─ [Última msg: "Confirma se há cercado?"]   │
│  ├─ [Você: "Sim, tem cercado novo"]            │
│  └─ [Nova mensagem...]                         │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Importante:** TUDO em UMA página (scroll), não múltiplas abas.

---

## 2️⃣ TOPÓGRAFO (DASHBOARD)

### Entrada
```
Topógrafo login: topografo@empresa.com

Dashboard exibe todos os trabalhos com:
├─ Filtros: Status, Cliente, Data
├─ Busca: Por nome ou CPF do cliente
└─ Ordenação: Mais recentes / Mais urgentes
```

### Visualização de Trabalhos
```
┌────────────────────────────────────────────────────────┐
│ TRABALHOS - Você tem 12 projetos em andamento         │
├────────────────────────────────────────────────────────┤
│                                                        │
│ 🔴 URGENTE - Gleba Rio Claro (SP)                     │
│  ├─ Clientes: João Silva + Maria Oliveira (2)        │
│  ├─ Status: Levantamento em campo                    │
│  ├─ Área total: 125.5 ha                             │
│  ├─ Lotes: 3 (Lote A, B, C)                          │
│  ├─ Data levantamento: 30/01                         │
│  ├─ Vizinhos identificados: 5                        │
│  ├─ Progresso: ████░░░░░░ 40%                        │
│  └─ [Ver detalhes]                                  │
│                                                        │
│ 🟡 EM ANÁLISE - Sítio Boa Vista (MG)                 │
│  ├─ Clientes: Pedro Santos (1)                       │
│  ├─ Status: Análise de vizinhos                      │
│  ├─ Área total: 45.8 ha                              │
│  ├─ Lotes: 1                                         │
│  ├─ Data levantamento: 25/01                         │
│  ├─ Vizinhos identificados: 3                        │
│  ├─ Progresso: ███████░░░ 70%                        │
│  └─ [Ver detalhes]                                  │
│                                                        │
│ 🟢 PRONTO PARA ENTREGA - Fazenda Sul (RS)            │
│  ├─ Clientes: Carlos Alberto (1)                     │
│  ├─ Status: Peças técnicas prontas                   │
│  ├─ Área total: 250 ha                               │
│  ├─ Lotes: 5                                         │
│  ├─ Peças: Memorial + Planta + Caderneta            │
│  └─ [Entregar] [Editar] [Ver detalhes]             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Detalhe do Trabalho (Múltiplos Clientes)
```
PROJETO: Gleba Rio Claro
════════════════════════════════════════

CLIENTES (Múltiplos):
├─ 👤 João Silva
│  ├─ CPF: 123.456.789-00
│  ├─ Email: joao@email.com
│  ├─ Telefone: (19) 98765-4321
│  ├─ Lotes: A, B (105 ha)
│  ├─ Status do pagamento: ✅ Pago
│  └─ Link de acesso: ativoreal.com/projeto/xxxyyy111
│
└─ 👤 Maria Oliveira
   ├─ CPF: 987.654.321-00
   ├─ Email: maria@email.com
   ├─ Telefone: (19) 99876-5432
   ├─ Lotes: C (20.5 ha)
   ├─ Status do pagamento: ⏳ Pendente R$ 500
   └─ Link de acesso: ativoreal.com/projeto/xxxyyy222

LOTES:
├─ Lote A: 50 ha (João)
│  ├─ Limites: 1.800m de perímetro
│  ├─ Vizinhos: 3 identificados
│  └─ Status: ✅ Levantamento concluído
├─ Lote B: 55 ha (João)
│  ├─ Limites: 1.950m de perímetro
│  ├─ Vizinhos: 2 identificados
│  └─ Status: ⏳ Aguardando confirmação de vizinhos
└─ Lote C: 20.5 ha (Maria)
   ├─ Limites: 980m de perímetro
   ├─ Vizinhos: 4 identificados
   └─ Status: ✅ Levantamento concluído

LEVANTAMENTO DE CAMPO:
├─ Data: 30/01/2026
├─ Topógrafo responsável: Você
├─ Equipamento: Drone + GPS RTK
├─ Pontos coletados: 847
├─ Precisão: ±0.15m
└─ Notas: "Cercado novo lado norte, vizinho confirmou limite"

CAMADAS DO GOVERNO (WMS):
├─ [+ Adicionar camada WMS]
├─ ✅ SIGEF: https://sigef.incra.gov.br/geo/wms
│  └─ Visível: ☑ | Opacidade: 70%
├─ ✅ CAR: https://car.gov.br/publico/municipios/wms
│  └─ Visível: ☑ | Opacidade: 50%
└─ ✅ FUNAI: https://geoserver.funai.gov.br/wms
   └─ Visível: ☐ | Opacidade: 80%

VIZINHOS IDENTIFICADOS:
├─ Fazenda Santa Maria (SIGEF - Matrícula 123456)
│  ├─ Confrontação: Lote A - Norte - 523m
│  └─ Status: ✅ Informação confirmada
├─ Propriedade de Pedro Santos (CPF 111.222.333-44)
│  ├─ Confrontação: Lote A - Leste - 387m
│  └─ Status: ⏳ Aguardando confirmação
├─ Terra Indígena Santuário (FUNAI)
│  ├─ Confrontação: Lote B - Oeste - 2km (buffer)
│  └─ Status: ✅ Sem sobreposição
└─ Via pública (Rua das Flores)
   ├─ Confrontação: Lotes A,B,C - Sul
   └─ Status: ✅ Confirmado

PEÇAS TÉCNICAS:
├─ [📝 Memorial Descritivo]
├─ [🗺️ Planta de Situação]
├─ [📊 Caderneta de Campo]
├─ [📋 Tabela de Coordenadas]
└─ [📑 Carta de Confrontação]

HISTÓRICO:
├─ 29/01 14:30 - Projeto criado por João Silva
├─ 29/01 16:45 - Maria Oliveira adicionada como cliente
├─ 30/01 08:00 - Levantamento em campo iniciado
├─ 30/01 17:30 - Dados processados
├─ 31/01 10:00 - Vizinhos identificados (você agora)
└─ [Adicionar nota]

AÇÕES DISPONÍVEIS:
├─ [Editar dados dos clientes]
├─ [Editar lotes]
├─ [Adicionar/Remover camadas WMS]
├─ [Gerar peças técnicas]
├─ [Exportar em CAD (futuro)]
├─ [Marcar como entregue]
└─ [Finalizar projeto]
```

---

## 3️⃣ FLUXO COMPLETO (Timeline)

### DIA 1: Cliente recebe link
```
Topógrafo envia: "ativoreal.com/projeto/abc123"

Cliente:
├─ Abre link
├─ Faz login (ou cria conta)
├─ Preenche formulário de cadastro
├─ Desenha propriedade no mapa (preview)
├─ Visualiza contrato
├─ Efetua pagamento (PIX/Cartão/Boleto)
└─ Fica aguardando topógrafo fazer levantamento
```

### DIA 2-3: Topógrafo faz levantamento
```
Topógrafo:
├─ Vai a campo com equipamento
├─ Coleta pontos GPS com precisão
├─ Tira fotos dos limites e vizinhos
├─ Anota notas em caderneta digital
└─ Retorna para processar dados

Sistema:
├─ Processa nuvem de pontos
├─ Identifica limites automáticos
├─ Busca vizinhos no banco (SIGEF, INCRA, CAR)
└─ Atualiza dashboard do cliente
```

### DIA 4-5: Topógrafo gera peças
```
Topógrafo (no sistema):
├─ Revisa dados coletados
├─ Valida limites e vizinhos
├─ Clica: [Gerar Peças Técnicas]
│  └─ Sistema cria:
│     ├─ Memorial descritivo
│     ├─ Planta de situação
│     ├─ Caderneta de campo
│     ├─ Tabela de coordenadas
│     └─ Carta de confrontação
├─ Revisa peças (com CAD futuro: Métrica Topo)
├─ Exporta em PDF/DWG
└─ Marca como "Pronto para entrega"

Cliente:
├─ Recebe notificação: "Peças técnicas prontas!"
├─ Acessa página
├─ Visualiza/Baixa peças
└─ Confirma: "Autorizo entrega ao INCRA"
```

### DIA 6+: Entrega
```
Topógrafo:
├─ Envia peças para INCRA/Prefeitura/Cartório
├─ Acompanha processo
├─ Marca projeto como "Entregue"

Cliente:
├─ Recebe protocolo de entrega
├─ Vê status: ✅ Processo concluído
└─ Gera relatório de tudo que foi feito
```

---

## 🏗️ ESTRUTURA DO APP (1 página por perfil)

### Cliente
```
Landing → Login → Dashboard único com:
├─ Formulário (topo)
├─ Mapa (meio)
├─ Contrato (rolagem)
├─ Pagamento (rolagem)
├─ Importar/Exportar (rolagem)
├─ Acompanhamento (rolagem)
└─ Chat com topógrafo (rodapé)
```

### Topógrafo
```
Login → Dashboard de trabalhos
├─ Lista de projetos (topo)
└─ Clique em projeto → Modal/Overlay com todos os detalhes
```

---

## 🎯 MVP MÍNIMO (O que fazer agora)

1. **Cliente - Página única funcionando**
   - ✅ Formulário editável
   - ✅ Mapa com desenho
   - ✅ Contrato visualizável
   - ✅ Pagamento integrado
   - ✅ Acompanhamento (lista de status)

2. **Topógrafo - Dashboard de trabalhos**
   - ✅ Lista de projetos
   - ✅ Filtros/Busca
   - ✅ Detalhe de projeto com múltiplos clientes
   - ✅ Histórico de atividades

3. **Backend**
   - ✅ Criar/Listar projetos
   - ✅ Múltiplos clientes por projeto
   - ✅ Múltiplos lotes por cliente
   - ✅ Salvar URLs de camadas WMS por projeto
   - ✅ Buscar vizinhos (PostGIS)
   - ✅ Gerar peças técnicas (template)

4. **Camadas WMS (OpenLayers)**
   - ✅ Topógrafo adiciona URL
   - ✅ Sistema valida e carrega camada
   - ✅ Controle de visibilidade/opacidade
   - ✅ Salva configuração por projeto

5. **Integração CAD** → FUTURO (não é MVP)

---
Camadas WMS (OpenLayers):** 2h
- **Testes e ajustes:** 2h

**Total: ~17
- **Frontend cliente (página única):** 4h
- **Frontend topógrafo (dashboard):** 3h
- **Backend (CRUD + lógica):** 4h
- **PostGIS (vizinhos):** 2h
- **Testes e ajustes:** 2h

**Total: ~15 horas** (2 dias completos)

---

Esse é o fluxo real?
