def gerar_relatorio_recomendacao(decisao):
    relatorio = "--- [CAMADA 2: DECISÃO DA INTELIGÊNCIA] ---\n"
    relatorio += f"Algoritmo recomendado: {decisao['recomendado']}\n"
    relatorio += f"Pontuação: {decisao['pontuacao']}/100\n"
    relatorio += f"Confiança da Recomendação: {decisao.get('confianca', 'N/A')}\n"
    relatorio += f"Complexidade esperada: {decisao.get('complexidade', 'N/A')}\n"
    relatorio += f"Memória: {decisao.get('memoria', 'N/A')} | Estável: {decisao.get('estabilidade', 'N/A')}\n"

    relatorio += "Justificativas:\n"
    for just in decisao.get("justificativas", []):
        relatorio += f"   • {just}\n"

    if decisao.get("avisos"):
        relatorio += "Avisos:\n"
        for aviso in decisao["avisos"]:
            relatorio += f"   • {aviso}\n"

    if decisao.get("alternativas"):
        relatorio += "Alternativas:\n"
        for alt in decisao["alternativas"]:
            relatorio += f"   • {alt}\n"

    return relatorio
