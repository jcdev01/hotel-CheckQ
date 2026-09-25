from domain.checkin import Checkin
from repository.checkin_repository import CheckinRepository
from datetime import datetime


class QuartoJaOcupadoError(Exception):
    """Levantada quando já existe um check-in ativo para esse quarto."""


class FilaVaziaError(Exception):
    """Levantada quando a recepção tenta atender e não há ninguém na fila."""


class NumeroQuartoInvalidoError(Exception):
    """Levantada quando o número do quarto está fora do limite do hotel."""


class DataEntradaInvalidaError(Exception):
    """Levantada quando a data de entrada é inválida (ex: no passado)."""


class DataSaidaInvalidaError(Exception):
    """Levantada quando a data de saída é anterior à de entrada."""


class CheckinService:
    total_quartos = 100

    def __init__(self, repository: CheckinRepository):
        self._repository = repository

    def solicitar_checkin(
        self,
        nome_hospede: str,
        numero_quarto: int,
        horario_entrada: datetime,
        horario_saida: datetime,
    ) -> Checkin:
        """Cria um novo check-in, validando dados de entrada antes de
        checar regras de negócio contra o estado atual (quarto ocupado)."""

        # 1. Validações de formato/valor dos dados recebidos, antes de
        # qualquer consulta ao repositório.
        if not nome_hospede or not nome_hospede.strip():
            raise ValueError("O nome do hóspede não pode ser vazio.")

        if numero_quarto < 1 or numero_quarto > self.total_quartos:
            raise NumeroQuartoInvalidoError(
                f"Número do quarto inválido. O hotel possui até {self.total_quartos} quartos disponíveis."
            )

        if horario_entrada < datetime.now(horario_entrada.tzinfo):
            raise DataEntradaInvalidaError(
                "A data de entrada não pode ser no passado."
            )

        if horario_saida < horario_entrada:
            raise DataSaidaInvalidaError(
                "A data de saída não pode ser antes da de entrada."
            )

        # 2. Regra de negócio que depende do estado atual, checada por último.
        todos = self._repository.listar_todos()
        quarto_ocupado = any(c.numero_quarto == numero_quarto for c in todos)

        if quarto_ocupado:
            raise QuartoJaOcupadoError(
                f"O quarto {numero_quarto} já está ocupado por outro check-in."
            )

        novo_checkin = Checkin(
            nome_hospede=nome_hospede,
            numero_quarto=numero_quarto,
            horario_entrada=horario_entrada,
            horario_saida=horario_saida,
        )
        return self._repository.adicionar(novo_checkin)

    def atender_proximo(self) -> Checkin:
        """Remove e retorna o check-in mais antigo da fila (FIFO).

        Checa explicitamente se a fila está vazia em vez de depender de um
        IndexError vindo da implementação do repositório — assim o
        comportamento não muda se o repositório trocar de lista em memória
        para banco de dados, por exemplo.
        """
        fila = self._repository.listar_todos()
        if not fila:
            raise FilaVaziaError("Não há check-ins aguardando na fila.")
        return self._repository.proximo()

    def listar_fila(self) -> list[Checkin]:
        return self._repository.listar_todos()