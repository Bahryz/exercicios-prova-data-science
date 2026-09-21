# Prompt - Questão 4: Amostragem Estratificada e Teorema Central do Limite (TCL)

## Contexto
Implementação em Python de amostragem estratificada por cultivar no dataset de vinhos da scikit-learn, comparação de histogramas populacional vs. amostral para a variável prolina, simulação computacional do TCL com 1.000 médias e validação do erro-padrão.

## Prompt Enviado
```text
Escreva um script modular em Python, seguindo princípios de Clean Code e com type hints, para resolver a Questão 4 da avaliação sobre o Wine Recognition Dataset (load_wine):

1. Mapeie a coluna target para 'Cultivar A', 'Cultivar B' e 'Cultivar C'.
2. Extraia uma amostra estratificada por cultivar correspondente a 20% das observações de cada grupo, usando random_state=42.
3. Compare, em uma mesma figura com Matplotlib/Seaborn de alta resolução (300 DPI), o histograma da variável 'proline' na amostra estratificada (n=36) e na população completa (N=178).
4. A partir do tamanho n=36, realize 1.000 reamostragens com reposição da variável 'proline' da população e calcule a média de cada reamostragem. Plote o histograma dessas 1.000 médias.
5. Calcule e compare no texto o desvio-padrão observado das médias com o valor teórico do erro-padrão previsto pelo TCL (sigma / sqrt(n)), indicando quantas vezes o erro-padrão é menor que o desvio populacional (fator sqrt(n) = 6).
6. Salve a figura gerada na pasta 'outputs/' com eixos e legendas claros.
```

## Como a Resposta foi Utilizada
O código sugerido serviu de base para estruturar a amostragem estratificada via `train_test_split(test_size=0.20, stratify=...)` e a reamostragem bootstrap vetorizada via `numpy.random.default_rng`, gerando as métricas exatas consolidadas no relatório.
