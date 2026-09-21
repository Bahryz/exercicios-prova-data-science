# Questão 10: Questão Integradora

## Enunciado
A diretoria da cooperativa avalia se é viável reduzir o número de testes laboratoriais por lote e se a diferença no teor alcoólico entre cultivares justifica uma política de preços diferenciada por cultivar.
a) A partir da população completa (load_wine), monte uma amostra estratificada por cultivar correspondente a 60% das observações de cada grupo, com random_state = 7.
b) Usando essa amostra, calcule a matriz de correlação completa e identifique as duas variáveis mais redundantes entre si, diferentes dos pares já utilizados na Questão 7.
c) Ainda usando essa amostra, teste estatisticamente se há diferença significativa no teor de alcohol entre os três cultivares, escolhendo e justificando o teste apropriado a partir da verificação dos pressupostos de normalidade e homogeneidade de variâncias.
d) Redija uma conclusão final, com no máximo 15 linhas, integrando: a representatividade da amostra construída no item (a), a redundância de variáveis identificada no item (b), e se a diferença no teor alcoólico encontrada no item (c) sustenta estatisticamente uma política de preços diferenciada por cultivar. A conclusão deve referenciar explicitamente as evidências estatísticas obtidas, não opiniões pessoais sobre o vinho.

## Registro de Prompts (IA Generativa)
- **1º Prompt:** "como tirar amostra estratificada de 60% com random_state=7 e achar o par mais redundante na matriz de correlacao excluindo os pares da questao 7?"
- **2º Prompt:** "na amostra de 60%, como testar se alcohol difere entre cultivares e redigir uma conclusao de 15 linhas ligando redundancia e preco?"
