# Regras do Motor de Decisão

O motor de decisão (`motor_decisao.py`) utiliza um sistema de pontuação dinâmica (Scoring System) para elencar a melhor opção. Cada algoritmo recebe uma pontuação base, que é penalizada ou bonificada de acordo com as características do vetor e as restrições do sistema.

## 1. Regras de Busca

| Condição / Cenário | Ação no Sistema de Pontuação | Justificativa Computacional |
| :--- | :--- | :--- |
| **Vetor desordenado (Inversões > 0)** | Bane imediatamente a **Busca Binária** | Pré-requisito matemático violado. |
| **Vetor perfeitamente ordenado** | Bonifica a **Busca Binária** em +50 pontos | Aproveitamento imediato da redução logarítmica O(log n). |
| **Restrição de Memória ativa** | Penaliza a **Busca Hash** em -40 pontos | Evita o overhead de construção do dicionário O(n). |
| **Buscas Frequentes / Repetitivas** | Bonifica **Binária** e **Hash** (+20) e penaliza **Sequencial** (-30) | Amortização do custo de setup sobre múltiplas consultas rápidas. |
| **Vetores Pequenos (N < 30)** | Bonifica **Busca Sequencial** (+40) | Evita overhead de estruturas complexas para poucos elementos. |

## 2. Regras de Ordenação

### Restrições Rígidas (Hard Constraints)
* **Exigência de Estabilidade:** Bane algoritmos inerentemente instáveis (Quick Sort, Heap Sort, Selection Sort). Bonifica Merge Sort (+40) e Insertion Sort (+10) para preservar a ordem de chaves idênticas.
* **Restrição de Memória RAM:** Bane o Merge Sort (pois requer O(n) de espaço extra). Bonifica algoritmos In-place como Heap Sort (+30) e Quick Sort (+15).
* **Dados em Disco (Paginação):** Bonifica o Merge Sort (+150) por seu padrão de acesso sequencial, e bane virtualmente o Quick e Heap Sort (-80) pelos acessos aleatórios que causam *page faults*.

### Avaliação de Desempenho e Contexto (Soft Constraints)
* **Tamanho do Array:** Algoritmos O(n²) (Bubble, Selection, Insertion) sofrem penalizações matemáticas severas (até -100 pontos) conforme o tamanho N ultrapassa 100 elementos. Algoritmos O(n log n) sofrem penalidades muito leves.
* **Cenário: Vetor Quase Ordenado (Inversão <= 10%):** O **Insertion Sort** recebe um bônus massivo (+100 pontos), pois aproxima-se do seu melhor caso linear O(n), superando opções mais complexas.
* **Cenário: Vetor Altamente Invertido (Inversão >= 85%):** Penaliza severamente o Insertion Sort (-100) e o Quick Sort (-25). Bonifica o Heap Sort (+25) e o Merge Sort (+15), que garantem teto de O(n log n) independentemente da desordem.