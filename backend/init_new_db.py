"""
Script para inicializar o novo banco de dados com a estrutura simplificada
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app.database import Base, engine
from app import db_models  # Import models to register them

def init_db():
    """
    Cria todas as tabelas no banco de dados
    """
    print("🗄️  Criando banco de dados com estrutura simplificada...")
    
    # Drop all existing tables
    print("🧹 Removendo tabelas antigas...")
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    print("✨ Criando novas tabelas...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Banco de dados criado com sucesso!")
    print("\nTabelas criadas:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")

if __name__ == "__main__":
    init_db()

