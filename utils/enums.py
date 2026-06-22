from enum import Enum


class Objetivo(Enum):
    ORDENAR = "ordenar"
    BUSCAR = "buscar"


class OrigemMetricas(Enum):
    DECLARADA = "Declarada"
    MEDIDA = "Medida"


class TipoDados(Enum):
    INT = "int"
    OBJECT = "object"


class AlgoritmoBusca(Enum):
    SEQUENCIAL = "Busca Sequencial"
    BINARIA = "Busca Binária"
    HASH = "Busca Hash"


class AlgoritmoOrdenacao(Enum):
    INSERTION = "Insertion Sort"
    SELECTION = "Selection Sort"
    BUBBLE = "Bubble Sort"
    MERGE = "Merge Sort"
    QUICK = "Quick Sort"
    HEAP = "Heap Sort"
