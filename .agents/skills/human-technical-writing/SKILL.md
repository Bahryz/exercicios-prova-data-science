---
name: human-technical-writing
description: Diretrizes de redação técnica e acadêmica humana para relatórios de Data Science, eliminando clichês de IA e focando em evidências numéricas e impacto prático.
---

# Diretrizes de Redação Técnica e Acadêmica Humana

Este documento define o padrão de escrita analítica para a elaboração de relatórios técnicos de avaliação e relatórios executivos para a vinícola.

## 1. Estrutura Canônica: Decisão Técnica + Evidência Numérica
- Toda afirmação analítica deve ser acompanhada imediatamente pelo suporte numérico exato que a fundamenta:
  - Citar a métrica exata: estatística de teste ($t$, $W$, $F$, $H$), valor-p com quatro casas decimais ou notação científica, Coeficiente de Variação ($CV\%$), média ($\bar{x}$) e desvio-padrão ($s$).
  - Evitar generalizações vagas como "o cultivar A tem valor mais alto" ou "a diferença foi significativa".
  - Modelo canônico: *"Adota-se a hipótese alternativa de diferenciação entre Cultivar A e Cultivar B para o teor alcoólico ($t(128) = 11{,}28$; $p = 4{,}12 \times 10^{-21}$), dado que a média observada no Cultivar A ($\bar{x} = 13{,}74\%$) supera em 1,51 ponto percentual a do Cultivar B ($\bar{x} = 12{,}23\%$)."*

## 2. Ritmo e Variação de Extensão Sintática
- Redija parágrafos com variação natural de extensão de períodos (frases curtas assertivas mescladas a sentenças compostas com orações subordinadas técnicas).
- Adote voz ativa quando relatar decisões metodológicas e impessoalidade sóbria ao descrever propriedades matemáticas e distribucionais.

## 3. Banimento Estrito de Clichês e Vícios de Linguagem de Modelos de IA
- É expressamente proibido o uso das seguintes expressões e correlatas:
  - "É crucial notar que..." / "É importante destacar..."
  - "Vamos mergulhar em..." / "Mergulho fascinante..."
  - "Em suma..." / "Em resumo..." / "Para concluir..."
  - "Como um cientista de dados experiente..."
  - "Uma dança de números..." / metáforas poéticas vazias.
  - "Este relatório tem como objetivo demonstrar..."
- A redação deve soar como um relatório técnico elaborado por um pesquisador sênior em química enológica e inferência estatística aplicada.

## 4. Foco no Impacto Prático para a Vinícola
- Conectar cada conclusão matemática a desdobramentos operacionais e estratégicos reais da cooperativa vinícola:
  - **Custos laboratoriais e eficiência analítica**: redução de ensaios duplicados por variáveis altamente colineares ($|r| > 0{,}7$).
  - **Controle de vinificação e estabilidade microbiológica**: implicações de compostos como ácido málico na fermentação malolática e magnésio como cofator leveduriforme.
  - **Política de precificação e rotulagem**: viabilidade de justificar faixas de preço superiores a partir de diferenciais consistentes de teor alcoólico e perfil fenólico.
