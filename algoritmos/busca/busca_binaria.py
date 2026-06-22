from utils.contador import ContadorInstrumentacao


def busca_binaria(arr_ordenado, alvo, contador: ContadorInstrumentacao):

    baixo = 0
    alto = len(arr_ordenado) - 1

    while baixo <= alto:
        meio = (baixo + alto) // 2

        contador.registrar_comparacao()
        if arr_ordenado[meio] == alvo:
            return meio
        elif arr_ordenado[meio] < alvo:
            baixo = meio + 1
        else:
            alto = meio - 1

    return -1
