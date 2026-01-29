import psycopg2
import os
import sys

# From the logs
# DB_HOST = "psql-bemreal-ai1-4764.postgres.database.azure.com"
# DB_USER = "bemrealadmin"
# DB_PASS = "BemReal4764!Secure"
# DB_NAME = "ativoreal_geo"

# Construction: postgresql://bemrealadmin:BemReal4764!Secure@psql-bemreal-ai1-4764.postgres.database.azure.com/ativoreal_geo?sslmode=require

try:
    print("Conectando ao banco de dados para habilitar PostGIS...")
    conn = psycopg2.connect(
        host="psql-bemreal-ai1-4764.postgres.database.azure.com",
        database="ativoreal_geo",
        user="bemrealadmin",
        password="BemReal4764!Secure",
        sslmode="require"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Criando extensão POSTGIS...")
    cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    print("Extensão criada com sucesso!")
    
    cur.close()
    conn.close()
    print("Configuração concluída.")

except Exception as e:
    print(f"Erro ao conectar ou configurar: {e}")
    sys.exit(1)
