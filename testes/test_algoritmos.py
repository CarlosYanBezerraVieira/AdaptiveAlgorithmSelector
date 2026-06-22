# testes/test_algoritmos.py
from algoritmos.busca.busca import busca_binaria, busca_hash, busca_sequencial
from algoritmos.ordenacao.ordenacao import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


# --- Testes de Ordenação ---
def test_ordenacao():
    array_desordenado = [64, 34, 25, 12, 22, 11, 90]
    array_ordenado = [11, 12, 22, 25, 34, 64, 90]

    # É fundamental passar uma cópia ([:]) porque os algoritmos ordenam in-place
    assert bubble_sort(array_desordenado[:]) == array_ordenado
    assert insertion_sort(array_desordenado[:]) == array_ordenado
    assert selection_sort(array_desordenado[:]) == array_ordenado
    assert merge_sort(array_desordenado[:]) == array_ordenado
    assert quick_sort(array_desordenado[:]) == array_ordenado
    assert heap_sort(array_desordenado[:]) == array_ordenado


# --- Testes de Busca ---
def test_busca():
    array_ordenado = [11, 12, 22, 25, 34, 64, 90]

    # Busca Sequencial
    assert busca_sequencial(array_ordenado, 25) == 3
    assert busca_sequencial(array_ordenado, 99) == -1

    # Busca Binária
    assert busca_binaria(array_ordenado, 90) == 6
    assert busca_binaria(array_ordenado, 10) == -1

    # Busca baseada em Hash
    assert busca_hash(array_ordenado, 11) == 0
    assert busca_hash(array_ordenado, 100) == -1


# --- Testes de Casos Limites ---
def test_casos_limites():
    array_vazio = []
    array_unico = [42]

    # Ordenação
    assert quick_sort(array_vazio[:]) == []
    assert merge_sort(array_unico[:]) == [42]

    # Busca
    assert busca_binaria(array_vazio, 10) == -1
    assert busca_sequencial(array_unico, 42) == 0
