# Prompt - Questão 7: Correlação Linear, Significância Estatística e Redundância Analítica

## Contexto
Implementação em Python para computar a matriz de correlação completa das 13 variáveis, filtrar pares com $|r| > 0{,}70$ excluindo o par já visto em aula (`flavanoids x total_phenols`), deduzir analiticamente a estatística $t$ de significância, validar com `pearsonr`, testar normalidade e calcular correlações de postos de Spearman e Kendall.

## Prompt Enviado
```text
Escreva um script em Python para a Questão 7 com foco em rigor estatístico:

1. Calcule a matriz de correlação de Pearson completa entre as 13 variáveis e liste todos os pares com |r| > 0,7, excluindo o par 'flavanoids' x 'total_phenols' analisado em aula.
2. Para o par de maior |r| restante, calcule manualmente a estatística t de significância da correlação: t = r * sqrt(n - 2) / sqrt(1 - r^2) e o p-valor bicaudal correspondente usando a distribuição t de Student (scipy.stats.t).
3. Confira e valide o resultado manual com a função oficial scipy.stats.pearsonr, interpretando o p-valor com alpha = 0,05.
4. Verifique a normalidade univariada das duas variáveis desse par via teste de Shapiro-Wilk. Havendo violação de normalidade, calcule os coeficientes de Spearman e Kendall para o par.
5. Produza um painel com o Heatmap da matriz 13x13 e um Scatter Plot do par mais correlacionado colorido por cultivar com a reta de regressão linear ajustada. Salve em 'outputs/'.
```

## Como a Resposta foi Utilizada
O código garantiu a implementação manual do teste de hipótese para a correlação linear de Pearson e sua checagem exata com a função do SciPy, gerando $t = 16{,}9340$ e $p = 8{,}60 \times 10^{-39}$ para o par `flavanoids x od280/od315`.
