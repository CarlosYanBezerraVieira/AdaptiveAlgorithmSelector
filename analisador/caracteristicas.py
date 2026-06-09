import random

def estimar_grau_ordenacao(arr, num_amostras=1000):
    """
    Estima o grau de ordenação do array verificando inversões (A[i] > A[j] com i < j).
    Usa amostragem aleatória para evitar custo O(n^2) em arrays grandes.
    """
    n = len(arr)
    if n < 2:
        return 0.0 # 0% de inversões (totalmente ordenado)
        
    inversoes = 0
    amostras_validas = 0
    
    tentativas = min(num_amostras, n * (n - 1) // 2)
    
    for _ in range(tentativas):
        i = random.randint(0, n - 2)
        j = random.randint(i + 1, n - 1)
        
        if arr[i] > arr[j]:
            inversoes += 1
        amostras_validas += 1
        
    if amostras_validas == 0:
        return 0.0
        
    taxa_inversoes = inversoes / amostras_validas
    return taxa_inversoes

def analisar_array(arr):
    """
    Extrai as métricas do array sem ordená-lo.
    """
    if not arr:
        return {"tamanho": 0, "tipo_dados": None}

    n = len(arr)
    
    # Usando sets para descobrir duplicatas rapidamente
    elementos_unicos = len(set(arr))
    percentual_duplicatas = ((n - elementos_unicos) / n) * 100

    # Amplitude (apenas se forem números)
    try:
        val_min = min(arr)
        val_max = max(arr)
        amplitude = val_max - val_min
    except TypeError:
        amplitude = None # Caso o array contenha strings ou objetos

    taxa_inversoes = estimar_grau_ordenacao(arr)
    quase_ordenado = taxa_inversoes < 0.10 # Consideramos quase ordenado se < 10% de inversões

    return {
        "tamanho": n,
        "percentual_duplicatas": percentual_duplicatas,
        "amplitude": amplitude,
        "tipo_dados": type(arr[0]).__name__,
        "taxa_inversoes": taxa_inversoes,
        "quase_ordenado": quase_ordenado
    }