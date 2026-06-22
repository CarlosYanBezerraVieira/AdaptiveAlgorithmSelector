METADADOS_ORDENACAO = {
    "Merge Sort": {
        "tempo_medio": "O(n log n)",
        "pior_caso": "O(n log n)",
        "espaco": "O(n)",
        "estavel": True,
        "descricao": "Algoritmo de divisão e conquista. Excelente garantia de tempo, mas consome memória extra."
    },
    "Quick Sort": {
        "tempo_medio": "O(n log n)",
        "pior_caso": "O(n^2)",
        "espaco": "O(log n)",
        "estavel": False,
        "descricao": "Geralmente o mais rápido na prática para grandes volumes na memória RAM."
    },
    "Heap Sort": {
        "tempo_medio": "O(n log n)",
        "pior_caso": "O(n log n)",
        "espaco": "O(1)",
        "estavel": False,
        "descricao": "Ótimo tempo garantido e não consome memória extra. Excelente para sistemas embarcados."
    },
    "Insertion Sort": {
        "tempo_medio": "O(n^2)",
        "pior_caso": "O(n^2)",
        "espaco": "O(1)",
        "estavel": True,
        "descricao": "Muito eficiente para arrays pequenos ou quase ordenados."
    },
    "Selection Sort": {
        "tempo_medio": "O(n^2)",
        "pior_caso": "O(n^2)",
        "espaco": "O(1)",
        "estavel": False,
        "descricao": "Faz o número mínimo de trocas. Útil apenas se a operação de escrita na memória for extremamente custosa."
    },
    "Bubble Sort": {
        "tempo_medio": "O(n^2)",
        "pior_caso": "O(n^2)",
        "espaco": "O(1)",
        "estavel": True,
        "descricao": "Fácil implementação, mas geralmente o pior desempenho prático entre as opções."
    }
}