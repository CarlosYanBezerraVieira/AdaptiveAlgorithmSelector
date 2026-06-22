import time
from unittest.mock import patch

from algoritmos.busca.busca_binaria import busca_binaria
from algoritmos.busca.busca_hash import TabelaHashInstrumentada
from algoritmos.busca.busca_sequencial import busca_sequencial
from algoritmos.ordenacao.bubble_sort import bubble_sort
from algoritmos.ordenacao.heap_sort import heap_sort
from algoritmos.ordenacao.insertion_sort import insertion_sort
from algoritmos.ordenacao.merge_sort import merge_sort
from algoritmos.ordenacao.quick_sort import quick_sort
from algoritmos.ordenacao.selection_sort import selection_sort
from analisador.caracteristicas import analisar_propriedades_array
from analisador.motor_decisao import selecionar_melhor_algoritmo
from analisador.questionario import executar_questionario
from utils.contador import ContadorInstrumentacao
from utils.gerador import gerar_aleatorio, gerar_invertido, gerar_quase_ordenado


def rodar_um_teste(nome_teste, array_dados, memoria, estabilidade, objetivo="ordenar"):
    print("=" * 65)
    print(f" CASO DE TESTE: {nome_teste} ")
    print("=" * 65 + "\n")
    
    # Analisa as propriedades extraídas do array
    propriedades = analisar_propriedades_array(
        arr=array_dados.copy(), 
        objetivo=objetivo, 
        restricao_memoria=memoria, 
        precisa_estabilidade=estabilidade
    )
    
    print("--- [CAMADA 1: METADADOS DO VETOR] ---")
    print(f"• Tamanho do array: {propriedades['tamanho']}")
    print(f"• Grau de ordenação (Inversões): {propriedades['grau_ordenacao']}")
    print(f"• Percentual de duplicatas: {propriedades['percentual_duplicatas']}%")
    print(f"• Amplitude dos valores: {propriedades['amplitude']}")
    print(f"• Tipo dos dados: {propriedades['tipo_dados']}")
    print(f"• Restrições de memória ativas? {propriedades['restricao_memoria']}")
    print(f"• Necessidade de estabilidade? {propriedades['precisa_estabilidade']}")
    print(f"• Objetivo da operação: {propriedades['objetivo'].upper()}\n")
    
    # Motor de decisão inteligente
    decisao = selecionar_melhor_algoritmo(propriedades)
    
    print("--- [CAMADA 2: DECISÃO DA INTELIGÊNCIA] ---")
    print(f"Algoritmo recomendado: {decisao['recomendado']}")
    print(f"Pontuação: {decisao['pontuacao']}/100")
    print(f"Complexidade esperada: {decisao['complexidade']}")
    print("Justificativas:")
    for just in decisao["justificativas"]:
        print(f"   • {just}")
    if decisao["avisos"]:
        print("Avisos:")
        for aviso in decisao["avisos"]:
            print(f"   • {aviso}")
    print("Alternativas:")
    for alt in decisao["alternativas"]:
        print(f"   • {alt}")
    print("\n" + "-"*65 + "\n")
    
    print(f"--- [CAMADA 3: BENCHMARK GERAL DE VALIDAÇÃO ({objetivo.upper()})] ---")
    
    # Seleciona o dicionário correto de algoritmos baseado no objetivo
    if objetivo == "ordenar":
        algoritmos = {
            "Insertion Sort": insertion_sort,
            "Selection Sort": selection_sort,
            "Bubble Sort": bubble_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort
        }
        
        for nome, funcao in algoritmos.items():
            contador = ContadorInstrumentacao()
            array_copia = array_dados.copy()
            
            tempo_inicio = time.perf_counter()
            funcao(array_copia, contador)
            tempo_fim = time.perf_counter()
            
            metricas = contador.obter_resultados()
            sinalizador = " <- [RECOMENDADO]" if nome == decisao["recomendado"] else ""
            print(f"[{nome}]{sinalizador}")
            print(
                f"   Tempo: {(tempo_fim - tempo_inicio):.5f}s | "
                f"Comparações: {metricas['comparacoes']} | Trocas: {metricas['trocas']}"
            )
            print("." * 40)
            
    elif objetivo == "buscar":
        algoritmos = {
            "Busca Sequencial": busca_sequencial,
            "Busca Binária": busca_binaria,
            "Busca Hash": TabelaHashInstrumentada
        }
        
        # Define um elemento alvo realista para buscar
        # (o elemento que está no meio do array)
        alvo = array_dados[len(array_dados) // 2]
        
        for nome, funcao in algoritmos.items():
            contador = ContadorInstrumentacao()
            array_copia = array_dados.copy()
            
            tempo_inicio = time.perf_counter()
            if nome == "Busca Hash":
                funcao(array_copia).buscar(alvo, contador)
            else:
                funcao(array_copia, alvo, contador)
            tempo_fim = time.perf_counter()
            
            metricas = contador.obter_resultados()
            sinalizador = " <- [RECOMENDADO]" if nome == decisao["recomendado"] else ""
            print(f"[{nome}]{sinalizador}")
            # Em busca não existem "Trocas" (swaps), por isso printamos apenas
            # iterações/comparações.
            print(
                f"   Tempo: {(tempo_fim - tempo_inicio):.6f}s | "
                f"Comparações/Acessos: {metricas['comparacoes']}"
            )
            print("." * 40)
            
    print("\n\n")


def rodar_teste_questionario(nome_teste, respostas_questionario):
    print("=" * 65)
    print(f" CASO DE TESTE: {nome_teste} ")
    print("=" * 65 + "\n")

    with patch("builtins.input", side_effect=respostas_questionario):
        propriedades = executar_questionario()

    print("--- [CAMADA 1: METADADOS DECLARADOS] ---")
    print(f"• Origem dos dados: {propriedades.get('origem', 'Declarada')}")
    print(f"• Tamanho estimado: {propriedades['tamanho']}")
    print(f"• Grau de ordenação declarado: {propriedades['grau_ordenacao']}")
    print(f"• Percentual de duplicatas: {propriedades['percentual_duplicatas']}%")
    print(f"• Tipo dos dados: {propriedades['tipo_dados']}")
    print(f"• Restrições de memória ativas? {propriedades['restricao_memoria']}")
    print(
        "• Necessidade de estabilidade? "
        f"{propriedades.get('precisa_estabilidade', False)}"
    )
    print(f"• Objetivo da operação: {propriedades['objetivo'].upper()}")
    print(f"• Dados em disco/paginação? {propriedades.get('dados_em_disco', False)}")
    print(f"• Busca frequente? {propriedades.get('busca_frequente', False)}\n")

    decisao = selecionar_melhor_algoritmo(propriedades)

    print("--- [CAMADA 2: DECISÃO DA INTELIGÊNCIA] ---")
    print(f"Algoritmo recomendado: {decisao['recomendado']}")
    print(f"Pontuação: {decisao['pontuacao']}/100")
    print(f"Complexidade esperada: {decisao['complexidade']}")
    print("Justificativas:")
    for just in decisao["justificativas"]:
        print(f"   • {just}")
    if decisao["avisos"]:
        print("Avisos:")
        for aviso in decisao["avisos"]:
            print(f"   • {aviso}")
    print("Alternativas:")
    for alt in decisao["alternativas"]:
        print(f"   • {alt}")

    print("\n" + "-" * 65 + "\n")
    print(
        "--- [CAMADA 3: BENCHMARK GERAL DE VALIDAÇÃO (QUESTIONÁRIO)] ---"
    )
    print("Benchmark ignorado: este cenário usa entrada declarada, sem array real.")
    print("\n\n")


def executar_diagnostico_sistema():
    tamanho = 1000
    
    # ==========================================
    # TESTES DE ORDENAÇÃO
    # ==========================================
    array_1 = gerar_aleatorio(tamanho)
    rodar_um_teste(
        "VETOR PADRÃO ALEATÓRIO",
        array_1,
        memoria=False,
        estabilidade=False,
        objetivo="ordenar",
    )
    
    array_2 = gerar_invertido(tamanho)
    rodar_um_teste(
        "VETOR INVERTIDO COM RESTRIÇÃO DE MEMÓRIA",
        array_2,
        memoria=True,
        estabilidade=False,
        objetivo="ordenar",
    )
    
    array_3 = gerar_quase_ordenado(tamanho)
    rodar_um_teste(
        "VETOR QUASE ORDENADO",
        array_3,
        memoria=False,
        estabilidade=False,
        objetivo="ordenar",
    )
    
    array_4 = gerar_aleatorio(tamanho)
    rodar_um_teste(
        "EXIGÊNCIA DE ESTABILIDADE NO BENCHMARK",
        array_4,
        memoria=False,
        estabilidade=True,
        objetivo="ordenar",
    )

    # ==========================================
    # TESTES DE BUSCA (NOVOS)
    # ==========================================
    # Cenário 5: Busca em Vetor NÃO ordenado (Deve banir Busca Binária)
    array_5 = gerar_aleatorio(tamanho)
    rodar_um_teste(
        "BUSCA EM DADOS NÃO ORDENADOS",
        array_5,
        memoria=False,
        estabilidade=False,
        objetivo="buscar",
    )
    
    # Cenário 6: Busca em Vetor Ordenado (Perfeito para Busca Binária)
    # Garantimos que o grau_ordenacao seja 0.0.
    array_6 = sorted(gerar_aleatorio(tamanho))
    rodar_um_teste(
        "BUSCA EM VETOR 100% ORDENADO",
        array_6,
        memoria=False,
        estabilidade=False,
        objetivo="buscar",
    )

    # Cenário 7: Busca em Vetor Ordenado com Restrição de Memória
    # (Bane/Penaliza Hash).
    array_7 = sorted(gerar_aleatorio(tamanho))
    rodar_um_teste(
        "BUSCA COM RESTRIÇÃO SEVERA DE MEMÓRIA",
        array_7,
        memoria=True,
        estabilidade=False,
        objetivo="buscar",
    )

    # ==========================================
    # TESTE DE QUESTIONÁRIO (NOVO)
    # ==========================================
    rodar_teste_questionario(
        "QUESTIONÁRIO - BUSCA REPETITIVA COM TIPO COMPLEXO",
        ["2", "1", "1", "S", "S", "2", "2"],
    )

if __name__ == "__main__":
    executar_diagnostico_sistema()
