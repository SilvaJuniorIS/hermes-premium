from fastapi import FastAPI
from src.jobs.runner import run_pipeline

app = FastAPI(title="HERMES PREMIUM API")


@app.get("/run/{perfil}")
def run(perfil: str):
    data = run_pipeline(perfil)
    return {
        "perfil": perfil,
        "total": len(data),
        "status": "ok"
    }