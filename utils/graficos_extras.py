from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

import matplotlib

from utils.graficos import (
    FORMATOS_PADRAO,
    FORMATOS_SUPORTADOS,
    GraficoGerado,
    ResultadoBenchmark,
    _normalizar_resultados,
)

matplotlib.use("Agg")

ALIASES_EXTRAS = {
    "memoria_kb": (
        "memoria_kb",
        "memoria",
        "memoria_pico_kb",
        "pico_memoria_kb",
        "uso_memoria_kb",
    ),
    "posicao_recomendado": (
        "posicao_recomendado",
        "rank_recomendado",
        "ranking_recomendado",
        "posicao_ranking",
    ),
    "tempo_decisao_segundos": (
        "tempo_decisao_segundos",
        "tempo_decisao",
        "tempo_seletor",
        "tempo_analise_pontuacao",
        "t_decisao",
    ),
}


def gerar_graficos_extras(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> list[GraficoGerado]:
    """Gera graficos complementares para enriquecer o relatorio."""
    registros = _normalizar_resultados_extras(resultados)
    if not registros:
        raise ValueError("Nao ha resultados para gerar graficos extras.")

    formatos_normalizados = _normalizar_formatos(formatos)

    return [
        grafico_trocas_por_algoritmo(registros, diretorio_saida, formatos_normalizados),
        grafico_memoria_por_algoritmo(
            registros,
            diretorio_saida,
            formatos_normalizados,
        ),
        grafico_tempo_decisao_por_tamanho(
            registros,
            diretorio_saida,
            formatos_normalizados,
        ),
        grafico_ranking_recomendado(registros, diretorio_saida, formatos_normalizados),
        grafico_heatmap_tempo(registros, diretorio_saida, formatos_normalizados),
    ]


def grafico_trocas_por_algoritmo(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados_extras(resultados)
    medias = _media_por_chave(registros, "algoritmo", "trocas")

    figura, eixo = _criar_figura()
    _desenhar_barras(
        eixo,
        medias,
        titulo="Trocas medias por algoritmo",
        eixo_y="Trocas medias",
        cor="#4f46e5",
    )
    return _salvar_figura(figura, diretorio_saida, "trocas_algoritmo", formatos)


def grafico_memoria_por_algoritmo(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados_extras(resultados)
    medias = _media_por_chave(registros, "algoritmo", "memoria_kb")

    figura, eixo = _criar_figura()
    _desenhar_barras(
        eixo,
        medias,
        titulo="Uso medio de memoria por algoritmo",
        eixo_y="Memoria media (KB)",
        cor="#0891b2",
    )
    return _salvar_figura(figura, diretorio_saida, "memoria_algoritmo", formatos)


def grafico_tempo_decisao_por_tamanho(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados_extras(resultados)
    _exigir_campos(
        registros,
        {"tamanho", "tempo_decisao_segundos"},
        "tempo de decisao",
    )

    tempos: dict[int, list[float]] = defaultdict(list)
    for registro in registros:
        tamanho = int(_valor_float(registro, "tamanho"))
        tempo = _valor_float(registro, "tempo_decisao_segundos")
        tempos[tamanho].append(tempo)

    tamanhos = sorted(tempos)
    medias = [mean(tempos[tamanho]) for tamanho in tamanhos]

    figura, eixo = _criar_figura()
    eixo.plot(tamanhos, medias, marker="o", linewidth=2, color="#16a34a")
    eixo.axhline(0.1, color="#dc2626", linestyle="--", linewidth=1.5)
    eixo.set_title("Tempo medio de decisao do seletor por tamanho")
    eixo.set_xlabel("Tamanho do dataset")
    eixo.set_ylabel("Tempo medio de decisao (s)")
    eixo.grid(axis="y", linestyle="--", alpha=0.35)
    eixo.text(
        tamanhos[-1],
        0.1,
        "limite esperado: 0.1s",
        color="#dc2626",
        ha="right",
        va="bottom",
        fontsize=8,
    )
    figura.tight_layout()

    return _salvar_figura(figura, diretorio_saida, "tempo_decisao_tamanho", formatos)


def grafico_ranking_recomendado(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados_extras(resultados)
    _exigir_campos(registros, {"cenario", "posicao_recomendado"}, "ranking")

    posicoes_por_cenario: dict[str, int] = {}
    for registro in registros:
        cenario = str(registro["cenario"])
        posicoes_por_cenario.setdefault(
            cenario,
            int(_valor_float(registro, "posicao_recomendado")),
        )

    distribuicao = {
        "Top-1": 0,
        "Top-2": 0,
        "Fora do Top-2": 0,
    }
    for posicao in posicoes_por_cenario.values():
        if posicao == 1:
            distribuicao["Top-1"] += 1
        elif posicao == 2:
            distribuicao["Top-2"] += 1
        else:
            distribuicao["Fora do Top-2"] += 1

    figura, eixo = _criar_figura()
    _desenhar_barras(
        eixo,
        distribuicao,
        titulo="Posicao do algoritmo recomendado no ranking real",
        eixo_y="Quantidade de cenarios",
        cor="#9333ea",
    )
    return _salvar_figura(figura, diretorio_saida, "ranking_recomendado", formatos)


def grafico_heatmap_tempo(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados_extras(resultados)
    _exigir_campos(
        registros,
        {"tipo_cenario", "algoritmo", "tempo_segundos"},
        "heatmap de tempo",
    )

    tempos: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for registro in registros:
        tipo = str(registro["tipo_cenario"])
        algoritmo = str(registro["algoritmo"])
        tempo = _valor_float(registro, "tempo_segundos")
        tempos[tipo][algoritmo].append(tempo)

    tipos = sorted(tempos)
    algoritmos = sorted({algoritmo for dados in tempos.values() for algoritmo in dados})
    matriz = []
    for tipo in tipos:
        linha = []
        for algoritmo in algoritmos:
            valores = tempos[tipo].get(algoritmo, [])
            linha.append(mean(valores) if valores else 0.0)
        matriz.append(linha)

    figura, eixo = _criar_figura(largura=11, altura=6)
    mapa = eixo.imshow(matriz, cmap="Blues", aspect="auto")
    eixo.set_title("Heatmap de tempo medio por algoritmo e tipo de dataset")
    eixo.set_xlabel("Algoritmo")
    eixo.set_ylabel("Tipo de dataset")
    eixo.set_xticks(range(len(algoritmos)), algoritmos, rotation=30, ha="right")
    eixo.set_yticks(range(len(tipos)), tipos)

    for indice_tipo, linha in enumerate(matriz):
        for indice_algoritmo, valor in enumerate(linha):
            eixo.text(
                indice_algoritmo,
                indice_tipo,
                f"{valor:.4f}",
                ha="center",
                va="center",
                fontsize=8,
            )

    figura.colorbar(mapa, ax=eixo, label="Tempo medio (s)")
    figura.tight_layout()

    return _salvar_figura(figura, diretorio_saida, "heatmap_tempo", formatos)


def _normalizar_resultados_extras(
    resultados: Iterable[ResultadoBenchmark],
) -> list[ResultadoBenchmark]:
    registros = _normalizar_resultados(resultados)
    return [_normalizar_resultado_extra(registro) for registro in registros]


def _normalizar_resultado_extra(registro: ResultadoBenchmark) -> ResultadoBenchmark:
    normalizado = dict(registro)

    for campo_canonico, aliases in ALIASES_EXTRAS.items():
        if campo_canonico in normalizado:
            continue

        for alias in aliases:
            if alias in normalizado:
                normalizado[campo_canonico] = normalizado[alias]
                break

    return normalizado


def _media_por_chave(
    registros: list[ResultadoBenchmark],
    chave_grupo: str,
    chave_valor: str,
) -> dict[str, float]:
    _exigir_campos(registros, {chave_grupo, chave_valor}, chave_valor)

    grupos: dict[str, list[float]] = defaultdict(list)
    for registro in registros:
        grupo = str(registro[chave_grupo])
        grupos[grupo].append(_valor_float(registro, chave_valor))

    return {
        grupo: mean(valores)
        for grupo, valores in sorted(grupos.items(), key=lambda item: item[0])
    }


def _desenhar_barras(
    eixo: Any,
    dados: dict[str, float | int],
    titulo: str,
    eixo_y: str,
    cor: str,
) -> None:
    rotulos = list(dados)
    valores = [float(valor) for valor in dados.values()]

    eixo.bar(rotulos, valores, color=cor)
    eixo.set_title(titulo)
    eixo.set_ylabel(eixo_y)
    eixo.grid(axis="y", linestyle="--", alpha=0.35)
    eixo.tick_params(axis="x", rotation=30)

    for indice, valor in enumerate(valores):
        eixo.text(indice, valor, f"{valor:.2f}", ha="center", va="bottom", fontsize=8)


def _salvar_figura(
    figura: Any,
    diretorio_saida: str | Path,
    nome_base: str,
    formatos: Iterable[str],
) -> GraficoGerado:
    from matplotlib import pyplot as plt

    saida = Path(diretorio_saida)
    saida.mkdir(parents=True, exist_ok=True)

    arquivos = []
    for formato in _normalizar_formatos(formatos):
        caminho = saida / f"{nome_base}.{formato}"
        figura.savefig(caminho, bbox_inches="tight", dpi=150)
        arquivos.append(caminho)

    plt.close(figura)
    return GraficoGerado(nome=nome_base, arquivos=tuple(arquivos))


def _criar_figura(largura: int = 10, altura: int = 5) -> tuple[Any, Any]:
    from matplotlib import pyplot as plt

    return plt.subplots(figsize=(largura, altura))


def _normalizar_formatos(formatos: Iterable[str]) -> tuple[str, ...]:
    normalizados = tuple(formato.lower().lstrip(".") for formato in formatos)
    if not normalizados:
        raise ValueError("Informe ao menos um formato de saida.")

    invalidos = set(normalizados) - FORMATOS_SUPORTADOS
    if invalidos:
        msg = f"Formatos nao suportados: {', '.join(sorted(invalidos))}."
        raise ValueError(msg)

    return normalizados


def _exigir_campos(
    registros: list[ResultadoBenchmark],
    campos: set[str],
    contexto: str,
) -> None:
    for indice, registro in enumerate(registros, start=1):
        ausentes = campos - set(registro)
        if ausentes:
            campos_ausentes = ", ".join(sorted(ausentes))
            msg = f"Resultado {indice} sem campos para {contexto}: {campos_ausentes}."
            raise ValueError(msg)


def _valor_float(registro: ResultadoBenchmark, campo: str) -> float:
    valor = registro[campo]
    if valor is None or valor == "":
        raise ValueError(f"Campo '{campo}' vazio.")

    if isinstance(valor, str):
        valor = valor.replace(",", ".")

    return float(valor)
