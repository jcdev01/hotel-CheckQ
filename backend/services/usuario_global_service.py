from domain.usuario_global import UsuarioGlobal
from repository.usuario_global_repository import UsuarioGlobalRepository
from security.senha import gerar_hash_senha
import os


class UsuarioGlobalService:

    def __init__(self, repository: UsuarioGlobalRepository):
        self._repository = repository

    def usuario_global_existe(self) -> bool:
        usuario = self._repository.buscar_usuario_global()
        return usuario is not None

    def criar_usuario_global_padrao(self) -> UsuarioGlobal:
        usuario = self._repository.buscar_usuario_global()

        # Se já existe um usuário global, não cria outro
        if usuario:
            return usuario

        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")

        if not username or not password:
            raise ValueError(
                "ADMIN_USERNAME e ADMIN_PASSWORD precisam estar configurados no .env"
            )

        senha_hash = gerar_hash_senha(password)

        novo_usuario = UsuarioGlobal(
            username=username,
            password=senha_hash
        )

        return self._repository.adicionar(novo_usuario)