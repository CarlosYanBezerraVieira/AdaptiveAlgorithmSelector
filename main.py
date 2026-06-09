import time
from utils.gerador import gerar_aleatorio, gerar_quase_ordenado, gerar_invertido
from utils.contador import ContadorInstrumentacao
from analisador.caracteristicas import analisar_propriedades_array
from analisador.motor_decisao import selecionar_melhor_algoritmo

from algoritmos.ordenacao.insertion_sort import insertion_sort
from algoritmos.ordenacao.selection_sort import selection_sort
from algoritmos.ordenacao.bubble_sort import bubble_sort
from algoritmos.ordenacao.merge_sort import merge_sort
from algoritmos.ordenacao.quick_sort import quick_sort
from algoritmos.ordenacao.heap_sort import heap_sort

def rodar_um_teste(nome_teste, array_dados, memoria, estabilidade):
    print("=" * 65)
    print(f" CASO DE TESTE: {nome_teste} ")
    print("=" * 65 + "\n")
    
    # Passamos uma cópia para a análise não gerar subprodutos no array original
    propriedades = analisar_propriedades_array(
        arr=array_dados.copy(), 
        objetivo="ordenar", 
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
    
    print("--- [CAMADA 3: BENCHMARK GERAL DE VALIDAÇÃO] ---")
    algoritmos_ordenacao = {
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort
    }
    
    for nome, funcao in algoritmos_ordenacao.items():
        contador = ContadorInstrumentacao()
        
        # CORREÇÃO CRÍTICA: Cada algoritmo recebe uma cópia idêntica e ISOLADA do array original
        array_copia = array_dados.copy()
        
        tempo_inicio = time.perf_counter()
        array_resultado = funcao(array_copia, contador)
        tempo_fim = time.perf_counter()
        
        tempo_total = tempo_fim - tempo_inicio
        metricas = contador.obter_resultados()
        
        sinalizador = " <- [RECOMENDADO]" if nome == decisao["recomendado"] else ""
        print(f"[{nome}]{sinalizador}")
        print(f"   Tempo: {tempo_total:.5f}s | Comparações: {metricas['comparacoes']} | Trocas: {metricas['trocas']}")
        print("." * 40)
    print("\n\n")

def executar_diagnostico_sistema():
    tamanho = 1000
    
    array_1 = gerar_aleatorio(tamanho)
    rodar_um_teste("VETOR PADRÃO ALEATÓRIO", array_1, memoria=False, estabilidade=False)
    
    array_2 = gerar_invertido(tamanho)
    rodar_um_teste("VETOR INVERTIDO COM RESTRIÇÃO DE MEMÓRIA", array_2, memoria=True, estabilidade=False)
    
    array_3 = gerar_quase_ordenado(tamanho)
    rodar_um_teste("VETOR QUASE ORDENADO", array_3, memoria=False, estabilidade=False)
    
    array_4 = gerar_aleatorio(tamanho)
    rodar_um_teste("EXIGÊNCIA DE ESTABILIDADE NO BECHMARK", array_4, memoria=False, estabilidade=True)

if __name__ == "__main__":
    executar_diagnostico_sistema()