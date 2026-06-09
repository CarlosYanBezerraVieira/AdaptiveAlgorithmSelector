def busca_sequencial(arr, target):
    """Busca linear simples, funciona em arrays desordenados."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1