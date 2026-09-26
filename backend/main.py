# Executar os comandos abaixo para iniciar o servidor:
# cd backend
# uvicorn main:app --reload

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.checkin_routes import router as checkin_routes
from routes.historico_chekin_routes import router as historico_chekin_routes
from routes.usuarios_routes import router as usuario_routes
from routes.auth_routes import router as auth_routes
from routes.usuario_global_routes import router as usuario_global_routes

from repository.usuario_global_repository import UsuarioGlobalRepository
from services.usuario_global_service import UsuarioGlobalService


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Inicializa o repository e o service do usuário global
    usuario_global_repository = UsuarioGlobalRepository()
    usuario_global_service = UsuarioGlobalService(
        usuario_global_repository
    )

    # Cria o usuário global padrão caso ainda não exista
    usuario_global_service.criar_usuario_global_padrao()

    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(checkin_routes)
app.include_router(historico_chekin_routes)
app.include_router(usuario_routes)
app.include_router(auth_routes)
app.include_router(usuario_global_routes)