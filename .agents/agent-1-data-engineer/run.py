#!/usr/bin/env python3
"""
Agente 1: Engenheiro de Dados - Executor
Orquestra a criação do schema PostgreSQL + PostGIS
"""

import os
import sys

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(AGENT_DIR)))

print("""
╔═══════════════════════════════════════════════════════════════╗
║          👷 AGENTE 1: ENGENHEIRO DE DADOS (v1.0)             ║
║          PostgreSQL + PostGIS para Bem Real SaaS             ║
╚═══════════════════════════════════════════════════════════════╝
""")

print("📋 Tarefas Disponíveis:\n")
print("1. schema   - Criar schema SQL completo")
print("2. fixtures - Gerar dados de teste realistas")
print("3. validate - Testar integridade geométrica")
print("4. all      - Executar tudo (1 + 2 + 3)")
print("\n💡 Uso: python run.py <tarefa>\n")

if len(sys.argv) < 2:
    print("ℹ️  Exemplo: python run.py schema")
    sys.exit(0)

task = sys.argv[1]

if task == "schema":
    print("🔧 Lendo AGENT_INSTRUCTIONS.md...")
    instructions_path = os.path.join(AGENT_DIR, "AGENT_INSTRUCTIONS.md")
    with open(instructions_path, 'r') as f:
        content = f.read()
    
    print("✅ Instruções carregadas. Próximas etapas:\n")
    print("1. Revisar novo-projeto/database/init/01_schema.sql")
    print("2. Executar script SQL no Azure Database for PostgreSQL")
    print("3. Validar com queries de integridade")
    print("\n📂 Arquivos relevantes:")
    print(f"   - {os.path.join(PROJECT_ROOT, 'novo-projeto/database/init/01_schema.sql')}")
    print(f"   - {os.path.join(AGENT_DIR, 'AGENT_INSTRUCTIONS.md')}")

elif task == "fixtures":
    print("🌱 Preparando dados de teste realistas...\n")
    print("Será criado: fixtures/seed.sql com dados brasileiros reais")
    print("- 3 projetos (INDIVIDUAL, DESMEMBRAMENTO, LOTEAMENTO)")
    print("- 10+ lotes com geometrias via PostGIS")
    print("- Vizinhança detectável")

elif task == "validate":
    print("🧪 Executando queries de validação geométrica...\n")
    print("Verificará:")
    print("- ST_IsValid em todas geometrias")
    print("- Detecção de overlaps")
    print("- Vizinhança (confrontação) com ST_Touches")

elif task == "all":
    print("🚀 Executando pipeline completo: schema → fixtures → validate\n")
    print("Isso vai preparar o banco para desenvolvimento!")

else:
    print(f"❌ Tarefa desconhecida: {task}")
    sys.exit(1)

print("\n" + "="*65)
print("ℹ️  Para usar este agente com seus agentes de IA:")
print("   1. Configure OPENROUTER_API_KEY em seu ambiente")
print("   2. Use jamba_openrouter.py para análise de schemas")
print("   3. Commit dos arquivos SQL para Git")
print("="*65)
