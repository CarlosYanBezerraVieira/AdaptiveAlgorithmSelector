from __future__ import annotations

import argparse
from collections.abc import Sequence

from utils.graficos import carregar_resultados, gerar_graficos_obrigatorios


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gera os graficos obrigatorios do seletor adaptativo.",
    )
    parser.add_argument(
        "--entrada",
        required=True,
        help="Arquivo .json ou .csv com os resultados da validacao empirica.",
    )
    parser.add_argument(
        "--saida",
        default="resultados/graficos",
        help="Diretorio onde os graficos serao salvos.",
    )
    parser.add_argument(
        "--formatos",
        nargs="+",
        default=["png", "pdf"],
        help="Formatos de saida: png, pdf ou svg.",
    )

    args = parser.parse_args(argv)
    resultados = carregar_resultados(args.entrada)
    graficos = gerar_graficos_obrigatorios(resultados, args.saida, args.formatos)

    for grafico in graficos:
        for arquivo in grafico.arquivos:
            print(f"Grafico gerado: {arquivo}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
