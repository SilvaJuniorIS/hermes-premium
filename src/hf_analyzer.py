# src/hf_analyzer.py
# Módulo de Análise de IA para o Projeto Hermes (com integração Hugging Face)

import os
import json
import requests
from src.config import IA_API_KEY_ENV_VAR # Agora esta variável será para a chave do Hugging Face

# URL da API de inferência do Hugging Face para um modelo de sumarização
# Modelo escolhido: sshleifer/distilbart-cnn-12-6 (alternativa ao bart-large-cnn)
HF_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

def configure_huggingface():
    """Configura a API do Hugging Face usando o token das variáveis de ambiente."""
    api_key = os.getenv(IA_API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"O token da API {IA_API_KEY_ENV_VAR} não foi encontrado nas variáveis de ambiente.")

    # --- LINHA DE DEBUG TEMPORÁRIA ---
    print(f"DEBUG: Token de API lido por os.getenv('{IA_API_KEY_ENV_VAR}'): {api_key[:5]}*****")
    # ---------------------------------

    headers = {"Authorization": f"Bearer {api_key}"}
    return headers, api_key # Retorna os headers e a chave para verificação

def analyze_licitacao_with_ia(licitacao_data: dict) -> dict:
    """
    Envia os dados de uma licitação para a IA do Hugging Face para análise e retorna um dicionário com os resultados.
    O Projeto Hermes utiliza esta função para extrair insights.
    """
    headers, api_key = configure_huggingface()
    print(f"Token de API Hugging Face configurado (primeiros 5 caracteres): {api_key[:5]}*****")
    print(f"Usando modelo Hugging Face via API de inferência: {HF_API_URL.split('/')[-1]}")

    # Conteúdo para ser enviado ao modelo.
    # Para um modelo de sumarização, enviamos o objeto da licitação.
    # Para uma análise mais complexa, poderíamos concatenar mais campos.
    input_text = f"""
    Analise a seguinte licitação e forneça um resumo conciso, a relevância para empresas em geral,
    riscos potenciais e uma recomendação clara: "Participar", "Não participar" ou "Analisar com cuidado".
    Formate a saída como um objeto JSON com as chaves: "resumo", "relevancia", "riscos", "recomendacao".

    Dados da Licitação:
    Objeto: {licitacao_data.get('objeto', 'Não informado')}
    Valor Estimado: {licitacao_data.get('valor_estimado', 'Não informado')}
    Modalidade: {licitacao_data.get('modalidade', 'Não informado')}
    Órgão: {licitacao_data.get('orgao', 'Não informado')}
    Estado: {licitacao_data.get('estado', 'Não informado')}
    Data Abertura: {licitacao_data.get('data_abertura', 'Não informado')}
    Link: {licitacao_data.get('link', 'Não informado')}
    """

    # A API de inferência do Hugging Face espera um dicionário com a chave "inputs"
    payload = {"inputs": input_text}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)

        ia_response = response.json()

        # A resposta de um modelo de sumarização pode vir como uma lista de dicionários
        # com a chave 'summary_text'. Precisamos adaptar para o formato JSON esperado.
        if isinstance(ia_response, list) and ia_response and 'summary_text' in ia_response[0]:
            summary_text = ia_response[0]['summary_text']

            # Como o modelo BART é para sumarização, ele não vai gerar JSON diretamente.
            # Precisamos fazer uma adaptação ou usar um modelo de LLM mais completo.
            # Por enquanto, vamos colocar o resumo e o resto como padrão.
            # Para um JSON formatado, precisaríamos de um modelo de LLM (como Mistral, Llama)
            # que possa seguir instruções de formatação.

            # Para esta primeira versão, vamos simular a extração do JSON a partir do resumo
            # ou usar um formato padrão.

            # Tentativa de extrair JSON se o modelo tentar formatar
            try:
                # Se o modelo conseguir gerar um JSON, tentamos parsear
                start_json = summary_text.find('{')
                end_json = summary_text.rfind('}')
                if start_json != -1 and end_json != -1:
                    json_part = summary_text[start_json : end_json + 1]
                    ia_analysis = json.loads(json_part)
                    return ia_analysis
                else:
                    # Se não for JSON, usamos um formato padrão com o resumo
                    return {
                        "resumo": summary_text,
                        "relevancia": "A ser analisada (Hugging Face - Sumarização)",
                        "riscos": "A ser analisado (Hugging Face - Sumarização)",
                        "recomendacao": "Analisar com cuidado"
                    }
            except json.JSONDecodeError:
                # Se a tentativa de JSON falhar, usamos o formato padrão
                return {
                    "resumo": summary_text,
                    "relevancia": "A ser analisada (Hugging Face - Sumarização)",
                    "riscos": "A ser analisado (Hugging Face - Sumarização)",
                    "recomendacao": "Analisar com cuidado"
                }
        else:
            # Se a resposta não for o formato esperado, logamos e retornamos padrão
            print(f"Projeto Hermes: Resposta inesperada do Hugging Face: {ia_response}")
            return {
                "resumo": "Erro na análise da IA (Hugging Face - formato inesperado).",
                "relevancia": "Desconhecida",
                "riscos": "Desconhecidos",
                "recomendacao": "Analisar com cuidado"
            }

    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao Hugging Face (modelo: {HF_API_URL.split('/')[-1]}): {e}")
        return {
            "resumo": "Erro na análise da IA (Hugging Face - requisição).",
            "relevancia": "Desconhecida",
            "riscos": "Desconhecidos",
            "recomendacao": "Analisar com cuidado"
        }
    except Exception as e:
        print(f"Erro inesperado ao analisar licitação com IA do Hugging Face (modelo: {HF_API_URL.split('/')[-1]}): {e}")
        return {
            "resumo": "Erro na análise da IA (Hugging Face - geral).",
            "relevancia": "Desconhecida",
            "riscos": "Desconhecidos",
            "recomendacao": "Analisar com cuidado"
        }

# Exemplo de uso (para testes locais)
if __name__ == "__main__":
    print("\n--- Teste do Hugging Face Analyzer ---")
    sample_licitacao = {
        "objeto": "Contratação de serviços de desenvolvimento de software para sistema de gestão de estoque.",
        "valor_estimado": "R$ 150.000,00",
        "modalidade": "Pregão Eletrônico",
        "orgao": "Prefeitura Municipal de Exemplo",
        "estado": "SP",
        "data_abertura": "2026-04-15",
        "link": "https://www.pncp.gov.br/exemplo"
    }

    # Para testar localmente, defina a variável de ambiente HF_API_KEY
    # Ex: os.environ[IA_API_KEY_ENV_VAR] = "hf_SUA_CHAVE_AQUI_PARA_TESTES"

    analysis = analyze_licitacao_with_ia(sample_licitacao)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    print("------------------------------------------\n")