# Graficos obrigatorios

Este modulo gera os graficos exigidos no enunciado do projeto a partir de
resultados ja coletados pela validacao empirica.

## Formato de entrada

Cada linha representa a execucao de um algoritmo em um cenario:

```json
{
  "cenario": "aleatorio_n1000",
  "tipo_cenario": "aleatorio",
  "tamanho": 1000,
  "algoritmo": "Merge Sort",
  "tempo_segundos": 0.012,
  "comparacoes": 3500,
  "trocas": 900,
  "overhead_percentual": 4.2,
  "acerto_top2": true
}
```

O arquivo pode ser `.json` ou `.csv`. Em JSON, ele pode ser uma lista direta ou
um objeto com a chave `resultados`.

Para facilitar a integracao com os outros modulos, o gerador tambem aceita
alguns aliases. Por exemplo, `nome` pode ser usado no lugar de `cenario`, e
`overhead` pode ser usado no lugar de `overhead_percentual`. Quando o nome do
cenario segue o padrao `Aleatorio_n1000`, `Invertido_n1000`,
`Quase_Ordenado_n1000` ou `Muitas_Duplicatas_n1000`, os campos `tipo_cenario` e
`tamanho` sao inferidos automaticamente.

## Como executar

```bash
python -m validacao.gerar_graficos --entrada resultados.json
```

Por padrao, os arquivos sao salvos em `resultados/graficos` nos formatos `png`
e `pdf`.

## Graficos gerados

- `tempo_execucao_algoritmo`: tempo medio de execucao por algoritmo.
- `comparacoes_algoritmo`: numero medio de comparacoes por algoritmo.
- `acuracia_tipo_dataset`: acuracia Top-2 do seletor por tipo de dataset.
- `overhead_medio`: overhead medio do seletor por tipo de dataset.
- `comportamento_tipo_dataset`: evolucao do tempo medio por tamanho e tipo de
  dataset.

## Integracao com o benchmark

Quando o modulo de benchmark e validacao estiver pronto, ele so precisa exportar
os campos acima. Assim, a parte de graficos nao depende diretamente da
implementacao interna dos algoritmos, do seletor ou dos contadores.
