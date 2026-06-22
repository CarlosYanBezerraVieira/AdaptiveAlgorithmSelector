from analisador.caracteristicas import analisar_propriedades_array
from analisador.motor_decisao import selecionar_melhor_algoritmo
from analisador.questionario import executar_questionario
from analisador.recommendation import gerar_relatorio_recomendacao
from utils.benchmark import rodar_benchmarks_gerais


def executar_analise_array(array_dados, objetivo, modo="direto"):
    print("\n" + "=" * 65)
    print(f" ANÁLISE DE ARRAY INFORMADO - OBJETIVO: {objetivo.upper()} ")
    print("=" * 65 + "\n")

    propriedades = analisar_propriedades_array(
        arr=array_dados.copy(),
        objetivo=objetivo,
        restricao_memoria=False,
        precisa_estabilidade=False,
    )

    print("--- [ METADADOS DO VETOR ] ---")
    print(f"• Tamanho do array: {propriedades['tamanho']}")
    print(f"• Grau de ordenação (Inversões): {propriedades['grau_ordenacao']}")
    print(f"• Percentual de duplicatas: {propriedades['percentual_duplicatas']}%")
    print(f"• Amplitude dos valores: {propriedades['amplitude']}")
    print(f"• Tipo dos dados: {propriedades['tipo_dados']}")
    print(f"• Objetivo da operação: {propriedades['objetivo'].upper()}\n")

    decisao = selecionar_melhor_algoritmo(propriedades)

    print(gerar_relatorio_recomendacao(decisao))
    print("\n" + "-" * 65 + "\n")

    if modo == "detalhado":
        rodar_benchmarks_gerais(array_dados, decisao["recomendado"])
    else:
        print("\n\n")


def ler_array_usuario():
    while True:
        entrada = input(
            "\nDigite os valores do array separados por vírgula "
            "(ex: 10, 3, 7, 1): "
        ).strip()

        if not entrada:
            print("[!] O array não pode estar vazio.")
            continue

        try:
            return [int(valor.strip()) for valor in entrada.split(",") if valor.strip()]
        except ValueError:
            print(
                "[!] Entrada inválida. Digite apenas números inteiros "
                "separados por vírgula."
            )


def perguntar_objetivo():
    while True:
        print("\nO que você deseja fazer com este array?")
        print("1. Ordenar os dados")
        print("2. Buscar um valor específico")
        opcao = input("Opção (1/2): ").strip()
        
        if opcao == "1":
            return "ordenar"
        elif opcao == "2":
            return "buscar"
        
        print("[!] Opção inválida. Digite 1 ou 2.")


def executar_analise_questionario(propriedades):
    print("=" * 65)
    print(" ANÁLISE BASEADA NO QUESTIONÁRIO ")
    print("=" * 65 + "\n")

    print("--- [ METADADOS DECLARADOS ] ---")
    print(f"• Tamanho estimado: {propriedades['tamanho']}")
    print(f"• Grau de ordenação (Inversões aproximadas): {propriedades['grau_ordenacao']}")
    print(f"• Percentual de duplicatas: {propriedades['percentual_duplicatas']}%")
    print(f"• Tipo dos dados: {propriedades.get('tipo_dados', 'int')}")
    print(f"• Restrições de memória ativas? {propriedades.get('restricao_memoria', False)}")
    print(f"• Necessidade de estabilidade? {propriedades.get('precisa_estabilidade', False)}")
    print(f"• Objetivo da operação: {propriedades.get('objetivo', 'ordenar').upper()}")
    print(f"• Dados em disco/paginação? {propriedades.get('dados_em_disco', False)}")
    print(f"• Busca frequente? {propriedades.get('busca_frequente', False)}\n")

    decisao = selecionar_melhor_algoritmo(propriedades)

    print(gerar_relatorio_recomendacao(decisao))
    print("\n" + "-" * 65 + "\n")


def menu_principal():
    print("=" * 65)
    print(" BEM-VINDO AO SELETOR ADAPTATIVO DE ALGORITMOS ")
    print("=" * 65)
    print("Como você deseja informar os dados para análise?")
    print("1. Digitar o array manualmente (Análise Direta)")
    print("2. Digitar o array manualmente (Análise + Benchmark/Tempo)")
    print("3. Responder o Questionário (Não tenho o array em mãos)")

    opcao = input("\nOpção (1/2/3): ").strip()

    if opcao == "3":
        propriedades_declaradas = executar_questionario()
        executar_analise_questionario(propriedades_declaradas)
    elif opcao in ["1", "2"]:
        modo = "detalhado" if opcao == "2" else "direto"
        
        # 1º: Pega o array do usuário
        array_usuario = ler_array_usuario()
        
        # 2º: Pergunta o que ele quer fazer (ordenar ou buscar)
        objetivo_usuario = perguntar_objetivo()
        
        # 3º: Roda a análise passando o array e o objetivo corretos
        executar_analise_array(array_usuario, objetivo=objetivo_usuario, modo=modo)
    else:
        print("\n[!] Opção inválida.")


if __name__ == "__main__":
    menu_principal()