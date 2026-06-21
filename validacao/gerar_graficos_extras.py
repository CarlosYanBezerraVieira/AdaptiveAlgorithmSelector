from __future__ import annotations

import argparse
from collections.abc import Sequence

from utils.graficos import carregar_resultados
from utils.graficos_extras import gerar_graficos_extras


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gera graficos extras do seletor adaptativo.",
    )
    parser.add_argument(
        "--entrada",
        required=True,
        help="Arquivo .json ou .csv com os resultados da validacao empirica.",
    )
    parser.add_argument(
        "--saida",
        default="resultados/graficos_extras",
        help="Diretorio onde os graficos extras serao salvos.",
    )
    parser.add_argument(
        "--formatos",
        nargs="+",
        default=["png", "pdf"],
        help="Formatos de saida: png, pdf ou svg.",
    )

    args = parser.parse_args(argv)
    resultados = carregar_resultados(args.entrada)
    graficos = gerar_graficos_extras(resultados, args.saida, args.formatos)

    for grafico in graficos:
        for arquivo in grafico.arquivos:
            print(f"Grafico extra gerado: {arquivo}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
