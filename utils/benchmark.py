import time
import tracemalloc

from algoritmos.ordenacao.bubble_sort import bubble_sort
from algoritmos.ordenacao.heap_sort import heap_sort
from algoritmos.ordenacao.insertion_sort import insertion_sort
from algoritmos.ordenacao.merge_sort import merge_sort
from algoritmos.ordenacao.quick_sort import quick_sort
from algoritmos.ordenacao.selection_sort import selection_sort
from utils.contador import ContadorInstrumentacao


def executar_benchmark(algoritmo_func, arr):
    arr_copia = arr.copy() if hasattr(arr, "copy") else arr[:]
    contador = ContadorInstrumentacao()

    tracemalloc.start()
    inicio = time.perf_counter()

    arr_ordenado = algoritmo_func(arr_copia, contador)

    fim = time.perf_counter()
    memoria_atual, pico_memoria = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    metricas = contador.obter_resultados()

    return {
        "tempo_segundos": fim - inicio,
        "memoria_kb": pico_memoria / 1024,
        "comparacoes": metricas["comparacoes"],
        "trocas": metricas["trocas"],
        "arr_ordenado": arr_ordenado,
    }


def rodar_benchmarks_gerais(array_dados, algoritmo_recomendado):
    print("--- [CAMADA 3: BENCHMARK GERAL DE VALIDAÇÃO] ---")
    algoritmos_ordenacao = {
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort,
    }

    for nome, funcao in algoritmos_ordenacao.items():
        resultados = executar_benchmark(funcao, array_dados)

        sinalizador = " <- [RECOMENDADO]" if nome == algoritmo_recomendado else ""
        print(f"[{nome}]{sinalizador}")
        print(
            f"   Tempo: {resultados['tempo_segundos']:.5f}s | "
            f"Comparações: {resultados['comparacoes']} | "
            f"Trocas: {resultados['trocas']} | "
            f"Pico Memória: {resultados['memoria_kb']:.2f} KB"
        )
        print("." * 40)
    print("\n\n")
