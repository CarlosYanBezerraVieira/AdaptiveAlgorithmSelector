from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")

FORMATOS_PADRAO = ("png", "pdf")
FORMATOS_SUPORTADOS = {"png", "pdf", "svg"}
PADRAO_CENARIO_COM_TAMANHO = re.compile(r"^(?P<tipo>.+)_n(?P<tamanho>\d+)$")

ALIASES_CAMPOS = {
    "acerto_top2": ("acerto_top2", "correto_top2", "top2", "recomendacao_top2"),
    "algoritmo": ("algoritmo", "nome_algoritmo", "algoritmo_nome"),
    "cenario": ("cenario", "nome_cenario", "nome"),
    "comparacoes": ("comparacoes", "comparações", "numero_comparacoes"),
    "overhead_percentual": ("overhead_percentual", "overhead", "overhead_medio"),
    "tamanho": ("tamanho", "n", "quantidade_elementos"),
    "tempo_segundos": (
        "tempo_segundos",
        "tempo",
        "tempo_medio",
        "tempo_execucao",
        "tempo_execucao_segundos",
    ),
    "tipo_cenario": ("tipo_cenario", "tipo_dataset", "categoria_cenario"),
    "trocas": ("trocas", "numero_trocas"),
}


@dataclass(frozen=True)
class GraficoGerado:
    nome: str
    arquivos: tuple[Path, ...]


ResultadoBenchmark = dict[str, Any]


def carregar_resultados(caminho: str | Path) -> list[ResultadoBenchmark]:
    """Carrega resultados de benchmark em JSON ou CSV."""
    arquivo = Path(caminho)

    if arquivo.suffix.lower() == ".json":
        with arquivo.open(encoding="utf-8") as dados_json:
            dados = json.load(dados_json)

        if isinstance(dados, dict):
            dados = dados.get("resultados", [])

        if not isinstance(dados, list):
            msg = "O JSON deve conter uma lista ou um objeto com a chave 'resultados'."
            raise ValueError(msg)

        return [_normalizar_resultado(dict(item)) for item in dados]

    if arquivo.suffix.lower() == ".csv":
        with arquivo.open(encoding="utf-8", newline="") as dados_csv:
            return [
                _normalizar_resultado(dict(item))
                for item in csv.DictReader(dados_csv)
            ]

    msg = "Formato nao suportado. Use arquivos .json ou .csv."
    raise ValueError(msg)


def gerar_graficos_obrigatorios(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> list[GraficoGerado]:
    """Gera todos os graficos exigidos no enunciado do projeto."""
    registros = _normalizar_resultados(resultados)
    if not registros:
        raise ValueError("Nao ha resultados para gerar graficos.")

    formatos_normalizados = _normalizar_formatos(formatos)

    return [
        grafico_tempo_execucao(registros, diretorio_saida, formatos_normalizados),
        grafico_comparacoes(registros, diretorio_saida, formatos_normalizados),
        grafico_acuracia_por_cenario(registros, diretorio_saida, formatos_normalizados),
        grafico_overhead_medio(registros, diretorio_saida, formatos_normalizados),
        grafico_comportamento_por_tipo(
            registros,
            diretorio_saida,
            formatos_normalizados,
        ),
    ]


def grafico_tempo_execucao(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados(resultados)
    medias = _media_por_chave(registros, "algoritmo", "tempo_segundos")

    figura, eixo = _criar_figura()
    _desenhar_barras(
        eixo,
        medias,
        titulo="Tempo medio de execucao por algoritmo",
        eixo_y="Tempo medio (s)",
        cor="#2563eb",
    )
    return _salvar_figura(figura, diretorio_saida, "tempo_execucao_algoritmo", formatos)


def grafico_comparacoes(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados(resultados)
    medias = _media_por_chave(registros, "algoritmo", "comparacoes")

    figura, eixo = _criar_figura()
    _desenhar_barras(
        eixo,
        medias,
        titulo="Comparacoes medias por algoritmo",
        eixo_y="Comparacoes medias",
        cor="#0f766e",
    )
    return _salvar_figura(figura, diretorio_saida, "comparacoes_algoritmo", formatos)


def grafico_acuracia_por_cenario(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados(resultados)
    _exigir_campos(registros, {"tipo_cenario", "acerto_top2"}, "acuracia")

    totais: dict[str, int] = defaultdict(int)
    acertos: dict[str, int] = defaultdict(int)
    for registro in registros:
        tipo = str(registro["tipo_cenario"])
        totais[tipo] += 1
        if _valor_bool(registro, "acerto_top2"):
            acertos[tipo] += 1

    percentuais = {
        tipo: (acertos[tipo] / total) * 100
        for tipo, total in sorted(totais.items())
    }

    figura, eixo = _criar_figura()
    _desenhar_barras(
        eixo,
        percentuais,
        titulo="Acuracia Top-2 do seletor por tipo de dataset",
        eixo_y="Acuracia Top-2 (%)",
        cor="#7c3aed",
    )
    eixo.set_ylim(0, 100)
    return _salvar_figura(figura, diretorio_saida, "acuracia_tipo_dataset", formatos)


def grafico_overhead_medio(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados(resultados)
    medias = _media_por_chave(registros, "tipo_cenario", "overhead_percentual")

    figura, eixo = _criar_figura()
    _desenhar_barras(
        eixo,
        medias,
        titulo="Overhead medio do seletor por tipo de dataset",
        eixo_y="Overhead medio (%)",
        cor="#ea580c",
    )
    return _salvar_figura(figura, diretorio_saida, "overhead_medio", formatos)


def grafico_comportamento_por_tipo(
    resultados: Iterable[ResultadoBenchmark],
    diretorio_saida: str | Path,
    formatos: Iterable[str] = FORMATOS_PADRAO,
) -> GraficoGerado:
    registros = _normalizar_resultados(resultados)
    _exigir_campos(
        registros,
        {"tipo_cenario", "tamanho", "tempo_segundos"},
        "comportamento por tipo",
    )

    tempos: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    for registro in registros:
        tipo = str(registro["tipo_cenario"])
        tamanho = int(_valor_float(registro, "tamanho"))
        tempo = _valor_float(registro, "tempo_segundos")
        tempos[tipo][tamanho].append(tempo)

    figura, eixo = _criar_figura()
    for tipo, dados_por_tamanho in sorted(tempos.items()):
        tamanhos = sorted(dados_por_tamanho)
        medias = [mean(dados_por_tamanho[tamanho]) for tamanho in tamanhos]
        eixo.plot(tamanhos, medias, marker="o", linewidth=2, label=tipo)

    eixo.set_title("Comportamento por tipo de conjunto de dados")
    eixo.set_xlabel("Tamanho do dataset")
    eixo.set_ylabel("Tempo medio (s)")
    eixo.grid(axis="y", linestyle="--", alpha=0.35)
    eixo.legend(title="Tipo de dataset")
    figura.tight_layout()

    return _salvar_figura(
        figura,
        diretorio_saida,
        "comportamento_tipo_dataset",
        formatos,
    )


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


def _normalizar_resultado(registro: ResultadoBenchmark) -> ResultadoBenchmark:
    normalizado = dict(registro)

    for campo_canonico, aliases in ALIASES_CAMPOS.items():
        if campo_canonico in normalizado:
            continue

        for alias in aliases:
            if alias in normalizado:
                normalizado[campo_canonico] = normalizado[alias]
                break

    cenario = normalizado.get("cenario")
    if cenario:
        partes_cenario = PADRAO_CENARIO_COM_TAMANHO.match(str(cenario))
        if partes_cenario:
            normalizado.setdefault(
                "tipo_cenario",
                _normalizar_tipo_cenario(partes_cenario.group("tipo")),
            )
            normalizado.setdefault("tamanho", int(partes_cenario.group("tamanho")))

    return normalizado


def _normalizar_resultados(
    resultados: Iterable[ResultadoBenchmark],
) -> list[ResultadoBenchmark]:
    return [_normalizar_resultado(dict(resultado)) for resultado in resultados]


def _normalizar_tipo_cenario(valor: str) -> str:
    return valor.strip().lower().replace(" ", "_")


def _desenhar_barras(
    eixo: Any,
    dados: dict[str, float],
    titulo: str,
    eixo_y: str,
    cor: str,
) -> None:
    rotulos = list(dados)
    valores = list(dados.values())

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


def _criar_figura() -> tuple[Any, Any]:
    from matplotlib import pyplot as plt

    return plt.subplots(figsize=(10, 5))


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


def _valor_bool(registro: ResultadoBenchmark, campo: str) -> bool:
    valor = registro[campo]
    if isinstance(valor, bool):
        return valor

    if isinstance(valor, str):
        normalizado = valor.strip().lower()
        if normalizado in {"true", "1", "sim", "yes"}:
            return True
        if normalizado in {"false", "0", "nao", "no"}:
            return False

    return bool(valor)
