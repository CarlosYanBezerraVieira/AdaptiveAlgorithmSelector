import time
import tracemalloc

def executar_benchmark(algoritmo_func, arr):
    arr_copia = arr[:]
    tracemalloc.start()
    inicio = time.perf_counter()
    
    arr_ordenado = algoritmo_func(arr_copia)
    
    fim = time.perf_counter()
    memoria_atual, pico_memoria = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        "tempo_segundos": fim - inicio,
        "memoria_kb": pico_memoria / 1024,
        "arr_ordenado": arr_ordenado
    }