# src/pncp_scraper.py
# Módulo para realizar a busca real de licitações no PNCP usando Selenium

import re
import time
import random
import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    ElementClickInterceptedException
)

PNCP_BASE_URL   = "https://www.pncp.gov.br"
PNCP_SEARCH_PATH = "/app/editais"
CHROMEDRIVER_PATH = "./chromedriver.exe"

# Labels possíveis para data de abertura no PNCP
LABELS_DATA_ABERTURA = [
    "Data de Abertura",
    "Abertura da Proposta",
    "Data Abertura",
    "Abertura da Sessão",
    "Data de Abertura da Sessão Pública",
    "Prazo para Recebimento das Propostas",
    "Data Limite para Recebimento"
]


def fetch_licitacoes_from_pncp(
    keywords: list,
    states: list,
    page_limit: int = 1,
    max_total: int = 1000         # NOVO: para encerrar ao atingir o limite
) -> list:
    """
    Busca licitações únicas no PNCP com limite máximo de coleta.
    Encerra automaticamente ao atingir max_total licitações únicas.
    """
    print(
        f"Projeto Hermes: Scraper iniciado | "
        f"Limite: {max_total} licitações únicas"
    )

    all_licitacoes  = []
    links_visitados = set()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )

    service = Service(CHROMEDRIVER_PATH)
    driver  = None

    try:
        driver = webdriver.Chrome(service=service, options=options)
        licitacao_id_counter = 1

        # Flag de encerramento por limite
        limite_atingido = False

        for keyword in keywords:
            if limite_atingido:
                break

            for state in states:
                if limite_atingido:
                    break

                for current_page in range(1, page_limit + 1):
                    if limite_atingido:
                        break

                    search_url = (
                        f"{PNCP_BASE_URL}{PNCP_SEARCH_PATH}"
                        f"?q={keyword}&estado={state}&pagina={current_page}"
                    )

                    print(
                        f"\nProjeto Hermes: [{keyword.upper()}][{state}]"
                        f"[Pág.{current_page}] | "
                        f"Coletadas até agora: {len(all_licitacoes)}/{max_total}"
                    )

                    # Carrega a página de lista
                    try:
                        driver.get(search_url)
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "a.br-item")
                            )
                        )
                    except TimeoutException:
                        print(
                            f"  Timeout ao carregar lista. "
                            f"Pulando [{keyword}][{state}][Pág.{current_page}]"
                        )
                        continue

                    soup      = BeautifulSoup(driver.page_source, 'html.parser')
                    list_items = soup.select("a.br-item")

                    if not list_items:
                        print("  Nenhum card encontrado. Pulando.")
                        continue

                    # Coleta dados básicos dos cards novos (sem duplicatas)
                    novos_cards = []

                    for card in list_items:
                        # Verifica limite antes de cada card
                        if len(all_licitacoes) + len(novos_cards) >= max_total:
                            limite_atingido = True
                            break

                        link = card.get('href')
                        if not link or link.startswith("javascript:"):
                            continue

                        full_link = f"{PNCP_BASE_URL}{link}"
                        if full_link in links_visitados:
                            continue

                        links_visitados.add(full_link)

                        # Extrai dados básicos do card
                        objeto_el = card.find(
                            'span',
                            string=lambda t: t and 'Objeto:' in t
                        )
                        objeto = (
                            objeto_el.get_text(strip=True)
                                     .replace('Objeto:', '').strip()
                            if objeto_el else "Não informado"
                        )

                        modalidade_el = card.find(
                            'strong', string='Modalidade da Contratação: '
                        )
                        modalidade = (
                            modalidade_el.next_sibling.strip()
                            if modalidade_el and modalidade_el.next_sibling
                            else "Não informada"
                        )

                        orgao_el = card.find('strong', string='Órgão:')
                        orgao = (
                            orgao_el.next_sibling.strip()
                            if orgao_el and orgao_el.next_sibling
                            else "Não informado"
                        )

                        atualizacao_el = card.find(
                            'strong', string='Última Atualização:'
                        )
                        ultima_atualizacao = (
                            atualizacao_el.next_sibling.strip()
                            if atualizacao_el and atualizacao_el.next_sibling
                            else "Não informada"
                        )

                        pncp_id_el = card.find(
                            'strong', string='Id contratação PNCP: '
                        )
                        pncp_id = (
                            pncp_id_el.next_sibling.strip()
                            if pncp_id_el and pncp_id_el.next_sibling
                            else "Não informado"
                        )

                        novos_cards.append({
                            "id":                licitacao_id_counter,
                            "objeto":            objeto,
                            "valor_estimado":    "Não encontrado",
                            "modalidade":        modalidade,
                            "orgao":             orgao,
                            "estado":            state,
                            "keyword":           keyword,
                            "ultima_atualizacao": ultima_atualizacao,
                            "data_abertura":     "Não encontrada",
                            "dias_restantes":    "N/A",
                            "link":              full_link,
                            "pncp_id":           pncp_id
                        })
                        licitacao_id_counter += 1

                    print(
                        f"  {len(novos_cards)} licitações novas nesta página "
                        f"(de {len(list_items)} cards)."
                    )

                    if not novos_cards:
                        continue

                    # Navega para detalhes de cada licitação nova
                    for idx, lic in enumerate(novos_cards, 1):
                        print(
                            f"  [{idx}/{len(novos_cards)}] "
                            f"ID {lic['id']} -> {lic['link']}"
                        )

                        try:
                            driver.get(lic['link'])
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located(
                                    (By.TAG_NAME, "body")
                                )
                            )
                            time.sleep(random.uniform(1.0, 2.0))

                            # Extração do Valor Estimado
                            lic['valor_estimado'] = _extrair_valor(driver)

                            # Extração da Data de Abertura
                            data_texto = _extrair_data_abertura(driver)
                            lic['data_abertura'] = data_texto

                            # Cálculo dos Dias Restantes
                            if data_texto != "Não encontrada":
                                match_data = re.search(
                                    r'(\d{2}/\d{2}/\d{4})', data_texto
                                )
                                if match_data:
                                    try:
                                        data_dt = datetime.strptime(
                                            match_data.group(1), '%d/%m/%Y'
                                        )
                                        lic['dias_restantes'] = (
                                            data_dt - datetime.now()
                                        ).days
                                    except ValueError:
                                        lic['dias_restantes'] = "Formato inválido"

                            print(
                                f"     Valor: {lic['valor_estimado']} | "
                                f"Abertura: {lic['data_abertura']} | "
                                f"Dias: {lic['dias_restantes']}"
                            )

                        except TimeoutException:
                            print(f"     Timeout na licitação ID {lic['id']}.")
                        except Exception as e:
                            print(f"     Erro na licitação ID {lic['id']}: {e}")
                        finally:
                            # Retorna à URL da lista (nunca usa driver.back())
                            try:
                                driver.get(search_url)
                                WebDriverWait(driver, 15).until(
                                    EC.presence_of_all_elements_located(
                                        (By.CSS_SELECTOR, "a.br-item")
                                    )
                                )
                                time.sleep(random.uniform(0.5, 1.0))
                            except TimeoutException:
                                print("     Aviso: Timeout ao recarregar lista.")

                    all_licitacoes.extend(novos_cards)
                    print(
                        f"\n  Total acumulado: {len(all_licitacoes)}/{max_total} "
                        f"licitações únicas."
                    )

                    # Verifica limite após processar a página
                    if len(all_licitacoes) >= max_total:
                        limite_atingido = True
                        print(
                            f"\nProjeto Hermes: Limite de {max_total} licitações "
                            f"atingido. Encerrando coleta."
                        )

        return all_licitacoes[:max_total]

    except WebDriverException as e:
        print(f"Projeto Hermes: Erro no WebDriver: {e}")
        return _simulate_licitacoes_if_no_real_data(keywords, states, max_total)
    except Exception as e:
        print(f"Projeto Hermes: Erro inesperado: {e}")
        return _simulate_licitacoes_if_no_real_data(keywords, states, max_total)
    finally:
        if driver:
            print("\nProjeto Hermes: Fechando navegador.")
            driver.quit()


def _extrair_valor(driver) -> str:
    """Tenta extrair o valor estimado da página de detalhes."""
    try:
        el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,
                "//strong[contains(text(),'VALOR TOTAL ESTIMADO DA COMPRA')]"
                "/following-sibling::*"
            ))
        )
        return el.text.strip()
    except TimeoutException:
        pass

    try:
        el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,
                "//span[strong[contains(text(),'Valor Estimado')]]"
                "/following-sibling::span"
            ))
        )
        return el.text.strip()
    except TimeoutException:
        pass

    try:
        body = driver.find_element(By.TAG_NAME, "body").text
        match = re.search(
            r'(?:Valor Total Estimado|Valor Estimado)[:\s]*R?\$?\s*([\d.,]+)',
            body,
            re.IGNORECASE
        )
        if match:
            return f"R$ {match.group(1).strip()}"
    except Exception:
        pass

    return "Não encontrado"


def _extrair_data_abertura(driver) -> str:
    """Tenta extrair a data de abertura da página de detalhes."""
    for label in LABELS_DATA_ABERTURA:
        try:
            el = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH,
                    f"//*[contains(text(),'{label}')]/following::*[1]"
                ))
            )
            candidato = el.text.strip()
            if re.search(r'\d{2}/\d{2}/\d{4}', candidato):
                return candidato
        except TimeoutException:
            continue

    # Fallback: regex no corpo da página
    try:
        body = driver.find_element(By.TAG_NAME, "body").text
        match = re.search(
            r'(?:aber\w*|proposta|recebimento|sess[aã]o)'
            r'[^.:\n]{0,60}(\d{2}/\d{2}/\d{4})',
            body,
            re.IGNORECASE
        )
        if match:
            return match.group(1).strip()
    except Exception:
        pass

    return "Não encontrada"


def _simulate_licitacoes_if_no_real_data(
    keywords: list,
    states: list,
    max_total: int = 1000
) -> list:
    """Gera licitações simuladas como fallback respeitando o limite."""
    print(f"Projeto Hermes: Gerando até {max_total} licitações simuladas.")

    generic_objects = [
        "Aquisição de material de escritório e suprimentos de informática.",
        "Contratação de serviços de limpeza e conservação para prédios públicos.",
        "Execução de obras de reforma e ampliação de escola municipal.",
        "Fornecimento de equipamentos de proteção individual (EPIs).",
        "Prestação de serviços de consultoria em gestão de projetos.",
        "Contratação de empresa para manutenção predial preventiva e corretiva.",
        "Aquisição de veículos tipo sedan para frota oficial.",
        "Fornecimento de alimentação escolar para rede de ensino.",
        "Contratação de serviços de desenvolvimento de sistema web.",
        "Aquisição de hardware e infraestrutura de rede.",
        "Prestação de serviços de segurança e vigilância patrimonial.",
        "Contratação de serviços de TI para suporte técnico.",
        "Desenvolvimento de software para gestão de contratos.",
        "Fornecimento de licenças de software para estações de trabalho.",
        "Implantação de solução de cloud computing para órgão público."
    ]

    simuladas = []
    for i in range(1, max_total + 1):
        dias       = random.randint(3, 60)
        data_dt    = datetime.now() + pd.Timedelta(days=dias)
        estado     = random.choice(states)
        keyword    = random.choice(keywords)

        simuladas.append({
            "id":                i,
            "objeto":            random.choice(generic_objects),
            "valor_estimado": (
                f"R$ {random.randint(10000, 1000000):,.2f}"
                .replace(",", "X").replace(".", ",").replace("X", ".")
            ),
            "modalidade": random.choice([
                "Pregão Eletrônico", "Concorrência",
                "Tomada de Preços", "Dispensa de Licitação"
            ]),
            "orgao":             f"Órgão Público de {estado}",
            "estado":            estado,
            "keyword":           keyword,
            "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y"),
            "data_abertura":     data_dt.strftime("%d/%m/%Y"),
            "dias_restantes":    dias,
            "link":   f"https://www.pncp.gov.br/licitacao/{i}",
            "pncp_id": f"SIMULADO-{random.randint(1000, 9999)}"
        })

    return simuladas


if __name__ == "__main__":
    print("\n--- Teste Rápido do Scraper ---")
    licitacoes = fetch_licitacoes_from_pncp(
        ["software"], ["SP"], page_limit=1, max_total=10
    )
    print(f"\n{len(licitacoes)} licitações retornadas:")
    for lic in licitacoes:
        print(
            f"  ID {lic['id']} | "
            f"Valor: {lic['valor_estimado']} | "
            f"Abertura: {lic['data_abertura']} | "
            f"Dias: {lic['dias_restantes']}"
        )
    print("------------------------------\n")