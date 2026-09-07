
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Checkin(Base):
   __tablename__ = "checkin"

   id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
   nome_hospede: Mapped[str] = mapped_column(String)
   numero_quarto: Mapped[int] = mapped_column(Integer)
   horario_entrada: Mapped[str] = mapped_column(String)
   horario_saida: Mapped[str] = mapped_column(String)

