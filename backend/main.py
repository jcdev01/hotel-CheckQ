#Executar os comandos abaixo para iniciar o servidor:
#cd backend
#uvicorn main:app --reload

from fastapi import FastAPI
from routes.checkin_routes import router as checkin_router

app = FastAPI()

app.include_router(checkin_router)
