from domain.checkin import Checkin  
from repository.historico_chekin_repository import HistoricoCheckinRepository
from domain.historico_checkin import HistoricoCheckin

class HistoricoCheckinService:
    def __init__(self, repository: HistoricoCheckinRepository):
        self._repository = repository

    def listar_historico(self) -> list[HistoricoCheckin]:
        return self._repository.listar_historico()