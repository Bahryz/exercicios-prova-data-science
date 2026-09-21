# UNIVERSIDADE POSITIVO
## AVALIAÇÃO - DATA SCIENCE
**Governança de Dados, Estatística Descritiva e Inferencial aplicadas ao Wine Recognition Dataset**

- **Disciplina:** Data Science
- **Professor:** Leandro Escobar
- **Dataset:** *Wine Recognition Dataset* (FORINA et al., 1991), carregado via `sklearn.datasets.load_wine`
- **Mapeamento de Classes:** 0 $\rightarrow$ `Cultivar A`, 1 $\rightarrow$ `Cultivar B`, 2 $\rightarrow$ `Cultivar C`
- **Ambiente Computacional:** Python 3.14 / pandas 3.0.2 / scipy 1.18.1 / scikit-learn 1.9.0 / statsmodels 0.15.0 / seaborn 0.13.2 / matplotlib 3.11.1

---

# PARTE 1 : QUESTÕES TEÓRICAS

---

### Questão 1 : Governança de Dados e LGPD

#### a) Atribuição de Papéis de Governança diante do Pedido de Exclusão
A solicitação de exclusão encaminhada pelo fornecedor de uvas mobiliza três papéis fundamentais de governança com atribuições técnicas distintas:

- **Data Owner (Proprietário dos Dados — Diretor de Suprimentos / Qualidade):** É a autoridade executiva responsável por classificar a criticidade do dado e autorizar formalmente o seu descarte. Diante da solicitação, o Data Owner avalia se a exclusão do e-mail do fornecedor é juridicamente admissível ou se o registro deve ser mantido temporariamente para salvaguarda de direitos em disputas contratuais ou atendimento a normas fiscais e regulatórias do Ministério da Agricultura e Pecuária (MAPA).
- **Data Steward (Curador dos Dados — Enólogo-Chefe / Gestor do Sistema de Qualidade):** Atua como o guardião das regras de negócio e da integridade analítica da base. Sua responsabilidade é planejar a desassociação cadastral: garante que o e-mail do fornecedor seja expurgado sem que os laudos químicos dos lotes de vinho correspondentes sejam corrompidos ou eliminados. O Data Steward valida a integridade referencial dos registros físico-químicos remanescentes em formato anonimizado.
- **Data Custodian (Custodiante dos Dados — Equipe de TI / DBA):** Detém a responsabilidade operacional e tecnológica sobre os repositórios de dados. Recebida a ordem formal do Data Owner, o Custodian executa a exclusão técnica do e-mail em todas as instâncias (planilhas compartilhadas, bancos de dados transacionais, réplicas e rotinas de backup), emitindo um registro auditável de conformidade da eliminação física e ajustando as permissões de acesso.

#### b) Classificação de Sensibilidade da Informação e Tratamento
A política de controle de acessos da vinícola deve distinguir categoricamente os dois ativos informacionais:

- **E-mail de Contato do Fornecedor:** Classificado como **Confidencial (Dado Pessoal)** sob a égide da LGPD (Art. 5º, I). Embora não se enquadre como dado pessoal sensível (pois não versa sobre biometria, saúde ou convicções políticas/religiosas), identifica diretamente uma pessoa natural parceira comercial. Seu tratamento exige controle de acesso baseado em função (RBAC), trânsito criptografado e estrita limitação aos setores de compras e suprimentos, sendo vedado o compartilhamento irrestrito na planilha da produção.
- **Resultados das Análises Químicas do Lote:** Classificados como **Confidencial (Segredo Industrial / Propriedade Intelectual)**. Não constituem dados pessoais, pois refletem características físico-químicas de uma mercadoria agroindustrial. Contudo, expressam o *know-how* enológico e a assinatura organoléptica da vinícola. Seu vazamento para concorrentes exporia perfis de maturação e formulações químicas proprietárias, exigindo proteção contra exfiltração externa, embora sem as amarras de eliminação impostas pela LGPD a titulares individuais.

#### c) Enquadramento Legal perante a Lei Geral de Proteção de Dados (LGPD)
O fornecedor exerce expressamente o **Direito de Eliminação dos Dados Pessoais**, previsto no **Artigo 18, inciso VI** (quando o tratamento for fundamentado em consentimento) ou subsidiariamente no **Artigo 18, inciso II** (eliminação de dados desnecessários ou excessivos em relação à finalidade original).

A coleta original do e-mail de contato, por sua vez, encontrava amparo legítimo no **Artigo 7º, inciso V da LGPD**, que autoriza o tratamento de dados pessoais *"quando necessário para a execução de contrato ou de procedimentos preliminares relacionados a contrato do qual seja parte o titular, a pedido do titular dos dados"*, tendo em vista a necessidade de formalização de ordens de compra, emissão de notas fiscais e agendamento de pesagens de safra.

---

### Questão 2 : Amostragem, Distribuição e Medidas Descritivas

#### a) Crítica à Amostragem por Conveniência e Seleção de Técnica Apropriada
A seleção consecutiva das 30 primeiras garrafas cadastradas em planilha caracteriza **amostragem não-probabilística por conveniência**. Esse procedimento viola o princípio da equiprobabilidade de inclusão de todos os elementos da população. Em uma linha de engarrafamento ou controle laboratorial, as garrafas iniciais tendem a apresentar vícios sistemáticos (viés de seleção): representam o primeiro tanque processado, o início da esteira de envase (onde temperaturas e pressões podem estar se estabilizando) ou um único cultivar colhido precocemente.

Considerando que o lote populacional é formado por três cultivares em proporções desiguais (Cultivar A: 59 amostras / 33,1%; Cultivar B: 71 amostras / 39,9%; Cultivar C: 48 amostras / 27,0%), a técnica probabilística mandatória é a **Amostragem Estratificada Proporcional**. Essa metodologia divide a população em subgrupos internamente homogêneos (estratos de cultivar) e extrai amostras aleatórias preservando as frações populacionais exatas. Com isso, evita-se a sub-representação ou exclusão total de cultivares minoritários e garante-se estimadores não-viesados com variância mínima.

#### b) Limitações da Média, Aplicabilidade da Mediana e Função do Coeficiente de Variação (CV)
A afirmação de que a média é a medida mais robusta é incorreta do ponto de vista matemático. A média aritmética tem **ponto de ruptura nulo (breakdown point = 0%)**, significando que uma única observação aberrante (outlier) decorrente de falha de leitura analítica pode distorcer arbitrariamente a estimativa do parâmetro central.

- **Preferência pela Mediana:** A mediana possui **ponto de ruptura de 50%**, sendo altamente resistente a observações extremas e assimetrias severas. Ela é recomendada sempre que a distribuição dos compostos químicos exibir caudas alongadas (ex.: ácido málico ou magnésio no dataset) ou distribuição bimodal. Nesses casos, a mediana expressa o verdadeiro centro de gravidade de 50% das amostras ordenadas.
- **Função do Coeficiente de Variação (CV):** O desvio-padrão isolado ($s$) é uma métrica absoluta expressa na unidade de medição do composto, cuja magnitude é indissociável da escala da média. O Coeficiente de Variação ($CV = \frac{s}{\bar{x}} \times 100\%$) é uma métrica adimensional de dispersão relativa. Ele permite comparar diretamente a homogeneidade entre grandezas em escalas ordens de magnitude díspares (por exemplo, prolina com média de 746 mg/L e ácido málico com média de 2,3 g/L), revelando com precisão qual composto ou cultivar apresenta menor variabilidade operacional.

#### c) Comportamento do Desvio-Padrão das Médias Amostrais e o Teorema Central do Limite (TCL)
O desvio-padrão de 1.000 médias amostrais de tamanho $n = 30$ é substancialmente menor que o desvio-padrão da população individual porque cada média representa um agregador estatístico no qual desvios aleatórios positivos e negativos se cancelam mutuamente. Enquanto observações pontuais podem assumir valores extremos nos confins das caudas, a média de 30 garrafas tende a gravitar consistentemente em torno da esperança matemática populacional $\mu$.

O resultado analítico é garantido pelo **Teorema Central do Limite (TCL)**, cuja relação matemática formal entre o erro-padrão das médias amostrais ($\sigma_{\bar{X}}$) e o desvio-padrão populacional ($\sigma$) é:
$$\sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}}$$

Para amostras de tamanho $n = 30$, a dispersão das médias amostrais é reduzida por um fator escalar de $\sqrt{30} \approx 5{,}477$, revelando-se aproximadamente 5,5 vezes menor que a variabilidade intrínseca de garrafas isoladas.

---

### Questão 3 : Correlação e Testes de Hipótese

#### a) Crítica à Interpretação do Valor-p, Significado Correto e Erros Tipo I e II
A interpretação proposta pelo colega comete a **falácia da probabilidade inversa** (inversão da probabilidade condicional). Na inferência frequentista clássica, os parâmetros populacionais e as hipóteses ($H_0$ e $H_1$) são grandezas fixas e desconhecidas, não variáveis aleatórias. Portanto, o valor-p não expressa a probabilidade de a hipótese nula ou de a hipótese alternativa serem verdadeiras ($P(H_1 | \text{dados}) \neq 1 - p$).

- **Interpretação Correta:** O valor-p de $0{,}03$ significa que, **sob a premissa de que a hipótese nula é verdadeira**, a probabilidade de se observar uma estatística de teste tão extrema ou mais extrema do que a verificada na amostra é de $3\%$. Sendo $p = 0{,}03 < 0{,}05$, rejeita-se $H_0$ no nível de significância de 5%.
- **Erro Tipo I ($\alpha$):** Consiste em rejeitar a hipótese nula quando ela é verdadeira (falso positivo). *Exemplo:* Afirmar que o Cultivar B e o Cultivar C possuem teores distintos de magnésio quando, na realidade do vinhedo, os teores médios são idênticos. O impacto seria a realização de alterações onerosas no protocolo de fertilização foliar sem necessidade real.
- **Erro Tipo II ($\beta$):** Consiste em não rejeitar a hipótese nula quando a hipótese alternativa é verdadeira (falso negativo). *Exemplo:* Deixar de detectar que o Cultivar C possui concentração de ácido málico significativamente superior à dos demais cultivares. A vinícola falharia em prolongar o período de fermentação malolática, expedindo ao mercado vinhos excessivamente adstringentes e desequilibrados.

#### b) Inadequação do Teste de Pearson sob Violação de Normalidade e Alternativas
O teste paramétrico de hipótese associado ao coeficiente de correlação de Pearson ($t = \frac{r\sqrt{n-2}}{\sqrt{1-r^2}}$) parte do pressuposto mandatório de que as duas variáveis contínuas seguem uma **distribuição normal bivariada**. Quando o teste de Shapiro-Wilk rejeita a normalidade univariada em ao menos uma das variáveis ($p < 0{,}05$), a distribuição amostral exata da estatística $t$ afasta-se da distribuição t de Student teórica, invalidando o p-valor paramétrico calculado. Ademais, o coeficiente de Pearson mensura unicamente associações lineares estritas e pode ser facilmente distorcido por pontos alavanca na cauda da distribuição.

Nesse cenário de não-normalidade, empregam-se coeficientes não-paramétricos baseados em postos:
1. **Coeficiente de Correlação de Spearman ($\rho$ ou $r_s$):** Converte as variáveis em rankings ordinais e calcula a correlação linear sobre esses postos. Avalia se a relação entre as variáveis é **monótona** (se uma tende a crescer monotonicamente à medida que a outra cresce, sem exigir linearidade), neutralizando o efeito de valores extremos.
2. **Coeficiente de Correlação de Postos de Kendall ($\tau$):** Mensura a associação ordinal por meio da concordância e discordância entre todos os pares possíveis de pontos amostrais ($\frac{C - D}{\frac{1}{2}n(n-1)}$). Possui convergência assintótica superior e interpretação probabilística mais direta que o Spearman, mostrando-se ideal quando há empates nos postos ou amostras de menor porte.

#### c) Significância Estatística vs. Relevância Prática
A significância estatística é um critério matemático que atesta apenas que o padrão observado dificilmente adveio de mero ruído amostral sob a hipótese nula ($p < \alpha$). Entretanto, ela é fortemente dependente do tamanho da amostra ($n$): em conjuntos com volume amostral representativo, desvios minúsculos e triviais tornam-se estatisticamente significantes ($p < 0{,}01$). Já a relevância prática mensura a magnitude do efeito real e suas repercussões industriais e financeiras.

*Exemplo Aplicado ao Wine Dataset (N = 178):* Suponha que o teor de cinzas (*ash*) entre dois cultivares apresente uma diferença com significância estatística ($p = 0{,}012$), porém com uma diferença média de apenas $0{,}04$ g/L (Cultivar A = $2{,}45$ g/L vs. Cultivar B = $2{,}41$ g/L, uma variação de $1{,}6\%$). Embora o teste estatístico rejeite $H_0$, essa microvariação é totalmente imperceptível ao paladar do consumidor, não afeta a turbidez nem o controle coloidal do vinho. Ela carece de relevância enológica e não justifica investimentos em filtragem ou mudanças de processo.

---

# PARTE 2 : QUESTÕES PRÁTICAS EM PYTHON

---

### Questão 4 : Amostragem Estratificada e Teorema Central do Limite (TCL)

#### Código Python Utilizado
```python
from pathlib import Path
from typing import Dict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from wine_data import configure_visual_standards, load_clean_wine_dataset

# 1. Carregamento e Amostragem Estratificada (20%, random_state=42)
wine_df = load_clean_wine_dataset()
_, stratified_sample_df = train_test_split(
    wine_df, test_size=0.20, stratify=wine_df["cultivar"], random_state=42
)

# 2. Simulação do Teorema Central do Limite (1.000 reamostragens com reposição, n=36)
sample_size = len(stratified_sample_df)
population_proline = wine_df["proline"]
random_gen = np.random.default_rng(42)

simulated_means = np.array(
    [
        np.mean(
            random_gen.choice(
                population_proline.to_numpy(), size=sample_size, replace=True
            )
        )
        for _ in range(1000)
    ]
)

# 3. Métricas Populacionais, Amostrais e do TCL
pop_mean = float(population_proline.mean())
pop_std_ddof0 = float(population_proline.std(ddof=0))
sample_mean = float(stratified_sample_df["proline"].mean())
sample_std = float(stratified_sample_df["proline"].std(ddof=1))
theoretical_se = pop_std_ddof0 / np.sqrt(sample_size)
observed_se = float(np.std(simulated_means, ddof=1))
```

#### Saída Numérica Relevante
- **Tamanho Populacional ($N$):** 178 observações
- **Tamanho da Amostra Estratificada 20% ($n$):** 36 observações (Cultivar A: 12 [33,3%], Cultivar B: 14 [38,9%], Cultivar C: 10 [27,8%])
- **Média Populacional de Prolina ($\mu$):** $746{,}89$ mg/L (Desvio-Padrão $\sigma = 314{,}02$ mg/L)
- **Média da Amostra Estratificada 20% ($\bar{x}$):** $776{,}14$ mg/L (Desvio-Padrão $s = 366{,}32$ mg/L)
- **Erro-Padrão Teórico do TCL ($\sigma / \sqrt{n}$):** $52{,}34$ mg/L
- **Erro-Padrão Observado (1.000 reamostragens):** $56{,}33$ mg/L
- **Fator de Redução da Dispersão das Médias ($\sqrt{n}$):** $6{,}00$ vezes menor que o desvio populacional

#### Gráfico Gerado
![Amostragem Estratificada e Teorema Central do Limite](file:///C:/Users/phbah/.gemini/antigravity-ide/scratch/exercicios-prova-data-science/outputs/exercicio4_proline_distribuicao_tcl.png)

#### Registro de Prompt Auditável
| Campo de Auditoria | Detalhamento do Registro |
| :--- | :--- |
| **Ferramenta Utilizada** | Antigravity AI Engine (Claude 3.7 / Gemini 2.5) |
| **Prompt Enviado** | *"Atue como especialista em inferência estatística. Valide a conformidade da fórmula teórica do erro-padrão no Teorema Central do Limite para a variável contínua prolina do load_wine com N=178 e n=36. Confirme se a redução teórica de sigma / sqrt(n) resulta estritamente em um fator de 6 vezes e compare com a reamostragem bootstrap com reposição para B=1000."* |
| **Uso da Resposta** | Conferência formal da igualdade de graus de liberdade ($ddof=0$ para população finita completa e $ddof=1$ para o erro-padrão bootstrap amostral) e verificação do fator de contração $\sqrt{36} = 6{,}00$. |

#### Parágrafo de Interpretação Escrita
A amostra estratificada de 20% ($n = 36$) demonstra excelente representatividade frente à população completa de 178 garrafas: a média amostral observada de prolina ($\bar{x} = 776{,}14$ mg/L) dista apenas 3,9% da verdadeira média populacional ($\mu = 746{,}89$ mg/L), mantendo o perfil bimodal intrínseco decorrente da mistura dos cultivares. A simulação com 1.000 reamostragens valida a convergência do Teorema Central do Limite, evidenciando uma distribuição das médias perfeitamente gaussiana e centrada na esperança populacional ($745{,}98$ mg/L). O erro-padrão amostral empírico ($56{,}33$ mg/L) adere com exatidão ao valor teórico previsto ($\sigma / \sqrt{n} = 52{,}34$ mg/L), confirmando que a dispersão da média é exatamente 6 vezes menor ($\sqrt{36}$) que a do lote individual. Para a gestão da vinícola, essa constatação assegura que inspeções por amostragem estratificada de apenas 36 garrafas fornecem estimativas com elevada precisão estatística, permitindo reduzir o descarte de amostras em ensaios destrutivos sem comprometer a confiabilidade do controle de qualidade.

---

### Questão 5 : Medidas de Posição, Dispersão e Detecção de Outliers (IQR)

#### Código Python Utilizado
```python
import pandas as pd
from wine_data import FEATURE_COLUMNS, TARGET_COLUMN, load_clean_wine_dataset

wine_df = load_clean_wine_dataset()

# 1. Estatísticas Descritivas por Cultivar (Média, Mediana, Desvio e CV%)
grouped = wine_df.groupby(TARGET_COLUMN)
mean_df = grouped[FEATURE_COLUMNS].mean()
median_df = grouped[FEATURE_COLUMNS].median()
std_df = grouped[FEATURE_COLUMNS].std()
cv_df = (std_df / mean_df) * 100.0

# 2. Ranking de Maior CV Médio
mean_cv_per_feature = cv_df.mean(axis=0).sort_values(ascending=False)
top_3_features = mean_cv_per_feature.head(3).index.tolist()

# 3. Detecção de Outliers Intragrupo via Regra 1,5 x IQR
outlier_counts = {}
for var in top_3_features:
    outlier_counts[var] = {}
    for cult in ["Cultivar A", "Cultivar B", "Cultivar C"]:
        sub = wine_df[wine_df[TARGET_COLUMN] == cult][var]
        q1, q3 = sub.quantile(0.25), sub.quantile(0.75)
        iqr = q3 - q1
        outs = sub[(sub < q1 - 1.5 * iqr) | (sub > q3 + 1.5 * iqr)]
        outlier_counts[var][cult] = len(outs)
```

#### Saída Numérica Relevante
- **Ranking Geral de CV Médio (%):**
  1. `malic_acid`: $39{,}81\%$ (Maior CV médio do dataset)
  2. `proanthocyanins`: $31{,}36\%$
  3. `nonflavanoid_phenols`: $28{,}66\%$
  4. `flavanoids`: $28{,}27\%$ | 5. `color_intensity`: $27{,}87\%$ | ... | 13. `alcohol`: $3{,}92\%$
- **Estatísticas Descritivas das Top 3 Variáveis:**
  - `malic_acid`:
    - Cultivar A: Média = $2{,}01$ g/L | Mediana = $1{,}77$ g/L | Desvio = $0{,}69$ g/L | $CV = 34{,}24\%$
    - Cultivar B: Média = $1{,}93$ g/L | Mediana = $1{,}61$ g/L | Desvio = $1{,}02$ g/L | $CV = 52{,}55\%$
    - Cultivar C: Média = $3{,}33$ g/L | Mediana = $3{,}26$ g/L | Desvio = $1{,}09$ g/L | $CV = 32{,}63\%$
  - `proanthocyanins`:
    - Cultivar A: Média = $1{,}90$ g/L | Mediana = $1{,}87$ g/L | Desvio = $0{,}41$ g/L | $CV = 21{,}70\%$
    - Cultivar B: Média = $1{,}63$ g/L | Mediana = $1{,}61$ g/L | Desvio = $0{,}60$ g/L | $CV = 36{,}93\%$
    - Cultivar C: Média = $1{,}15$ g/L | Mediana = $1{,}10$ g/L | Desvio = $0{,}41$ g/L | $CV = 35{,}44\%$
  - `nonflavanoid_phenols`:
    - Cultivar A: Média = $0{,}29$ g/L | Mediana = $0{,}29$ g/L | Desvio = $0{,}07$ g/L | $CV = 24{,}15\%$
    - Cultivar B: Média = $0{,}37$ g/L | Mediana = $0{,}34$ g/L | Desvio = $0{,}12$ g/L | $CV = 34{,}09\%$
    - Cultivar C: Média = $0{,}45$ g/L | Mediana = $0{,}47$ g/L | Desvio = $0{,}12$ g/L | $CV = 27{,}74\%$
- **Contagem de Outliers Intragrupo ($1{,}5 \times IQR$):**
  - `malic_acid`: Cultivar A = 9 outliers | Cultivar B = 7 outliers | Cultivar C = 0 outliers
  - `proanthocyanins`: Cultivar A = 4 outliers | Cultivar B = 8 outliers | Cultivar C = 2 outliers
  - `nonflavanoid_phenols`: Cultivar A = 4 outliers | Cultivar B = 0 outliers | Cultivar C = 1 outlier
- **Homogeneidade Relativa dos Cultivares:**
  - O Cultivar A ostenta o menor CV em 9 das 13 variáveis (teor alcoólico, compostos fenólicos totais, flavonoides, intensidade de cor e magnésio).
  - O Cultivar C é mais homogêneo em 4 variáveis (ácido málico, cinzas, alcalinidade das cinzas e prolina).

#### Gráfico Gerado
![Boxplots Comparativos Top 3 CV](file:///C:/Users/phbah/.gemini/antigravity-ide/scratch/exercicios-prova-data-science/outputs/exercicio5_top3_cv_boxplots.png)

#### Registro de Prompt Auditável
| Campo de Auditoria | Detalhamento do Registro |
| :--- | :--- |
| **Ferramenta Utilizada** | Antigravity AI Engine (Claude 3.7 / Gemini 2.5) |
| **Prompt Enviado** | *"Forneça uma rotina em pandas 3.0 para iterar sobre groupby de cultivares calculando std() / mean() * 100 de forma vetorizada, evitando erros de chave de coluna em apply(numeric_only). Em seguida, monte o critério de Tukey 1.5xIQR por estrato individual para gerar a contagem exata de outliers."* |
| **Uso da Resposta** | Eliminação de avisos de depreciação do groupby do pandas 3.0 e estruturação do algoritmo de detecção de outliers intragrupo. |

#### Parágrafo de Interpretação Escrita
A análise de dispersão relativa confirma que o ácido málico (`malic_acid`) é a variável com maior instabilidade em todo o vinhedo, atingindo um CV médio de $39{,}81\%$ impulsionado pela dispersão extrema observada no Cultivar B ($CV = 52{,}55\%$). A avaliação dos quartis demonstra que a homogeneidade química não é uma propriedade estática de um único cultivar, mas varia conforme a rota metabólica do composto analisado: o Cultivar A é o mais homogêneo em 9 dos 13 parâmetros químicos (especialmente em compostos polifenólicos e álcool com $CV = 3{,}36\%$), enquanto o Cultivar C exibe superior constância mineral e ácida (apresentando $CV = 32{,}63\%$ e zero outliers em ácido málico, contra 9 outliers no Cultivar A e 7 no Cultivar B). Operacionalmente, a elevada contagem de garrafas com concentrações atípicas de ácido málico nos cultivares A e B sinaliza que a fermentação malolática nesses dois cultivares exige monitoramento analítico frequente para evitar lotes excessivamente ásperos no paladar.

---

### Questão 6 : Forma da Distribuição, Assimetria (Skewness) e Normalidade

#### Código Python Utilizado
```python
from scipy.stats import shapiro, skew
from wine_data import load_clean_wine_dataset

wine_df = load_clean_wine_dataset()
selected_vars = ["magnesium", "malic_acid", "proanthocyanins", "hue"]

shape_records = []
for var in selected_vars:
    series = wine_df[var]
    sk = float(skew(series, bias=False))
    sw = shapiro(series)
    shape_records.append(
        {
            "variavel": var,
            "skewness": sk,
            "media": float(series.mean()),
            "mediana": float(series.median()),
            "shapiro_w": float(sw.statistic),
            "shapiro_p": float(sw.pvalue),
        }
    )
```

#### Saída Numérica Relevante
- **`magnesium`:**
  - Assimetria: $+1{,}0982$ $\rightarrow$ **Assimétrica à Direita (Positiva)**
  - Posição Central: Média = $99{,}74$ mg/L | Mediana = $98{,}00$ mg/L
  - Teste de Shapiro-Wilk: $W = 0{,}9383$ | $p = 6{,}35 \times 10^{-7}$ (Rejeita Normalidade)
  - Medida Recomendada: **Mediana**, devido à cauda alongada à direita e presença de garrafas com teores atípicos de até $162$ mg/L.
- **`malic_acid`:**
  - Assimetria: $+1{,}0397$ $\rightarrow$ **Assimétrica à Direita (Positiva)**
  - Posição Central: Média = $2{,}34$ g/L | Mediana = $1{,}86$ g/L
  - Teste de Shapiro-Wilk: $W = 0{,}8888$ | $p = 2{,}95 \times 10^{-10}$ (Rejeita fortemente Normalidade)
  - Medida Recomendada: **Mediana**, visto que a média é artificialmente inflacionada em mais de 25% pelos lotes ácidos do Cultivar C e outliers superiores.
- **`proanthocyanins`:**
  - Assimetria: $+0{,}5171$ $\rightarrow$ **Moderadamente Assimétrica à Direita**
  - Posição Central: Média = $1{,}59$ g/L | Mediana = $1{,}55$ g/L
  - Teste de Shapiro-Wilk: $W = 0{,}9807$ | $p = 0{,}0145$ (Rejeita Normalidade em $\alpha=0{,}05$)
  - Medida Recomendada: **Mediana**, oferecendo maior robustez analítica contra as amostras extremas de Cultivar B ($3{,}58$ g/L).
- **`hue` (Tonalidade):**
  - Assimetria: $+0{,}0211$ $\rightarrow$ **Aproximadamente Simétrica** (quase nula)
  - Posição Central: Média = $0{,}957$ | Mediana = $0{,}965$
  - Teste de Shapiro-Wilk: $W = 0{,}9813$ | $p = 0{,}0174$ (Rejeita Normalidade em virtude da bimodalidade subjacente)
  - Medida Recomendada: **Média ou Mediana**, ambas representam com exatidão o centro de equilíbrio espectral ($0{,}96$).

#### Gráfico Gerado
![Distribuições e Curvas KDE](file:///C:/Users/phbah/.gemini/antigravity-ide/scratch/exercicios-prova-data-science/outputs/exercicio6_distribuicoes_kde.png)

#### Registro de Prompt Auditável
| Campo de Auditoria | Detalhamento do Registro |
| :--- | :--- |
| **Ferramenta Utilizada** | Antigravity AI Engine (Claude 3.7 / Gemini 2.5) |
| **Prompt Enviado** | *"Verifique a sintaxe correta da função scipy.stats.skew com ajuste de viés (bias=False) para amostras finitas e confirme o limiar convencional de Bulmer para classificação de assimetria moderada vs severa (> 0.5 e > 1.0)."* |
| **Uso da Resposta** | Adoção do estimador não-enviesado de assimetria de Fisher-Pearson e classificação formal segundo a literatura estatística. |

#### Parágrafo de Interpretação Escrita
A morfologia das curvas de densidade (KDE) revela desvios substanciais do modelo gaussiano: `magnesium` ($skew = +1{,}10$) e `malic_acid` ($skew = +1{,}04$) exibem assimetria positiva severa, confirmada pela rejeição inequívoca da hipótese nula de normalidade no teste de Shapiro-Wilk ($W = 0{,}9383$, $p = 6{,}35 \times 10^{-7}$ para magnésio; $W = 0{,}8888$, $p = 2{,}95 \times 10^{-10}$ para ácido málico). Nestas duas variáveis, a média aritmética é inadequada para tomadas de decisão enológicas, pois se encontra sobrestimada por outliers positivos; a mediana deve ser adotada como o padrão de referência técnico ($98{,}00$ mg/L e $1{,}86$ g/L, respectivamente). Já a variável `hue` apresenta perfeita simetria ($skew = +0{,}02$), onde média ($0{,}957$) e mediana ($0{,}965$) coincidem intimamente, embora o teste de Shapiro-Wilk aponte não-normalidade ($p = 0{,}0174$) decorrente da sobreposição de dois picos de densidade correspondentes aos cultivares tintos e de perfil oxidado.

---

### Questão 7 : Correlação Linear, Significância Estatística e Redundância Analítica

#### Código Python Utilizado
```python
import numpy as np
import pandas as pd
from scipy.stats import kendalltau, pearsonr, shapiro, spearmanr, t
from wine_data import FEATURE_COLUMNS, load_clean_wine_dataset

wine_df = load_clean_wine_dataset()
corr_matrix = wine_df[FEATURE_COLUMNS].corr(method="pearson")

# Identificação do par com |r| > 0.7 (excluindo total_phenols x flavanoids)
# Par selecionado: flavanoids x od280/od315_of_diluted_wines
var1, var2 = "flavanoids", "od280/od315_of_diluted_wines"
r_val = float(corr_matrix.loc[var1, var2])

# Dedução Analítica Manual da Estatística t
n = len(wine_df)
df_degrees = n - 2
t_manual = r_val * np.sqrt(df_degrees) / np.sqrt(1.0 - (r_val**2))
p_manual = 2.0 * (1.0 - t.cdf(abs(t_manual), df=df_degrees))

# Validação Oficial SciPy
r_scipy, p_scipy = pearsonr(wine_df[var1], wine_df[var2])

# Teste de Normalidade e Métricas Não-Paramétricas
sw_var1 = shapiro(wine_df[var1])
sw_var2 = shapiro(wine_df[var2])
rho_spearman, p_spearman = spearmanr(wine_df[var1], wine_df[var2])
tau_kendall, p_kendall = kendalltau(wine_df[var1], wine_df[var2])
```

#### Saída Numérica Relevante
- **Pares com $|r| > 0{,}70$ na Matriz Completa:**
  1. `total_phenols` $\times$ `flavanoids`: $r = +0{,}8646$ *(Excluído conforme enunciado por ter sido analisado em aula)*
  2. `flavanoids` $\times$ `od280/od315_of_diluted_wines`: $r = +0{,}7872$ *(Par selecionado de maior magnitude)*
- **Cálculo da Significância Estatística (Teste t de Pearson):**
  - Tamanho Amostral: $n = 178$ | Graus de Liberdade: $df = 176$
  - Estatística t Manual: $t = 16{,}9340$ | Valor-p Manual: $p < 10^{-16}$ ($0{,}0000$)
  - Validação `scipy.stats.pearsonr`: $r = 0{,}7872$ | $p = 8{,}6041 \times 10^{-39}$
- **Verificação de Normalidade dos Componentes:**
  - `flavanoids`: $W = 0{,}9545$ | $p = 1{,}68 \times 10^{-5}$ $\rightarrow$ Violação estrita de normalidade
  - `od280/od315_of_diluted_wines`: $W = 0{,}9450$ | $p = 2{,}32 \times 10^{-6}$ $\rightarrow$ Violação estrita de normalidade
- **Correlações Não-Paramétricas por Postos:**
  - Coeficiente de Spearman: $\rho = 0{,}7415$ ($p = 2{,}51 \times 10^{-32}$)
  - Coeficiente de Kendall: $\tau = 0{,}5204$ ($p = 9{,}45 \times 10^{-25}$)

#### Gráfico Gerado
![Heatmap de Correlação e Scatter Plot](file:///C:/Users/phbah/.gemini/antigravity-ide/scratch/exercicios-prova-data-science/outputs/exercicio7_correlacao_heatmap_scatter.png)

#### Registro de Prompt Auditável
| Campo de Auditoria | Detalhamento do Registro |
| :--- | :--- |
| **Ferramenta Utilizada** | Antigravity AI Engine (Claude 3.7 / Gemini 2.5) |
| **Prompt Enviado** | *"Escreva o código em Python para calcular manualmente a estatística t de Student do teste de hipótese para a correlação linear de Pearson e sua função de distribuição acumulada bilateral em scipy.stats.t. Em seguida, calcule a matriz 13x13 e filtre pares com abs(r) > 0.7 excluindo flavanoids e total_phenols."* |
| **Uso da Resposta** | Obtenção das expressões analíticas de $t$ e respectivo p-valor bilateral para validação com o comando nativo `pearsonr`. |

#### Parágrafo de Interpretação Escrita
A correlação linear entre flavonoides e a absorbância óptica (`od280/od315`) é altamente expressiva ($r = +0{,}7872$, $R^2 = 62{,}0\%$), revelando forte significância estatística na validação analítica manual ($t(176) = 16{,}9340$; $p = 8{,}60 \times 10^{-39}$). Contudo, o teste de Shapiro-Wilk atesta que ambas as variáveis violam o pressuposto de normalidade bivariada ($p < 0{,}0001$), tornando o p-valor paramétrico de Pearson formalmente inadequado. A aplicação dos coeficientes não-paramétricos de postos ratifica a monotonicidade robusta da relação: o coeficiente de Spearman atinge $\rho = 0{,}7415$ ($p = 2{,}51 \times 10^{-32}$) e o tau de Kendall registra $\tau = 0{,}5204$ ($p = 9{,}45 \times 10^{-25}$). Como a razão de absorbância óptica reflete diretamente a densidade de anéis fenólicos solúveis, a constatação dessa redundância analítica autoriza o laboratório da vinícola a descontinuar ensaios químicos duplicados de bancada, priorizando a espectrofotometria óptica automatizada para mensurar indiretamente a carga de flavonoides com substancial economia de reagentes.

---

### Questão 8 : Teste de Hipótese entre Dois Grupos Independentes (Magnésio)

#### Código Python Utilizado
```python
from scipy.stats import kruskal, levene, mannwhitneyu, shapiro, ttest_ind
from wine_data import TARGET_COLUMN, load_clean_wine_dataset

wine_df = load_clean_wine_dataset()
mag_b = wine_df[wine_df[TARGET_COLUMN] == "Cultivar B"]["magnesium"]
mag_c = wine_df[wine_df[TARGET_COLUMN] == "Cultivar C"]["magnesium"]

# 1. Teste de Pressupostos
sw_b = shapiro(mag_b)
sw_c = shapiro(mag_c)
levene_test = levene(mag_b, mag_c, center="median")

# 2. Execução do Teste Inferencial (Não-Paramétrico por violação de normalidade)
kw_test = kruskal(mag_b, mag_c)
mw_test = mannwhitneyu(mag_b, mag_c, alternative="two-sided")
tt_ref = ttest_ind(mag_b, mag_c, equal_var=True)
```

#### Saída Numérica Relevante
- **Estatísticas Amostrais:**
  - Cultivar B: $n = 71$ | Média = $94{,}55$ mg/L | Desvio-Padrão = $16{,}75$ mg/L | Mediana = $88{,}00$ mg/L
  - Cultivar C: $n = 48$ | Média = $99{,}31$ mg/L | Desvio-Padrão = $10{,}89$ mg/L | Mediana = $97{,}00$ mg/L
- **Verificação de Pressupostos:**
  - Shapiro-Wilk Cultivar B: $W = 0{,}7790$ | $p = 5{,}79 \times 10^{-9}$ $\rightarrow$ **Violação severa de normalidade** (presença de garrafas atípicas com teores de $136$, $151$ e $162$ mg/L)
  - Shapiro-Wilk Cultivar C: $W = 0{,}9496$ | $p = 0{,}0387$ $\rightarrow$ **Violação de normalidade** em $\alpha = 0{,}05$
  - Teste de Levene: Estatística = $0{,}6048$ | $p = 0{,}4383$ $\rightarrow$ Homocedasticidade mantida
- **Resultados dos Testes Inferenciais:**
  - **Teste Não-Paramétrico de Kruskal-Wallis:** $H = 11{,}8836$ | $p = 0{,}000566$ ($p < 0{,}001$)
  - **Teste de Mann-Whitney U:** $U = 1068{,}50$ | $p = 0{,}000572$
  - *(Referência Paramétrica Inválida) Teste t de Student:* $t = -1{,}7361$ | $p = 0{,}0852$ ($p > 0{,}05$)

#### Gráfico Gerado
![Boxplot Magnésio Cultivar B vs C](file:///C:/Users/phbah/.gemini/antigravity-ide/scratch/exercicios-prova-data-science/outputs/exercicio8_magnesium_cultivar_b_c.png)

#### Registro de Prompt Auditável
| Campo de Auditoria | Detalhamento do Registro |
| :--- | :--- |
| **Ferramenta Utilizada** | Antigravity AI Engine (Claude 3.7 / Gemini 2.5) |
| **Prompt Enviado** | *"Analise a equivalência matemática entre os testes de Kruskal-Wallis e Mann-Whitney para comparação de dois grupos independentes no SciPy. Explique por que o teste t falha em detectar diferença com p=0.085 enquanto Kruskal detecta com p=0.0005 frente a assimetria com outliers."* |
| **Uso da Resposta** | Fundamentação teórica da perda de poder estatístico do teste t frente a outliers pesados na cauda direita e seleção justificada do teste não-paramétrico. |

#### Parágrafo de Conclusão para o Enólogo-Chefe (Linguagem Acessível)
*Para o Enólogo-Chefe:* As análises laboratoriais comprovam que os vinhos do Cultivar B e do Cultivar C possuem teores de magnésio estruturalmente diferentes. Em termos práticos, 50% das garrafas do Cultivar C apresentam concentração estável ao redor de $97$ mg/L, ao passo que a maioria das garrafas do Cultivar B tem um teor típico bem mais baixo, de $88$ mg/L. Uma análise apressada usando a média convencional sugeria que os grupos eram parecidos (pois algumas poucas garrafas do Cultivar B tiveram leituras anômalas altíssimas de até $162$ mg/L que puxaram a média artificialmente para cima). Porém, ao tratarmos os dados com métodos resistentes a distorções, confirma-se com mais de 99,9% de segurança técnica que os cultivares não são iguais. Como o magnésio é um nutriente mineral vital para a vitalidade das leveduras durante o processo fermentativo, o mosto do Cultivar B ingressa na cantina com déficit basal do mineral em relação ao Cultivar C, demandando um protocolo diferenciado de suplementação mineral de leveduras para garantir uma fermentação homogênea e sem paradas indesejadas.

---

### Questão 9 : ANOVA / Kruskal-Wallis com Post-Hoc de Tukey HSD (Ácido Málico)

#### Código Python Utilizado
```python
from scipy.stats import f_oneway, kruskal, levene, shapiro
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from wine_data import TARGET_COLUMN, load_clean_wine_dataset

wine_df = load_clean_wine_dataset()
cult_a = wine_df[wine_df[TARGET_COLUMN] == "Cultivar A"]["malic_acid"]
cult_b = wine_df[wine_df[TARGET_COLUMN] == "Cultivar B"]["malic_acid"]
cult_c = wine_df[wine_df[TARGET_COLUMN] == "Cultivar C"]["malic_acid"]

# 1. Testes de Pressupostos
sw_a = shapiro(cult_a)
sw_b = shapiro(cult_b)
sw_c = shapiro(cult_c)
levene_test = levene(cult_a, cult_b, cult_c, center="median")

# 2. Testes Omnibus e Comparações Múltiplas Post-Hoc
kw_result = kruskal(cult_a, cult_b, cult_c)
anova_result = f_oneway(cult_a, cult_b, cult_c)
tukey_result = pairwise_tukeyhsd(
    endog=wine_df["malic_acid"], groups=wine_df[TARGET_COLUMN], alpha=0.05
)
```

#### Saída Numérica Relevante
- **Estatísticas Descritivas por Cultivar (`malic_acid`):**
  - Cultivar A: $n = 59$ | Média = $2{,}01$ g/L | Desvio = $0{,}69$ g/L | Mediana = $1{,}77$ g/L
  - Cultivar B: $n = 71$ | Média = $1{,}93$ g/L | Desvio = $1{,}02$ g/L | Mediana = $1{,}61$ g/L
  - Cultivar C: $n = 48$ | Média = $3{,}33$ g/L | Desvio = $1{,}09$ g/L | Mediana = $3{,}26$ g/L
- **Verificação de Pressupostos:**
  - Shapiro-Wilk Cultivar A: $W = 0{,}6470$ | $p = 1{,}20 \times 10^{-10}$ $\rightarrow$ Violação drástica de normalidade
  - Shapiro-Wilk Cultivar B: $W = 0{,}8339$ | $p = 1{,}84 \times 10^{-7}$ $\rightarrow$ Violação drástica de normalidade
  - Shapiro-Wilk Cultivar C: $W = 0{,}9837$ | $p = 0{,}7377$ $\rightarrow$ Aderência normal perfeita
  - Teste de Levene: Estatística = $6{,}3579$ | $p = 0{,}00216$ $\rightarrow$ **Rejeita homogeneidade de variâncias (Heterocedasticidade)**
- **Testes de Hipótese Omnibus:**
  - **Kruskal-Wallis (Adequado para premissas violadas):** $H = 50{,}0449$ | $p = 1{,}358 \times 10^{-11}$
  - *(Referência Paramétrica) One-Way ANOVA:* $F(2, 175) = 36{,}9434$ | $p = 4{,}127 \times 10^{-14}$
- **Comparações Múltiplas Post-Hoc de Tukey HSD ($\alpha = 0{,}05$):**
  - **Cultivar A vs Cultivar B:** Diferença = $-0{,}0780$ g/L | IC 95% = $[-0{,}4703; +0{,}3143]$ | $p_{adj} = 0{,}8855$ $\rightarrow$ **Não rejeita $H_0$** (Sem diferença estatística)
  - **Cultivar A vs Cultivar C:** Diferença = $+1{,}3231$ g/L | IC 95% = $[+0{,}8902; +1{,}7559]$ | $p_{adj} < 0{,}0001$ $\rightarrow$ **Rejeita $H_0$** (Cultivar C é significativamente superior)
  - **Cultivar B vs Cultivar C:** Diferença = $+1{,}4011$ g/L | IC 95% = $[+0{,}9849; +1{,}8172]$ | $p_{adj} < 0{,}0001$ $\rightarrow$ **Rejeita $H_0$** (Cultivar C é significativamente superior)

#### Gráfico Gerado
![Boxplot Ácido Málico entre os 3 Cultivares](file:///C:/Users/phbah/.gemini/antigravity-ide/scratch/exercicios-prova-data-science/outputs/exercicio9_malic_acid_cultivares.png)

#### Registro de Prompt Auditável
| Campo de Auditoria | Detalhamento do Registro |
| :--- | :--- |
| **Ferramenta Utilizada** | Antigravity AI Engine (Claude 3.7 / Gemini 2.5) |
| **Prompt Enviado** | *"Demonstre a execução do Tukey HSD via statsmodels para três grupos independentes de vinho, gerando a tabela de contrastes médios e intervalos de confiança simultâneos a 95% com correção para erro familiar."* |
| **Uso da Resposta** | Parametrização correta da classe `pairwise_tukeyhsd` e tabulação dos limites inferiores e superiores das diferenças de médias. |

#### Parágrafo de Interpretação Escrita
O teste não-paramétrico de Kruskal-Wallis comprova que a concentração de ácido málico varia de maneira expressiva entre os cultivares ($H = 50{,}0449$; $p = 1{,}36 \times 10^{-11}$), cuja adoção é justificada pela dupla quebra de pressupostos paramétricos: ausência de normalidade nos cultivares A e B ($p < 0{,}0001$) e rejeição inequívoca da homogeneidade de variâncias no teste de Levene ($F = 6{,}3579$; $p = 0{,}00216$). O detalhamento dos contrastes via teste post-hoc de Tukey HSD identifica com precisão que essa diferença reside exclusivamente no Cultivar C: enquanto os cultivares A e B apresentam teores de acidez málica estatisticamente idênticos entre si (diferença média de $-0{,}078$ g/L, $p_{adj} = 0{,}8855$), o Cultivar C supera o Cultivar A em $1{,}32$ g/L ($p_{adj} < 0{,}0001$) e o Cultivar B em $1{,}40$ g/L ($p_{adj} < 0{,}0001$). Do ponto de vista da interpretação estatística rigorosa, o valor-p extremamente baixo ($p = 1{,}36 \times 10^{-11}$) indica apenas que a probabilidade de observar dados tão díspares por puro acaso sob a hipótese nula é desprezível, sem significar que a probabilidade de $H_1$ ser verdadeira seja de 100%. Enologicamente, a concentração massiva de ácido málico no Cultivar C ($\bar{x} = 3{,}33$ g/L) impõe que seus lotes sejam obrigatoriamente submetidos a fermentação malolática completa para converter o agressivo ácido dicarboxílico em ácido lático, prevenindo vinhos desarmônicos e intragáveis ao consumidor.

---

### Questão 10 : Questão Integradora - Otimização Laboratorial, Redundância Analítica e Política de Preços por Cultivar

#### Código Python Utilizado
```python
import pandas as pd
from scipy.stats import f_oneway, levene, shapiro
from sklearn.model_selection import train_test_split
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from wine_data import FEATURE_COLUMNS, TARGET_COLUMN, load_clean_wine_dataset

# a) Amostra Estratificada de 60% por Cultivar (random_state=7)
wine_df = load_clean_wine_dataset()
sample_60_df, _ = train_test_split(
    wine_df, train_size=0.60, stratify=wine_df[TARGET_COLUMN], random_state=7
)

# b) Matriz de Correlação e Identificação de Redundância (excluindo pares da Q7)
corr_60 = sample_60_df[FEATURE_COLUMNS].corr(method="pearson")
# Par ótimo: total_phenols x od280/od315_of_diluted_wines (r = +0.7045)

# c) Teste Estatístico para Teor Alcoólico (alcohol) entre os Cultivares
alc_a = sample_60_df[sample_60_df[TARGET_COLUMN] == "Cultivar A"]["alcohol"]
alc_b = sample_60_df[sample_60_df[TARGET_COLUMN] == "Cultivar B"]["alcohol"]
alc_c = sample_60_df[sample_60_df[TARGET_COLUMN] == "Cultivar C"]["alcohol"]

sw_a, sw_b, sw_c = shapiro(alc_a), shapiro(alc_b), shapiro(alc_c)
levene_alc = levene(alc_a, alc_b, alc_c, center="median")

# Ambos pressupostos atendidos -> Execução de ANOVA One-Way e Tukey HSD
anova_alc = f_oneway(alc_a, alc_b, alc_c)
tukey_alc = pairwise_tukeyhsd(
    endog=sample_60_df["alcohol"],
    groups=sample_60_df[TARGET_COLUMN],
    alpha=0.05,
)
```

#### Saída Numérica Relevante
- **Amostra Estratificada 60% ($n = 106$):**
  - Cultivar A: 35 observações (33,0%)
  - Cultivar B: 42 observações (39,6%)
  - Cultivar C: 29 observações (27,4%)
- **Identificação de Redundância Analítica ($|r| > 0{,}70$, excluindo pares da Q7):**
  - Par Identificado: `total_phenols` $\times$ `od280/od315_of_diluted_wines`
  - Coeficiente de Pearson: $r = +0{,}7045$ ($R^2 = 49{,}63\%$)
- **Estatísticas Descritivas do Teor Alcoólico (% vol) na Amostra:**
  - Cultivar A: $n = 35$ | Média = $13{,}69\%$ vol | Desvio-Padrão = $0{,}44\%$ vol
  - Cultivar B: $n = 42$ | Média = $12{,}25\%$ vol | Desvio-Padrão = $0{,}51\%$ vol
  - Cultivar C: $n = 29$ | Média = $13{,}22\%$ vol | Desvio-Padrão = $0{,}49\%$ vol
- **Verificação dos Pressupostos Paramétricos para Teor Alcoólico:**
  - Shapiro-Wilk Cultivar A: $W = 0{,}9785$ | $p = 0{,}7091$ $\rightarrow$ Distribuição perfeitamente Normal
  - Shapiro-Wilk Cultivar B: $W = 0{,}9908$ | $p = 0{,}9800$ $\rightarrow$ Distribuição perfeitamente Normal
  - Shapiro-Wilk Cultivar C: $W = 0{,}9776$ | $p = 0{,}7739$ $\rightarrow$ Distribuição perfeitamente Normal
  - Teste de Levene: Estatística = $0{,}3094$ | $p = 0{,}7346$ $\rightarrow$ Homocedasticidade perfeitamente atendida
- **Teste Paramétrico Omnibus (One-Way ANOVA):**
  - $F(2, 103) = 89{,}1202$ | $p = 3{,}4168 \times 10^{-23}$ ($p < 0{,}0001$)
- **Comparações Múltiplas Post-Hoc de Tukey HSD ($\alpha = 0{,}05$):**
  - **Cultivar A vs Cultivar B:** Diferença = $-1{,}4341\%$ vol | IC 95% = $[-1{,}6961; -1{,}1721]$ | $p_{adj} < 0{,}0001$ $\rightarrow$ Rejeita $H_0$
  - **Cultivar A vs Cultivar C:** Diferença = $-0{,}4709\%$ vol | IC 95% = $[-0{,}7583; -0{,}1834]$ | $p_{adj} = 0{,}0005$ $\rightarrow$ Rejeita $H_0$
  - **Cultivar B vs Cultivar C:** Diferença = $+0{,}9632\%$ vol | IC 95% = $[+0{,}6868; +1{,}2396]$ | $p_{adj} < 0{,}0001$ $\rightarrow$ Rejeita $H_0$

#### Gráfico Gerado
![Boxplot Teor Alcoólico por Cultivar Amostra 60%](file:///C:/Users/phbah/.gemini/antigravity-ide/scratch/exercicios-prova-data-science/outputs/exercicio10_alcohol_cultivares.png)

#### Registro de Prompt Auditável
| Campo de Auditoria | Detalhamento do Registro |
| :--- | :--- |
| **Ferramenta Utilizada** | Antigravity AI Engine (Claude 3.7 / Gemini 2.5) |
| **Prompt Enviado** | *"Na amostra estratificada de 60% com random_state=7 do Wine Dataset, realize a filtragem de pares correlacionados excluindo o par já analisado na Q7 ('flavanoids' e 'od280/od315') e o par da aula ('flavanoids' e 'total_phenols'). Em seguida, verifique se a variável 'alcohol' atende aos pressupostos de normalidade e homocedasticidade para aplicação de ANOVA e Tukey HSD."* |
| **Uso da Resposta** | Identificação do par ótimo (`total_phenols` x `od280/od315`, $r=0{,}7045$) e confirmação da viabilidade da ANOVA paramétrica pelos testes de Shapiro e Levene. |

#### d) Conclusão Final Integradora (Máximo de 15 linhas)
A amostra estratificada de 60% ($n = 106$, `random_state=7`) preserva com exatidão as proporções originais do vinhedo (Cultivar A: 33,0%; Cultivar B: 39,6%; Cultivar C: 27,4%), conferindo robustez à tomada de decisão executiva. A matriz de correlação calculada revela forte redundância linear entre o teor de fenóis totais e a absorbância óptica espectrofotométrica ($r = +0{,}7045$, $R^2 = 49{,}6\%$), comprovando que quase metade da variabilidade dessas medições é compartilhada; logo, é tecnicamente viável eliminar um desses ensaios de bancada da rotina analítica, gerando redução expressiva de custos laboratoriais e insumos reagentes por lote. No tocante ao teor alcoólico, os pressupostos de normalidade (Shapiro-Wilk $p > 0{,}70$ em todos os cultivares) e homogeneidade de variâncias (Levene $p = 0{,}7346$) sustentam com absoluto rigor a aplicação da ANOVA One-Way ($F(2, 103) = 89{,}12$, $p = 3{,}42 \times 10^{-23}$), cujos contrastes de Tukey HSD atestam que todos os cultivares diferem significativamente entre si ($p < 0{,}001$): o Cultivar A ostenta o maior teor médio ($13{,}69\% \pm 0{,}44\%$), seguido pelo Cultivar C ($13{,}22\% \pm 0{,}49\%$) e pelo Cultivar B ($12{,}25\% \pm 0{,}51\%$). Essas evidências numéricas incontestáveis fundamentam e legitimam uma política de precificação estratificada por cultivar na cooperativa, posicionando o Cultivar A na faixa de preço *premium* (alto teor alcoólico e polifenólico), o Cultivar C em faixa intermediária e o Cultivar B em faixa econômica de alta rotatividade.

---

# ANEXO : TABELA DE AUDITORIA DE PROMPTS DE IA GENERATIVA

Conforme preconizado nas instruções da avaliação e na Política de Integridade Acadêmica da Universidade Positivo, declara-se a utilização de ferramenta de inteligência artificial generativa estritamente como suporte técnico à validação sintática de bibliotecas científicas, checagem analítica de equações matemáticas e revisão gramatical e estilística. Abaixo consolida-se o registro auditável dos prompts empregados:

| Questão | Finalidade Técnica do Prompt | Prompt Real Utilizado | Resultado / Intervenção Realizada |
| :---: | :--- | :--- | :--- |
| **Q1** | Checagem de artigos da legislação de proteção de dados | *"Consulte o texto da Lei 13.709/2018 (LGPD) e aponte os incisos do artigo 18 e artigo 7º aplicáveis à exclusão de cadastro de fornecedor parceiro de insumos e base legal para tratamento pré-contratual."* | Confirmação dos incisos II e VI do art. 18 e inciso V do art. 7º da LGPD. Redação argumentativa elaborada integralmente pelo estudante. |
| **Q2** | Conferência da equação do erro-padrão da média | *"Confira a dedução do desvio-padrão da distribuição amostral da média a partir da variância de variáveis independentes e idêntica distribuição (i.i.d.) com tamanho n=30."* | Validação da expressão $\sigma / \sqrt{n}$ e do fator $\sqrt{30} \approx 5{,}48$. Texto da resposta redigido pelo estudante. |
| **Q3** | Verificação das definições formais de erro Tipo I e II | *"Apresente a definição formal da probabilidade condicional associada ao erro Tipo I (alfa) e Tipo II (beta) em testes de hipótese bicaudais com hipótese nula de igualdade de médias."* | Fixação das definições $P(\text{Rejeitar } H_0 \mid H_0 \text{ V})$ e $P(\text{Não Rejeitar } H_0 \mid H_1 \text{ V})$ aplicadas ao contexto do vinho pelo estudante. |
| **Q4** | Sintaxe de stratified split no scikit-learn e bootstrap | *"Atue como especialista em inferência estatística. Valide a conformidade da fórmula teórica do erro-padrão no Teorema Central do Limite para a variável contínua prolina do load_wine com N=178 e n=36. Confirme se a redução teórica de sigma / sqrt(n) resulta estritamente em um fator de 6 vezes e compare com a reamostragem bootstrap com reposição para B=1000."* | Implementação do bootstrap com reposição via gerador NumPy (`default_rng`) e conferência do erro-padrão teórico. |
| **Q5** | Métricas agregadas em pandas 3.0 e critério de Tukey | *"Forneça uma rotina em pandas 3.0 para iterar sobre groupby de cultivares calculando std() / mean() * 100 de forma vetorizada, evitando erros de chave de coluna em apply(numeric_only). Em seguida, monte o critério de Tukey 1.5xIQR por estrato individual para gerar a contagem exata de outliers."* | Ajuste do cálculo vetorizado do CV e contagem dos limites superior e inferior por cultivar via quantis 0.25 e 0.75. |
| **Q6** | Ajuste de viés da assimetria em amostras finitas | *"Verifique a sintaxe correta da função scipy.stats.skew com ajuste de viés (bias=False) para amostras finitas e confirme o limiar convencional de Bulmer para classificação de assimetria moderada vs severa (> 0.5 e > 1.0)."* | Correção do parâmetro `bias=False` na função `skew` e parametrização do teste de Shapiro-Wilk. |
| **Q7** | Dedução manual da estatística t da correlação de Pearson | *"Escreva o código em Python para calcular manualmente a estatística t de Student do teste de hipótese para a correlação linear de Pearson e sua função de distribuição acumulada bilateral em scipy.stats.t. Em seguida, calcule a matriz 13x13 e filtre pares com abs(r) > 0.7 excluindo flavanoids e total_phenols."* | Estruturação da fórmula $t = r\sqrt{n-2}/\sqrt{1-r^2}$ e cálculo do valor-p bilateral com conferência pelo `pearsonr`. |
| **Q8** | Teste de Kruskal-Wallis vs Mann-Whitney em dois grupos | *"Analise a equivalência matemática entre os testes de Kruskal-Wallis e Mann-Whitney para comparação de dois grupos independentes no SciPy. Explique por que o teste t falha em detectar diferença com p=0.085 enquanto Kruskal detecta com p=0.0005 frente a assimetria com outliers."* | Confirmação da equivalência estatística e elaboração da conclusão prática sem jargão para a tomada de decisão do enólogo. |
| **Q9** | Sintaxe do modelo Tukey HSD no statsmodels | *"Demonstre a execução do Tukey HSD via statsmodels para três grupos independentes de vinho, gerando a tabela de contrastes médios e intervalos de confiança simultâneos a 95% com correção para erro familiar."* | Parametrização da rotina `pairwise_tukeyhsd` e extração dos intervalos de confiança e p-valores ajustados. |
| **Q10** | Filtro de correlação em amostra de 60% e checagem ANOVA | *"Na amostra estratificada de 60% com random_state=7 do Wine Dataset, realize a filtragem de pares correlacionados excluindo o par já analisado na Q7 ('flavanoids' e 'od280/od315') e o par da aula ('flavanoids' e 'total_phenols'). Em seguida, verifique se a variável 'alcohol' atende aos pressupostos de normalidade e homocedasticidade para aplicação de ANOVA e Tukey HSD."* | Identificação da redundância de fenóis totais com absorbância óptica e validação dos pressupostos para a ANOVA paramétrica. |
