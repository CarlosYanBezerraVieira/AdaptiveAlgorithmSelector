from utils.contador import ContadorInstrumentacao


def busca_sequencial(arr, alvo, contador: ContadorInstrumentacao):

    for i in range(len(arr)):
        contador.registrar_comparacao()
        if arr[i] == alvo:
            return i

    return -1
