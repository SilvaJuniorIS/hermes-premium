from src.notifier import enviar_whatsapp_alerta

if __name__ == "__main__":
    alertas = [
        {
            "objeto": "TESTE HERMES",
            "valor": 150000,
            "estado": "SP",
            "score": 6,
            "delta": 0.5
        }
    ]

    enviar_whatsapp_alerta(alertas)