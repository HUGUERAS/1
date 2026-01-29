from database import engine
from models import Base
import logging

# Configurar logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

print("Criando tabelas no banco de dados remoto...")
try:
    Base.metadata.create_all(bind=engine)
    print("Sucesso! Tabelas criadas.")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")
