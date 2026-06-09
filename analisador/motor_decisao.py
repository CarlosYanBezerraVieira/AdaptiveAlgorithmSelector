# analisador/motor_decisao.py

def avaliar_algoritmos_ordenacao(caracteristicas, exige_estabilidade=False, restricao_memoria=False):
    """
    Atribui pontuações aos algoritmos com base nas características detectadas.
    Retorna uma lista ordenada do melhor para o pior.
    """
    tamanho = caracteristicas.get("tamanho", 0)
    quase_ordenado = caracteristicas.get("quase_ordenado", False)
    
    # Pontuação base (todos começam com 100)
    algoritmos = {
        "Merge Sort": {"pontos": 100, "justificativas": [], "avisos": []},
        "Quick Sort": {"pontos": 100, "justificativas": [], "avisos": []},
        "Heap Sort": {"pontos": 100, "justificativas": [], "avisos": []},
        "Insertion Sort": {"pontos": 100, "justificativas": [], "avisos": []},
        "Selection Sort": {"pontos": 100, "justificativas": [], "avisos": []},
        "Bubble Sort": {"pontos": 100, "justificativas": [], "avisos": []}
    }

    # 1. Regra de Eliminação: Datasets muito grandes (n > 10^5) eliminam O(n^2)
    if tamanho > 100000:
        for alg in ["Bubble Sort", "Insertion Sort", "Selection Sort"]:
            algoritmos[alg]["pontos"] = 0
            algoritmos[alg]["avisos"].append(f"Eliminado: Inviável para datasets grandes (n > 10^5).")
        
        algoritmos["Merge Sort"]["justificativas"].append("Excelente para grandes volumes.")
        algoritmos["Quick Sort"]["justificativas"].append("Altamente eficiente para grandes volumes.")

    # 2. Regra de Bônus: Array quase ordenado
    if quase_ordenado and tamanho <= 100000:
        algoritmos["Insertion Sort"]["pontos"] += 35
        algoritmos["Insertion Sort"]["justificativas"].append("Bônus (+35): O array está quase ordenado, tornando a execução próxima a O(n).")

    # 3. Regra de Penalidade: Necessidade de Estabilidade
    if exige_estabilidade:
        for alg in ["Quick Sort", "Heap Sort", "Selection Sort"]:
            algoritmos[alg]["pontos"] -= 50
            algoritmos[alg]["avisos"].append("Penalidade (-50): O algoritmo não garante estabilidade.")
        
        algoritmos["Merge Sort"]["justificativas"].append("Garante a estabilidade exigida.")
        algoritmos["Insertion Sort"]["justificativas"].append("Garante a estabilidade exigida.")
        algoritmos["Bubble Sort"]["justificativas"].append("Garante a estabilidade exigida.")

    # 4. Regra de Restrição de Memória
    if restricao_memoria:
        algoritmos["Merge Sort"]["pontos"] -= 30
        algoritmos["Merge Sort"]["avisos"].append("Penalidade (-30): Consome memória auxiliar O(n).")
        
        algoritmos["Heap Sort"]["justificativas"].append("Excelente para restrição de memória (In-place O(1)).")
        
    # Tratamento final para evitar pontuações negativas ou acima de 100
    for alg, dados in algoritmos.items():
        if dados["pontos"] < 0:
            dados["pontos"] = 0
        if dados["pontos"] > 100:
            dados["pontos"] = 100

    # Ordena o dicionário com base na pontuação (do maior para o menor)
    ranking = sorted(algoritmos.items(), key=lambda item: item[1]["pontos"], reverse=True)
    
    return ranking