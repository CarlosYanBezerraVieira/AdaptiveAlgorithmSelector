from utils.contador import ContadorInstrumentacao


def selection_sort(arr, contador: ContadorInstrumentacao):
    arr_copia = arr.copy()
    n = len(arr_copia)

    for i in range(n):
        idx_minimo = i
        for j in range(i + 1, n):
            contador.registrar_comparacao()
            if arr_copia[j] < arr_copia[idx_minimo]:
                idx_minimo = j

        if idx_minimo != i:
            arr_copia[i], arr_copia[idx_minimo] = arr_copia[idx_minimo], arr_copia[i]
            contador.registrar_troca()

    return arr_copia
