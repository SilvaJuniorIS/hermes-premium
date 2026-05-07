def calcular_score(lic, referencia):
    score = 0
    motivos = []

    valor = lic.get("valor_estimado_num") or 0
    media = referencia.get("media")

    if media:
        if valor > media:
            score += 30
            motivos.append("Acima da média")
        else:
            score -= 10
            motivos.append("Abaixo da média")

    if lic.get("keyword"):
        score += 20
        motivos.append("Keyword relevante")

    if lic.get("orgao"):
        score += 10
        motivos.append("Órgão identificado")

    score = max(0, min(100, score))

    return {
        "score": score,
        "classificacao": (
            "ALTA" if score >= 70 else
            "MEDIA" if score >= 40 else
            "BAIXA"
        ),
        "motivos": ", ".join(motivos)
    }