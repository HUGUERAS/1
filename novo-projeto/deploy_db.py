import os
import sys
import psycopg2
from urllib.parse import urlparse

def run_sql_file(cursor, file_path):
    print(f"Executando {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql = f.read()
            cursor.execute(sql)
            print(f"✓ {file_path} executado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao executar {file_path}: {e}")
        raise e

def main():
    if len(sys.argv) < 5:
        print("Uso: python deploy_db.py <server_name> <user> <password> <database>")
        sys.exit(1)

    server_name = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    database = sys.argv[4]

    # Construir string de conexão
    # Azure Flexible Server requer user=username (nao user@server)
    # Host = servername.postgres.database.azure.com
    
    host = f"{server_name}.postgres.database.azure.com"
    
    print(f"Conectando ao banco de dados: {host} / {database}...")
    
    conn_str = f"host={host} dbname={database} user={user} password={password} sslmode=require"

    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Lista de arquivos em ordem
        files = [
            'database/init/01_schema.sql',
            'database/init/02_advanced_schema.sql',
            'database/init/03_pay_as_you_go_schema.sql',
            'database/init/04_users_auth.sql',
            'database/init/05_features_completas.sql'
        ]
        
        for f in files:
            if os.path.exists(f):
                run_sql_file(cursor, f)
            else:
                print(f"⚠️ Arquivo não encontrado: {f}")
        
        print("\n✅ Setup do banco de dados concluído com sucesso!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erro de conexão: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
