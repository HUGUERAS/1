#!/usr/bin/env python3
"""
Agent 1: Database Engineer - Execute Schema
Executes 01_schema.sql on PostgreSQL and validates
"""

import psycopg2
from psycopg2 import sql
import os
import sys

# Connection parameters
DB_HOST = "ativo-real-db.postgres.database.azure.com"
DB_USER = "topografo"
DB_PASSWORD = "Bem@Real2026!"
DB_NAME = "postgres"
DB_PORT = 5432

print("=" * 60)
print("🚀 AGENT 1: Database Engineer")
print("=" * 60)

try:
    print(f"\n🔗 Connecting to {DB_HOST}...")
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        sslmode="require"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("✅ Connected!")
    
    # Read schema file
    schema_file = r"c:\Users\User\cooking-agent\ai1\.agents\agent-1-data-engineer\01_schema_clean.sql"
    print(f"\n📖 Reading schema from: {schema_file}")
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Execute schema
    print("\n⚙️  Executing schema SQL...")
    cursor.execute(schema_sql)
    print("✅ Schema executed!")
    
    # Validate
    print("\n🔍 Validating...")
    
    # Check tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    print(f"\n📊 Tables created: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Check extensions
    cursor.execute("SELECT extname FROM pg_extension ORDER BY extname")
    extensions = cursor.fetchall()
    print(f"\n🔌 Extensions active: {len(extensions)}")
    for ext in extensions:
        print(f"   - {ext[0]}")
    
    # Check data
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM projects")
    project_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM lots")
    lots_count = cursor.fetchone()[0]
    
    print(f"\n📈 Test data inserted:")
    print(f"   - Users: {user_count}")
    print(f"   - Projects: {project_count}")
    print(f"   - Lots: {lots_count}")
    
    # Run verification queries
    print(f"\n✅ Running verification queries...")
    cursor.execute("""
        SELECT COUNT(*) FROM lots WHERE geom_geojson IS NOT NULL
    """)
    valid_geoms = cursor.fetchone()[0]
    print(f"   - Lots with geometry: {valid_geoms} ✅")
    
    cursor.execute("""
        SELECT COUNT(*) FROM wms_layers
    """)
    wms_count = cursor.fetchone()[0]
    print(f"   - WMS Layers configured: {wms_count} ✅")
    
    print("\n" + "=" * 60)
    print("✅ AGENT 1 SCHEMA COMPLETE")
    print("=" * 60)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    sys.exit(1)
