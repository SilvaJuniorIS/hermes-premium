# src/ia_analyzer.py
# Módulo de Análise de IA para o Projeto Hermes (com integração OpenAI)

import os
import json
from openai import OpenAI # Importa a classe OpenAI da biblioteca
from src.config import IA_API_KEY_ENV_VAR # Agora esta variável será para a chave da OpenAI

# A variável de ambiente para a chave da OpenAI será OPENAI_API_KEY
# Certifique-se de que IA_API_KEY_ENV_VAR em src/config.py esteja definida como "OPENAI_API_KEY"

def configure_openai():
    """Configura a API da OpenAI usando a chave de API das variáveis de ambiente."""
    api_key = os.getenv(IA_API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"A chave da API {IA_API_KEY_ENV_VAR} não foi encontrada nas variáveis de ambiente.")

    # --- LINHA DE DEBUG TEMPORÁRIA ---
    print(f"DEBUG: Chave de API lida por os.getenv('{IA_API_KEY_ENV_VAR}'): {api_key}")
    # ---------------------------------

    # A biblioteca OpenAI automaticamente pega a chave da variável de ambiente OPENAI_API_KEY
    # se ela estiver definida. Podemos instanciar o cliente diretamente.
    client = OpenAI(api_key=api_key)
    return client, api_key # Retorna o cliente e a chave para verificação

def analyze_licitacao_with_ia(licitacao_data: dict) -> dict:
    """
    Envia os dados de uma licitação para a IA da OpenAI para análise e retorna um dicionário com os resultados.
    O Projeto Hermes utiliza esta função para extrair insights.
    """
    client, api_key = configure_openai() # Configura o cliente OpenAI e pega a chave
    print(f"Chave de API OpenAI configurada (primeiros 5 caracteres): {api_key[:5]}*****")

    # Usaremos um modelo GPT-3.5 Turbo, que é eficiente e bom para esta tarefa.
    # Você pode experimentar com 'gpt-4' se tiver acesso e quiser resultados ainda mais avançados.
    model_name = "gpt-4o" 
    print(f"Usando modelo OpenAI: {model_name}")

    prompt_content = f"""
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

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "Você é um analista de licitações experiente e imparcial, especializado em identificar oportunidades e riscos para empresas."},
                {"role": "user", "content": prompt_content}
            ],
            response_format={"type": "json_object"} # Solicita a resposta em formato JSON
        )

        # A resposta da OpenAI vem no formato de objeto, precisamos extrair o conteúdo
        ia_analysis_text = response.choices[0].message.content
        ia_analysis = json.loads(ia_analysis_text)
        return ia_analysis
    except Exception as e:
        print(f"Erro ao analisar licitação com IA da OpenAI (modelo: {model_name}): {e}")
        return {
            "resumo": "Erro na análise da IA.",
            "relevancia": "Desconhecida",
            "riscos": "Desconhecidos",
            "recomendacao": "Analisar com cuidado"
        }

# Exemplo de uso (para testes locais)
if __name__ == "__main__":
    # Para testar localmente, defina a variável de ambiente OPENAI_API_KEY
    # Ex: os.environ[IA_API_KEY_ENV_VAR] = "SUA_CHAVE_AQUI_PARA_TESTES"

    # A função list_available_models não é aplicável diretamente para OpenAI da mesma forma que Gemini
    # Mas podemos simular uma verificação ou apenas informar o modelo usado.
    print("\n--- Verificação de Configuração OpenAI ---")
    try:
        client, _ = configure_openai()
        # Uma forma simples de verificar se a API está acessível é tentar listar modelos,
        # mas a API de chat da OpenAI não tem um método 'list_models' direto para isso.
        # A simples instanciação do cliente já é um bom sinal.
        # Nota: O método client.models.list() pode ser custoso ou não ser o ideal para uma simples verificação.
        # Apenas configurar o cliente já é um bom teste.
        print(f"Cliente OpenAI configurado com sucesso para o modelo {OpenAI().models.list().data[0].id if OpenAI().models.list().data else 'N/A'}")
    except Exception as e:
        print(f"Erro na configuração ou acesso inicial à OpenAI: {e}")
    print("------------------------------------------\n")

    sample_licitacao = {
        "objeto": "Contratação de serviços de desenvolvimento de software para sistema de gestão de estoque.",
        "valor_estimado": "R$ 150.000,00",
        "modalidade": "Pregão Eletrônico",
        "orgao": "Prefeitura Municipal de Exemplo",
        "estado": "SP",
        "data_abertura": "2026-04-15",
        "link": "https://www.pncp.gov.br/exemplo"
    }

    print("Analisando licitação de exemplo com IA da OpenAI do Projeto Hermes...")
    analysis = analyze_licitacao_with_ia(sample_licitacao)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))