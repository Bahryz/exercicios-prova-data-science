# Questão 4: Amostragem Estratificada e Teorema Central do Limite

## Enunciado
a) Monte uma amostra estratificada por cultivar correspondente a 20% das observações de cada grupo, respeitando a proporção original de cada cultivar no dataset, com random_state = 42 para garantir reprodutibilidade.
b) Compare, em uma mesma figura, o histograma da variável proline na amostra estratificada e o histograma da mesma variável na população completa (178 amostras).
c) A partir do tamanho da amostra obtida no item (a), realize 1.000 reamostragens com reposição da variável proline e calcule a média de cada reamostragem. Plote o histograma dessas 1.000 médias e compare, no texto, o desvio-padrão observado dessas médias com o valor teórico previsto pelo TCL (σ/√n), indicando quantas vezes o erro-padrão é menor que o desvio-padrão populacional.
d) Conclua, em um parágrafo, se a amostra estratificada do item (a) é representativa da população quanto à variável proline.

## Registro de Prompts (IA Generativa)
- **1º Prompt:** "como fazer amostragem estratificada de 20% por cultivar no wine dataset com random_state=42 e comparar os histogramas de proline na amostra e na populacao?"
- **2º Prompt:** "como simular o TCL com 1000 reamostragens da media de proline em python e validar se o erro padrao observado bate com sigma / sqrt(n)?"
