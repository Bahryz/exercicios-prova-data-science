# Questão 7: Correlação, Significância e Redundância

## Enunciado
a) Calcule a matriz de correlação completa entre as 13 variáveis e liste todos os pares com |r| > 0,7, excluindo o par flavanoids × total_phenols já analisado em aula.
b) Para o par de maior |r| encontrado no item (a), calcule manualmente a estatística t de significância (t = r·√(n−2)/√(1−r²)) e confira o resultado com scipy.stats.pearsonr, interpretando o p-valor obtido com α = 0,05.
c) Verifique a normalidade (Shapiro-Wilk) das duas variáveis desse par. Caso alguma delas viole a normalidade, calcule também a correlação de Spearman e de Kendall para o mesmo par, comentando as diferenças encontradas em relação ao coeficiente de Pearson.
d) Produza um heatmap da matriz de correlação completa e um scatter plot do par de maior correlação, colorido por cultivar e com a reta ajustada.

## Registro de Prompts (IA Generativa)
- **1º Prompt:** "como calcular a matriz de correlacao do wine dataset e filtrar pares com |r| > 0.7 tirando flavanoids x total_phenols?"
- **2º Prompt:** "como calcular a estatistica t na mao para o r de pearson t = r*sqrt(n-2)/sqrt(1-r^2) e conferir com scipy.stats.pearsonr?"
- **3º Prompt:** "se shapiro rejeitar normalidade, como calcular spearman e kendall tau para esse par?"
