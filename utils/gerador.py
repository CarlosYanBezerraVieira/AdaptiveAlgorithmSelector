import random

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