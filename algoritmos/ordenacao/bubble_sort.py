from utils.contador import ContadorInstrumentacao


def bubble_sort(arr, contador: ContadorInstrumentacao):
    arr_copia = arr.copy()
    n = len(arr_copia)

    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            contador.registrar_comparacao()
            if arr_copia[j] > arr_copia[j + 1]:
                arr_copia[j], arr_copia[j + 1] = arr_copia[j + 1], arr_copia[j]
                contador.registrar_troca()
                trocou = True
        if not trocou:
            break

    return arr_copia
