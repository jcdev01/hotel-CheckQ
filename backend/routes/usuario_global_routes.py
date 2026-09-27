from fastapi import APIRouter

from repository.usuario_global_repository import UsuarioGlobalRepository
from services.usuario_global_service import UsuarioGlobalService


router = APIRouter()

_repository = UsuarioGlobalRepository()
_service = UsuarioGlobalService(_repository)


@router.get("/admin/user")
def verificar_usuario_global():
    existe = _service.usuario_global_existe()

    return {
        "criado": existe
    }