import os
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
class UsuarioGlobalSchema(BaseModel):
    username: str
    password: str 
class LoginSchema(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login_hospede(dados: LoginSchema):
    try:
        usuario = _service.autenticar_usuario(dados.email, dados.senha)
        return {"mensagem": "Login aprovado", "nome": usuario.nome}
    except Exception as erro:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

@router.post("/admin/login")
def login_admin(dados: LoginSchema):
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "recepcao123")
    if dados.email == admin_user and dados.senha == admin_pass:
        return{"mensagem": "Acessi liberado"}
    raise HTTPException(status_code=401, detail="adm invalido")

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

@router.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int):
    try:
        usuario = _service.obter_por_id(usuario_id)
        return usuario
    except UsuarioNaoEncontradoError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    try:
        _service.remover_usuario(usuario_id)
        return {"message": f"Usuário com ID {usuario_id} deletado com sucesso."}
    except UsuarioNaoEncontradoError as erro: 
        raise HTTPException(status_code=404, detail=str(erro))

