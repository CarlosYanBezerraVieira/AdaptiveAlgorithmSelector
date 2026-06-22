def quick_sort(arr, contador):
    arr_copia = list(arr)
    _quick_sort_recursivo(arr_copia, 0, len(arr_copia) - 1, contador)
    return arr_copia


def _quick_sort_recursivo(arr, baixo, alto, contador):
    if baixo < alto:
        indice_particao = _particionar(arr, baixo, alto, contador)
        _quick_sort_recursivo(arr, baixo, indice_particao - 1, contador)
        _quick_sort_recursivo(arr, indice_particao + 1, alto, contador)


def _particionar(arr, baixo, alto, contador):
    # Escolha do pivô usando Mediana de Três para evitar estouro de pilha
    meio = (baixo + alto) // 2
    indices = [baixo, meio, alto]

    # Ordena os três índices para achar a mediana ideal
    for i in range(3):
        for j in range(i + 1, 3):
            contador.registrar_comparacao()
            if arr[indices[i]] > arr[indices[j]]:
                arr[indices[i]], arr[indices[j]] = arr[indices[j]], arr[indices[i]]
                contador.registrar_troca()

    # Coloca a mediana (que ficou no meio) no final para servir de pivô
    arr[meio], arr[alto] = arr[alto], arr[meio]
    contador.registrar_troca()

    pivo = arr[alto]
    i = baixo - 1

    for j in range(baixo, alto):
        contador.registrar_comparacao()
        if arr[j] <= pivo:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            contador.registrar_troca()

    arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
    contador.registrar_troca()
    return i + 1
