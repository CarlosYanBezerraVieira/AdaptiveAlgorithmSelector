from validacao.validar_seletor import (
    calcular_impacto_tipo_dataset,
    calcular_metricas_obrigatorias,
    calcular_overhead_percentual,
    identificar_tipo_cenario,
    salvar_relatorio_validacao,
    validar_seletor,
)


def test_calcular_metricas_obrigatorias():
    resumos = [
        {
            "tipo_cenario": "aleatorio",
            "acerto_top2": True,
            "overhead_percentual": 5.0,
            "tempo_decisao_segundos": 0.01,
        },
        {
            "tipo_cenario": "aleatorio",
            "acerto_top2": False,
            "overhead_percentual": 15.0,
            "tempo_decisao_segundos": 0.03,
        },
        {
            "tipo_cenario": "invertido",
            "acerto_top2": True,
            "overhead_percentual": 10.0,
            "tempo_decisao_segundos": 0.02,
        },
    ]

    metricas = calcular_metricas_obrigatorias(resumos)

    assert metricas["total_cenarios"] == 3
    assert metricas["acertos_top2"] == 2
    assert metricas["taxa_acerto_top2"] == (2 / 3) * 100
    assert metricas["overhead_medio_percentual"] == 10.0
    assert metricas["tempo_medio_decisao_segundos"] == 0.02
    assert metricas["taxas_por_tipo"] == {
        "aleatorio": 50.0,
        "invertido": 100.0,
    }
    assert metricas["impacto_tipo_dataset"] == 50.0


def test_calcular_overhead_percentual():
    assert calcular_overhead_percentual(0.01, 0.1) == 10.0
    assert calcular_overhead_percentual(0.01, 0.0) == 0.0


def test_identificar_tipo_cenario():
    assert identificar_tipo_cenario("Aleatorio_n1000") == "aleatorio"
    assert identificar_tipo_cenario("Quase_Ordenado_n1000") == "quase_ordenado"
    assert identificar_tipo_cenario("Invertido_n1000") == "invertido"
    assert identificar_tipo_cenario("Muitas_Duplicatas_n1000") == "muitas_duplicatas"
    assert identificar_tipo_cenario("Cenario_customizado") == "outros"


def test_calcular_impacto_tipo_dataset():
    assert calcular_impacto_tipo_dataset({"a": 80.0, "b": 55.0}) == 25.0
    assert calcular_impacto_tipo_dataset({}) == 0.0


def test_validar_seletor_gera_resultados_para_graficos():
    relatorio = validar_seletor(
        cenarios=[
            {"nome": "Aleatorio_n6", "dados": [5, 1, 4, 2, 3, 0]},
            {"nome": "Invertido_n6", "dados": [6, 5, 4, 3, 2, 1]},
        ],
        repeticoes=1,
        seed=1,
    )

    assert set(relatorio) == {"metricas", "cenarios", "resultados"}
    assert relatorio["metricas"]["total_cenarios"] == 2
    assert len(relatorio["cenarios"]) == 2
    assert len(relatorio["resultados"]) == 12

    primeira_linha = relatorio["resultados"][0]
    campos_esperados = {
        "cenario",
        "tipo_cenario",
        "tamanho",
        "algoritmo",
        "tempo_segundos",
        "comparacoes",
        "trocas",
        "memoria_kb",
        "overhead_percentual",
        "acerto_top2",
        "tempo_decisao_segundos",
        "posicao_recomendado",
    }
    assert campos_esperados <= set(primeira_linha)


def test_salvar_relatorio_validacao_json_e_csv(tmp_path):
    relatorio = {
        "metricas": {"total_cenarios": 1},
        "cenarios": [{"cenario": "Aleatorio_n3"}],
        "resultados": [
            {
                "cenario": "Aleatorio_n3",
                "tipo_cenario": "aleatorio",
                "tamanho": 3,
                "algoritmo": "Merge Sort",
                "tempo_segundos": 0.1,
            }
        ],
    }

    caminho_json = salvar_relatorio_validacao(relatorio, tmp_path / "relatorio.json")
    caminho_csv = salvar_relatorio_validacao(relatorio, tmp_path / "relatorio.csv")

    assert caminho_json.exists()
    assert caminho_csv.exists()
    assert "total_cenarios" in caminho_json.read_text(encoding="utf-8")
    assert "Merge Sort" in caminho_csv.read_text(encoding="utf-8")
