from pathlib import Path

# =========================
# BANCO (FONTE ÚNICA)
# =========================
DB_PATH = Path("data/hermes.sqlite3").resolve()

# =========================
# OUTPUT
# =========================
OUTPUT_DIR = "output"

# =========================
# IA
# =========================
IA_API_KEY_ENV_VAR = "OPENAI_API_KEY"

# =========================
# KEYWORDS
# =========================
KEYWORDS = [
    "serviços",
    "material",
    "equipamento",
    "obras",
    "consultoria",
    "manutenção",
    "software",
    "hardware",
    "limpeza",
    "segurança",
    "alimentação",
    "veículos"
]

# =========================
# STATES
# =========================
STATES = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO"
]
