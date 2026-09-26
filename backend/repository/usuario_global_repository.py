from typing import Optional
from sqlalchemy.orm import Session

from domain.usuario_global import UsuarioGlobal
from domain.base import Base, engine


class UsuarioGlobalRepository:

    def __init__(self):
        Base.metadata.create_all(engine)

    def adicionar(self, usuario: UsuarioGlobal) -> UsuarioGlobal:
        with Session(engine) as session:
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario

    def buscar_usuario_global(self) -> Optional[UsuarioGlobal]:
        with Session(engine) as session:
            return session.query(UsuarioGlobal).first()