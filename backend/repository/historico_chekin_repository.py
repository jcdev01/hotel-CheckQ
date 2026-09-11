from domain.checkin import Checkin
from domain.base import Base, engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.historico_checkin import HistoricoCheckin


class HistoricoCheckinRepository:
    

    def listar_historico(self) -> list[HistoricoCheckin]:
        """Retorna todos os checkins atendidos, na ordem de chegada (ORDER BY id)."""
        with Session(engine) as session:
            resultado = session.execute(
                select(HistoricoCheckin).order_by(HistoricoCheckin.id)
            )
            return list(resultado.scalars().all())