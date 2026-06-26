# Métricas de Validação Empírica

Este módulo documenta as quatro métricas obrigatórias exigidas para comprovação científica do seletor. Os resultados são calculados via `validacao/validar_seletor.py`.

## Definição das Métricas

1. **Taxa de Acerto Top-2 (%):**
   Mede a porcentagem de vezes em que a recomendação feita pela IA do seletor corresponde a um dos dois algoritmos mais rápidos medidos na prática (pelo motor de benchmark).

2. **Overhead Médio do Seletor (%):**
   Calcula o custo que o "cérebro" de análise cobra do tempo total. A fórmula no sistema é:
   `Overhead (%) = (Tempo_Decisão / Tempo_Algoritmo_Recomendado) * 100`

3. **Tempo Médio de Decisão (s):**
   Registra o tempo cronometrado exclusivamente para a extração probabilística de features (em `caracteristicas.py`) e a execução do pipeline de scoring (`motor_decisao.py`).

4. **Impacto do Tipo de Conjunto de Dados (%):**
   Mede a consistência do sistema avaliando a discrepância da acurácia. A fórmula é:
   `Impacto = Max(Taxas_Por_Tipo) - Min(Taxas_Por_Tipo)` (ex: Acerto no vetor aleatório vs. vetor invertido).