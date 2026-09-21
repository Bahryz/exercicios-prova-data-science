---
name: clean-code-ds
description: Diretrizes estritas de Clean Code e engenharia de software aplicadas a Python e Data Science no domínio vitivinícola.
---

# Diretrizes de Clean Code para Ciência de Dados e Estatística

Este documento estabelece as regras de arquitetura de software e estilo de código a serem seguidas rigorosamente em scripts de análise estatística e ciência de dados.

## 1. Princípio da Responsabilidade Única (SRP) e Funções Curtas
- Cada função deve desempenhar apenas uma tarefa conceitual bem definida (ex.: carregar dados, calcular matriz de correlação, executar teste de normalidade, plotar gráfico).
- Funções devem ter tamanho enxuto (preferencialmente abaixo de 25-30 linhas).
- Funções de cálculo estatístico não devem realizar manipulações de interface nem salvar arquivos em disco; o salvamento e a apresentação gráfica devem ser delegados a funções de visualização dedicadas.

## 2. Nomenclatura Expressiva no Domínio Vitivinícola
- Variáveis, constantes e funções devem adotar vocabulário técnico rigoroso e contextualizado ao domínio do vinho e da análise laboratorial.
- **Proibição absoluta de variáveis descartáveis e crípticas**:
  - Proibido o uso de nomes como `df`, `df1`, `df2`, `temp`, `data`, `res`, `aux`, `x`, `y` (exceto `x` e `y` estritamente como coordenadas em loops de anotação gráfica pura).
  - Exemplos recomendados: `wine_features_df`, `cultivar_series`, `proline_concentration_mg_l`, `phenolic_correlation_matrix`, `normality_test_result`.

## 3. Tipagem Estrita (Type Hints)
- Todas as funções, métodos e parâmetros devem conter anotações de tipo (`typing` e `pandas/numpy`):
  ```python
  from typing import Dict, List, Optional, Tuple, Union
  import pandas as pd
  import numpy as np

  def calculate_coefficient_of_variation(
      chemical_values: pd.Series,
  ) -> float: ...
  ```

## 4. Ausência de Comentários Óbvios
- Não comente sintaxe básica da linguagem ou o que o código já expressa por si só (ex.: `# itera sobre as colunas`, `# importa pandas`).
- Utilize docstrings no formato padrão para explicar contratos, suposições estatísticas e fórmulas matemáticas quando não triviais.

## 5. Padronização Global de Estilo Visual (Matplotlib e Seaborn)
- Todas as rotinas de visualização devem definir configurações visuais globais elegantes e consistentes:
  - Resolução gráfica mínima de 300 DPI (`dpi=300`).
  - Paleta de cores sóbria e harmoniosa (ex.: Seaborn `color_palette('colorblind')` ou tons vinho/ardósia: `#722F37`, `#2E5B88`, `#507255`).
  - Títulos descritivos (`title`), eixos rotulados com grandezas e unidades (`xlabel`, `ylabel`), e legendas com os cultivares devidamente identificados.
  - Grade suave (`alpha=0.25` a `0.3`) e ausência de ruído gráfico desnecessário (chartjunk).
