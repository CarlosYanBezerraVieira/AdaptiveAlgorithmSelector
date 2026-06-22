import random


def analisar_propriedades_array(
    arr, objetivo="ordenar", restricao_memoria=False, precisa_estabilidade=False
):
    if not arr:
        return {}

    tamanho = len(arr)
    min_val = min(arr)
    max_val = max(arr)
    amplitude = max_val - min_val
    tipo_dados = type(arr[0]).__name__

    elementos_unicos = len(set(arr))
    percentual_duplicatas = ((tamanho - elementos_unicos) / tamanho) * 100

    inversoes_detectadas = 0
    tamanho_amostra = min(1000, tamanho)

    for _ in range(tamanho_amostra):
        idx1 = random.randint(0, tamanho - 2)
        idx2 = random.randint(idx1 + 1, tamanho - 1)
        if arr[idx1] > arr[idx2]:
            inversoes_detectadas += 1

    grau_ordenacao = inversoes_detectadas / tamanho_amostra

    return {
        "tamanho": tamanho,
        "grau_ordenacao": round(grau_ordenacao, 4),
        "percentual_duplicatas": round(percentual_duplicatas, 2),
        "amplitude": amplitude,
        "tipo_dados": tipo_dados,
        "restricao_memoria": restricao_memoria,
        "precisa_estabilidade": precisa_estabilidade,
        "objetivo": objetivo,
    }
