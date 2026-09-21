# Prompt - Questão 5: Medidas de Posição, Dispersão e Detecção de Outliers (IQR)

## Contexto
Implementação em Python para cálculo de estatísticas descritivas (média, mediana, desvio-padrão e Coeficiente de Variação) para as 13 variáveis do dataset agrupadas por cultivar, identificação das 3 variáveis de maior CV médio, detecção de outliers pelo critério de Tukey ($1{,}5 \times IQR$) e geração de boxplots comparativos.

## Prompt Enviado
```text
Desenvolva um código limpo e tipado em Python para a Questão 5 do Wine Recognition Dataset:

1. Agrupe os dados por cultivar e calcule média, mediana, desvio-padrão e Coeficiente de Variação (CV = std/mean * 100) para todas as 13 variáveis físico-químicas. Identifique qual variável tem o maior CV médio entre os três cultivares.
2. Identifique as 3 variáveis de maior CV médio e, aplicando a regra de 1,5 x IQR (interquartile range), detecte e conte quantos outliers existem dentro de cada cultivar para cada uma dessas três variáveis.
3. Construa boxplots comparativos com sobreposição de stripplot entre os cultivares para essas três variáveis em um único painel e salve em 'outputs/'.
4. Imprima no terminal uma tabela clara com as contagens de outliers e os rankings de CV para apoiar a conclusão sobre se existe um único cultivar mais homogêneo ou se varia conforme a variável.
```

## Como a Resposta foi Utilizada
A resposta auxiliou na formatação da tabela de agregação multi-índice e na vetorização do cálculo dos quartis $Q_1$ e $Q_3$ por subgrupo de cultivar para o critério de Tukey, validando que `malic_acid` lidera o CV com 39,81%.
