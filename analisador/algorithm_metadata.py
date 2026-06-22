from utils.enums import AlgoritmoBusca, AlgoritmoOrdenacao

METADADOS_ORDENACAO = {
    AlgoritmoOrdenacao.MERGE.value: {
        "complexidade": "O(n log n) garantido",
        "memoria": "O(n)",
        "estavel": "Sim",
        "descricao": "Algoritmo de divisão e conquista. Excelente garantia de tempo, mas consome memória extra.",
    },
    AlgoritmoOrdenacao.QUICK.value: {
        "complexidade": "O(n log n) médio",
        "memoria": "O(log n) médio",
        "estavel": "Não",
        "descricao": "Geralmente o mais rápido na prática para grandes volumes na memória RAM.",
    },
    AlgoritmoOrdenacao.HEAP.value: {
        "complexidade": "O(n log n) garantido",
        "memoria": "O(1)",
        "estavel": "Não",
        "descricao": "Ótimo tempo garantido e não consome memória extra. Excelente para sistemas embarcados.",
    },
    AlgoritmoOrdenacao.INSERTION.value: {
        "complexidade": "O(n) no melhor caso / O(n²) no pior",
        "memoria": "O(1)",
        "estavel": "Sim",
        "descricao": "Muito eficiente para arrays pequenos ou quase ordenados.",
    },
    AlgoritmoOrdenacao.SELECTION.value: {
        "complexidade": "O(n²)",
        "memoria": "O(1)",
        "estavel": "Não",
        "descricao": "Faz o número mínimo de trocas. Útil apenas se a operação de escrita na memória for extremamente custosa.",
    },
    AlgoritmoOrdenacao.BUBBLE.value: {
        "complexidade": "O(n²)",
        "memoria": "O(1)",
        "estavel": "Sim",
        "descricao": "Fácil implementação, mas geralmente o pior desempenho prático entre as opções.",
    },
}

METADADOS_BUSCA = {
    AlgoritmoBusca.SEQUENCIAL.value: {
        "complexidade": "O(n)",
        "memoria": "O(1)",
        "estavel": "N/A",
        "descricao": "Busca linear elemento por elemento. Única opção para dados não ordenados quando não há índice.",
    },
    AlgoritmoBusca.BINARIA.value: {
        "complexidade": "O(log n)",
        "memoria": "O(1)",
        "estavel": "N/A",
        "descricao": "Busca eficiente reduzindo pela metade o espaço de busca. Exige ordenação prévia do array.",
    },
    AlgoritmoBusca.HASH.value: {
        "complexidade": "O(1)",
        "memoria": "O(n)",
        "estavel": "N/A",
        "descricao": "Acesso direto através de função hash. Requer memória extra proporcional ao tamanho dos dados.",
    },
}
