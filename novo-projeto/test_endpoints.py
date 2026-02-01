# 🚀 SCRIPT DE TESTE - BACKEND ENDPOINTS
# Execute este script para testar todos os novos endpoints

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:7071/api"

print("=" * 60)
print("🚀 TESTANDO ENDPOINTS BACKEND")
print("=" * 60)

# Teste 1: WMS Layers
print("\n1️⃣ Testando WMS Layers...")

# Criar camada WMS
print("   → POST /wms-layers (criar)")
try:
    response = requests.post(f"{BASE_URL}/wms-layers", json={
        "projeto_id": 1,
        "name": "SIGEF - Teste",
        "url": "https://sigef.incra.gov.br/wms",
        "visible": True,
        "opacity": 0.7
    })
    if response.status_code == 201:
        layer = response.json()
        layer_id = layer['id']
        print(f"   ✅ Camada criada: ID {layer_id}")
    else:
        print(f"   ❌ Erro: {response.status_code} - {response.text}")
        layer_id = None
except Exception as e:
    print(f"   ❌ Erro de conexão: {e}")
    layer_id = None

# Listar camadas
print("   → GET /wms-layers?projeto_id=1 (listar)")
try:
    response = requests.get(f"{BASE_URL}/wms-layers?projeto_id=1")
    if response.status_code == 200:
        layers = response.json()
        print(f"   ✅ {len(layers)} camada(s) encontrada(s)")
    else:
        print(f"   ❌ Erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Atualizar camada
if layer_id:
    print(f"   → PATCH /wms-layers/{layer_id} (atualizar)")
    try:
        response = requests.patch(f"{BASE_URL}/wms-layers/{layer_id}", json={
            "visible": False,
            "opacity": 0.5
        })
        if response.status_code == 200:
            print(f"   ✅ Camada atualizada")
        else:
            print(f"   ❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

# Teste 2: Chat
print("\n2️⃣ Testando Chat...")

# Enviar mensagem
print("   → POST /chat/messages (enviar)")
try:
    response = requests.post(f"{BASE_URL}/chat/messages", json={
        "projeto_id": 1,
        "sender_id": 1,
        "sender_role": "TOPOGRAFO",
        "message": "Olá! Teste de mensagem do sistema."
    })
    if response.status_code == 201:
        msg = response.json()
        print(f"   ✅ Mensagem enviada: ID {msg['id']}")
    else:
        print(f"   ❌ Erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Listar mensagens
print("   → GET /chat/messages?projeto_id=1 (listar)")
try:
    response = requests.get(f"{BASE_URL}/chat/messages?projeto_id=1&limit=10")
    if response.status_code == 200:
        messages = response.json()
        print(f"   ✅ {len(messages)} mensagem(ns) encontrada(s)")
    else:
        print(f"   ❌ Erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 3: Status History
print("\n3️⃣ Testando Status History...")
print("   → GET /lotes/1/status-history (histórico)")
try:
    response = requests.get(f"{BASE_URL}/lotes/1/status-history")
    if response.status_code == 200:
        history = response.json()
        print(f"   ✅ {len(history)} registro(s) de histórico")
    else:
        print(f"   ❌ Erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# Teste 4: Magic Link
print("\n4️⃣ Testando Magic Link...")
print("   → GET /auth/magic-link/test-token (validar)")
try:
    response = requests.get(f"{BASE_URL}/auth/magic-link/550e8400-e29b-41d4-a716-446655440000")
    if response.status_code in [200, 404, 403]:
        result = response.json()
        if result.get('valid'):
            print(f"   ✅ Link válido!")
        else:
            print(f"   ⚠️ Link inválido/expirado (esperado se não existir)")
    else:
        print(f"   ❌ Erro: {response.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "=" * 60)
print("✅ TESTES CONCLUÍDOS!")
print("=" * 60)
print("\n💡 PRÓXIMOS PASSOS:")
print("   1. Se houver erros de conexão: inicie o backend (func start)")
print("   2. Se houver erros 404: verifique as rotas no function_app.py")
print("   3. Se houver erros 500: verifique os logs do backend")
print("   4. Teste o frontend: cd ativo-real && npm run dev")
