from src.hermes_api_client import fetch_licitacoes_from_pncp_api
from src.config import KEYWORDS, STATES


def run_collection(perfil: str, max_total: int = 100):
    data, stats = fetch_licitacoes_from_pncp_api(
        keywords=KEYWORDS,
        states=STATES,
        max_total=max_total
    )

    return data, stats