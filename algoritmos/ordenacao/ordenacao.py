from utils.contador import ContadorInstrumentacao

from .bubble_sort import bubble_sort as _bubble_sort
from .heap_sort import heap_sort as _heap_sort
from .insertion_sort import insertion_sort as _insertion_sort
from .merge_sort import merge_sort as _merge_sort
from .quick_sort import quick_sort as _quick_sort
from .selection_sort import selection_sort as _selection_sort


def bubble_sort(arr):
    return _bubble_sort(arr, ContadorInstrumentacao())


def insertion_sort(arr):
    return _insertion_sort(arr, ContadorInstrumentacao())


def selection_sort(arr):
    return _selection_sort(arr, ContadorInstrumentacao())


def merge_sort(arr):
    return _merge_sort(arr, ContadorInstrumentacao())


def quick_sort(arr):
    return _quick_sort(arr, ContadorInstrumentacao())


def heap_sort(arr):
    return _heap_sort(arr, ContadorInstrumentacao())
