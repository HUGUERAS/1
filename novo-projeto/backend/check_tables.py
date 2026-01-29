from database import SessionLocal
from models import Lote, Projeto, SigefIncra
from sqlalchemy import text

def check_db():
    db = SessionLocal()
    try:
        # Check tables existence by querying
        print("Checking tables...")
        
        try:
            lote_count = db.query(Lote).count()
            print(f"Lotes count: {lote_count}")
        except Exception as e:
            print(f"Error querying Lotes: {e}")

        try:
            projeto_count = db.query(Projeto).count()
            print(f"Projetos count: {projeto_count}")
        except Exception as e:
            print(f"Error querying Projetos: {e}")

        try:
            sigef_count = db.query(SigefIncra).count()
            print(f"SigefIncra count: {sigef_count}")
        except Exception as e:
            print(f"Error querying SigefIncra: {e}")
            
    except Exception as e:
        print(f"General DB Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
