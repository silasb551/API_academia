from sqlalchemy.orm import Session
from .models import Exercicio
from .schemas import ExercicioCriar



# Função para criar um exercício
def criar_exercicio(db: Session, exercicio: ExercicioCriar):
    db_exercicio = Exercicio(**exercicio.model_dump())
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio

def criar_exercicios_iniciais(db: Session):
    exercicios = [

        {
            "nome": "Flexão Diamante",
            "url_video": "https://www.youtube.com/watch?v=PAauHMIhWKg",
            "descricao": "Flexão de braços diamante é um exercício que envolve as articulações de cotovelo e ombro, solicitando fortemente a musculatura de peitoral, ombro e tríceps. Envolve também a musculatura estabilizadora do quadril e tronco, exercitando indiretamente a musculatura abdominal."
        },
        {
            "nome": "Remada Prancha",
            "url_video": "https://www.youtube.com/watch?v=LDAetC9WbeM",
            "descricao": "A remada em prancha com halteres é um bom exercício para intensificar o músculo dorsal e reforçar todos os músculos do core. É um excelente desafio funcional para elevar o nível de intensidade."
        },
        {
            "nome": "Agachamento Com Uma Perna",
            "url_video": "https://www.youtube.com/watch?v=b-p1hBJ-_tg",
            "descricao": "O agachamento com uma perna é um dos exercícios mais completos, envolvendo grupos musculares dos membros inferiores e toda a região do core. Quando feito com uma barra, também ativa os paravertebrais."
        },
        {
            "nome": "Agachamento Com Barra",
            "url_video": "https://www.youtube.com/watch?v=0idszCQ-Ky0",
            "descricao": "O agachamento livre com barra é um exercício completo da musculação, priorizando quadríceps, glúteos e adutores."
        },
        {
            "nome": "Bíceps Alternados Com Halteres",
            "url_video": "https://www.youtube.com/watch?v=n-TsjQkOa3c",
            "descricao": "A rosca alternada é um dos principais exercícios para fortalecimento dos braços, focado nos músculos dos bíceps."
        },
        {
            "nome": "Supino Reto Com Barra",
            "url_video": "https://www.youtube.com/watch?v=Kr2erpSyu3M",
            "descricao": "O supino reto com barra permite maior amplitude de movimento, ativando peito, bíceps braquial e tríceps. Requer equilíbrio e coordenação."
        }
    
    ]
    for exercicio in exercicios:
        db_exercicio = Exercicio(**exercicio)
        db.add(db_exercicio)
    db.commit()
    return {"mensagem": "Exercicios criados"}


#exercício pelo ID
def obter_exercicio_por_id(db: Session, exercicio_id: int):
    return db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()


#get pelo ID
def obter_exercicio(db: Session, exercicio_id: int):
    return obter_exercicio_por_id(db, exercicio_id)

#get
def obter_exercicios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Exercicio).offset(skip).limit(limit).all()

#put
def atualizar_exercicio(db: Session, exercicio_id: int, dados_exercicio: ExercicioCriar):
    db_exercicio = obter_exercicio_por_id(db, exercicio_id)
    if db_exercicio:
        db_exercicio.nome = dados_exercicio.nome
        db_exercicio.url_video = dados_exercicio.url_video
        db_exercicio.descricao = dados_exercicio.descricao
        db.commit()
        db.refresh(db_exercicio)
        return db_exercicio
    return None

# delete

def deletar_exercicio(db: Session, exercicio_id: int):
    db_exercicio = obter_exercicio_por_id(db, exercicio_id)
    if db_exercicio:
        db.delete(db_exercicio)
        db.commit()
        return {"mensagem": "Exercicio deletado"}
    return {"mensagem": "Exercicio não encontrado"}
