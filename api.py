from fastapi import FastAPI
from src.main import run_pipeline, DEFAULT_CONFIG

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Hermes rodando"}

@app.post("/run")
def run():
    run_pipeline("cloud", DEFAULT_CONFIG)
    return {"status": "execução iniciada"}