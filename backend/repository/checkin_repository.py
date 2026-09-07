from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from domain.checkin import Base, Checkin


class CheckinRepository:
    def __init__(self, caminho_banco: str = "sqlite:///checkin.db"):
        self._engine = create_engine(caminho_banco)
        Base.metadata.create_all(self._engine)  # cria a tabela se não existir

    def adicionar(self, checkin: Checkin) -> Checkin:
        """Salva um novo checkin no banco (equivalente ao save() do JPA)."""
        with Session(self._engine) as session:
            session.add(checkin)
            session.commit()
            session.refresh(checkin)  # atualiza o objeto com o id gerado
            return checkin

    def listar_todos(self) -> list[Checkin]:
        """Retorna todos os checkins, na ordem de chegada (ORDER BY id)."""
        with Session(self._engine) as session:
            resultado = session.execute(
                select(Checkin).order_by(Checkin.id)
            )
            return list(resultado.scalars().all())

    def proximo(self) -> Checkin:
        """Remove e retorna o checkin mais antigo da fila (o primeiro)."""
        with Session(self._engine) as session:
            resultado = session.execute(
                select(Checkin).order_by(Checkin.id).limit(1)
            )
            checkin = resultado.scalars().first()

            if checkin is None:
                raise IndexError("Fila vazia — não há check-in para atender")

            session.delete(checkin)
            session.commit()
            return checkin