# 🔧 Plano de Refatoração Cirúrgica - Ativo Real

## 🚨 PROBLEMA DIAGNOSTICADO

**Sintomas:**
- IAs não conseguem descrever o app
- Sem progresso real há semanas
- Cada mudança quebra algo

**Causa Raiz:**
- **Código morto** não removido
- **Duplicações** não consolidadas
- **Falta de testes** = medo de mudar
- **Documentação fragmentada** em 15 arquivos .md

---

## ✂️ FASE 1: AMPUTAÇÃO (1 dia)

### Remover arquivos MORTOS:

**Backend:**
```bash
DELETE novo-projeto/backend/AI_ENDPOINTS_TO_ADD.py  # Já está em function_app.py
DELETE novo-projeto/backend/check_tables.py          # Script pontual
DELETE novo-projeto/backend/create_tables.py         # Usa init/01_schema.sql
DELETE novo-projeto/backend/debug_connection.py      # Debug temporário
DELETE novo-projeto/test_openrouter_debug.py         # Teste já feito
DELETE novo-projeto/list_models.py                   # One-time script
DELETE novo-projeto/compare_models.py                # One-time script
```

**Frontend:**
```bash
DELETE ativo-real/src/components/AIChat.tsx          # Use AIAssistant.tsx
DELETE ativo-real/src/components/AIBotChat.tsx       # Use AIAssistant.tsx
DELETE ativo-real/demo.html                          # Não usado
```

**Documentação:**
```bash
# Manter APENAS:
- README.md (overview)
- ARCHITECTURE_SPECS.md (arquitetura)
- DEPLOY_GUIDE.md (deploy)

# DELETAR redundantes:
DELETE DEPLOY_INSTRUCTIONS.md
DELETE DEPLOY.md
DELETE PROJETO.md
DELETE MELHORIAS_CONSISTENCIA.md
DELETE ORGANIZACAO_INTERFACE.md
DELETE INTEGRACAO_ICONES_SVG.md
... (outros 10 arquivos)
```

---

## 🔄 FASE 2: CONSOLIDAÇÃO (2 dias)

### Backend - UM cliente AI:

```python
# DELETAR: jamba_analyzer.py, jamba_openrouter.py, ai_assistant.py
# MANTER: openrouter_client.py (único)

# novo-projeto/backend/ai_service.py (NOVO)
"""
Cliente AI unificado - Single Source of Truth
"""
class AIService:
    def __init__(self):
        # Prioridade: GitHub Models (grátis) > OpenRouter (pago)
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        if self.github_token:
            self.client = GitHubModelsClient()  # GRÁTIS
        elif self.openrouter_key:
            self.client = OpenRouterClient()
        else:
            raise ValueError("Configure GITHUB_TOKEN ou OPENROUTER_API_KEY")
    
    def analyze_topography(self, data): ...
    def validate_geometry(self, geojson): ...
    def generate_report(self, project): ...
    def chat(self, messages): ...
```

### Frontend - UM hook AI:

```typescript
// DELETAR: AIChat, AIBotChat
// MANTER: AIAssistant.tsx + useOpenRouter.ts

// Usar em qualquer lugar:
const { chat, loading } = useOpenRouter();
```

---

## 📝 FASE 3: DOCUMENTAÇÃO VIVA (1 dia)

### README.md (ÚNICO):

```markdown
# Ativo Real - GeoPlatform

## O que é?
Sistema de regularização fundiária com mapas interativos.

## Stack
- Frontend: React + OpenLayers (Azure SWA)
- Backend: Python + Azure Functions + PostgreSQL/PostGIS
- Auth: JWT
- AI: GitHub Models (grátis) ou OpenRouter (pago)

## Quick Start
1. `cd novo-projeto/backend && func start`
2. `cd ativo-real && npm run dev`
3. Abrir http://localhost:5173

## Estrutura
/backend
  function_app.py  - API REST (auth + projetos + AI)
  models.py        - SQLAlchemy models
  ai_service.py    - Cliente AI unificado
  
/ativo-real/src
  App.tsx          - Rotas (/, /login, /dashboard, /map)
  DashboardTopografo.tsx
  GlobalMap.tsx
  /components/shared  - Componentes reutilizáveis

## Perfis
- Topógrafo: cria projetos, desenha lotes
- Proprietário: visualiza + paga
- Agricultor: gestão CAR
```

**FIM**. Deletar outros 14 .md.

---

## 🧪 FASE 4: TESTES BÁSICOS (1 dia)

```python
# tests/test_api.py
def test_login_success():
    response = client.post("/auth/login", json={
        "email": "test@test.com", 
        "password": "123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_criar_projeto_requires_auth():
    response = client.post("/projetos", json={...})
    assert response.status_code == 401
```

```typescript
// frontend/tests/App.test.tsx
test('Landing page renders', () => {
  render(<App />);
  expect(screen.getByText('Topógrafo')).toBeInTheDocument();
});
```

---

## 🎯 FASE 5: FEATURE FLAG (ongoing)

```python
# Novas features sempre atrás de flag
FEATURES = {
    "ai_assistant": os.getenv("FEATURE_AI_ASSISTANT") == "true",
    "infinitepay": os.getenv("FEATURE_PAYMENTS") == "true"
}

@app.route("/ai/chat")
def ai_chat():
    if not FEATURES["ai_assistant"]:
        return {"error": "Feature disabled"}, 403
    ...
```

---

## 📊 RESULTADO ESPERADO

**Antes:**
- 50+ arquivos Python (muitos mortos)
- 15+ arquivos .md (duplicados)
- 3 clientes AI (confuso)
- 0 testes
- IAs perdidas

**Depois:**
- 10 arquivos Python (vivos)
- 1 README.md (claro)
- 1 cliente AI (simples)
- 20 testes (confiança)
- IAs entendem tudo

**Tempo:** 5 dias
**Impacto:** Projeto volta a ter velocidade

---

## 🚀 EXECUÇÃO

**Dia 1:** Deletar arquivos mortos (FASE 1)
**Dia 2-3:** Consolidar AI (FASE 2)
**Dia 4:** README único + deletar .mds (FASE 3)
**Dia 5:** Testes básicos (FASE 4)

**Regra de ouro:** 
- ✅ DELETAR é melhor que comentar
- ✅ 1 jeito certo é melhor que 3 jeitos
- ✅ Código testado > documentação
