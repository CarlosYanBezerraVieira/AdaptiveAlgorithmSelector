from __future__ import annotations

import csv
import json

import pytest

from utils.graficos import carregar_resultados, gerar_graficos_obrigatorios


def _resultados_exemplo() -> list[dict[str, object]]:
    return [
        {
            "cenario": "aleatorio_n100",
            "tipo_cenario": "aleatorio",
            "tamanho": 100,
            "algoritmo": "Merge Sort",
            "tempo_segundos": 0.012,
            "comparacoes": 700,
            "trocas": 120,
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
            "overhead_percentual": 3.4,
            "acerto_top2": True,
        },
        {
            "cenario": "invertido_n1000",
            "tipo_cenario": "invertido",
            "tamanho": 1000,
            "algoritmo": "Heap Sort",
            "tempo_segundos": 0.044,
            "comparacoes": 9800,
            "trocas": 1400,
            "overhead_percentual": 7.2,
            "acerto_top2": True,
        },
    ]


def test_carregar_resultados_json_e_csv(tmp_path):
    resultados = _resultados_exemplo()

    caminho_json = tmp_path / "resultados.json"
    caminho_json.write_text(json.dumps({"resultados": resultados}), encoding="utf-8")

    caminho_csv = tmp_path / "resultados.csv"
    with caminho_csv.open("w", encoding="utf-8", newline="") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=resultados[0].keys())
        escritor.writeheader()
        escritor.writerows(resultados)

    assert carregar_resultados(caminho_json)[0]["algoritmo"] == "Merge Sort"
    assert carregar_resultados(caminho_csv)[0]["algoritmo"] == "Merge Sort"


def test_gerar_graficos_obrigatorios_cria_arquivos(tmp_path):
    graficos = gerar_graficos_obrigatorios(
        _resultados_exemplo(),
        tmp_path,
        formatos=["png"],
    )

    nomes = {grafico.nome for grafico in graficos}
    assert nomes == {
        "tempo_execucao_algoritmo",
        "comparacoes_algoritmo",
        "acuracia_tipo_dataset",
        "overhead_medio",
        "comportamento_tipo_dataset",
    }

    for grafico in graficos:
        assert len(grafico.arquivos) == 1
        assert grafico.arquivos[0].exists()
        assert grafico.arquivos[0].stat().st_size > 0


def test_gerar_graficos_aceita_nome_de_cenario_da_branch_davi(tmp_path):
    resultados = [
        {
            "nome": "Aleatorio_n1000",
            "algoritmo": "Merge Sort",
            "tempo_segundos": 0.018,
            "comparacoes": 6000,
            "overhead": 4.0,
            "top2": "true",
        },
        {
            "nome": "Quase_Ordenado_n1000",
            "algoritmo": "Insertion Sort",
            "tempo_segundos": 0.009,
            "comparacoes": 1300,
            "overhead": 3.0,
            "top2": "sim",
        },
    ]

    graficos = gerar_graficos_obrigatorios(resultados, tmp_path, formatos=["png"])

    assert len(graficos) == 5
    assert all(grafico.arquivos[0].exists() for grafico in graficos)


def test_gerar_graficos_obrigatorios_exige_campos_obrigatorios(tmp_path):
    resultados = [{"algoritmo": "Merge Sort", "tempo_segundos": 0.01}]

    with pytest.raises(ValueError, match="comparacoes"):
        gerar_graficos_obrigatorios(resultados, tmp_path, formatos=["png"])
