# Prompt - Questão 6: Forma da Distribuição, Assimetria e Testes de Normalidade

## Contexto
Implementação em Python para avaliar o formato da distribuição em quatro variáveis selecionadas (`magnesium`, `malic_acid`, `proanthocyanins` e `hue`), computando assimetria de Fisher-Pearson, teste de Shapiro-Wilk e gráficos de histograma com densidade estimada (KDE).

## Prompt Enviado
```text
Crie uma rotina modular em Python para o Exercício 6 da avaliação de Data Science:

1. Para as variáveis 'magnesium', 'malic_acid', 'proanthocyanins' e 'hue', calcule o coeficiente de assimetria (skewness) de Fisher-Pearson não-enviesado para os três cultivares em conjunto e classifique cada uma segundo Bulmer (aproximadamente simétrica, assimétrica à direita ou à esquerda).
2. Plote um painel 2x2 com histogramas e curvas de densidade estimada (KDE) para as quatro variáveis, marcando com linhas verticais a média e a mediana.
3. Aplique o teste de Shapiro-Wilk (scipy.stats.shapiro) para confirmar ou refutar a hipótese de normalidade e forneça uma recomendação fundamentada se a média ou a mediana representa melhor o valor típico de cada variável.
4. Salve o gráfico em 'outputs/exercicio6_distribuicoes_kde.png'.
```

## Como a Resposta foi Utilizada
O retorno forneceu os parâmetros da biblioteca `scipy.stats.skew(bias=False)` e a parametrização do `sns.histplot(kde=True)`. A interpretação prática e a defesa do uso da mediana em variáveis com caudas pesadas foram redigidas pelo aluno.
