import time
from src.main import run_pipeline, DEFAULT_CONFIG

PERFIS = [
    "limpeza_higiene",
    "medicamentos",
    "ti_eletro_domesticos"
]

INTERVALO = 60 * 60 * 6  # a cada 6 horas

while True:
    print("🚀 Iniciando ciclo automático Hermes...")

    for perfil in PERFIS:
        try:
            print(f"\n🔎 Rodando perfil: {perfil}")
            run_pipeline(perfil, DEFAULT_CONFIG)
        except Exception as e:
            print(f"Erro no perfil {perfil}: {e}")

    print(f"\n⏳ Aguardando próximo ciclo ({INTERVALO}s)...\n")
    time.sleep(INTERVALO)