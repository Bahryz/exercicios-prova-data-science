# Prompt - Questão 9: Comparação Múltipla de Grupos e Teste Post-Hoc (Ácido Málico)

## Contexto
Implementação em Python para avaliar o teor de ácido málico entre os três cultivares de vinho, avaliando pressupostos de normalidade e homocedasticidade, executando o teste omnibus (Kruskal-Wallis e ANOVA) e o teste post-hoc de Tukey HSD.

## Prompt Enviado
```text
Desenvolva uma solução modular em Python para a Questão 9:

1. Verifique se o teor de 'malic_acid' difere significativamente entre os três cultivares (A, B e C), checando a normalidade de cada grupo com Shapiro-Wilk e a homogeneidade de variâncias com o teste de Levene.
2. Escolha e justifique o teste omnibus adequado (ANOVA One-Way ou Kruskal-Wallis) dependendo dos pressupostos.
3. Sendo o resultado estatisticamente significante, aplique o teste post-hoc de Tukey HSD (statsmodels.stats.multicomp.pairwise_tukeyhsd) para identificar os contrastes entre cada par de cultivares a 95% de confiança.
4. Construa o boxplot comparativo entre os três cultivares com dispersão de pontos e salve em 'outputs/exercicio9_malic_acid_cultivares.png'.
5. Forneça a base estatística para redigir a interpretação dos resultados sem incorrer nas falácias frequentistas de valor-p discutidas em aula.
```

## Como a Resposta foi Utilizada
O retorno confirmou a quebra dupla de pressupostos (não-normalidade nos cultivares A e B e heterocedasticidade com $p = 0{,}0022$), justificando Kruskal-Wallis ($H = 50{,}04$, $p = 1{,}36 \times 10^{-11}$) e gerando a tabela completa de Tukey HSD com os intervalos de confiança simultâneos.
