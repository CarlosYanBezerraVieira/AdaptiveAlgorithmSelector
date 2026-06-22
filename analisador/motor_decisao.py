from analisador.algorithm_metadata import METADADOS_BUSCA, METADADOS_ORDENACAO
from utils.constants import (
    GRAU_ALTAMENTE_INVERTIDO,
    GRAU_INVERSAO_ALTO_QUICK,
    GRAU_QUASE_ORDENADO_IDEAL,
    GRAU_QUASE_ORDENADO_LIMITE_INSERTION,
    LIMITE_TAMANHO_BUSCA_PEQUENA,
    LIMITE_TAMANHO_ORDENACAO_MEDIO,
    LIMITE_TAMANHO_QUASE_ORDENADO,
    PONTUACAO_BANIDO,
    PONTUACAO_CORTE_ALTERNATIVA,
    SCORE_BASE_BUBBLE,
    SCORE_BASE_BUSCA_BINARIA,
    SCORE_BASE_BUSCA_HASH,
    SCORE_BASE_BUSCA_SEQUENCIAL,
    SCORE_BASE_HEAP,
    SCORE_BASE_INSERTION,
    SCORE_BASE_MERGE,
    SCORE_BASE_QUICK,
    SCORE_BASE_SELECTION,
)
from utils.enums import (
    AlgoritmoBusca,
    AlgoritmoOrdenacao,
    Objetivo,
    OrigemMetricas,
    TipoDados,
)


def selecionar_melhor_algoritmo(propriedades):
    tamanho = propriedades.get("tamanho", 0)
    grau_ordenacao = propriedades.get("grau_ordenacao", 0.0)
    percentual_duplicatas = propriedades.get("percentual_duplicatas", 0.0)
    restricao_memoria = propriedades.get("restricao_memoria", False)
    precisa_estabilidade = propriedades.get("precisa_estabilidade", False)
    objetivo = propriedades.get("objetivo", Objetivo.ORDENAR.value)

    # Novos parâmetros do Modo Questionário
    origem = propriedades.get("origem", OrigemMetricas.MEDIDA.value)
    tipo_dados = propriedades.get("tipo_dados", TipoDados.INT.value)
    dados_em_disco = propriedades.get("dados_em_disco", False)
    busca_frequente = propriedades.get("busca_frequente", False)

    confianca = (
        "Média (Baseada em Respostas)"
        if origem == OrigemMetricas.DECLARADA.value
        else "Alta (Baseada em Array Real)"
    )

    # =================================================================
    # FLUXO DE DECISÃO: BUSCA
    # =================================================================
    if objetivo == Objetivo.BUSCAR.value:
        # Base de pontuação inicial para algoritmos de busca
        pontuacao = {
            AlgoritmoBusca.SEQUENCIAL.value: SCORE_BASE_BUSCA_SEQUENCIAL,
            AlgoritmoBusca.BINARIA.value: SCORE_BASE_BUSCA_BINARIA,
            AlgoritmoBusca.HASH.value: SCORE_BASE_BUSCA_HASH,
        }

        # RESTRIÇÃO RÍGIDA: Busca Binária EXIGE ordenação absoluta (grau deve ser estritamente 0.0)
        if grau_ordenacao > 0.0:
            pontuacao[AlgoritmoBusca.BINARIA.value] = (
                PONTUACAO_BANIDO  # Banida por violação de pré-requisito matemático
            )
        else:
            pontuacao[AlgoritmoBusca.BINARIA.value] += (
                50  # Altamente recomendada se o vetor estiver ordenado
            )

        # Restrição de Memória afeta a Busca Hash (tabelas hash exigem overhead de espaço)
        if restricao_memoria:
            pontuacao[AlgoritmoBusca.HASH.value] -= 40

        # Nova Regra: Frequência de Busca
        if busca_frequente:
            pontuacao[AlgoritmoBusca.BINARIA.value] += 20
            pontuacao[AlgoritmoBusca.HASH.value] += 20
            pontuacao[AlgoritmoBusca.SEQUENCIAL.value] -= 30
        elif origem == OrigemMetricas.DECLARADA.value and not busca_frequente:
            pontuacao[AlgoritmoBusca.SEQUENCIAL.value] += 30

        # Vetores muito pequenos dispensam estruturas complexas ou ordenação prévia
        if tamanho < LIMITE_TAMANHO_BUSCA_PEQUENA:
            pontuacao[AlgoritmoBusca.SEQUENCIAL.value] += 40
            if pontuacao[AlgoritmoBusca.HASH.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoBusca.HASH.value] -= 20
        else:
            # Penalização por tempo linear O(n) para busca sequencial em tamanhos maiores
            penalidade_n = min(60, tamanho // 100)
            if pontuacao[AlgoritmoBusca.SEQUENCIAL.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoBusca.SEQUENCIAL.value] -= penalidade_n

        # Determinação do vencedor e filtragem de alternativas válidas (não banidas)
        melhor = max(pontuacao, key=pontuacao.get)
        alternativas = [
            alg
            for alg in pontuacao
            if alg != melhor and pontuacao[alg] > PONTUACAO_CORTE_ALTERNATIVA
        ]
        alternativas = sorted(alternativas, key=lambda x: pontuacao[x], reverse=True)[
            :2
        ]

        # Geração de Justificativas Dinâmicas e Coerentes baseadas em Metadados
        justificativas = []
        avisos = []

        if melhor == AlgoritmoBusca.HASH.value:
            justificativas.append(
                "Permite indexação direta com tempo de busca constante O(1)."
            )
            justificativas.append(
                "Ideal para máxima eficiência computacional quando há memória disponível."
            )
            if restricao_memoria:
                avisos.append(
                    "Aviso: A tabela hash consome memória extra para o mapeamento de chaves."
                )

        elif melhor == AlgoritmoBusca.BINARIA.value:
            justificativas.append(
                f"O vetor está perfeitamente ordenado (Grau de inversão: {grau_ordenacao})."
            )
            justificativas.append(
                "Reduz o espaço de busca de forma logarítmica a cada iteração."
            )

        elif melhor == AlgoritmoBusca.SEQUENCIAL.value:
            if grau_ordenacao > 0.0:
                justificativas.append(
                    f"O vetor está desordenado (Grau de inversão: {grau_ordenacao}), tornando a busca binária inviável."
                )
            else:
                justificativas.append(
                    f"O volume de dados é muito reduzido para justificar estruturas complexas ({tamanho} elementos)."
                )
            justificativas.append(
                "Evita o overhead de processamento com tabelas hash ou ordenações prévias."
            )

        return {
            "recomendado": melhor,
            "pontuacao": min(100, max(0, pontuacao[melhor])),
            "complexidade": METADADOS_BUSCA[melhor]["complexidade"],
            "memoria": METADADOS_BUSCA[melhor]["memoria"],
            "estabilidade": METADADOS_BUSCA[melhor]["estavel"],
            "confianca": confianca,
            "justificativas": justificativas,
            "avisos": avisos,
            "alternativas": alternativas,
        }

    # =================================================================
    # FLUXO DE DECISÃO: ORDENAÇÃO
    # =================================================================
    else:
        # 1. Base de pontuação inicial equilibrada
        pontuacao = {
            AlgoritmoOrdenacao.INSERTION.value: SCORE_BASE_INSERTION,
            AlgoritmoOrdenacao.SELECTION.value: SCORE_BASE_SELECTION,
            AlgoritmoOrdenacao.BUBBLE.value: SCORE_BASE_BUBBLE,
            AlgoritmoOrdenacao.MERGE.value: SCORE_BASE_MERGE,
            AlgoritmoOrdenacao.QUICK.value: SCORE_BASE_QUICK,
            AlgoritmoOrdenacao.HEAP.value: SCORE_BASE_HEAP,
        }

        # 2. RESTRIÇÕES RÍGIDAS (HARD CONSTRAINTS) - BANIMENTOS ABSOLUTOS

        # Se exige ESTABILIDADE, bane algoritmos inerentemente instáveis
        if precisa_estabilidade:
            pontuacao[AlgoritmoOrdenacao.QUICK.value] = PONTUACAO_BANIDO
            pontuacao[AlgoritmoOrdenacao.HEAP.value] = PONTUACAO_BANIDO
            pontuacao[AlgoritmoOrdenacao.SELECTION.value] = PONTUACAO_BANIDO

            pontuacao[AlgoritmoOrdenacao.MERGE.value] += 40
            pontuacao[AlgoritmoOrdenacao.INSERTION.value] += 10

        # Se há RESTRIÇÃO DE MEMÓRIA, bane o Merge Sort (alocação auxiliar O(n))
        if restricao_memoria:
            pontuacao[AlgoritmoOrdenacao.MERGE.value] = PONTUACAO_BANIDO

            # Valoriza alternativas estáveis em espaço (In-place)
            if pontuacao[AlgoritmoOrdenacao.HEAP.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.HEAP.value] += 30
            if (
                pontuacao[AlgoritmoOrdenacao.QUICK.value] > PONTUACAO_BANIDO
                and grau_ordenacao < GRAU_INVERSAO_ALTO_QUICK
            ):
                pontuacao[AlgoritmoOrdenacao.QUICK.value] += 15

        # Nova Regra: Dados em Disco (Paginação)
        if dados_em_disco:
            if pontuacao[AlgoritmoOrdenacao.MERGE.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.MERGE.value] += (
                    150  # Merge Sort brilha em ordenação externa
                )
            if pontuacao[AlgoritmoOrdenacao.QUICK.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.QUICK.value] -= 80  # Péssimo com paginação
            if pontuacao[AlgoritmoOrdenacao.HEAP.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.HEAP.value] -= 80

        # Penalização progressiva por tempo de execução baseada no tamanho
        if tamanho > LIMITE_TAMANHO_ORDENACAO_MEDIO:
            # Deduz até 100 pontos dependendo do quão grande o array é para algoritmos O(n²)
            penalidade_n2 = min(100, tamanho // 50)
            if pontuacao[AlgoritmoOrdenacao.SELECTION.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.SELECTION.value] -= penalidade_n2
            if pontuacao[AlgoritmoOrdenacao.BUBBLE.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.BUBBLE.value] -= penalidade_n2

            # Insertion Sort sofre penalidade O(n²) se não estiver quase ordenado
            if (
                pontuacao[AlgoritmoOrdenacao.INSERTION.value] > PONTUACAO_BANIDO
                and grau_ordenacao > GRAU_QUASE_ORDENADO_LIMITE_INSERTION
            ):
                pontuacao[AlgoritmoOrdenacao.INSERTION.value] -= penalidade_n2

            # Algoritmos O(n log n) também têm uma penalidade levíssima pelo tempo, mas muito menor
            penalidade_nlogn = min(15, tamanho // 1000)
            if pontuacao[AlgoritmoOrdenacao.MERGE.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.MERGE.value] -= penalidade_nlogn
            if pontuacao[AlgoritmoOrdenacao.QUICK.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.QUICK.value] -= penalidade_nlogn
            if pontuacao[AlgoritmoOrdenacao.HEAP.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.HEAP.value] -= penalidade_nlogn

        # 3. ANÁLISE DE CENÁRIOS CONTEXTUAIS (DESEMPENHO PRÁTICO)

        # CENÁRIO A: Vetor Quase Ordenado
        if (
            grau_ordenacao <= GRAU_QUASE_ORDENADO_IDEAL
            and tamanho <= LIMITE_TAMANHO_QUASE_ORDENADO
        ):
            if pontuacao[AlgoritmoOrdenacao.INSERTION.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.INSERTION.value] += 100
            if pontuacao[AlgoritmoOrdenacao.QUICK.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.QUICK.value] -= 20
            if pontuacao[AlgoritmoOrdenacao.HEAP.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.HEAP.value] -= 20

        # CENÁRIO B: Vetor Altamente Invertido (Pior caso do Quick Sort clássico)
        elif grau_ordenacao >= GRAU_ALTAMENTE_INVERTIDO:
            if pontuacao[AlgoritmoOrdenacao.HEAP.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.HEAP.value] += 25
            if pontuacao[AlgoritmoOrdenacao.MERGE.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.MERGE.value] += 15
            if pontuacao[AlgoritmoOrdenacao.QUICK.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.QUICK.value] -= 25
            if pontuacao[AlgoritmoOrdenacao.INSERTION.value] > PONTUACAO_BANIDO:
                pontuacao[AlgoritmoOrdenacao.INSERTION.value] -= (
                    100  # Penalidade severa: Pior caso O(n²) real
                )

        # 4. FILTRAGEM SEGURA DE ALTERNATIVAS
        melhor = max(pontuacao, key=pontuacao.get)

        # Bloqueia qualquer possibilidade de algoritmos banidos entrarem na lista
        alternativas = [
            alg
            for alg in pontuacao
            if alg != melhor and pontuacao[alg] > PONTUACAO_CORTE_ALTERNATIVA
        ]
        alternativas = sorted(alternativas, key=lambda x: pontuacao[x], reverse=True)[
            :2
        ]

        # 5. GERAÇÃO DE JUSTIFICATIVAS CONTEXTUAIS
        justificativas = []
        if melhor == AlgoritmoOrdenacao.QUICK.value:
            justificativas.append(
                f"O vetor está misturado de forma homogênea (Grau de inversão: {grau_ordenacao})."
            )
            justificativas.append(
                "O cenário não impõe limites de memória ou necessidade de estabilidade."
            )
            justificativas.append(
                "Estatisticamente, apresenta a menor constante de tempo de execução prática."
            )

        elif melhor == AlgoritmoOrdenacao.HEAP.value:
            justificativas.append(
                f"O array exibe alto índice de inversão estrutural (Grau de inversão: {grau_ordenacao})."
            )
            justificativas.append(
                "Há restrições severas de memória em tempo de execução."
            )
            justificativas.append(
                "Garante o teto logarítmico O(n log n) trabalhando de forma In-place (Espaço O(1))."
            )

        elif melhor == AlgoritmoOrdenacao.INSERTION.value:
            justificativas.append(
                f"Detectada pré-ordenação quase completa dos elementos (Grau de inversão: {grau_ordenacao})."
            )
            justificativas.append(
                "Sob esta condição, o algoritmo opera de forma linear, aproximando-se de O(n)."
            )
            justificativas.append(
                "Reduz drasticamente os ciclos de CPU ao mitigar trocas e deslocamentos de ponteiros."
            )

        elif melhor == AlgoritmoOrdenacao.MERGE.value:
            justificativas.append(
                "A estabilidade da ordenação foi definida como requisito crítico de negócio."
            )
            justificativas.append(
                "Assegura que registros com chaves equivalentes mantenham suas posições relativas originais."
            )
            justificativas.append(
                "Mantém o comportamento assintótico previsível de O(n log n) sob qualquer distribuição."
            )

        # Tratamento de Avisos do Sistema
        avisos = []
        if melhor == AlgoritmoOrdenacao.MERGE.value:
            avisos.append(
                "Este algoritmo aloca memória adicional proporcional ao tamanho do array original."
            )
        if (
            melhor == AlgoritmoOrdenacao.QUICK.value
            and grau_ordenacao >= GRAU_INVERSAO_ALTO_QUICK
        ):
            avisos.append(
                "Aviso: Alto grau de inversão detectado. Risco latente de degradação caso ocorra má distribuição do pivô."
            )
        if (
            tipo_dados == TipoDados.OBJECT.value
            and METADADOS_ORDENACAO[melhor]["estavel"] == "Não"
        ):
            avisos.append(
                "Aviso: Elementos são objetos complexos, mas o algoritmo escolhido não é estável. Pode bagunçar campos secundários."
            )
        if dados_em_disco and melhor == AlgoritmoOrdenacao.MERGE.value:
            justificativas.append(
                "Excelente escolha para Ordenação Externa (dados que não cabem na RAM) por causa de seus acessos sequenciais."
            )

        return {
            "recomendado": melhor,
            "pontuacao": min(100, max(0, pontuacao[melhor])),
            "complexidade": METADADOS_ORDENACAO[melhor]["complexidade"],
            "memoria": METADADOS_ORDENACAO[melhor]["memoria"],
            "estabilidade": METADADOS_ORDENACAO[melhor]["estavel"],
            "confianca": confianca,
            "justificativas": justificativas,
            "avisos": avisos,
            "alternativas": alternativas,
        }
