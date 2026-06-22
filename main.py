import time
from utils.gerador import gerar_aleatorio, gerar_quase_ordenado, gerar_invertido
from utils.contador import ContadorInstrumentacao
from analisador.caracteristicas import analisar_propriedades_array
from analisador.motor_decisao import selecionar_melhor_algoritmo
from analisador.questionario import executar_questionario

from algoritmos.ordenacao.insertion_sort import insertion_sort
from algoritmos.ordenacao.selection_sort import selection_sort
from algoritmos.ordenacao.bubble_sort import bubble_sort
from algoritmos.ordenacao.merge_sort import merge_sort
from algoritmos.ordenacao.quick_sort import quick_sort
from algoritmos.ordenacao.heap_sort import heap_sort

def rodar_um_teste(nome_teste, array_dados, memoria, estabilidade, modo="direto"):
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
    print(f"Confiança da Recomendação: {decisao.get('confianca', 'Alta (Baseada em Array Real)')}")
    print(f"Complexidade esperada: {decisao['complexidade']}")
    print(f"Memória: {decisao.get('memoria', 'N/A')} | Estável: {decisao.get('estabilidade', 'N/A')}")
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
    
    if modo == "detalhado":
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
    else:
        print("\n\n")

def executar_diagnostico_sistema():
    tamanho = 1000
    
    array_1 = gerar_aleatorio(tamanho)
    rodar_um_teste("VETOR PADRÃO ALEATÓRIO (DIRETO)", array_1, memoria=False, estabilidade=False, modo="direto")
    
    array_2 = gerar_invertido(tamanho)
    rodar_um_teste("VETOR INVERTIDO COM RESTRIÇÃO DE MEMÓRIA (DIRETO)", array_2, memoria=True, estabilidade=False, modo="direto")
    
    array_3 = gerar_quase_ordenado(tamanho)
    rodar_um_teste("VETOR QUASE ORDENADO (DIRETO)", array_3, memoria=False, estabilidade=False, modo="direto")
    
    array_4 = gerar_aleatorio(tamanho)
    rodar_um_teste("EXIGÊNCIA DE ESTABILIDADE NO BECHMARK (DETALHADO)", array_4, memoria=False, estabilidade=True, modo="detalhado")

def rodar_teste_declarado(propriedades):
    print("=" * 65)
    print(" CASO DE TESTE: QUESTIONÁRIO (ENTRADA DECLARADA) ")
    print("=" * 65 + "\n")
    
    print("--- [CAMADA 1: METADADOS DECLARADOS] ---")
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
    
    print("--- [CAMADA 2: DECISÃO DA INTELIGÊNCIA] ---")
    print(f"Algoritmo recomendado: {decisao['recomendado']}")
    print(f"Pontuação: {decisao['pontuacao']}/100")
    print(f"Confiança da Recomendação: {decisao.get('confianca', 'N/A')}")
    print(f"Complexidade esperada: {decisao['complexidade']}")
    print(f"Memória: {decisao.get('memoria', 'N/A')} | Estável: {decisao.get('estabilidade', 'N/A')}")
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
    print("[!] O Benchmark empírico foi ignorado pois não há array real (Modo Declarado).\n\n")

def menu_principal():
    print("=" * 65)
    print(" BEM-VINDO AO SELETOR ADAPTATIVO DE ALGORITMOS ")
    print("=" * 65)
    print("Escolha o modo de execução para a demonstração:")
    print("1. Modo Direto (Apenas recomendação baseada em análise)")
    print("2. Modo Detalhado (Recomendação + Benchmark Empírico completo)")
    print("3. Rodar Bateria de Testes de Diagnóstico (Misto)")
    print("4. Modo Questionário (Responder perguntas sobre o problema)")
    
    opcao = input("Opção (1/2/3/4): ").strip()
    
    if opcao == "4":
        propriedades_declaradas = executar_questionario()
        rodar_teste_declarado(propriedades_declaradas)
    elif opcao in ["1", "2"]:
        modo = "detalhado" if opcao == "2" else "direto"
        print("\n[!] Gerando um array aleatório de exemplo para a demonstração interativa...")
        tamanho_exemplo = 1500
        array_ex = gerar_aleatorio(tamanho_exemplo)
        rodar_um_teste("TESTE DE DEMONSTRAÇÃO INTERATIVA", array_ex, memoria=False, estabilidade=False, modo=modo)
    else:
        print("\n[!] Iniciando bateria de testes de diagnóstico interno...\n")
        executar_diagnostico_sistema()

if __name__ == "__main__":
    menu_principal()