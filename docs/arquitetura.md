# Arquitetura do Sistema

O **Adaptive Algorithm Selector** é um sistema projetado para analisar conjuntos de dados ou restrições não-funcionais e recomendar o algoritmo de ordenação ou busca mais eficiente para o contexto específico. 

O projeto adota uma arquitetura modular baseada em responsabilidades bem definidas, facilitando a manutenção, a inclusão de novos algoritmos e a execução de testes empíricos.

## Visão Geral dos Módulos

O sistema é dividido nas seguintes camadas principais:

* **CLI (`cli.py`, `main.py`):** Interface de linha de comando que interage com o usuário, captura os dados (diretamente ou via questionário) e exibe as recomendações e os resultados dos benchmarks.
* **Analisador:** Camada responsável por extrair metadados do vetor de dados e processar a lógica de pontuação. No ecossistema atual, essa responsabilidade está concentrada em `caracteristicas.py` (extração de propriedades) e `motor_decisao.py` (inteligência de seleção).
* **Algoritmos (`/algoritmos/`):** Implementações puras dos algoritmos de busca e ordenação. Eles são isolados da lógica de decisão e injetados com um `ContadorInstrumentacao` para coletar métricas de desempenho in-place.
* **Utilitários (`/utils/`):** Contém geradores de arrays de teste, constantes de pontuação, enumeradores e o motor de benchmark que avalia o consumo de memória e tempo de CPU.
* **Validação (`/validacao/`):** Ferramentas para gerar gráficos de desempenho e calcular as métricas exigidas para a validação estatística do seletor.

## Fluxo de Execução Principal

1. **Entrada de Dados:** O usuário fornece um array (Modo Direto) ou responde a perguntas sobre as restrições do ambiente (Modo Questionário).
2. **Extração de Metadados (`caracteristicas.py`):** O sistema calcula o grau de ordenação (inversões), detecta duplicatas, mede a amplitude e identifica o tipo de dado.
3. **Motor de Decisão (`motor_decisao.py`):** Com base nos metadados, o motor inicia um sistema de pontuação. Restrições rígidas (como falta de memória) banem certos algoritmos, enquanto características favoráveis (como array já quase ordenado) bonificam outros.
4. **Recomendação (`recommendation.py`):** O algoritmo com maior pontuação final é selecionado. O sistema apresenta justificativas e alertas de forma dinâmica.
5. **Benchmark (`benchmark.py`):** Se solicitado, o sistema executa os algoritmos contra o conjunto de dados real, permitindo a comparação de tempo, memória, trocas e comparações do algoritmo recomendado versus os demais.