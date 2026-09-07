# executar o comando uvicorn main:app --reload (a partir de dentro da pasta backend/)
from fastapi import FastAPI
from routes.checkin_routes import router as checkin_router

app = FastAPI()

app.include_router(checkin_router)
