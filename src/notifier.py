import smtplib
from email.mime.text import MIMEText
import pywhatkit as kit
import time


def enviar_email_alerta(alertas):
    if not alertas:
        return

    corpo = "🚨 OPORTUNIDADES DETECTADAS\n\n"

    for a in alertas:
        corpo += f"""
Objeto: {a['objeto']}
Valor: {a['valor']}
Estado: {a['estado']}
Score: {a['score']}
Delta: {a['delta']}
------------------------
"""

    msg = MIMEText(corpo)
    msg["Subject"] = "🚨 Hermes - Oportunidades detectadas"
    msg["From"] = "israeldasilvajunior@gmail.com"
    msg["To"] = "badwolfsp@hotmail.com"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("israeldasilvajunior@gmail.com", "vjwx qhrd zxjz prva")
            server.send_message(msg)

        print("📧 Email enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")


def enviar_whatsapp_alerta(oportunidades):
    mensagem = "🚨 ALERTA HERMES 🚨\n\n"

    for o in oportunidades:
        mensagem += f"""
📦 {o['objeto']}
💰 R$ {o['valor']}
📍 {o['estado']}
⭐ Score: {o['score']}
📊 Delta: {o['delta']}
-------------------------
"""

    print("📲 Abrindo WhatsApp Web...")

    # envia com delay maior
    kit.sendwhatmsg_instantly(
        phone_no="+5511951411782",
        message=mensagem,
        wait_time=15,   # ⬅️ AUMENTA ISSO
        tab_close=False
    )

    # 🔥 força ENTER depois
    time.sleep(5)
    import pyautogui
    pyautogui.press("enter")

    print("✅ Mensagem enviada!")
