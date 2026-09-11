from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime
from domain.base import Base


    
class HistoricoCheckin(Base):
    __tablename__ = "historico_checkin"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_hospede: Mapped[str] = mapped_column(String)
    numero_quarto: Mapped[int] = mapped_column(Integer)
    horario_entrada: Mapped[datetime] = mapped_column(DateTime)
    horario_saida: Mapped[datetime] = mapped_column(DateTime)

