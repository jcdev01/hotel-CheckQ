from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.usuario_service import UsuarioService, UsuarioNaoEncontradoError, DadosInvalidosError
from services.auth_service import AuthService
from repository.usuario_repository import UsuarioRepository

router = APIRouter()

_usuario_repository = UsuarioRepository()
_usuario_service = UsuarioService(_usuario_repository)
_auth_service = AuthService()


class LoginSchema(BaseModel):
    email: str
    senha: str


@router.post("/auth/login")
def login(dados: LoginSchema):
    try:
        usuario = _usuario_service.autenticar_usuario(dados.email, dados.senha)
    except (UsuarioNaoEncontradoError, DadosInvalidosError):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token = _auth_service.gerar_token(usuario)
    return {"token": token, "nome": usuario.nome}