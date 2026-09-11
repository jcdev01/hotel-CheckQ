from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from services.usuario_service import (
    UsuarioService,
    UsuarioJaExisteError,
    MenorDeIdadeError,
    UsuarioNaoEncontradoError,
    DadosInvalidosError
)

from repository.usuario_repository import UsuarioRepository

router = APIRouter()

_repository = UsuarioRepository()
_service = UsuarioService(_repository)

class UsuarioCreateSchema(BaseModel):
    nome: str
    cpf: str
    email: str
    senha: str
    telefone: str
    data_nascimento: datetime

@router.get("/usuarios")
def listar_usuarios():
    return _service.listar_usuarios()

@router.post("/usuarios")
def cadastrar_usuario(dados: UsuarioCreateSchema):
    try:
        usuario = _service.cadastrar_usuario(
            nome=dados.nome,
            cpf=dados.cpf,
            email=dados.email,
            senha=dados.senha,
            telefone=dados.telefone,
            data_nascimento=dados.data_nascimento.date()
        )
        return usuario
    except (UsuarioJaExisteError, MenorDeIdadeError, DadosInvalidosError) as erro:
        raise HTTPException(status_code=400, detail=str(erro))
