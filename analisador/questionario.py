from utils.enums import Objetivo, OrigemMetricas, TipoDados


def executar_questionario():
    print("=" * 65)
    print(" QUESTIONÁRIO DE ANÁLISE DECLARADA ")
    print("=" * 65)

    propriedades = {
        "origem": OrigemMetricas.DECLARADA.value,
        "tamanho": 1000,
        "grau_ordenacao": 0.5,
        "percentual_duplicatas": 0.0,
        "amplitude": 1000,
        "tipo_dados": TipoDados.INT.value,
        "restricao_memoria": False,
        "precisa_estabilidade": False,
        "objetivo": Objetivo.ORDENAR.value,
        "dados_em_disco": False,
        "busca_frequente": False,
    }

    print("\n1. Qual é o seu objetivo principal?")
    print("   [1] Ordenar dados")
    print("   [2] Buscar um dado")
    obj = input("-> ")
    propriedades["objetivo"] = (
        Objetivo.BUSCAR.value if obj == "2" else Objetivo.ORDENAR.value
    )

    print("\n2. Qual é a estimativa do número de elementos?")
    print("   [1] Pequeno (até 100)")
    print("   [2] Médio (de 100 a 10.000)")
    print("   [3] Grande (mais de 10.000)")
    tam = input("-> ")
    if tam == "1":
        propriedades["tamanho"] = 50
    elif tam == "3":
        propriedades["tamanho"] = 100000
    else:
        propriedades["tamanho"] = 5000

    if propriedades["objetivo"] == Objetivo.ORDENAR.value:
        print("\n3. Como você descreveria a desordem atual dos dados?")
        print("   [1] Quase ordenados")
        print("   [2] Totalmente aleatórios")
        print("   [3] Invertidos (ordem decrescente mas quero crescente)")
        ordem = input("-> ")
        if ordem == "1":
            propriedades["grau_ordenacao"] = 0.05
        elif ordem == "3":
            propriedades["grau_ordenacao"] = 1.0
        else:
            propriedades["grau_ordenacao"] = 0.5
    else:
        print("\n3. Os dados já se encontram ordenados no momento da busca?")
        print("   [1] Sim")
        print("   [2] Não")
        ordem = input("-> ")
        propriedades["grau_ordenacao"] = 0.0 if ordem == "1" else 0.5

    print("\n4. Existem muitos valores repetidos/duplicados no conjunto?")
    dup = input("   [S] Sim / [N] Não -> ").strip().upper()
    if dup == "S":
        propriedades["percentual_duplicatas"] = 50.0

    if propriedades["objetivo"] == Objetivo.ORDENAR.value:
        print(
            (
                "\n5. A estabilidade do algoritmo é obrigatória? "
                "(Manter a ordem original de itens iguais)"
            )
        )
        est = input("   [S] Sim / [N] Não -> ").strip().upper()
        if est == "S":
            propriedades["precisa_estabilidade"] = True

    print(
        "\n6. Existe alguma restrição severa de memória no ambiente em que vai rodar?"
    )
    mem = input("   [S] Sim / [N] Não -> ").strip().upper()
    if mem == "S":
        propriedades["restricao_memoria"] = True

    print(
        (
            "\n7. Os elementos são numéricos simples "
            "ou objetos complexos (ex: dicionários/instâncias)?"
        )
    )
    print("   [1] Simples")
    print("   [2] Complexos")
    tipo = input("-> ")
    if tipo == "2":
        propriedades["tipo_dados"] = TipoDados.OBJECT.value

    if propriedades["objetivo"] == Objetivo.ORDENAR.value:
        print(
            (
                "\n8. Os dados cabem inteiramente na memória RAM "
                "ou vêm de um arquivo enorme (disco)?"
            )
        )
        print("   [1] Cabem na RAM")
        print("   [2] Vêm de um arquivo gigante (Paginação)")
        disco = input("-> ")
        if disco == "2":
            propriedades["dados_em_disco"] = True
    else:
        print(
            (
                "\n8. Você fará essa busca apenas uma vez "
                "ou buscará milhares de vezes no mesmo conjunto?"
            )
        )
        print("   [1] Uma vez")
        print("   [2] Milhares de vezes")
        freq = input("-> ")
        if freq == "2":
            propriedades["busca_frequente"] = True

    print("\n[!] Questionário finalizado. Processando recomendação...\n")
    return propriedades
