from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.base import Base, engine
from domain.checkin import Checkin
from domain.historico_checkin import HistoricoCheckin


class CheckinRepository:
    def __init__(self):  
        Base.metadata.create_all(engine)  # cria a tabela se não existir

    def adicionar(self, checkin: Checkin) -> Checkin:
        """Salva um novo checkin no banco """
        with Session(engine) as session:
            session.add(checkin)
            session.commit()
            session.refresh(checkin)  # atualiza o objeto com o id gerado
            return checkin

    def listar_todos(self) -> list[Checkin]:
        """Retorna todos os checkins, na ordem de chegada (ORDER BY id)."""
        with Session(engine) as session:
            resultado = session.execute(
                select(Checkin).order_by(Checkin.id)
            )
            return list(resultado.scalars().all())

    def proximo(self) -> Checkin:
        """Remove e retorna o checkin mais antigo da fila (o primeiro)."""
        with Session(engine) as session:
            resultado = session.execute(
                select(Checkin).order_by(Checkin.id).limit(1)
            )
            checkin = resultado.scalars().first()

            if checkin is None:
                raise IndexError("Fila vazia — não há check-in para atender")

            registro_historico =HistoricoCheckin(
                nome_hospede=checkin.nome_hospede,
                numero_quarto=checkin.numero_quarto,
                horario_entrada=checkin.horario_entrada,
                horario_saida=checkin.horario_saida,
            )
            session.add(registro_historico)

            session.delete(checkin)
            session.commit()
            return checkin