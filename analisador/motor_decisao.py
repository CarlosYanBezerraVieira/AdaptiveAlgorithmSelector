def selecionar_melhor_algoritmo(propriedades):
    tamanho = propriedades.get("tamanho", 0)
    grau_ordenacao = propriedades.get("grau_ordenacao", 0.0)
    percentual_duplicatas = propriedades.get("percentual_duplicatas", 0.0)
    restricao_memoria = propriedades.get("restricao_memoria", False)
    precisa_estabilidade = properties_estabilidade = propriedades.get("precisa_estabilidade", False)
    objetivo = propriedades.get("objetivo", "ordenar")

    # =================================================================
    # FLUXO DE DECISÃO: BUSCA
    # =================================================================
    if objetivo == "buscar":
        # Base de pontuação inicial para algoritmos de busca
        pontuacao = {"Busca Sequencial": 50, "Busca Binária": 40, "Busca Hash": 60}
        
        # RESTRIÇÃO RÍGIDA: Busca Binária EXIGE ordenação absoluta (grau deve ser estritamente 0.0)
        if grau_ordenacao > 0.0:
            pontuacao["Busca Binária"] = -1000  # Banida por violação de pré-requisito matemático
        else:
            pontuacao["Busca Binária"] += 50    # Altamente recomendada se o vetor estiver ordenado
            
        # Restrição de Memória afeta a Busca Hash (tabelas hash exigem overhead de espaço)
        if restricao_memoria:
            pontuacao["Busca Hash"] -= 40
            
        # Vetores muito pequenos dispensam estruturas complexas ou ordenação prévia
        if tamanho < 30:
            pontuacao["Busca Sequencial"] += 40
            if pontuacao["Busca Hash"] > -100:
                pontuacao["Busca Hash"] -= 20
            
        # Determinação do vencedor e filtragem de alternativas válidas (não banidas)
        melhor = max(pontuacao, key=pontuacao.get)
        alternativas = [alg for alg in pontuacao if alg != melhor and pontuacao[alg] > -500]
        alternativas = sorted(alternativas, key=lambda x: pontuacao[x], reverse=True)[:2]
        
        complexidades = {"Busca Sequencial": "O(n)", "Busca Binária": "O(log n)", "Busca Hash": "O(1)"}
        
        # Geração de Justificativas Dinâmicas e Coerentes baseadas em Metadados
        justificativas = []
        avisos = []
        
        if melhor == "Busca Hash":
            justificativas.append("Permite indexação direta com tempo de busca constante O(1).")
            justificativas.append("Ideal para máxima eficiência computacional quando há memória disponível.")
            if restricao_memoria:
                avisos.append("Aviso: A tabela hash consome memória extra para o mapeamento de chaves.")
                
        elif melhor == "Busca Binária":
            justificativas.append(f"O vetor está perfeitamente ordenado (Grau de inversão: {grau_ordenacao}).")
            justificativas.append("Reduz o espaço de busca de forma logarítmica a cada iteração.")
            
        elif melhor == "Busca Sequencial":
            if grau_ordenacao > 0.0:
                justificativas.append(f"O vetor está desordenado (Grau de inversão: {grau_ordenacao}), tornando a busca binária inviável.")
            else:
                justificativas.append(f"O volume de dados é muito reduzido para justificar estruturas complexas ({tamanho} elementos).")
            justificativas.append("Evita o overhead de processamento com tabelas hash ou ordenações prévias.")

        return {
            "recomendado": melhor, 
            "pontuacao": min(100, max(0, pontuacao[melhor])),
            "complexidade": complexidades[melhor], 
            "justificativas": justificativas,
            "avisos": avisos, 
            "alternativas": alternativas
        }

    # =================================================================
    # FLUXO DE DECISÃO: ORDENAÇÃO
    # =================================================================
    else:
        # 1. Base de pontuação inicial equilibrada
        pontuacao = {
            "Insertion Sort": 30, "Selection Sort": 25, "Bubble Sort": 20,
            "Merge Sort": 50, "Quick Sort": 55, "Heap Sort": 45
        }
        
        # 2. RESTRIÇÕES RÍGIDAS (HARD CONSTRAINTS) - BANIMENTOS ABSOLUTOS
        
        # Se exige ESTABILIDADE, bane algoritmos inerentemente instáveis
        if precisa_estabilidade:
            pontuacao["Quick Sort"] = -1000
            pontuacao["Heap Sort"] = -1000
            pontuacao["Selection Sort"] = -1000
            
            pontuacao["Merge Sort"] += 40
            pontuacao["Insertion Sort"] += 10

        # Se há RESTRIÇÃO DE MEMÓRIA, bane o Merge Sort (alocação auxiliar O(n))
        if restricao_memoria:
            pontuacao["Merge Sort"] = -1000
            
            # Valoriza alternativas estáveis em espaço (In-place)
            if pontuacao["Heap Sort"] > -100:
                pontuacao["Heap Sort"] += 30
            if pontuacao["Quick Sort"] > -100 and grau_ordenacao < 0.70:
                pontuacao["Quick Sort"] += 15

        # Penalização progressiva por tamanho (Evita algoritmos O(n²) em vetores grandes)
        if tamanho > 500:
            if pontuacao["Selection Sort"] > -100: pontuacao["Selection Sort"] -= 50
            if pontuacao["Bubble Sort"] > -100:    pontuacao["Bubble Sort"] -= 50
            
            # Insertion Sort só sobrevive em arrays grandes se estiver quase ordenado
            if pontuacao["Insertion Sort"] > -100 and grau_ordenacao > 0.12:
                pontuacao["Insertion Sort"] -= 50

        # 3. ANÁLISE DE CENÁRIOS CONTEXTUAIS (DESEMPENHO PRÁTICO)
        
        # CENÁRIO A: Vetor Quase Ordenado
        if grau_ordenacao <= 0.10 and tamanho <= 2000:
            if pontuacao["Insertion Sort"] > -100:
                pontuacao["Insertion Sort"] += 100
            if pontuacao["Quick Sort"] > -100:   pontuacao["Quick Sort"] -= 20
            if pontuacao["Heap Sort"] > -100:    pontuacao["Heap Sort"] -= 20

        # CENÁRIO B: Vetor Altamente Invertido (Pior caso do Quick Sort clássico)
        elif grau_ordenacao >= 0.85:
            if pontuacao["Heap Sort"] > -100:    pontuacao["Heap Sort"] += 25
            if pontuacao["Merge Sort"] > -100:   pontuacao["Merge Sort"] += 15
            if pontuacao["Quick Sort"] > -100:   pontuacao["Quick Sort"] -= 25

        # 4. FILTRAGEM SEGURA DE ALTERNATIVAS
        melhor = max(pontuacao, key=pontuacao.get)
        
        # Bloqueia qualquer possibilidade de algoritmos banidos (-1000) entrarem na lista
        alternativas = [alg for alg in pontuacao if alg != melhor and pontuacao[alg] > -500]
        alternativas = sorted(alternativas, key=lambda x: pontuacao[x], reverse=True)[:2]
        
        complexidades = {
            "Insertion Sort": "O(n) no melhor caso / O(n²) no pior", 
            "Selection Sort": "O(n²)", 
            "Bubble Sort": "O(n²)",
            "Merge Sort": "O(n log n) garantido", 
            "Quick Sort": "O(n log n) médio", 
            "Heap Sort": "O(n log n) garantido"
        }
        
        # 5. GERAÇÃO DE JUSTIFICATIVAS CONTEXTUAIS
        justificativas = []
        if melhor == "Quick Sort":
            justificativas.append(f"O vetor está misturado de forma homogênea (Grau de inversão: {grau_ordenacao}).")
            justificativas.append("O cenário não impõe limites de memória ou necessidade de estabilidade.")
            justificativas.append("Estatisticamente, apresenta a menor constante de tempo de execução prática.")
            
        elif melhor == "Heap Sort":
            justificativas.append(f"O array exibe alto índice de inversão estrutural (Grau de inversão: {grau_ordenacao}).")
            justificativas.append("Há restrições severas de memória em tempo de execução.")
            justificativas.append("Garante o teto logarítmico O(n log n) trabalhando de forma In-place (Espaço O(1)).")
            
        elif melhor == "Insertion Sort":
            justificativas.append(f"Detectada pré-ordenação quase completa dos elementos (Grau de inversão: {grau_ordenacao}).")
            justificativas.append("Sob esta condição, o algoritmo opera de forma linear, aproximando-se de O(n).")
            justificativas.append("Reduz drasticamente os ciclos de CPU ao mitigar trocas e deslocamentos de ponteiros.")
            
        elif melhor == "Merge Sort":
            justificativas.append("A estabilidade da ordenação foi definida como requisito crítico de negócio.")
            justificativas.append("Assegura que registros com chaves equivalentes mantenham suas posições relativas originais.")
            justificativas.append("Mantém o comportamento assintótico previsível de O(n log n) sob qualquer distribuição.")

        # Tratamento de Avisos do Sistema
        avisos = []
        if melhor == "Merge Sort":
            avisos.append("Este algoritmo aloca memória adicional proporcional ao tamanho do array original.")
        if melhor == "Quick Sort" and grau_ordenacao >= 0.7:
            avisos.append("Aviso: Alto grau de inversão detectado. Risco latente de degradação caso ocorra má distribuição do pivô.")

        return {
            "recomendado": melhor,
            "pontuacao": min(100, max(0, pontuacao[melhor])),
            "complexidade": complexidades[melhor], 
            "justificativas": justificativas,
            "avisos": avisos, 
            "alternativas": alternativas
        }