from typing import Optional
from sqlalchemy.orm import Session
from domain.usuario import Usuario

class UsuarioRepository:
    def __init__(self, session: Session):
        self._session = session

    def adicionar(self, usuario: Usuario) -> Usuario:
        self._session.add(usuario)
        self._commit()
        self._session.refresh(usuario)
        return usuario

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.session.query(Usuario).filter(Usuario.id == usuario_id).first()

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return self.session.query(Usuario).filter(Usuario.email == email). first()

    def buscar_por_cpf(self, cpf: str) -> Optional[Usuario]:
        return self.session.query(Usuario).filter(Usuario.cpf == cpf).first()

    def listar_todos(self) -> list[Usuario]:
        return self._session.query(Usuario).all()

    def atualizar(self, usuario: Usuario) -> Usuario:
        self._session.commit()
        self._session.refresh(usuario)
        return usuario

    def deletar(self, usuario_id: int) -> bool:
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            self._session.delete(usuario)
            self._session.commit()
            return True
        return False