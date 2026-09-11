from datetime import date
from typing import Optional
from domain.usuario import Usuario
from repository.usuario_repository import UsuarioRepository

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
        self._repoitory = repository

    def cadastrar_usuario(self, nome: str, cpf: str, email: str, senha_hash: str, telefone: str, data_nascimento: date) -> Usuario:
        """
        Aplica as regras de negócio e cadastra um novo cliente no sistema.
        """

        if not nome or not cpf or not email or not senha_hash:
            raise DadosInvalidosError("Todos os campos obrigatórios devem ser preenchidos.")

        hoje = date.today()
        idade = hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
        )
        if idade < 18:
            raise MenorDeIdadeError("O cliente deve ter no mínimo 18 anos para realizar cadastro.")

        # 3. Validação de Duplicidade (E-mail único)
        if self._repository.buscar_por_email(email):
            raise UsuarioJaExisteError(f"Já existe um usuário cadastrado com o e-mail: {email}")

        # 4. Validação de Duplicidade (CPF único)
        if self._repository.buscar_por_cpf(cpf):
            raise UsuarioJaExisteError(f"Já existe um usuário cadastrado com o CPF: {cpf}")

        # 5. Instanciação e Persistência
        novo_usuario = Usuario(
            nome=nome,
            cpf=cpf,
            email=email,
            senha_hash=senha_hash,
            telefone=telefone,
            data_nascimento=data_nascimento
        )

        return self._repository.adicionar(novo_usuario)

    def obter_por_id(self, usuario_id: int) -> Usuario:
        """Retorna um usuário pelo seu ID ou levanta exceção se não existir."""
        usuario = self._repository.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {usuario_id} não foi encontrado.")
        return usuario

    def obter_por_email(self, email: str) -> Usuario:
        """Retorna um usuário pelo e-mail ou levanta exceção se não existir."""
        usuario = self._repository.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário com e-mail {email} não foi encontrado.")
        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        """Retorna a lista completa de usuários cadastrados."""
        return self._repository.listar_todos()

    def atualizar_perfil(
        self,
        usuario_id: int,
        nome: Optional[str] = None,
        telefone: Optional[str] = None
    ) -> Usuario:
        """Atualiza informações do perfil do usuário."""
        usuario = self.obter_por_id(usuario_id)

        if nome:
            usuario.nome = nome
        if telefone:
            usuario.telefone = telefone

        return self._repository.atualizar(usuario)

    def remover_usuario(self, usuario_id: int) -> bool:
        """Exclui o cadastro de um usuário do sistema."""
        self.obter_por_id(usuario_id)  # Valida se existe antes de deletar
        return self._repository.deletar(usuario_id)