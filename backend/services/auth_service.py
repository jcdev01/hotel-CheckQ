import secrets
from datetime import datetime, timedelta

from domain.usuario import Usuario
from repository.usuario_global_repository import UsuarioGlobalRepository
from security.senha import comparar_senha


_tokens_ativos: dict[str, tuple[int, datetime]] = {}

DURACAO_TOKEN = timedelta(hours=2)


class CredenciaisInvalidasError(Exception):
    pass


class AuthService:

    def __init__(self):
        self._usuario_global_repository = UsuarioGlobalRepository()


    

    def gerar_token(self, usuario: Usuario) -> str:
        token = secrets.token_urlsafe(32)
        expira_em = datetime.now() + DURACAO_TOKEN

        _tokens_ativos[token] = (usuario.id, expira_em)

        return token

    def validar_token(self, token: str) -> int | None:
        """Retorna o id do usuário se o token for válido, ou None."""

        dados = _tokens_ativos.get(token)

        if dados is None:
            return None

        usuario_id, expira_em = dados

        if datetime.now() > expira_em:
            del _tokens_ativos[token]
            return None

        return usuario_id

    def autenticar_admin(self, username: str, password: str) -> bool:

        usuario = self._usuario_global_repository.buscar_usuario_global()

        if not usuario:
            raise CredenciaisInvalidasError(
                "Usuário administrador não encontrado."
            )

        if usuario.username != username:
            raise CredenciaisInvalidasError(
                "Credenciais de administrador inválidas."
            )

        if not comparar_senha(password, usuario.password):
            raise CredenciaisInvalidasError(
                "Credenciais de administrador inválidas."
            )

        

        return True