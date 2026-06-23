from __future__ import annotations

import argparse
import csv
import json
import random
import time
from collections import defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path
from statistics import mean
from typing import Any

from algoritmos.ordenacao.bubble_sort import bubble_sort
from algoritmos.ordenacao.heap_sort import heap_sort
from algoritmos.ordenacao.insertion_sort import insertion_sort
from algoritmos.ordenacao.merge_sort import merge_sort
from algoritmos.ordenacao.quick_sort import quick_sort
from algoritmos.ordenacao.selection_sort import selection_sort
from analisador.caracteristicas import analisar_propriedades_array
from analisador.motor_decisao import selecionar_melhor_algoritmo
from utils.benchmark import executar_benchmark
from utils.enums import Objetivo
from utils.gerador import gerar_cenarios

ALGORITMOS_ORDENACAO = {
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}

TAMANHOS_PADRAO = (30, 100, 1000)


def validar_seletor(
    cenarios: Iterable[dict[str, Any]] | None = None,
    tamanhos: Sequence[int] = TAMANHOS_PADRAO,
    repeticoes: int = 1,
    seed: int | None = 42,
    restricao_memoria: bool = False,
    precisa_estabilidade: bool = False,
) -> dict[str, Any]:
    """Executa validacao empirica e calcula as metricas obrigatorias."""
    if repeticoes < 1:
        raise ValueError("A quantidade de repeticoes deve ser maior ou igual a 1.")

    cenarios_validacao = list(cenarios) if cenarios is not None else _gerar_cenarios(
        tamanhos,
        seed,
    )
    if not cenarios_validacao:
        raise ValueError("Informe ao menos um cenario para validacao.")

    resultados: list[dict[str, Any]] = []
    resumos: list[dict[str, Any]] = []

    for cenario in cenarios_validacao:
        resultado_cenario = validar_cenario(
            cenario,
            repeticoes=repeticoes,
            restricao_memoria=restricao_memoria,
            precisa_estabilidade=precisa_estabilidade,
        )
        resultados.extend(resultado_cenario["resultados"])
        resumos.append(resultado_cenario["resumo"])

    metricas = calcular_metricas_obrigatorias(resumos)

    return {
        "metricas": metricas,
        "cenarios": resumos,
        "resultados": resultados,
    }


def validar_cenario(
    cenario: dict[str, Any],
    repeticoes: int = 1,
    restricao_memoria: bool = False,
    precisa_estabilidade: bool = False,
) -> dict[str, Any]:
    """Valida um cenario e retorna resumo + linhas para graficos."""
    nome = str(cenario["nome"])
    dados = list(cenario["dados"])
    tipo_cenario = str(cenario.get("tipo_cenario") or identificar_tipo_cenario(nome))
    tamanho = len(dados)
    classe_tamanho = classificar_tamanho(tamanho)
    memoria_cenario = bool(cenario.get("restricao_memoria", restricao_memoria))
    estabilidade_cenario = bool(
        cenario.get("precisa_estabilidade", precisa_estabilidade)
    )

    inicio_analise = time.perf_counter()
    propriedades = analisar_propriedades_array(
        arr=dados.copy(),
        objetivo=Objetivo.ORDENAR.value,
        restricao_memoria=memoria_cenario,
        precisa_estabilidade=estabilidade_cenario,
    )
    fim_analise = time.perf_counter()

    decisao = selecionar_melhor_algoritmo(propriedades)
    fim_decisao = time.perf_counter()

    tempo_analise = fim_analise - inicio_analise
    tempo_pontuacao = fim_decisao - fim_analise
    tempo_decisao = fim_decisao - inicio_analise
    recomendado = decisao["recomendado"]

    benchmarks = executar_benchmarks_cenario(dados, repeticoes)
    ranking = sorted(benchmarks, key=lambda item: item["tempo_segundos"])
    ranking_algoritmos = [item["algoritmo"] for item in ranking]
    top2 = ranking_algoritmos[:2]
    acerto_top2 = recomendado in top2
    posicao_recomendado = (
        ranking_algoritmos.index(recomendado) + 1
        if recomendado in ranking_algoritmos
        else None
    )

    benchmark_recomendado = _buscar_benchmark(benchmarks, recomendado)
    tempo_recomendado = benchmark_recomendado["tempo_segundos"]
    overhead_percentual = calcular_overhead_percentual(
        tempo_decisao,
        tempo_recomendado,
    )

    resumo = {
        "cenario": nome,
        "tipo_cenario": tipo_cenario,
        "classe_tamanho": classe_tamanho,
        "tamanho": tamanho,
        "algoritmo_recomendado": recomendado,
        "pontuacao_recomendacao": decisao["pontuacao"],
        "top2_real": top2,
        "posicao_recomendado": posicao_recomendado,
        "acerto_top2": acerto_top2,
        "tempo_analise_segundos": tempo_analise,
        "tempo_pontuacao_segundos": tempo_pontuacao,
        "tempo_decisao_segundos": tempo_decisao,
        "tempo_algoritmo_recomendado": tempo_recomendado,
        "overhead_percentual": overhead_percentual,
    }

    linhas_graficos = []
    for item in benchmarks:
        linhas_graficos.append(
            {
                "cenario": nome,
                "tipo_cenario": tipo_cenario,
                "classe_tamanho": classe_tamanho,
                "tamanho": tamanho,
                "algoritmo": item["algoritmo"],
                "tempo_segundos": item["tempo_segundos"],
                "comparacoes": item["comparacoes"],
                "trocas": item["trocas"],
                "memoria_kb": item["memoria_kb"],
                "algoritmo_recomendado": recomendado,
                "pontuacao_recomendacao": decisao["pontuacao"],
                "tempo_decisao_segundos": tempo_decisao,
                "tempo_analise_segundos": tempo_analise,
                "tempo_pontuacao_segundos": tempo_pontuacao,
                "overhead_percentual": overhead_percentual,
                "acerto_top2": acerto_top2,
                "posicao_recomendado": posicao_recomendado,
            }
        )

    return {
        "resumo": resumo,
        "resultados": linhas_graficos,
    }


def executar_benchmarks_cenario(
    dados: Sequence[Any],
    repeticoes: int = 1,
) -> list[dict[str, Any]]:
    """Executa todos os algoritmos de ordenacao e calcula medias."""
    benchmarks = []
    esperado = sorted(dados)

    for nome, algoritmo in ALGORITMOS_ORDENACAO.items():
        execucoes = [executar_benchmark(algoritmo, dados) for _ in range(repeticoes)]
        ultimo_resultado = execucoes[-1]["arr_ordenado"]
        if ultimo_resultado != esperado:
            raise ValueError(f"{nome} nao ordenou corretamente o cenario.")

        benchmarks.append(
            {
                "algoritmo": nome,
                "tempo_segundos": mean(item["tempo_segundos"] for item in execucoes),
                "memoria_kb": mean(item["memoria_kb"] for item in execucoes),
                "comparacoes": round(mean(item["comparacoes"] for item in execucoes)),
                "trocas": round(mean(item["trocas"] for item in execucoes)),
            }
        )

    return benchmarks


def calcular_metricas_obrigatorias(
    resumos_cenarios: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Calcula as quatro metricas obrigatorias da secao 9.1."""
    if not resumos_cenarios:
        raise ValueError("Nao ha cenarios para calcular metricas.")

    total_cenarios = len(resumos_cenarios)
    total_acertos = sum(1 for resumo in resumos_cenarios if resumo["acerto_top2"])
    taxas_por_tipo = calcular_taxas_por_tipo(resumos_cenarios)

    return {
        "total_cenarios": total_cenarios,
        "acertos_top2": total_acertos,
        "taxa_acerto_top2": (total_acertos / total_cenarios) * 100,
        "overhead_medio_percentual": mean(
            resumo["overhead_percentual"] for resumo in resumos_cenarios
        ),
        "tempo_medio_decisao_segundos": mean(
            resumo["tempo_decisao_segundos"] for resumo in resumos_cenarios
        ),
        "impacto_tipo_dataset": calcular_impacto_tipo_dataset(taxas_por_tipo),
        "taxas_por_tipo": taxas_por_tipo,
    }


def calcular_taxas_por_tipo(
    resumos_cenarios: Sequence[dict[str, Any]],
) -> dict[str, float]:
    grupos: dict[str, list[bool]] = defaultdict(list)
    for resumo in resumos_cenarios:
        grupos[str(resumo["tipo_cenario"])].append(bool(resumo["acerto_top2"]))

    return {
        tipo: (sum(acertos) / len(acertos)) * 100
        for tipo, acertos in sorted(grupos.items())
    }


def calcular_impacto_tipo_dataset(taxas_por_tipo: dict[str, float]) -> float:
    if not taxas_por_tipo:
        return 0.0

    taxas = list(taxas_por_tipo.values())
    return max(taxas) - min(taxas)


def calcular_overhead_percentual(
    tempo_decisao: float,
    tempo_algoritmo: float,
) -> float:
    if tempo_algoritmo <= 0:
        return 0.0

    return (tempo_decisao / tempo_algoritmo) * 100


def identificar_tipo_cenario(nome_cenario: str) -> str:
    nome = nome_cenario.lower()
    if "quase" in nome:
        return "quase_ordenado"
    if "invertido" in nome:
        return "invertido"
    if "duplicata" in nome:
        return "muitas_duplicatas"
    if "aleatorio" in nome:
        return "aleatorio"
    if "pequeno" in nome:
        return "pequeno"
    if "grande" in nome:
        return "grande"
    return "outros"


def classificar_tamanho(tamanho: int) -> str:
    if tamanho < 100:
        return "pequeno"
    if tamanho < 10000:
        return "medio"
    return "grande"


def salvar_relatorio_validacao(
    relatorio: dict[str, Any],
    caminho: str | Path,
) -> Path:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)

    if destino.suffix.lower() == ".json":
        destino.write_text(
            json.dumps(relatorio, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return destino

    if destino.suffix.lower() == ".csv":
        resultados = relatorio["resultados"]
        if not resultados:
            raise ValueError("Nao ha resultados para salvar em CSV.")

        with destino.open("w", encoding="utf-8", newline="") as arquivo_csv:
            escritor = csv.DictWriter(arquivo_csv, fieldnames=resultados[0].keys())
            escritor.writeheader()
            escritor.writerows(resultados)
        return destino

    raise ValueError("Formato nao suportado. Use .json ou .csv.")


def imprimir_resumo_metricas(metricas: dict[str, Any]) -> None:
    print("=== METRICAS OBRIGATORIAS ===")
    print(f"Cenarios avaliados: {metricas['total_cenarios']}")
    print(
        "Taxa de acerto Top-2: "
        f"{metricas['taxa_acerto_top2']:.2f}% "
        f"({metricas['acertos_top2']} acertos)"
    )
    print(f"Overhead medio: {metricas['overhead_medio_percentual']:.2f}%")
    print(
        "Tempo medio de decisao: "
        f"{metricas['tempo_medio_decisao_segundos']:.6f}s"
    )
    print(f"Impacto por tipo de dataset: {metricas['impacto_tipo_dataset']:.2f}%")
    print("Taxas por tipo:")
    for tipo, taxa in metricas["taxas_por_tipo"].items():
        print(f" - {tipo}: {taxa:.2f}%")


def _gerar_cenarios(tamanhos: Sequence[int], seed: int | None) -> list[dict[str, Any]]:
    estado_random = random.getstate()
    try:
        if seed is not None:
            random.seed(seed)
        return gerar_cenarios(list(tamanhos))
    finally:
        random.setstate(estado_random)


def _buscar_benchmark(
    benchmarks: Sequence[dict[str, Any]],
    algoritmo: str,
) -> dict[str, Any]:
    for benchmark in benchmarks:
        if benchmark["algoritmo"] == algoritmo:
            return benchmark

    raise ValueError(f"Algoritmo recomendado nao encontrado no benchmark: {algoritmo}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Valida empiricamente o seletor e calcula metricas obrigatorias.",
    )
    parser.add_argument(
        "--saida",
        default="resultados/validacao/metricas_obrigatorias.json",
        help="Arquivo .json ou .csv para salvar os resultados.",
    )
    parser.add_argument(
        "--tamanhos",
        nargs="+",
        type=int,
        default=list(TAMANHOS_PADRAO),
        help="Tamanhos dos arrays usados nos cenarios padrao.",
    )
    parser.add_argument(
        "--repeticoes",
        type=int,
        default=1,
        help="Quantidade de repeticoes de cada benchmark.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed usada para gerar cenarios reprodutiveis.",
    )

    args = parser.parse_args(argv)
    relatorio = validar_seletor(
        tamanhos=args.tamanhos,
        repeticoes=args.repeticoes,
        seed=args.seed,
    )
    caminho = salvar_relatorio_validacao(relatorio, args.saida)

    imprimir_resumo_metricas(relatorio["metricas"])
    print(f"\nResultados salvos em: {caminho}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
