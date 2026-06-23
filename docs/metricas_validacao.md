# Metricas obrigatorias da validacao

Este modulo consolida as metricas exigidas na secao 9.1 do enunciado:

- taxa de acerto Top-2;
- overhead medio;
- tempo medio de decisao;
- impacto do tipo de conjunto de dados.

## Como executar

```bash
python -m validacao.validar_seletor
```

Por padrao, o relatorio e salvo em:

```text
resultados/validacao/metricas_obrigatorias.json
```

Tambem e possivel customizar tamanhos, repeticoes e saida:

```bash
python -m validacao.validar_seletor --tamanhos 30 100 1000 --repeticoes 3 --saida resultados/validacao/metricas.csv
```

## Campos exportados

O JSON possui tres blocos:

- `metricas`: resumo das quatro metricas obrigatorias.
- `cenarios`: resumo por cenario avaliado.
- `resultados`: linhas por algoritmo, prontas para alimentar os graficos.

Cada linha de `resultados` possui campos como:

```json
{
  "cenario": "Aleatorio_n1000",
  "tipo_cenario": "aleatorio",
  "tamanho": 1000,
  "algoritmo": "Quick Sort",
  "tempo_segundos": 0.012,
  "comparacoes": 3500,
  "trocas": 900,
  "memoria_kb": 48.5,
  "tempo_decisao_segundos": 0.004,
  "overhead_percentual": 4.2,
  "acerto_top2": true,
  "posicao_recomendado": 1
}
```

## Como gerar graficos a partir da validacao

Depois de gerar o JSON:

```bash
python -m validacao.gerar_graficos --entrada resultados/validacao/metricas_obrigatorias.json
```

Os graficos serao salvos em `resultados/graficos`.

## Observacoes

- O tempo de decisao mede apenas analise de caracteristicas + pontuacao.
- O tempo de ordenacao nao entra no tempo de decisao.
- O overhead e calculado como `tempo_decisao / tempo_algoritmo_recomendado * 100`,
  que equivale a formula do professor quando `Tseletor` inclui decisao +
  algoritmo recomendado.
- A validacao padrao usa tamanhos pequenos e medios para evitar que algoritmos
  O(n^2) tornem a execucao local muito demorada. Para experimentos finais, a
  equipe pode informar tamanhos maiores via `--tamanhos`.
