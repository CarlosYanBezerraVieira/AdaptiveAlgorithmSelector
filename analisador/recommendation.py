from analisador.algorithm_metadata import METADADOS_ORDENACAO

def gerar_relatorio_recomendacao(ranking, caracteristicas):
  
    if not ranking:
        return "Nenhum algoritmo atendeu aos critérios."

    melhor_algoritmo = ranking[0]
    nome_algoritmo = melhor_algoritmo[0]
    pontuacao = melhor_algoritmo[1]["pontos"]
    justificativas = melhor_algoritmo[1]["justificativas"]
    
    metadados = METADADOS_ORDENACAO.get(nome_algoritmo, {})

    relatorio = f"=== RECOMENDAÇÃO DO SISTEMA ===\n"
    relatorio += f"Tamanho do Array Analisado: {caracteristicas.get('tamanho', 0)} elementos\n"
    relatorio += f"\n🏆 O Vencedor: {nome_algoritmo} (Pontuação: {pontuacao}/100)\n"
    relatorio += f"Resumo: {metadados.get('descricao', '')}\n\n"
    
    relatorio += "Por que esta foi a melhor escolha?\n"
    for just in justificativas:
        relatorio += f" - {just}\n"
        
    relatorio += f"\n📊 Complexidade Teórica do {nome_algoritmo}:\n"
    relatorio += f" - Tempo Médio: {metadados.get('tempo_medio', 'N/A')}\n"
    relatorio += f" - Pior Caso: {metadados.get('pior_caso', 'N/A')}\n"
    relatorio += f" - Memória Auxiliar: {metadados.get('espaco', 'N/A')}\n"
    
    return relatorio