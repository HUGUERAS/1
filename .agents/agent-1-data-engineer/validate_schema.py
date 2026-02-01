#!/usr/bin/env python3
"""
Agent 1: Validate existing schema
"""

import psycopg2

print("=" * 60)
print("🚀 AGENT 1: Schema Validation")
print("=" * 60)

try:
    print(f"\n🔗 Connecting to ativo-real-db.postgres.database.azure.com...")
    conn = psycopg2.connect(
        host="ativo-real-db.postgres.database.azure.com",
        user="topografo",
        password="Bem@Real2026!",
        database="postgres",
        port=5432,
        sslmode="require"
    )
    print("✅ Connected!")
    
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    tables = cursor.fetchall()
    
    print(f"\n📊 Tables in database:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"   - {table[0]}: {count} rows")
    
    # Check enums
    cursor.execute("""
        SELECT typname FROM pg_type
        WHERE typtype = 'e'
        ORDER BY typname
    """)
    enums = cursor.fetchall()
    
    print(f"\n📋 Enums created:")
    for enum in enums:
        print(f"   - {enum[0]}")
    
    # Data summary
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"\n👥 Users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM projects")
    print(f"📁 Projects: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM lots")
    print(f"📍 Lots: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM payments")
    print(f"💳 Payments: {cursor.fetchone()[0]}")
    
    print("\n" + "=" * 60)
    print("✅ AGENT 1 SCHEMA VALIDATED")
    print("=" * 60)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import sys
    sys.exit(1)
