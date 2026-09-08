from domain.checkin import Checkin
from repository.checkin_repository import CheckinRepository
from datetime import datetime


class QuartoJaOcupadoError(Exception):
    """Levantado quando já existe um check-in ativo para esse quarto."""


class FilaVaziaError(Exception):
    """Levantado quando a recepção tenta atender e não há ninguém na fila."""


class CheckinService:
    def __init__(self, repository: CheckinRepository):
        self._repository = repository

    def solicitar_checkin(self, nome_hospede: str, numero_quarto: int,
                           horario_entrada: datetime, horario_saida: datetime) -> Checkin:
        """Cria um novo check-in, bloqueando quarto já ocupado."""
        todos = self._repository.listar_todos()
        quarto_ocupado = any(c.numero_quarto == numero_quarto for c in todos)

        if quarto_ocupado:
            raise QuartoJaOcupadoError(
                f"O quarto {numero_quarto} já está ocupado por outro check-in na fila"
            )

        novo_checkin = Checkin(
            nome_hospede=nome_hospede,
            numero_quarto=numero_quarto,
            horario_entrada=horario_entrada,
            horario_saida=horario_saida,
        )
        return self._repository.adicionar(novo_checkin)

    def atender_proximo(self) -> Checkin:
        """Remove e retorna o check-in mais antigo da fila (FIFO)."""
        try:
            return self._repository.proximo()
        except IndexError:
            raise FilaVaziaError("Não há check-ins aguardando na fila")
    def listar_fila(self) -> list[Checkin]:
        return self._repository.listar_todos()



    def listar_historico(self) -> list[Checkin]:
        return self._repository.listar_historico()