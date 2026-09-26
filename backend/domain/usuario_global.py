from datetime import date, datetime
from sqlalchemy import String, Integer, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from domain.base import Base


class UsuarioGlobal(Base):
    __tablename__ = "usuario_global"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] =mapped_column(String)
  