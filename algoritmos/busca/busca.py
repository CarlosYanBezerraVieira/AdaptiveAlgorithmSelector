from utils.contador import ContadorInstrumentacao

from .busca_binaria import busca_binaria as _busca_binaria
from .busca_hash import TabelaHashInstrumentada
from .busca_sequencial import busca_sequencial as _busca_sequencial


def busca_sequencial(arr, alvo):
    return _busca_sequencial(arr, alvo, ContadorInstrumentacao())


def busca_binaria(arr_ordenado, alvo):
    return _busca_binaria(arr_ordenado, alvo, ContadorInstrumentacao())


def busca_hash(arr, alvo):
    return TabelaHashInstrumentada(arr).buscar(alvo, ContadorInstrumentacao())
