#executar o comando uvicorn backend.main:app --reload para rodar a API

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Mensagem":"Hello World"}
