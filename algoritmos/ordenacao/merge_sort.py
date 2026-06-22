from utils.contador import ContadorInstrumentacao


def merge_sort(arr, contador: ContadorInstrumentacao):
    arr_copia = arr.copy()
    _merge_sort_recursivo(arr_copia, contador)
    return arr_copia


def _merge_sort_recursivo(arr, contador: ContadorInstrumentacao):
    if len(arr) > 1:
        meio = len(arr) // 2
        esquerda = arr[:meio]
        direita = arr[meio:]

        _merge_sort_recursivo(esquerda, contador)
        _merge_sort_recursivo(direita, contador)

        i = j = k = 0

        while i < len(esquerda) and j < len(direita):
            contador.registrar_comparacao()
            if esquerda[i] <= direita[j]:
                arr[k] = esquerda[i]
                i += 1
            else:
                arr[k] = direita[j]
                j += 1
            contador.registrar_troca()
            k += 1

        while i < len(esquerda):
            arr[k] = esquerda[i]
            i += 1
            k += 1
            contador.registrar_troca()

        while j < len(direita):
            arr[k] = direita[j]
            j += 1
            k += 1
            contador.registrar_troca()
