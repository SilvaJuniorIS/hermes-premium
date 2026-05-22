import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================================================================
# CONFIGURAÇÕES DE E-MAIL - PREENCHA AQUI!
# ==============================================================================

# Servidor SMTP e Porta
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Credenciais de Login
SMTP_USERNAME = "israeldasilvajunior@gmail.com"
SMTP_PASSWORD = "vjwx qhrd zxjz prva" # Senha de aplicativo

# Remetente e Destinatários
EMAIL_FROM = "israeldasilvajunior@gmail.com"
EMAIL_TO = [
    "badwolfsp@hotmail.com",
    # "destinatario2@empresa.com.br", # Mantenha esta linha comentada ou remova se não for usar
]

# ==============================================================================
# FUNÇÃO DE ENVIO DE E-MAIL (NÃO ALTERAR ABAIXO DESTA LINHA, A MENOS QUE SAIBA O QUE ESTÁ FAZENDO)
# ==============================================================================

def send_email(subject, body, attachment_path=None):
    """
    Envia um e-mail com um anexo opcional.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = ", ".join(EMAIL_TO)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html')) # Usando HTML para o corpo do e-mail

        if attachment_path and os.path.exists(attachment_path):
            part = MIMEBase('application', 'octet-stream')
            with open(attachment_path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
            msg.attach(part)
            logging.info(f"Anexo '{os.path.basename(attachment_path)}' adicionado ao e-mail.")
        else:
            logging.warning(f"Nenhum anexo válido encontrado em '{attachment_path}'. E-mail será enviado sem anexo.")

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Habilita segurança TLS
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()
        logging.info(f"E-mail enviado com sucesso para {', '.join(EMAIL_TO)}.")
        return True
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")
        return False

if __name__ == "__main__":
    # Este bloco é para testes manuais do script send_report.py
    # Ele NÃO é executado quando o main.py chama send_email
    logging.info("Executando send_report.py diretamente para teste.")
    test_subject = "Teste de Envio de E-mail do Projeto Hermes"
    test_body = """
    <html>
    <body>
        <p>Olá,</p>
        <p>Este é um e-mail de teste enviado pelo script <b>send_report.py</b> do Projeto Hermes.</p>
        <p>Se você recebeu este e-mail, a configuração está funcionando!</p>
        <p>Atenciosamente,<br>Projeto Hermes</p>
    </body>
    </html>
    """
    # Para testar com anexo, coloque um caminho válido para um arquivo existente
    # test_attachment = "C:\\caminho\\para\\seu\\arquivo.xlsx"
    test_attachment = None # Altere para o caminho do seu anexo de teste, se houver

    if send_email(test_subject, test_body, test_attachment):
        logging.info("Teste de e-mail concluído com sucesso.")
    else:
        logging.error("Teste de e-mail falhou.")
