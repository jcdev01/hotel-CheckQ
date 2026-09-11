from datetime import date
from typing import Optional

from domain.usuario import Usuario
from repository.usuario_repository import UsuarioRepository
from security.senha import gerar_hash_senha, comparar_senha


class UsuarioJaExisteError(Exception):
    """Levantado quando se tenta criar um e-mail ou CPF já existente no banco de dados."""


class MenorDeIdadeError(Exception):
    """Levantado quando o cliente tenta se cadastrar com menos de 18 anos."""


class UsuarioNaoEncontradoError(Exception):
    """Levantado quando a busca por um usuário específico não retorna resultados."""


class DadosInvalidosError(Exception):
    """Levantado quando dados obrigatórios do formulário não são informados."""


class UsuarioService:

    def __init__(self, repository: UsuarioRepository):
        self._repository = repository

    def cadastrar_usuario(
        self,
        nome: str,
        cpf: str,
        email: str,
        senha: str,
        telefone: str,
        data_nascimento: date
    ) -> Usuario:

        if not nome or not cpf or not email or not senha:
            raise DadosInvalidosError(
                "Todos os campos obrigatórios devem ser preenchidos."
            )

        hoje = date.today()

        idade = hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day)
            < (data_nascimento.month, data_nascimento.day)
        )

        if idade < 18:
            raise MenorDeIdadeError(
                "O cliente deve ter no mínimo 18 anos para realizar cadastro."
            )

        if self._repository.buscar_por_email(email):
            raise UsuarioJaExisteError(
                f"Já existe um usuário cadastrado com o e-mail: {email}"
            )

        if self._repository.buscar_por_cpf(cpf):
            raise UsuarioJaExisteError(
                f"Já existe um usuário cadastrado com o CPF: {cpf}"
            )

        # Transforma a senha antes de salvar no banco
        senha_hash = gerar_hash_senha(senha)

        novo_usuario = Usuario(
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senha_hash,
            telefone=telefone,
            data_nascimento=data_nascimento
        )

        return self._repository.adicionar(novo_usuario)

    def obter_por_id(self, usuario_id: int) -> Usuario:
        usuario = self._repository.buscar_por_id(usuario_id)

        if not usuario:
            raise UsuarioNaoEncontradoError(
                f"Usuário com ID {usuario_id} não foi encontrado."
            )

        return usuario

    def obter_por_email(self, email: str) -> Usuario:
        usuario = self._repository.buscar_por_email(email)

        if not usuario:
            raise UsuarioNaoEncontradoError(
                f"Usuário com e-mail {email} não foi encontrado."
            )

        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        return self._repository.listar_todos()

    def atualizar_perfil(
        self,
        usuario_id: int,
        nome: Optional[str] = None,
        telefone: Optional[str] = None
    ) -> Usuario:

        usuario = self.obter_por_id(usuario_id)

        if nome:
            usuario.nome = nome

        if telefone:
            usuario.telefone = telefone

        return self._repository.atualizar(usuario)

    def remover_usuario(self, usuario_id: int) -> bool:
        self.obter_por_id(usuario_id)
        return self._repository.deletar(usuario_id)