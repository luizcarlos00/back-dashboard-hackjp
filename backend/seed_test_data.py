"""
Script para popular o banco com dados de teste para o dashboard
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.db_models import User, Content, Video, Activity, UserVideoProgress, UserActivityResponse
import uuid
from datetime import datetime, timedelta
import random

def seed_test_data():
    """
    Popula o banco com dados de teste
    """
    db = SessionLocal()
    
    try:
        print("🌱 Populando banco com dados de teste...")
        
        # Limpar dados existentes (opcional)
        print("🧹 Limpando dados antigos...")
        db.query(UserActivityResponse).delete()
        db.query(UserVideoProgress).delete()
        db.query(Activity).delete()
        db.query(Video).delete()
        db.query(Content).delete()
        db.query(User).delete()
        db.commit()
        
        # 1. Criar usuários
        print("👥 Criando usuários...")
        users = []
        names = [
            ('Ana Silva', 12, 'fundamental'),
            ('Bruno Costa', 16, 'medio'),
            ('Carla Santos', 20, 'superior'),
            ('Diego Rocha', 14, 'fundamental'),
            ('Elisa Pereira', 17, 'medio'),
            ('Felipe Lima', 22, 'superior'),
            ('Gabriela Alves', 13, 'fundamental'),
            ('Hugo Fernandes', 18, 'superior'),
            ('Iara Moreira', 15, 'medio'),
            ('João Mendes', 21, 'superior'),
        ]
        
        for name, idade, nivel in names:
            user = User(
                id=str(uuid.uuid4()),
                device_id=f"device-{uuid.uuid4().hex[:8]}",
                nome=name,
                idade=idade,
                nivel_educacional=nivel,
                interesses=["matematica", "ciencias", "programacao"],
                created_at=datetime.now() - timedelta(days=random.randint(30, 90))
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        print(f"✅ {len(users)} usuários criados")
        
        # 2. Criar conteúdos
        print("📚 Criando conteúdos...")
        contents_data = [
            {
                'title': 'Matemática Básica - Frações',
                'description': 'Aprenda frações de forma divertida',
                'publico_alvo': 'fundamental',
                'category': 'matematica'
            },
            {
                'title': 'Introdução à Programação',
                'description': 'Primeiros passos em Python',
                'publico_alvo': 'medio',
                'category': 'programacao'
            },
            {
                'title': 'Álgebra Linear',
                'description': 'Matrizes e vetores',
                'publico_alvo': 'superior',
                'category': 'matematica'
            },
            {
                'title': 'Ciências - O Sistema Solar',
                'description': 'Explorando os planetas',
                'publico_alvo': 'fundamental',
                'category': 'ciencias'
            },
            {
                'title': 'Física - Mecânica',
                'description': 'Leis de Newton',
                'publico_alvo': 'medio',
                'category': 'fisica'
            }
        ]
        
        contents = []
        for content_data in contents_data:
            content = Content(
                id=str(uuid.uuid4()),
                **content_data,
                is_active=True,
                created_at=datetime.now() - timedelta(days=random.randint(60, 180))
            )
            db.add(content)
            contents.append(content)
        
        db.commit()
        print(f"✅ {len(contents)} conteúdos criados")
        
        # 3. Criar vídeos
        print("🎥 Criando vídeos...")
        videos = []
        video_ids = [
            'dQw4w9WgXcQ',  # Never Gonna Give You Up
            'jNQXAC9IVRw',  # Me at the zoo
            '9bZkp7q19f0',  # Gangnam Style
            'kJQP7kiw5Fk',  # Despacito
            'OPf0YbXqDm0'   # Mark Ronson
        ]
        
        for idx, content in enumerate(contents):
            # Criar 3-5 vídeos por conteúdo
            num_videos = random.randint(3, 5)
            for i in range(num_videos):
                video = Video(
                    id=str(uuid.uuid4()),
                    content_id=content.id,
                    video_id=video_ids[i % len(video_ids)],
                    title=f"{content.title} - Parte {i+1}",
                    quantity_until_e2e=3,
                    order_index=i,
                    created_at=datetime.now() - timedelta(days=random.randint(30, 90))
                )
                db.add(video)
                videos.append(video)
        
        db.commit()
        print(f"✅ {len(videos)} vídeos criados")
        
        # 4. Criar atividades
        print("📝 Criando atividades...")
        activities = []
        for content in contents:
            # Criar 2-4 atividades por conteúdo
            num_activities = random.randint(2, 4)
            for i in range(num_activities):
                activity = Activity(
                    id=str(uuid.uuid4()),
                    content_id=content.id,
                    question=f"Questão {i+1} sobre {content.title}: Explique o conceito principal abordado.",
                    order_index=i,
                    created_at=datetime.now() - timedelta(days=random.randint(30, 90))
                )
                db.add(activity)
                activities.append(activity)
        
        db.commit()
        print(f"✅ {len(activities)} atividades criadas")
        
        # 5. Criar progresso de vídeos (alguns usuários assistiram alguns vídeos)
        print("📊 Criando progresso de vídeos...")
        progress_count = 0
        for user in users:
            # Cada usuário assiste entre 5-15 vídeos
            num_watched = random.randint(5, 15)
            watched_videos = random.sample(videos, min(num_watched, len(videos)))
            
            for video in watched_videos:
                progress = UserVideoProgress(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    video_id=video.id,
                    watched=True,
                    watched_at=datetime.now() - timedelta(days=random.randint(1, 60))
                )
                db.add(progress)
                progress_count += 1
        
        db.commit()
        print(f"✅ {progress_count} registros de progresso criados")
        
        # 6. Criar respostas de atividades
        print("💬 Criando respostas de atividades...")
        responses_count = 0
        for user in users:
            # Cada usuário responde entre 3-8 atividades
            num_responses = random.randint(3, 8)
            responded_activities = random.sample(activities, min(num_responses, len(activities)))
            
            for activity in responded_activities:
                grau = random.uniform(0.4, 1.0)  # Grau de aprendizagem entre 0.4 e 1.0
                response = UserActivityResponse(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    activity_id=activity.id,
                    answer=f"Resposta do usuário {user.nome} para a atividade sobre {activity.question[:30]}...",
                    grau_aprendizagem=round(grau, 2),
                    responded=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 50))
                )
                db.add(response)
                responses_count += 1
        
        db.commit()
        print(f"✅ {responses_count} respostas criadas")
        
        print("\n✨ Dados de teste criados com sucesso!")
        print(f"\n📊 Resumo:")
        print(f"  - {len(users)} usuários")
        print(f"  - {len(contents)} conteúdos")
        print(f"  - {len(videos)} vídeos")
        print(f"  - {len(activities)} atividades")
        print(f"  - {progress_count} vídeos assistidos")
        print(f"  - {responses_count} atividades respondidas")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_test_data()

