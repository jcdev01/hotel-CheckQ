from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.checkin_service import (
    CheckinService,
    QuartoJaOcupadoError,
    FilaVaziaError,
)
from repository.checkin_repository import CheckinRepository

router = APIRouter()

# Instâncias compartilhadas (repository -> service)
_repository = CheckinRepository()
_service = CheckinService(_repository)


# --- Schema: o que a API espera receber no POST ---
class CheckinCreateSchema(BaseModel):
    nome_hospede: str
    numero_quarto: int
    horario_entrada: str
    horario_saida: str


@router.post("/fila")
def solicitar_checkin(dados: CheckinCreateSchema):
    try:
        checkin = _service.solicitar_checkin(
            nome_hospede=dados.nome_hospede,
            numero_quarto=dados.numero_quarto,
            horario_entrada=dados.horario_entrada,
            horario_saida=dados.horario_saida,
        )
        return checkin
    except QuartoJaOcupadoError as erro:
        raise HTTPException(status_code=409, detail=str(erro))


@router.get("/fila")
def listar_fila():
    return _service.listar_fila()


@router.delete("/fila/proximo")
def atender_proximo():
    try:
        return _service.atender_proximo()
    except FilaVaziaError as erro:
        raise HTTPException(status_code=404, detail=str(erro))