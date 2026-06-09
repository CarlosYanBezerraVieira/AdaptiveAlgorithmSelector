def heap_sort(arr):
    def heapify(items, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and items[l] > items[largest]:
            largest = l
        if r < n and items[r] > items[largest]:
            largest = r
        if largest != i:
            items[i], items[largest] = items[largest], items[i]
            heapify(items, n, largest)

    n = len(arr)
    # Constrói o heap máximo
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    # Extrai os elementos um a um
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)
    return arr