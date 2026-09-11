#rota apra o front chekin-recepcao
from fastapi import APIRouter
from services.historico_chekin_service import HistoricoCheckinService  
from repository.historico_chekin_repository import HistoricoCheckinRepository

router=APIRouter()
_repository = HistoricoCheckinRepository()
_service = HistoricoCheckinService(_repository)



@router.get("/historico")
def listar_historico():
    return _service.listar_historico()