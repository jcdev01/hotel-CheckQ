from typing import Optional
from sqlalchemy.orm import Session

from domain.usuario import Usuario
from domain.base import Base, engine


class UsuarioRepository:

    def __init__(self):
        Base.metadata.create_all(engine)

    def adicionar(self, usuario: Usuario) -> Usuario:
        with Session(engine) as session:
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        with Session(engine) as session:
            return (
                session.query(Usuario)
                .filter(Usuario.id == usuario_id)
                .first()
            )

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        with Session(engine) as session:
            return (
                session.query(Usuario)
                .filter(Usuario.email == email)
                .first()
            )

    def buscar_por_cpf(self, cpf: str) -> Optional[Usuario]:
        with Session(engine) as session:
            return (
                session.query(Usuario)
                .filter(Usuario.cpf == cpf)
                .first()
            )

    def listar_todos(self) -> list[Usuario]:
        with Session(engine) as session:
            return session.query(Usuario).all()

    def atualizar(self, usuario: Usuario) -> Usuario:
        with Session(engine) as session:
            session.merge(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario

    def deletar(self, usuario_id: int) -> bool:
        with Session(engine) as session:
            usuario = (
                session.query(Usuario)
                .filter(Usuario.id == usuario_id)
                .first()
            )

            if usuario:
                session.delete(usuario)
                session.commit()
                return True

            return False