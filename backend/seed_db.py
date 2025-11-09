"""
Script para popular o banco de dados com dados de exemplo
"""
from app.database import SessionLocal
from app.db_models import User, Content, Video, Question, Answer
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database():
    """
    Popula o banco com dados de exemplo
    """
    db = SessionLocal()
    
    try:
        logger.info("🌱 Iniciando seed do banco de dados...")
        
        # 1. Criar usuários de exemplo
        logger.info("Criando usuários...")
        user1 = User(
            device_id="device_001",
            nome="João Silva",
            email="joao@example.com",
            idade=25,
            nivel_educacional="Ensino Médio"
        )
        user2 = User(
            device_id="device_002",
            nome="Maria Santos",
            email="maria@example.com",
            idade=22,
            nivel_educacional="Superior"
        )
        db.add_all([user1, user2])
        db.commit()
        logger.info(f"✅ Usuários criados: {user1.nome}, {user2.nome}")
        
        # 2. Criar conteúdos/matérias
        logger.info("Criando conteúdos...")
        content_matematica = Content(
            title="Matemática Básica",
            description="Fundamentos de matemática para iniciantes",
            category="Matemática",
            difficulty_level=1,
            keywords=["soma", "subtração", "multiplicação", "divisão"],
            is_active=True,
            order_index=1
        )
        
        content_portugues = Content(
            title="Português - Gramática",
            description="Conceitos básicos de gramática portuguesa",
            category="Português",
            difficulty_level=1,
            keywords=["sujeito", "predicado", "verbos", "substantivos"],
            is_active=True,
            order_index=2
        )
        
        content_historia = Content(
            title="História do Brasil",
            description="Principais eventos da história brasileira",
            category="História",
            difficulty_level=2,
            keywords=["brasil", "independência", "república"],
            is_active=True,
            order_index=3
        )
        
        db.add_all([content_matematica, content_portugues, content_historia])
        db.commit()
        logger.info(f"✅ Conteúdos criados: {content_matematica.title}, {content_portugues.title}, {content_historia.title}")
        
        # 3. Criar vídeos relacionados aos conteúdos
        logger.info("Criando vídeos...")
        video1 = Video(
            content_id=content_matematica.id,
            title="Adição e Subtração",
            description="Aprenda operações básicas de adição e subtração",
            url="https://www.youtube.com/watch?v=exemplo1",
            thumbnail_url="https://img.youtube.com/vi/exemplo1/maxresdefault.jpg",
            duration_seconds=180,
            expected_concepts=["soma", "subtração", "números naturais"],
            is_active=True,
            order_index=1
        )
        
        video2 = Video(
            content_id=content_matematica.id,
            title="Multiplicação Simples",
            description="Entenda como fazer multiplicações básicas",
            url="https://www.youtube.com/watch?v=exemplo2",
            thumbnail_url="https://img.youtube.com/vi/exemplo2/maxresdefault.jpg",
            duration_seconds=240,
            expected_concepts=["multiplicação", "tabuada"],
            is_active=True,
            order_index=2
        )
        
        video3 = Video(
            content_id=content_portugues.id,
            title="Sujeito e Predicado",
            description="Identifique sujeito e predicado em frases",
            url="https://www.youtube.com/watch?v=exemplo3",
            thumbnail_url="https://img.youtube.com/vi/exemplo3/maxresdefault.jpg",
            duration_seconds=200,
            expected_concepts=["sujeito", "predicado", "oração"],
            is_active=True,
            order_index=1
        )
        
        video4 = Video(
            content_id=content_historia.id,
            title="Descobrimento do Brasil",
            description="Como o Brasil foi descoberto",
            url="https://www.youtube.com/watch?v=exemplo4",
            thumbnail_url="https://img.youtube.com/vi/exemplo4/maxresdefault.jpg",
            duration_seconds=300,
            expected_concepts=["descobrimento", "Pedro Álvares Cabral"],
            is_active=True,
            order_index=1
        )
        
        db.add_all([video1, video2, video3, video4])
        db.commit()
        logger.info(f"✅ {4} vídeos criados")
        
        # 4. Criar questões relacionadas aos conteúdos
        logger.info("Criando questões...")
        
        # Questão de múltipla escolha - Matemática
        question1 = Question(
            content_id=content_matematica.id,
            question_text="Quanto é 2 + 2?",
            question_type="multiple_choice",
            options=["3", "4", "5", "6"],
            correct_option_index=1,
            difficulty_level=1,
            points=10,
            explanation="A soma de 2 + 2 é igual a 4",
            is_active=True,
            order_index=1
        )
        
        # Questão aberta - Matemática
        question2 = Question(
            content_id=content_matematica.id,
            question_text="Explique o que é multiplicação e dê um exemplo.",
            question_type="open_ended",
            expected_keywords=["multiplicação", "vezes", "resultado"],
            expected_concepts=["operação matemática", "repetição"],
            difficulty_level=2,
            points=20,
            explanation="Multiplicação é uma operação que representa adição repetida",
            is_active=True,
            order_index=2
        )
        
        # Questão verdadeiro/falso - Português
        question3 = Question(
            content_id=content_portugues.id,
            question_text="O sujeito é sempre o primeiro elemento da frase?",
            question_type="true_false",
            options=["Verdadeiro", "Falso"],
            correct_option_index=1,
            difficulty_level=2,
            points=10,
            explanation="O sujeito pode aparecer em diferentes posições na frase",
            is_active=True,
            order_index=1
        )
        
        # Questão de múltipla escolha - História
        question4 = Question(
            content_id=content_historia.id,
            question_text="Em que ano o Brasil foi descoberto?",
            question_type="multiple_choice",
            options=["1492", "1500", "1822", "1889"],
            correct_option_index=1,
            difficulty_level=1,
            points=10,
            explanation="O Brasil foi descoberto por Pedro Álvares Cabral em 1500",
            is_active=True,
            order_index=1
        )
        
        # Questão dissertativa - História
        question5 = Question(
            content_id=content_historia.id,
            question_text="Descreva os principais eventos que levaram à independência do Brasil.",
            question_type="essay",
            expected_keywords=["Dom Pedro I", "independência", "Portugal", "1822"],
            expected_concepts=["processo histórico", "autonomia"],
            difficulty_level=3,
            points=30,
            explanation="A independência foi um processo gradual culminando no grito do Ipiranga em 1822",
            is_active=True,
            order_index=2
        )
        
        db.add_all([question1, question2, question3, question4, question5])
        db.commit()
        logger.info(f"✅ {5} questões criadas")
        
        # 5. Criar algumas respostas de exemplo
        logger.info("Criando respostas de exemplo...")
        
        answer1 = Answer(
            user_id=user1.id,
            question_id=question1.id,
            response_type="option",
            selected_option_index=1,
            is_correct=True,
            points_earned=10,
            feedback="Parabéns! Resposta correta."
        )
        
        answer2 = Answer(
            user_id=user1.id,
            question_id=question2.id,
            response_type="text",
            text_response="Multiplicação é quando você soma um número várias vezes. Por exemplo, 3 x 4 = 12, que é o mesmo que 3+3+3+3.",
            concepts_identified=["multiplicação", "soma repetida", "exemplo numérico"],
            quality_score=0.9,
            is_correct=True,
            points_earned=20,
            feedback="Excelente explicação! Você demonstrou compreensão clara do conceito."
        )
        
        answer3 = Answer(
            user_id=user2.id,
            question_id=question3.id,
            response_type="option",
            selected_option_index=1,
            is_correct=True,
            points_earned=10,
            feedback="Correto! O sujeito pode aparecer em diferentes posições."
        )
        
        db.add_all([answer1, answer2, answer3])
        db.commit()
        logger.info(f"✅ {3} respostas criadas")
        
        logger.info("🎉 Seed concluído com sucesso!")
        logger.info(f"   - {2} usuários")
        logger.info(f"   - {3} conteúdos")
        logger.info(f"   - {4} vídeos")
        logger.info(f"   - {5} questões")
        logger.info(f"   - {3} respostas")
        
    except Exception as e:
        logger.error(f"❌ Erro durante seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()


