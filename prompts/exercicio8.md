# Prompt - Questão 8: Teste de Hipótese entre Dois Grupos (Magnésio)

## Contexto
Implementação em Python para comparar o teor de magnésio entre o Cultivar B e o Cultivar C, avaliando pressupostos de normalidade por estrato e homocedasticidade, selecionando o teste estatístico pertinente e redigindo conclusão enológica em linguagem acessível.

## Prompt Enviado
```text
Crie uma rotina em Python para resolver o Exercício 8 da avaliação:

1. Compare a variável 'magnesium' entre o Cultivar B (n=71) e o Cultivar C (n=48).
2. Verifique o pressuposto de normalidade em cada grupo via Shapiro-Wilk e a homogeneidade de variâncias entre os dois grupos via teste de Levene (center='median').
3. Com base nos resultados dos pressupostos, escolha e execute o teste estatístico de hipótese cabível (teste t de Student se atendidos os pressupostos, ou teste não-paramétrico de Kruskal-Wallis / Mann-Whitney se violados), interpretando o p-valor com alpha = 0,05.
4. Gere um boxplot comparativo de alta qualidade e salve em 'outputs/exercicio8_magnesium_cultivar_b_c.png'.
5. Formule um resumo dos resultados que fundamente uma explicação prática, em termos simples e sem jargões matemáticos, para ser apresentada ao enólogo-chefe da vinícola.
```

## Como a Resposta foi Utilizada
A resposta elucidou por que o teste t falhava em nível $\alpha=0{,}05$ ($p = 0{,}085$) devido aos outliers severos de magnésio no Cultivar B, enquanto o teste não-paramétrico de Kruskal-Wallis confirmava a diferença com alta significância ($p = 0{,}00057$), orientando a conclusão para o enólogo.
