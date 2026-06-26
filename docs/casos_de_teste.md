# Casos de Teste (Suíte de Validação)

Este documento mapeia formalmente a suíte de validação contida no script de testes (`testes/mainb.py`). Cada caso estressa uma ramificação específica do Motor de Decisão.

## Mapeamento dos Cenários

### CT-01: Vetor Padrão Aleatório
* **Configuração:** Tamanho N = 1000, Distribuição aleatória, Sem restrição de memória, Sem exigência de estabilidade.
* **Comportamento Esperado:** Recomendação do `Quick Sort` (devido à constante de tempo menor na prática).

### CT-02: Vetor Invertido com Restrição de Memória
* **Configuração:** Dados em ordem decrescente, Restrição de memória ativa.
* **Comportamento Esperado:** Banimento do *Merge Sort* (quebra de restrição de espaço). Punição do *Quick Sort* (risco de pior caso). Recomendação final do `Heap Sort` (In-place e estável em O(n log n)).

### CT-03: Vetor Quase Ordenado
* **Configuração:** Array ordenado com apenas 5% de perturbação.
* **Comportamento Esperado:** Vitória do `Insertion Sort` (recebe bônus maciço por atuar perto da sua complexidade linear O(n)).

### CT-04: Exigência de Estabilidade
* **Configuração:** Dados aleatórios, flag de estabilidade = True.
* **Comportamento Esperado:** Banimento imediato dos algoritmos instáveis (*Quick, Heap, Selection*). Recomendação segura do `Merge Sort`.

### CT-05: Busca em Dados Não Ordenados
* **Configuração:** Vetor aleatório, Alvo = elemento existente.
* **Comportamento Esperado:** Banimento imediato da *Busca Binária* (pré-requisito quebrado). Recomendação direcionada à `Busca Hash`.

### CT-06: Busca em Vetor 100% Ordenado
* **Configuração:** Vetor pré-ordenado.
* **Comportamento Esperado:** Bonificação máxima da `Busca Binária` (aproveitamento imediato da redução logarítmica).

### CT-07: Busca com Restrição Severa de Memória
* **Configuração:** Vetor ordenado, Memória restrita.
* **Comportamento Esperado:** Penalização drástica da *Busca Hash* (pelo custo O(n) do dicionário). Indicação e vitória da `Busca Binária`.