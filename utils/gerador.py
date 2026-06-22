import random

def gerar_aleatorio(tamanho, min_val=0, max_val=100000):
    """Gera um array completamente aleatório."""
    return [random.randint(min_val, max_val) for _ in range(tamanho)]

def gerar_quase_ordenado(tamanho, percentual_desordenado=0.05):
    """Gera um array inicialmente ordenado e bagunça uma pequena porcentagem de elementos."""
    arr = list(range(tamanho))
    # Calcula quantos elementos vai bagunçar (ex: 5%)
    trocas = int(tamanho * percentual_desordenado)
    for _ in range(trocas):
        idx1 = random.randint(0, tamanho - 1)
        idx2 = random.randint(0, tamanho - 1)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr

def gerar_invertido(tamanho):
    """Gera un array perfeitamente ordenado de forma decrescente."""
    return list(range(tamanho, 0, -1))

def gerar_com_duplicatas(tamanho, n_valores_unicos=10):
    """Gera um array onde os números se repetem exaustivamente."""
    valores_possiveis = [random.randint(0, 10000) for _ in range(n_valores_unicos)]
    return [random.choice(valores_possiveis) for _ in range(tamanho)]

def gerar_cenarios(tamanhos=[1000, 10000, 50000]):
    cenarios = []
    for n in tamanhos:
        cenarios.append({"nome": f"Aleatorio_n{n}", "dados": [random.randint(0, n) for _ in range(n)]})
        cenarios.append({"nome": f"Invertido_n{n}", "dados": list(range(n, 0, -1))})
        
        arr_quase = list(range(n))
        for _ in range(n // 20):
            i, j = random.randint(0, n-1), random.randint(0, n-1)
            arr_quase[i], arr_quase[j] = arr_quase[j], arr_quase[i]
        cenarios.append({"nome": f"Quase_Ordenado_n{n}", "dados": arr_quase})
        
        cenarios.append({"nome": f"Muitas_Duplicatas_n{n}", "dados": [random.randint(1, 10) for _ in range(n)]})
    return cenarios
