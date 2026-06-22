
from enum import Enum

class ComplexidadeTempo(Enum):
    O_1 = "O(1)"
    O_LOG_N = "O(log n)"
    O_N = "O(n)"
    O_N_LOG_N = "O(n log n)"
    O_N2 = "O(n^2)"

class CategoriaAlgoritmo(Enum):
    ORDENACAO = "Ordenação"
    BUSCA = "Busca"