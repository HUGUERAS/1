import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Pega a URL original
original_url = os.getenv("DATABASE_URL", "")

if not original_url:
    print("ERRO: DATABASE_URL nao encontrada no .env")
    sys.exit(1)

# Monta uma URL de teste apontando para o banco padrao 'postgres' e forcando SSL
# Formato esperado: postgresql://user:pass@host:port/db
try:
    # Simples replace para mudar o banco alvo para teste
    base_url = original_url.rsplit('/', 1)[0]
    test_url = f"{base_url}/postgres?sslmode=require"
except:
    test_url = original_url

print(f"--- TESTE DE CONEXAO ---")
print(f"Alvo: Banco de dados 'postgres' (sistema)")

try:
    engine = create_engine(test_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.scalar()
        print(f"\n[SUCESSO] Conectado com sucesso!")
        print(f"Versao do Banco: {version}")
        print("\nDiagnostico: Sua senha e usuario estao CORRETOS e o Firewall liberou.")
except Exception as e:
    err = str(e)
    print("\n[FALHA] Nao foi possivel conectar.")
    
    if "password authentication failed" in err:
        print(">>> CAUSA: USUARIO ou SENHA incorretos.")
        print("   1. Verifique se o usuario e realmente 'admin'. (Veja no Portal Azure > Overview > Admin username)")
        print("   2. Verifique se a senha no arquivo .env e EXATAMENTE a que voce definiu.")
    
    elif "no pg_hba.conf entry" in err:
        print(">>> CAUSA: BLOQUEIO DE FIREWALL.")
        print("   O Azure ainda nao liberou seu IP. Pode levar alguns minutos apos salvar.")
        try:
            ip = err.split('host "')[1].split('"')[0]
            print(f"   IP Detectado: {ip}")
        except:
            pass
            
    else:
        print(f"Erro tecnico: {err}")
