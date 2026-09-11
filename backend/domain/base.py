from sqlalchemy.orm import DeclarativeBase
import os
from sqlalchemy import create_engine

os.makedirs("data", exist_ok=True)  # cria o diretório "data" se não existir
engine = create_engine("sqlite:///data/checkin.db")


class Base(DeclarativeBase):
    pass


