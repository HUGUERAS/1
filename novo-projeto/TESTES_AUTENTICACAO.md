# 🧪 Guia de Testes - Sistema de Autenticação JWT

## 📋 Visão Geral

Este documento fornece instruções completas para testar o sistema de autenticação JWT implementado no Ativo Real.

## 🛠️ Pré-requisitos

1. **Migração SQL aplicada**: Execute `04_users_auth.sql` no PostgreSQL
2. **Backend rodando**: Azure Functions ou local com `func start`
3. **Variável de ambiente**: `JWT_SECRET_KEY` configurada (default: "CHANGE-THIS-SECRET-KEY-IN-PRODUCTION-USE-LONG-RANDOM-STRING")

## 🔧 Setup Inicial

### Aplicar Migração SQL

```powershell
# Conectar no PostgreSQL do Azure
$env:PGPASSWORD = "sua_senha"
psql -h seu-servidor.postgres.database.azure.com -U seu_usuario -d ativo_real -f "novo-projeto/database/init/04_users_auth.sql"
```

### Verificar Seed Data

Após migração, 3 usuários de teste estarão disponíveis:

| Email | Senha | Role | Descrição |
|-------|-------|------|-----------|
| admin@ativoreal.com | Admin123! | ADMIN | Administrador do sistema |
| topografo@ativoreal.com | Topo123! | TOPOGRAFO | Topógrafo profissional |
| cliente@ativoreal.com | Cliente123! | CLIENTE | Cliente padrão |

## 📡 Endpoints de Autenticação

### 1. POST /api/auth/register - Registro de Usuário

**Request:**
```bash
curl -X POST https://seu-app.azurewebsites.net/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Silva",
    "email": "maria@example.com",
    "password": "SenhaSegura123!",
    "role": "CLIENTE",
    "telefone": "(11) 98765-4321",
    "cpf_cnpj": "123.456.789-00"
  }'
```

**Response Success (201):**
```json
{
  "id": 4,
  "name": "Maria Silva",
  "email": "maria@example.com",
  "role": "CLIENTE",
  "avatar": null,
  "telefone": "(11) 98765-4321",
  "cpf_cnpj": "123.456.789-00",
  "is_active": true,
  "email_verified": false,
  "criado_em": "2026-01-31T12:00:00.000Z",
  "ultimo_login": null
}
```

**Response Error (409) - Email já existe:**
```json
{
  "error": "Email já cadastrado"
}
```

---

### 2. POST /api/auth/login - Login

**Request:**
```bash
curl -X POST https://seu-app.azurewebsites.net/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "topografo@ativoreal.com",
    "password": "Topo123!"
  }'
```

**Response Success (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800,
  "user": {
    "id": 2,
    "name": "Topógrafo Teste",
    "email": "topografo@ativoreal.com",
    "role": "TOPOGRAFO",
    "is_active": true,
    "email_verified": true,
    "criado_em": "2026-01-31T10:00:00.000Z",
    "ultimo_login": "2026-01-31T12:15:00.000Z"
  }
}
```

**Response Error (401) - Credenciais inválidas:**
```json
{
  "error": "Credenciais inválidas"
}
```

**Response Error (403) - Conta inativa:**
```json
{
  "error": "Conta inativa. Entre em contato com o suporte."
}
```

---

### 3. GET /api/auth/me - Perfil do Usuário Autenticado

**Request:**
```bash
curl -X GET https://seu-app.azurewebsites.net/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response Success (200):**
```json
{
  "id": 2,
  "name": "Topógrafo Teste",
  "email": "topografo@ativoreal.com",
  "role": "TOPOGRAFO",
  "avatar": null,
  "telefone": "(11) 98765-4321",
  "cpf_cnpj": "123.456.789-00",
  "is_active": true,
  "email_verified": true,
  "criado_em": "2026-01-31T10:00:00.000Z",
  "ultimo_login": "2026-01-31T12:15:00.000Z"
}
```

**Response Error (401) - Token ausente:**
```json
{
  "error": "Token de autenticação ausente"
}
```

**Response Error (401) - Token expirado:**
```json
{
  "error": "Token expirado"
}
```

---

### 4. POST /api/auth/refresh - Refresh Token

**Request:**
```bash
curl -X POST https://seu-app.azurewebsites.net/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Response Success (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

**Response Error (401) - Refresh token inválido:**
```json
{
  "error": "Token inválido - não é refresh token"
}
```

---

## 🔒 Endpoints Protegidos

### 5. POST /api/lotes - Criar Lote (Requer TOPOGRAFO ou ADMIN)

**Request:**
```bash
curl -X POST https://seu-app.azurewebsites.net/api/lotes \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "matricula": "12345",
    "proprietario": "João Silva",
    "coordinates": [
      [-47.9292, -15.7801],
      [-47.9282, -15.7801],
      [-47.9282, -15.7811],
      [-47.9292, -15.7811],
      [-47.9292, -15.7801]
    ]
  }'
```

**Response Success (201):**
```json
{
  "id": 1,
  "matricula": "12345",
  "proprietario": "João Silva",
  "area_ha": 10.5,
  "perimetro_m": 1250.0,
  "warnings": [],
  "criado_em": "2026-01-31T12:30:00.000Z"
}
```

**Response Error (401) - Token ausente:**
```json
{
  "error": "Token de autenticação ausente"
}
```

**Response Error (403) - Role insuficiente:**
```json
{
  "error": "Acesso negado. Roles permitidas: TOPOGRAFO, ADMIN"
}
```

---

### 6. POST /api/assinaturas - Criar Assinatura (Requer autenticação)

**Request:**
```bash
curl -X POST https://seu-app.azurewebsites.net/api/assinaturas \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "plano_id": 2,
    "metodo_pagamento": "PIX"
  }'
```

**Response Success (201):**
```json
{
  "id": 1,
  "usuario_id": 2,
  "plano_id": 2,
  "status": "ATIVA",
  "inicio_em": "2026-01-31T12:30:00.000Z",
  "expira_em": "2026-02-28T12:30:00.000Z",
  "proximo_pagamento": "2026-02-28T12:30:00.000Z",
  "metodo_pagamento": "PIX"
}
```

---

### 7. GET /api/assinaturas/current - Assinatura Atual (Requer autenticação)

**Request:**
```bash
curl -X GET https://seu-app.azurewebsites.net/api/assinaturas/current \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response Success (200):**
```json
{
  "assinatura": {
    "id": 1,
    "usuario_id": 2,
    "plano_id": 2,
    "status": "ATIVA",
    "inicio_em": "2026-01-31T12:30:00.000Z",
    "expira_em": "2026-02-28T12:30:00.000Z",
    "metodo_pagamento": "PIX"
  },
  "plano": {
    "id": 2,
    "nome": "BÁSICO",
    "descricao": "Plano para pequenos produtores",
    "preco_mensal": 49.90,
    "limite_projetos": 3,
    "limite_lotes": 10
  }
}
```

**Response Error (404) - Sem assinatura ativa:**
```json
{
  "error": "Nenhuma assinatura ativa encontrada"
}
```

---

## 🧪 Scripts de Teste Automatizados

### PowerShell - Teste Completo do Fluxo

```powershell
# Configurar base URL
$BASE_URL = "https://seu-app.azurewebsites.net/api"

# 1. Register novo usuário
Write-Host "🔵 Testando registro..." -ForegroundColor Cyan
$registerBody = @{
    name = "Teste Automatizado"
    email = "teste.auto@example.com"
    password = "Teste123!"
    role = "CLIENTE"
} | ConvertTo-Json

$registerResponse = Invoke-RestMethod -Uri "$BASE_URL/auth/register" `
    -Method POST `
    -Body $registerBody `
    -ContentType "application/json"

Write-Host "✅ Usuário criado: $($registerResponse.email)" -ForegroundColor Green

# 2. Login com novo usuário
Write-Host "`n🔵 Testando login..." -ForegroundColor Cyan
$loginBody = @{
    email = "teste.auto@example.com"
    password = "Teste123!"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Uri "$BASE_URL/auth/login" `
    -Method POST `
    -Body $loginBody `
    -ContentType "application/json"

$accessToken = $loginResponse.access_token
$refreshToken = $loginResponse.refresh_token

Write-Host "✅ Login bem-sucedido. Token obtido." -ForegroundColor Green
Write-Host "   Access Token: $($accessToken.Substring(0, 20))..." -ForegroundColor Gray
Write-Host "   User ID: $($loginResponse.user.id)" -ForegroundColor Gray

# 3. Buscar perfil com token
Write-Host "`n🔵 Testando GET /auth/me..." -ForegroundColor Cyan
$headers = @{
    "Authorization" = "Bearer $accessToken"
}

$meResponse = Invoke-RestMethod -Uri "$BASE_URL/auth/me" `
    -Method GET `
    -Headers $headers

Write-Host "✅ Perfil obtido: $($meResponse.name) ($($meResponse.role))" -ForegroundColor Green

# 4. Testar refresh token
Write-Host "`n🔵 Testando refresh token..." -ForegroundColor Cyan
Start-Sleep -Seconds 2  # Aguardar 2 segundos

$refreshBody = @{
    refresh_token = $refreshToken
} | ConvertTo-Json

$newTokenResponse = Invoke-RestMethod -Uri "$BASE_URL/auth/refresh" `
    -Method POST `
    -Body $refreshBody `
    -ContentType "application/json"

Write-Host "✅ Token refreshed com sucesso" -ForegroundColor Green
Write-Host "   Novo Access Token: $($newTokenResponse.access_token.Substring(0, 20))..." -ForegroundColor Gray

# 5. Tentar acessar endpoint protegido com role insuficiente
Write-Host "`n🔵 Testando acesso negado (CLIENTE tentando criar lote)..." -ForegroundColor Cyan
$loteBody = @{
    matricula = "TEST-123"
    proprietario = "Teste"
    coordinates = @(
        @(-47.9292, -15.7801),
        @(-47.9282, -15.7801),
        @(-47.9282, -15.7811),
        @(-47.9292, -15.7801)
    )
} | ConvertTo-Json

try {
    $loteResponse = Invoke-RestMethod -Uri "$BASE_URL/lotes" `
        -Method POST `
        -Body $loteBody `
        -Headers $headers `
        -ContentType "application/json"
    
    Write-Host "❌ ERRO: Cliente conseguiu criar lote (não deveria!)" -ForegroundColor Red
} catch {
    $errorResponse = $_.ErrorDetails.Message | ConvertFrom-Json
    if ($errorResponse.error -like "*Acesso negado*") {
        Write-Host "✅ Acesso negado corretamente (403)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Erro inesperado: $($errorResponse.error)" -ForegroundColor Yellow
    }
}

Write-Host "`n🎉 Todos os testes completados!" -ForegroundColor Green
```

---

## 🔍 Verificação de Logs

### Logs de Sucesso

```
🔐 Login request recebido
✅ Login bem-sucedido: topografo@ativoreal.com (TOPOGRAFO)
👤 Get current user - user_id: 2
🔄 Token refresh request recebido
✅ Token refreshed para user_id: 2
```

### Logs de Erro

```
❌ Login falhou - email não encontrado: usuario@inexistente.com
❌ Login falhou - senha incorreta para: topografo@ativoreal.com
❌ Login falhou - usuário inativo: usuario@desativado.com
❌ Refresh token inválido: Token expirado
```

---

## 🛡️ Matriz de RBAC

| Endpoint | ADMIN | TOPOGRAFO | CLIENTE | AGRICULTOR | Anônimo |
|----------|-------|-----------|---------|------------|---------|
| POST /auth/register | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /auth/login | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /auth/refresh | ✅ | ✅ | ✅ | ✅ | ✅ |
| GET /auth/me | ✅ | ✅ | ✅ | ✅ | ❌ |
| POST /lotes | ✅ | ✅ | ❌ | ❌ | ❌ |
| GET /lotes | ✅ | ✅ | ✅ | ✅ | ❌ |
| POST /projetos | ✅ | ✅ | ❌ | ❌ | ❌ |
| GET /projetos | ✅ | ✅ | ✅ | ✅ | ❌ |
| GET /planos | ✅ | ✅ | ✅ | ✅ | ✅ |
| POST /assinaturas | ✅ | ✅ | ✅ | ✅ | ❌ |
| GET /assinaturas/current | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## 📊 Casos de Teste

### ✅ Cenários de Sucesso

1. **Registro de novo usuário**
   - Input válido → 201 Created
   - Usuário criado no banco com senha hash bcrypt
   - `is_active = true`, `email_verified = false`

2. **Login com credenciais válidas**
   - Email/senha corretos → 200 OK
   - Retorna access_token (30min) e refresh_token (7 dias)
   - Atualiza `ultimo_login` no banco

3. **Acesso a perfil com token válido**
   - Token válido no header → 200 OK
   - Retorna dados do usuário autenticado

4. **Refresh token**
   - Refresh token válido → 200 OK
   - Retorna novo access_token

5. **Acesso a endpoint protegido com role adequada**
   - TOPOGRAFO criando lote → 201 Created
   - ADMIN criando projeto → 201 Created

### ❌ Cenários de Erro

1. **Registro com email duplicado**
   - Email já existe → 409 Conflict
   - Mensagem: "Email já cadastrado"

2. **Login com senha incorreta**
   - Email válido, senha errada → 401 Unauthorized
   - Mensagem: "Credenciais inválidas"

3. **Login de usuário inativo**
   - `is_active = false` → 403 Forbidden
   - Mensagem: "Conta inativa. Entre em contato com o suporte."

4. **Acesso sem token**
   - Header Authorization ausente → 401 Unauthorized
   - Mensagem: "Token de autenticação ausente"

5. **Acesso com token expirado**
   - Token com `exp` passado → 401 Unauthorized
   - Mensagem: "Token expirado"

6. **Acesso com role insuficiente**
   - CLIENTE tentando criar lote → 403 Forbidden
   - Mensagem: "Acesso negado. Roles permitidas: TOPOGRAFO, ADMIN"

7. **Refresh com access token**
   - Token tipo "access" em /refresh → 401 Unauthorized
   - Mensagem: "Token inválido - não é refresh token"

---

## 🔧 Troubleshooting

### Problema: "Token de autenticação ausente"
**Causa:** Header `Authorization` não enviado ou mal formatado  
**Solução:** Enviar header `Authorization: Bearer <token>`

### Problema: "Token expirado"
**Causa:** Access token com mais de 30 minutos  
**Solução:** Usar endpoint `/auth/refresh` com refresh_token

### Problema: "Credenciais inválidas" mesmo com senha correta
**Causa:** Email com case diferente ou espaços extras  
**Solução:** Verificar email exato no banco (case-sensitive)

### Problema: "Acesso negado" mesmo sendo TOPOGRAFO
**Causa:** Token desatualizado após mudança de role  
**Solução:** Fazer logout e login novamente para obter novo token

### Problema: Erro 500 em qualquer endpoint de auth
**Causa:** Migração SQL não aplicada ou tabela `users` ausente  
**Solução:** Aplicar `04_users_auth.sql` no PostgreSQL

---

## 🚀 Próximos Passos

1. **Testar localmente com Azure Functions Core Tools**
   ```powershell
   cd novo-projeto/backend
   func start
   ```

2. **Aplicar migração SQL no Azure**
   ```powershell
   psql -h <servidor>.postgres.database.azure.com -U <usuario> -d ativo_real -f "database/init/04_users_auth.sql"
   ```

3. **Configurar JWT_SECRET_KEY no Azure**
   ```powershell
   az functionapp config appsettings set `
     --name <nome-function-app> `
     --resource-group <resource-group> `
     --settings JWT_SECRET_KEY="<seu-secret-key-seguro>"
   ```

4. **Executar suite de testes automatizados**
   ```powershell
   .\TESTES_AUTENTICACAO.ps1
   ```

---

## 📝 Checklist de Validação

- [ ] Migração SQL aplicada com sucesso
- [ ] 3 usuários seed criados (admin, topografo, cliente)
- [ ] Registro de novo usuário funciona (201)
- [ ] Login com credenciais válidas retorna tokens (200)
- [ ] GET /auth/me retorna perfil com token válido (200)
- [ ] Refresh token gera novo access_token (200)
- [ ] Endpoint protegido bloqueia acesso sem token (401)
- [ ] Endpoint protegido bloqueia role insuficiente (403)
- [ ] Endpoint protegido permite acesso com role adequada (200/201)
- [ ] Logs de auditoria registram login/logout
- [ ] JWT_SECRET_KEY configurado em produção

---

**Última atualização:** 31/01/2026  
**Versão:** 1.0  
**Autor:** GitHub Copilot - Sistema de Autenticação JWT
