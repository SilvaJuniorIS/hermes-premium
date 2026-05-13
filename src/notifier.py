import os
import smtplib
import time
from email.message import EmailMessage
from email.mime.text import MIMEText

import pywhatkit as kit


def _smtp_config() -> dict[str, str | int]:
    """Credenciais apenas via variáveis de ambiente (ver .env.example). Nunca commitar segredos."""
    return {
        "host": os.getenv("HERMES_SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("HERMES_SMTP_PORT", "465")),
        "user": os.getenv("HERMES_SMTP_USER", ""),
        "password": os.getenv("HERMES_SMTP_PASSWORD", ""),
        "from": os.getenv("HERMES_EMAIL_FROM", os.getenv("HERMES_SMTP_USER", "")),
    }


def _send_email_message(msg: EmailMessage | MIMEText) -> None:
    config = _smtp_config()
    if not str(config["user"]).strip() or not str(config["password"]).strip():
        raise RuntimeError(
            "SMTP nao configurado: defina HERMES_SMTP_USER e HERMES_SMTP_PASSWORD no ambiente."
        )
    with smtplib.SMTP_SSL(str(config["host"]), int(config["port"])) as server:
        server.login(str(config["user"]), str(config["password"]))
        server.send_message(msg)


def enviar_planilha_oportunidades(
    destinatario: str,
    arquivo_bytes: bytes,
    nome_arquivo: str,
    total: int,
    filtros: str,
    destaques: list[dict],
) -> None:
    config = _smtp_config()
    linhas_destaques = []

    for item in destaques[:5]:
        valor = float(item.get("valor_estimado_num") or 0)
        linhas_destaques.append(
            "- "
            f"Score {float(item.get('score') or 0):.0f} | "
            f"{item.get('classificacao') or '-'} | "
            f"{item.get('orgao') or '-'} | "
            f"{item.get('municipio') or '-'} / {item.get('estado') or '-'} | "
            f"Valor estimado: R$ {valor:,.2f}"
        )

    corpo = f"""Ola,

Segue em anexo a planilha de oportunidades gerada pelo HERMES.

HERMES - Inteligencia em Licitacoes Publicas
Proposito: transformar dados publicos em oportunidades estrategicas.

Resumo do envio:
- Total de oportunidades na planilha: {total}
- Filtros usados: {filtros or 'sem filtros adicionais'}

Como ler o score:
- Score alto indica maior aderencia ao perfil comercial configurado.
- O calculo considera termos encontrados no objeto, valor estimado, palavras-chave fortes e sinais de prioridade definidos no perfil.
- A classificacao ALTA deve ser tratada primeiro pelo time comercial.
- A classificacao MEDIA merece validacao rapida.
- A classificacao BAIXA pode ficar em monitoramento.

Destaques da lista:
{chr(10).join(linhas_destaques) if linhas_destaques else '- Nenhum destaque disponivel.'}

Recomendacao:
Abra primeiro as oportunidades com maior score e maior valor estimado, confira o objeto, o orgao, o municipio, a data de abertura e o link da fonte antes de decidir a abordagem comercial.

Atenciosamente,
HERMES
"""

    msg = EmailMessage()
    msg["Subject"] = f"HERMES - {total} oportunidades priorizadas"
    msg["From"] = str(config["from"])
    msg["To"] = destinatario
    msg.set_content(corpo)
    msg.add_attachment(
        arquivo_bytes,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=nome_arquivo,
    )

    _send_email_message(msg)


def enviar_email_alerta(alertas):
    if not alertas:
        return

    corpo = "OPORTUNIDADES DETECTADAS\n\n"

    for a in alertas:
        corpo += f"""
Objeto: {a['objeto']}
Valor: {a['valor']}
Estado: {a['estado']}
Score: {a['score']}
Delta: {a['delta']}
------------------------
"""

    config = _smtp_config()
    msg = MIMEText(corpo)
    msg["Subject"] = "HERMES - Oportunidades detectadas"
    msg["From"] = str(config["from"])
    alert_to = os.getenv("HERMES_ALERT_EMAIL_TO", "").strip()
    if not alert_to:
        print("HERMES_ALERT_EMAIL_TO nao definido; alerta por e-mail ignorado.")
        return
    msg["To"] = alert_to

    try:
        _send_email_message(msg)
        print("Email enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")


def enviar_whatsapp_alerta(oportunidades):
    mensagem = "ALERTA HERMES\n\n"

    for o in oportunidades:
        mensagem += f"""
{o['objeto']}
R$ {o['valor']}
{o['estado']}
Score: {o['score']}
Delta: {o['delta']}
-------------------------
"""

    print("Abrindo WhatsApp Web...")

    phone = os.getenv("HERMES_WHATSAPP_E164", "").strip()
    if not phone:
        print("HERMES_WHATSAPP_E164 nao definido; alerta WhatsApp ignorado.")
        return

    kit.sendwhatmsg_instantly(
        phone_no=phone,
        message=mensagem,
        wait_time=15,
        tab_close=False,
    )

    time.sleep(5)
    import pyautogui

    pyautogui.press("enter")

    print("Mensagem enviada.")
