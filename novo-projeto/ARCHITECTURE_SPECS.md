# 🏗️ Especificação de Arquitetura: Bem Real SaaS

Este documento define a lógica, fluxo de dados e requisitos para o sistema de regularização fundiária, focado na segregação de 3 perfis de usuários.

## 🎭 Os 3 Atores (Perfis) e Integração com Legado

### 1. 👷‍♂️ O Topógrafo (Admin/Orquestrador) - **FOCO DESTA ATUALIZAÇÃO**
*   **Onde Fica:** Acessível pelo card "Topógrafo" na Landing Page (`App.tsx`).
*   **Papel:** Criador do Projeto e Revisor Técnico.
*   **Responsabilidades:**
    *   Define o perímetro global da Fazenda (Área Mãe).
    *   Configura as regras do desmembramento (ex: tamanho mínimo de lote).
    *   Gera os "Links Mágicos" para convidar os proprietários.
    *   **Visão de Deus (God Mode):** Vê o mapa completo com todos os lotes (preenchidos e vazios) e pode corrigir desenhos dos clientes.

### 2. 🤠 O Proprietário Individual (Urbano/Rural) - Preservado
*   **Onde Fica:** Cards "Proprietário" e "Agricultor" na Landing Page.
*   **Status Atual:** As páginas existentes (`RuralDashboard.tsx`, etc.) **SERÃO MANTIDAS**.
*   **Evolução:** No futuro, esses perfis poderão visualizar também os projetos onde foram convidados pelo Topógrafo, unificando a experiência.

### 3. Fatores de Integração
*   O novo sistema de "Bem Real" (Gestão de Projetos) será um módulo adicional dentro do Portal do Topógrafo.
*   As funcionalidades de **Cadastro Ambiental Rural (CAR)** do Agricultor e **Consulta de Matrícula** do Proprietário Urbano continuam funcionando independentemente.

---

## 📐 Fluxo de Dados e User Stories

### User Story 1: O Fluxo do Topógrafo (Setup)
1.  **Criação do Projeto:**
    *   Topógrafo faz upload de um KML/Shapefile da "Fazenda Mãe" ou desenha no mapa.
    *   Sistema valida se essa área mãe sobrepõe terra indígena ou quilombola (SIGEF Check).
2.  **Disparo de Convites:**
    *   Input: Lista de emails/phones dos clientes.
    *   Processo: Sistema gera tokens JWT únicos com validade (ex: 7 dias) contendo `projeto_id` e permissão `draw:self`.
    *   Output: Envio de WhatsApp/Email automático.

### User Story 2: O Fluxo do Cliente (Execution)
1.  **Acesso Seguro:**
    *   Cliente clica no link -> API valida token -> Frontend carrega o mapa centralizado na região do projeto.
2.  **Desenho Guiado (The Pit of Success):**
    *   O cliente usa ferramenta de polígono.
    *   **Restrição Hard:** O desenho não pode sair de dentro do polígono da "Fazenda Mãe" definido pelo Topógrafo.
    *   **Validação Live:** Ao fechar o polígono, o Backend verifica `ST_Intersects` com vizinhos e SIGEF.
        *   *Sucesso:* Área fica verde. Botão "Avançar" habilita.
        *   *Erro:* Área fica vermelha e mostra mensagem amigável: "Sua cerca está invadindo a área do Sr. João. Por favor, ajuste os pontos."
3.  **Checkout e Legal:**
    *   Tela de Pagamento (Stripe/InfinitePay).
    *   Geração de Contrato PDF com os dados do desenho (Área, Perímetro, Confrontantes).

---

## 🛠️ Stack Tecnológica Sugerida (Geometria & Dados)

### Backend (The Brain)
*   **Linguagem:** Python 3.11 (Azure Functions).
*   **Libs Geométricas:** 
    *   `Shapely`: Para operações booleanas (Union, Difference, Intersection) e validação topológica (`is_valid`).
    *   `PyProj`: Para cálculo preciso de área geodésica (m² reais na curvatura da terra).
*   **Banco de Dados:** PostgreSQL + **PostGIS** (Mandatório).
    *   Tipos: `GEOGRAPHY` para cálculos de área/distância, `GEOMETRY` (SIRGAS 2000) para operações de desenho.

### Frontend (The Canvas)
*   **Framework:** React + Vite.
*   **Map Engine:** **OpenLayers**.
    *   *Por que não Google Maps?* Google Maps é ruim para edição precisa de polígonos. OpenLayers permite Snapping (imã) nativo e manipulação de vértices profissional.
*   **State Management:** Zustand ou Context API (para guardar o estado do desenho antes de salvar).

---

## 🔒 Modelo de Segurança (Nível de Dados)

| Ator | Insert | Update | Delete | Select (Ver) |
| :--- | :--- | :--- | :--- | :--- |
| **Topógrafo** | ✅ Projetos, Lotes | ✅ Tudo | ✅ Tudo | ✅ Tudo |
| **Cliente** | ✅ Seu Lote (Rascunho) | ✅ Seu Lote (Até Pagar) | ❌ | ✅ Seu Lote + Vizinhos (Read-only) |

### Regra de Ouro da Topologia
> "A soma das partes não pode ser maior que o todo, e as partes não podem se sobrepor."

1.  **Constraint de Banco:** `Check(ST_Within(lote.geom, projeto.geom))`
2.  **Constraint de Banco:** `Exclude(lote.geom WITH &&)` (Evita sobreposição no nível do índice espacial).

---

## 📝 Próximos Passos (Implementação)

1.  Criar tabela `Usuarios` com perfis (`ROLE_TOPOGRAPHER`, `ROLE_CLIENT`).
2.  Criar rota `POST /invite` que gera links assinados.
3.  Implementar o middleware que impede o Cliente de salvar se o desenho não passar na validação geométrica do Backend.
