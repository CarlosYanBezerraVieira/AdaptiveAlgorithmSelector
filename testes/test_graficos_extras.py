from __future__ import annotations

import pytest

from utils.graficos_extras import gerar_graficos_extras


def _resultados_extras_exemplo() -> list[dict[str, object]]:
    return [
        {
            "cenario": "aleatorio_n100",
            "tipo_cenario": "aleatorio",
            "tamanho": 100,
            "algoritmo": "Merge Sort",
            "tempo_segundos": 0.012,
            "comparacoes": 700,
            "trocas": 120,
            "memoria_kb": 48.5,
            "tempo_decisao_segundos": 0.003,
            "posicao_recomendado": 1,
            "overhead_percentual": 4.5,
            "acerto_top2": True,
        },
        {
            "cenario": "aleatorio_n100",
            "tipo_cenario": "aleatorio",
            "tamanho": 100,
            "algoritmo": "Insertion Sort",
            "tempo_segundos": 0.021,
            "comparacoes": 2100,
            "trocas": 950,
            "memoria_kb": 12.1,
            "tempo_decisao_segundos": 0.003,
            "posicao_recomendado": 1,
            "overhead_percentual": 4.5,
            "acerto_top2": False,
        },
        {
            "cenario": "quase_ordenado_n100",
            "tipo_cenario": "quase_ordenado",
            "tamanho": 100,
            "algoritmo": "Insertion Sort",
            "tempo_segundos": 0.006,
            "comparacoes": 180,
            "trocas": 20,
            "memoria_kb": 10.9,
            "tempo_decisao_segundos": 0.002,
            "posicao_recomendado": 2,
            "overhead_percentual": 3.1,
            "acerto_top2": True,
        },
        {
            "cenario": "quase_ordenado_n1000",
            "tipo_cenario": "quase_ordenado",
            "tamanho": 1000,
            "algoritmo": "Insertion Sort",
            "tempo_segundos": 0.032,
            "comparacoes": 1800,
            "trocas": 200,
            "memoria_kb": 24.2,
            "tempo_decisao_segundos": 0.006,
            "posicao_recomendado": 3,
            "overhead_percentual": 3.4,
            "acerto_top2": False,
        },
        {
            "cenario": "invertido_n1000",
            "tipo_cenario": "invertido",
            "tamanho": 1000,
            "algoritmo": "Heap Sort",
            "tempo_segundos": 0.044,
            "comparacoes": 9800,
            "trocas": 1400,
            "memoria_kb": 31.8,
            "tempo_decisao_segundos": 0.005,
            "posicao_recomendado": 1,
            "overhead_percentual": 7.2,
            "acerto_top2": True,
        },
    ]


def test_gerar_graficos_extras_cria_arquivos(tmp_path):
    graficos = gerar_graficos_extras(
        _resultados_extras_exemplo(),
        tmp_path,
        formatos=["png"],
    )

    nomes = {grafico.nome for grafico in graficos}
    assert nomes == {
        "trocas_algoritmo",
        "memoria_algoritmo",
        "tempo_decisao_tamanho",
        "ranking_recomendado",
        "heatmap_tempo",
    }

    for grafico in graficos:
        assert len(grafico.arquivos) == 1
        assert grafico.arquivos[0].exists()
        assert grafico.arquivos[0].stat().st_size > 0


def test_gerar_graficos_extras_aceita_aliases(tmp_path):
    resultados = [
        {
            "nome": "Aleatorio_n100",
            "algoritmo": "Merge Sort",
            "tempo_segundos": 0.012,
            "trocas": 120,
            "memoria": 48.5,
            "tempo_decisao": 0.003,
            "rank_recomendado": 1,
        },
        {
            "nome": "Aleatorio_n100",
            "algoritmo": "Heap Sort",
            "tempo_segundos": 0.014,
            "trocas": 140,
            "memoria": 31.2,
            "tempo_decisao": 0.003,
            "rank_recomendado": 1,
        },
    ]

    graficos = gerar_graficos_extras(resultados, tmp_path, formatos=["png"])

    assert len(graficos) == 5
    assert all(grafico.arquivos[0].exists() for grafico in graficos)


def test_gerar_graficos_extras_exige_memoria(tmp_path):
    resultados = [
        {
            "cenario": "aleatorio_n100",
            "tipo_cenario": "aleatorio",
            "tamanho": 100,
            "algoritmo": "Merge Sort",
            "tempo_segundos": 0.012,
            "trocas": 120,
            "tempo_decisao_segundos": 0.003,
            "posicao_recomendado": 1,
        },
    ]

    with pytest.raises(ValueError, match="memoria_kb"):
        gerar_graficos_extras(resultados, tmp_path, formatos=["png"])
