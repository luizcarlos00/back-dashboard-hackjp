"""
Script para inicializar o banco de dados do zero
Cria todas as tabelas conforme definido em db_models.py
"""
from app.database import engine, Base
from app.db_models import User, Content, Video, Question, Answer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """
    Cria todas as tabelas no banco de dados
    """
    try:
        logger.info("Iniciando criação das tabelas...")
        
        # Isso cria todas as tabelas definidas nos models
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Tabelas criadas com sucesso!")
        logger.info("Tabelas criadas:")
        logger.info("  - users")
        logger.info("  - contents")
        logger.info("  - videos")
        logger.info("  - questions")
        logger.info("  - answers")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        raise


def drop_all_tables():
    """
    Remove todas as tabelas do banco de dados
    ⚠️ CUIDADO: Esta operação é irreversível!
    """
    try:
        logger.warning("⚠️  ATENÇÃO: Removendo todas as tabelas do banco de dados...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Todas as tabelas foram removidas")
    except Exception as e:
        logger.error(f"❌ Erro ao remover tabelas: {e}")
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        # Confirmação antes de dropar as tabelas
        confirmation = input("⚠️  Tem certeza que deseja REMOVER TODAS as tabelas? (sim/não): ")
        if confirmation.lower() == "sim":
            drop_all_tables()
            logger.info("Recriando as tabelas...")
            init_database()
        else:
            logger.info("Operação cancelada")
    else:
        init_database()


