#Executar os comandos abaixo para iniciar o servidor:
#cd backend
#uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.checkin_routes import router as checkin_router
from routes.historico_chekin_routes import router as historico_chekin_routes
from routes.usuarios_routes import router as usuario_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(checkin_router)
app.include_router(historico_chekin_routes)
app.include_router(usuario_router)
