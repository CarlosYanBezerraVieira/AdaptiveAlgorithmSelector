from utils.contador import ContadorInstrumentacao


def insertion_sort(arr, contador: ContadorInstrumentacao):
    """
    Implementação do Insertion Sort integrada com o instrumentador do projeto.
    """
    # Fazemos uma cópia para não alterar o array original do benchmark
    arr_copia = arr.copy()

    for i in range(1, len(arr_copia)):
        chave = arr_copia[i]
        j = i - 1

        # Cada entrada no loop realiza uma comparação
        contador.registrar_comparacao()
        while j >= 0 and arr_copia[j] > chave:
            arr_copia[j + 1] = arr_copia[j]
            contador.registrar_troca()  # Houve um deslocamento/troca de posição
            j -= 1
            if j >= 0:
                contador.registrar_comparacao()

        arr_copia[j + 1] = chave

    return arr_copia
