from utils.contador import ContadorInstrumentacao

def heap_sort(arr, contador: ContadorInstrumentacao):
    arr_copia = arr.copy()
    n = len(arr_copia)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr_copia, n, i, contador)
    for i in range(n - 1, 0, -1):
        arr_copia[0], arr_copia[i] = arr_copia[i], arr_copia[0]
        contador.registrar_troca()
        _heapify(arr_copia, i, 0, contador)
    return arr_copia

def _heapify(arr, n, i, contador: ContadorInstrumentacao):
    maior = i
    esquerda = 2 * i + 1
    direita = 2 * i + 2
    if esquerda < n:
        contador.registrar_comparacao()
        if arr[esquerda] > arr[maior]:
            maior = esquerda
    if direita < n:
        contador.registrar_comparacao()
        if arr[direita] > arr[maior]:
            maior = direita
    if maior != i:
        arr[i], arr[maior] = arr[maior], arr[i]
        contador.registrar_troca()
        _heapify(arr, n, maior, contador)