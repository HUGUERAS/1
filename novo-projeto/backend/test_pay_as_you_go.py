"""
Testes básicos para validar o modelo Pay As You Go
"""
from datetime import datetime, timedelta

# Mock para testar schemas sem banco de dados
def test_schemas_import():
    """Testa se os schemas podem ser importados corretamente"""
    try:
        import sys
        sys.path.insert(0, '/home/runner/work/1/1/novo-projeto/backend')
        
        from schemas import (
            StatusAssinatura,
            PlanoBase,
            PlanoResponse,
            AssinaturaCreate,
            AssinaturaResponse,
            AssinaturaComPlano,
            AssinaturaAtualResponse,
            AlterarPlanoRequest,
            HistoricoAssinaturaResponse
        )
        
        print("✅ Todos os schemas foram importados com sucesso!")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar schemas: {e}")
        return False


def test_status_assinatura_enum():
    """Testa se o enum StatusAssinatura tem todos os valores"""
    import sys
    sys.path.insert(0, '/home/runner/work/1/1/novo-projeto/backend')
    
    from schemas import StatusAssinatura
    
    expected_values = ["TRIAL", "PENDENTE", "ATIVA", "CANCELADA", "SUSPENSA", "EXPIRADA"]
    actual_values = [status.value for status in StatusAssinatura]
    
    assert set(actual_values) == set(expected_values), "StatusAssinatura deve ter todos os valores esperados"
    print("✅ Enum StatusAssinatura validado!")


def test_plano_schema():
    """Testa criação de schema PlanoBase"""
    import sys
    sys.path.insert(0, '/home/runner/work/1/1/novo-projeto/backend')
    
    from schemas import PlanoBase
    
    plano_data = {
        "nome": "TESTE",
        "descricao": "Plano de teste",
        "preco_mensal": 99.99,
        "max_projetos": 10,
        "max_lotes_por_projeto": 50,
        "storage_mb": 1024
    }
    
    plano = PlanoBase(**plano_data)
    
    assert plano.nome == "TESTE"
    assert plano.preco_mensal == 99.99
    assert plano.max_projetos == 10
    print("✅ PlanoBase validado!")


def test_assinatura_create_schema():
    """Testa criação de schema AssinaturaCreate"""
    import sys
    sys.path.insert(0, '/home/runner/work/1/1/novo-projeto/backend')
    
    from schemas import AssinaturaCreate
    
    assinatura_data = {
        "plano_id": 2,
        "usuario_id": 123,
        "metodo_pagamento": "PIX"
    }
    
    assinatura = AssinaturaCreate(**assinatura_data)
    
    assert assinatura.plano_id == 2
    assert assinatura.usuario_id == 123
    assert assinatura.metodo_pagamento == "PIX"
    print("✅ AssinaturaCreate validado!")


def test_models_import():
    """Testa se os models podem ser importados"""
    try:
        import sys
        sys.path.insert(0, '/home/runner/work/1/1/novo-projeto/backend')
        
        from models import (
            StatusAssinaturaEnum,
            PlanoPagamento,
            Assinatura,
            HistoricoAssinatura
        )
        
        print("✅ Todos os models foram importados com sucesso!")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar models: {e}")
        return False


def test_logic_services_import():
    """Testa se as funções de logic_services podem ser importadas"""
    try:
        import sys
        sys.path.insert(0, '/home/runner/work/1/1/novo-projeto/backend')
        
        from logic_services import (
            listar_planos_ativos,
            obter_plano_por_id,
            criar_assinatura_logic,
            obter_assinatura_atual,
            cancelar_assinatura_logic,
            alterar_plano_logic,
            renovar_assinatura_logic,
            verificar_limite_plano,
            registrar_evento_historico
        )
        
        print("✅ Todas as funções de logic_services foram importadas com sucesso!")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar logic_services: {e}")
        return False


def test_sql_migration_syntax():
    """Valida a sintaxe básica do arquivo SQL de migration"""
    sql_file_path = '/home/runner/work/1/1/novo-projeto/database/init/03_pay_as_you_go_schema.sql'
    
    try:
        with open(sql_file_path, 'r') as f:
            content = f.read()
        
        # Verificar se contém as tabelas esperadas
        assert 'CREATE TABLE IF NOT EXISTS planos_pagamento' in content
        assert 'CREATE TABLE IF NOT EXISTS assinaturas' in content
        assert 'CREATE TABLE IF NOT EXISTS historico_assinaturas' in content
        
        # Verificar se contém os ENUMs
        assert 'CREATE TYPE status_assinatura AS ENUM' in content
        
        # Verificar se contém funções
        assert 'CREATE OR REPLACE FUNCTION assinatura_esta_ativa' in content
        assert 'CREATE OR REPLACE FUNCTION obter_limites_plano' in content
        assert 'CREATE OR REPLACE FUNCTION registrar_evento_assinatura' in content
        
        # Verificar se contém views
        assert 'CREATE OR REPLACE VIEW v_assinaturas_ativas' in content
        assert 'CREATE OR REPLACE VIEW v_metricas_assinaturas' in content
        
        # Verificar se contém dados iniciais (seed)
        assert "INSERT INTO planos_pagamento" in content
        assert "'FREE'" in content
        assert "'BASICO'" in content
        assert "'PROFISSIONAL'" in content
        assert "'ENTERPRISE'" in content
        
        print("✅ Migration SQL validada com sucesso!")
        print(f"   - Arquivo: {sql_file_path}")
        print(f"   - Tamanho: {len(content)} bytes")
        return True
        
    except FileNotFoundError:
        print(f"❌ Arquivo SQL não encontrado: {sql_file_path}")
        return False
    except AssertionError as e:
        print(f"❌ Validação SQL falhou: {e}")
        return False


def test_documentation_exists():
    """Verifica se os arquivos de documentação foram criados"""
    import os
    
    base_path = '/home/runner/work/1/1/novo-projeto'
    docs = [
        'MODELO_PAY_AS_YOU_GO.md',
        'GUIA_PRATICO_PAY_AS_YOU_GO.md'
    ]
    
    all_exist = True
    for doc in docs:
        doc_path = os.path.join(base_path, doc)
        if os.path.exists(doc_path):
            size = os.path.getsize(doc_path)
            print(f"✅ {doc} encontrado ({size} bytes)")
        else:
            print(f"❌ {doc} NÃO encontrado")
            all_exist = False
    
    return all_exist


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 TESTES DE VALIDAÇÃO - MODELO PAY AS YOU GO")
    print("="*60 + "\n")
    
    tests = [
        ("Importação de Schemas", test_schemas_import),
        ("Enum StatusAssinatura", test_status_assinatura_enum),
        ("Schema PlanoBase", test_plano_schema),
        ("Schema AssinaturaCreate", test_assinatura_create_schema),
        ("Importação de Models", test_models_import),
        ("Importação de Logic Services", test_logic_services_import),
        ("Sintaxe SQL Migration", test_sql_migration_syntax),
        ("Documentação", test_documentation_exists)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Teste: {test_name}")
        print("-" * 60)
        try:
            result = test_func()
            if result or result is None:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ FALHOU: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 RESUMO: {passed} passaram, {failed} falharam")
    print("="*60 + "\n")
    
    if failed == 0:
        print("🎉 TODOS OS TESTES PASSARAM! Implementação validada com sucesso!")
    else:
        print("⚠️ Alguns testes falharam. Revise os erros acima.")
