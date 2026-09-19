import secrets
from datetime import datetime, timedelta

from domain.usuario import Usuario

# Guarda os tokens válidos em memória: {token: (usuario_id, expira_em)}
_tokens_ativos: dict[str, tuple[int, datetime]] = {}

DURACAO_TOKEN = timedelta(hours=2)


class AuthService:
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