# Graficos extras

Este modulo gera visualizacoes complementares para enriquecer o relatorio sem
substituir os graficos obrigatorios.

## Campos adicionais

Cada linha continua representando a execucao de um algoritmo em um cenario. Para
os extras, alem dos campos dos graficos obrigatorios, use:

```json
{
  "trocas": 900,
  "memoria_kb": 48.5,
  "tempo_decisao_segundos": 0.0042,
  "posicao_recomendado": 1
}
```

Aliases aceitos:

- `memoria`, `memoria_pico_kb`, `pico_memoria_kb` para `memoria_kb`.
- `tempo_decisao`, `tempo_seletor`, `t_decisao` para
  `tempo_decisao_segundos`.
- `rank_recomendado`, `ranking_recomendado`, `posicao_ranking` para
  `posicao_recomendado`.

## Como executar

```bash
python -m validacao.gerar_graficos_extras --entrada resultados.json
```

Por padrao, os arquivos sao salvos em `resultados/graficos_extras` nos formatos
`png` e `pdf`.

## Graficos gerados

- `trocas_algoritmo`: trocas medias por algoritmo.
- `memoria_algoritmo`: uso medio de memoria por algoritmo.
- `tempo_decisao_tamanho`: tempo medio de decisao por tamanho do dataset.
- `ranking_recomendado`: posicao do algoritmo recomendado no ranking real.
- `heatmap_tempo`: tempo medio por tipo de dataset e algoritmo.

## Integracao

Os graficos extras esperam os resultados ja consolidados pela validacao
empirica. Eles nao executam algoritmos e nao calculam ranking real; apenas
visualizam os campos exportados pela camada de benchmark/validacao.
