# Prompt - Questão 10: Questão Integradora (Redundância e Política de Preços)

## Contexto
Implementação em Python de subamostragem estratificada de 60%, identificação de variáveis redundantes para redução de custos de análises laboratoriais por lote e teste paramétrico (ANOVA e Tukey HSD) para avaliar se o teor alcoólico fundamenta política de preços diferenciada.

## Prompt Enviado
```text
Escreva um script em Python para a Questão 10 (Questão Integradora):

1. A partir do Wine Recognition Dataset (178 amostras), extraia uma amostra estratificada por cultivar de 60% das observações de cada grupo, com random_state=7 (resultando em n=106).
2. Usando essa amostra, calcule a matriz de correlação de Pearson completa e identifique o par de variáveis mais redundantes entre si (com maior |r|), desconsiderando explicitamente os pares já analisados na Questão 7 ('flavanoids x od280/od315' e 'flavanoids x total_phenols').
3. Ainda com a amostra de 60%, teste se há diferença estatística no teor alcoólico ('alcohol') entre os três cultivares. Cheque a normalidade (Shapiro-Wilk) e a homogeneidade de variâncias (Levene), selecione o teste adequado (ANOVA ou Kruskal) e aplique o post-hoc de Tukey HSD.
4. Gere o boxplot comparativo de teor alcoólico por cultivar e salve em 'outputs/exercicio10_alcohol_cultivares.png'.
5. Consolide as evidências numéricas (tamanhos amostrais, r de Pearson, F da ANOVA, diferenças de médias e p-valores do Tukey HSD) para permitir redigir uma conclusão executiva de até 15 linhas para a diretoria da vinícola.
```

## Como a Resposta foi Utilizada
A resposta localizou o par ótimo de redundância analítica (`total_phenols x od280/od315`, com $r = +0{,}7045$, $R^2 = 49{,}6\%$) e confirmou a perfeita adequação paramétrica da ANOVA One-Way ($F = 89{,}12$, $p = 3{,}42 \times 10^{-23}$), subsidiando a redação da síntese executiva de 14 linhas.
