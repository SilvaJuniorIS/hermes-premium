# check_pncp_dates.py
import requests
import json
import os
import sys

# Adiciona o diretório pai ao PATH para que a importação de src.pncp_api_client funcione
# Isso é útil se você estiver executando o script diretamente na raiz do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa as configurações da API do seu pncp_api_client.py
try:
    from src.pncp_api_client import PNCP_API_BASE_URL, PNCP_API_TOKEN
except ImportError:
    print("Erro: Não foi possível importar PNCP_API_BASE_URL e PNCP_API_TOKEN de src.pncp_api_client.")
    print("Verifique se o arquivo src/pncp_api_client.py existe e contém essas variáveis.")
    print("Certifique-se também de que o diretório 'src' está na mesma pasta que 'check_pncp_dates.py'.")
    exit()

def get_licitacao_details(pncp_id: str):
    headers = {
        "Authorization": f"Bearer {PNCP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    # A API do PNCP para detalhes de uma licitação específica é geralmente /v1/licitacoes/{pncp_id}
    # ou /v1/publicacoes/{pncp_id} dependendo do tipo.
    # Vamos tentar o endpoint de publicações, que é mais abrangente.
    url = f"{PNCP_API_BASE_URL}/v1/publicacoes/{pncp_id}"

    print(f"Consultando URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Levanta um erro para status HTTP ruins (4xx ou 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar a API do PNCP para {pncp_id}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
        return None

if __name__ == "__main__":
    # Substitua pelo PNCP_ID que você quer investigar do seu relatório Excel
    PNCP_ID_TO_CHECK = "82892308000153-1-000099/2026" # Exemplo: ID 1 do seu relatório

    print(f"Buscando detalhes para o PNCP ID: {PNCP_ID_TO_CHECK}")
    details = get_licitacao_details(PNCP_ID_TO_CHECK)

    if details:
        print("\n--- Resposta JSON Completa da API ---")
        print(json.dumps(details, indent=4, ensure_ascii=False))
        print("\n--- Fim da Resposta JSON ---")
    else:
        print(f"Não foi possível obter detalhes para o PNCP ID: {PNCP_ID_TO_CHECK}")
