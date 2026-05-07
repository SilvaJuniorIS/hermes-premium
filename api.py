from fastapi import FastAPI
from pydantic import BaseModel

from src.main import run_pipeline, DEFAULT_CONFIG

app = FastAPI()

class RunRequest(BaseModel):
    perfil: str = "default"

@app.get("/")
def home():
    return {"status": "Hermes rodando 🚀"}

@app.post("/run")
def run(req: RunRequest):
    run_pipeline(req.perfil, DEFAULT_CONFIG)
    return {"status": f"Execução iniciada: {req.perfil}"}