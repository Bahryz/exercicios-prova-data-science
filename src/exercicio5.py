"""Exercício 5: Medidas de Posição, Dispersão, Coeficiente de Variação (CV) e Detecção de Outliers (IQR).

Calcula estatísticas descritivas completas para as 13 variáveis por cultivar,
identifica as variáveis de maior dispersão relativa e mapeia anomalias enológicas.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from wine_data import (
    FEATURE_COLUMNS,
    PALETA_CULTIVARES,
    TARGET_COLUMN,
    configure_visual_standards,
    load_clean_wine_dataset,
)


def compute_descriptive_statistics_by_cultivar(
    wine_dataframe: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series]:
    """Calcula média, mediana, desvio-padrão e CV (%) para todas as 13 variáveis

    agrupadas por cultivar de uva, além do CV médio entre os cultivares.

    Args:
        wine_dataframe: DataFrame com as características e coluna de cultivar.

    Returns:
        Tuple[pd.DataFrame, pd.Series]:
            - DataFrame multi-índice consolidado com as 4 estatísticas descritivas.
            - Série com o CV médio de cada variável ordenado decrescentemente.
    """
    grouped_cultivars = wine_dataframe.groupby(TARGET_COLUMN)

    mean_metrics = grouped_cultivars[FEATURE_COLUMNS].mean()
    median_metrics = grouped_cultivars[FEATURE_COLUMNS].median()
    std_metrics = grouped_cultivars[FEATURE_COLUMNS].std()
    cv_metrics = (std_metrics / mean_metrics) * 100.0

    consolidated_records: List[Dict[str, object]] = []
    for cultivar_label in ["Cultivar A", "Cultivar B", "Cultivar C"]:
        for feature_name in FEATURE_COLUMNS:
            consolidated_records.append(
                {
                    "cultivar": cultivar_label,
                    "variavel": feature_name,
                    "media": mean_metrics.loc[cultivar_label, feature_name],
                    "mediana": median_metrics.loc[cultivar_label, feature_name],
                    "desvio_padrao": std_metrics.loc[
                        cultivar_label, feature_name
                    ],
                    "cv_percentual": cv_metrics.loc[
                        cultivar_label, feature_name
                    ],
                }
            )

    descriptive_df = pd.DataFrame(consolidated_records)
    mean_cv_per_feature = cv_metrics.mean(axis=0).sort_values(ascending=False)

    return descriptive_df, mean_cv_per_feature


def detect_outliers_iqr_by_cultivar(
    wine_dataframe: pd.DataFrame, target_variables: List[str]
) -> pd.DataFrame:
    """Aplica o critério de Tukey (1,5 * IQR) para detectar e quantificar outliers

    intragrupo para cada cultivar nas variáveis selecionadas.

    Args:
        wine_dataframe: DataFrame populacional completo.
        target_variables: Lista das variáveis de interesse (ex.: top 3 CV).

    Returns:
        pd.DataFrame: Resumo contendo limites inferior/superior e contagem de outliers.
    """
    outlier_summary_records: List[Dict[str, object]] = []

    for variable_name in target_variables:
        for cultivar_label in ["Cultivar A", "Cultivar B", "Cultivar C"]:
            cultivar_subset = wine_dataframe[
                wine_dataframe[TARGET_COLUMN] == cultivar_label
            ][variable_name]
            first_quartile = float(cultivar_subset.quantile(0.25))
            third_quartile = float(cultivar_subset.quantile(0.75))
            interquartile_range = third_quartile - first_quartile

            lower_bound = first_quartile - 1.5 * interquartile_range
            upper_bound = third_quartile + 1.5 * interquartile_range

            outlier_series = cultivar_subset[
                (cultivar_subset < lower_bound)
                | (cultivar_subset > upper_bound)
            ]

            outlier_summary_records.append(
                {
                    "variavel": variable_name,
                    "cultivar": cultivar_label,
                    "n_total": len(cultivar_subset),
                    "q1": first_quartile,
                    "q3": third_quartile,
                    "iqr": interquartile_range,
                    "limite_inferior": lower_bound,
                    "limite_superior": upper_bound,
                    "quantidade_outliers": len(outlier_series),
                    "valores_outliers": [
                        round(val, 2) for val in outlier_series.tolist()
                    ],
                }
            )

    return pd.DataFrame(outlier_summary_records)


def plot_top3_cv_boxplots(
    wine_dataframe: pd.DataFrame,
    top_3_variables: List[str],
    output_filepath: Path,
) -> None:
    """Gera painel de boxplots comparativos com distribuição dos cultivares.

    Args:
        wine_dataframe: DataFrame com dados físico-químicos e rótulos.
        top_3_variables: Lista com as 3 variáveis de maior CV médio.
        output_filepath: Caminho do arquivo para gravação.
    """
    configure_visual_standards()
    figure, axes_array = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    variable_labels_map = {
        "malic_acid": "Ácido Málico (g/L)",
        "proanthocyanins": "Proantocianinas (g/L)",
        "nonflavanoid_phenols": "Fenóis Não-Flavonoides (g/L)",
    }

    for axis_index, variable_name in enumerate(top_3_variables):
        current_axis = axes_array[axis_index]
        sns.boxplot(
            data=wine_dataframe,
            x=TARGET_COLUMN,
            y=variable_name,
            hue=TARGET_COLUMN,
            palette=PALETA_CULTIVARES,
            ax=current_axis,
            width=0.45,
            fliersize=5,
            flierprops={"marker": "D", "markerfacecolor": "#B22222"},
            legend=False,
        )
        sns.stripplot(
            data=wine_dataframe,
            x=TARGET_COLUMN,
            y=variable_name,
            color="#222222",
            alpha=0.35,
            jitter=0.15,
            size=4,
            ax=current_axis,
        )
        current_axis.set_title(
            f"{variable_labels_map.get(variable_name, variable_name)}",
            fontsize=11,
            pad=10,
        )
        current_axis.set_xlabel("")
        current_axis.set_ylabel("Concentração")
        current_axis.grid(True, linestyle="--", alpha=0.3)

    figure.suptitle(
        "Dispersão e Outliers (Regra 1,5×IQR) - Top 3 Variáveis em Coeficiente de Variação (CV)",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    figure.savefig(output_filepath, dpi=300, bbox_inches="tight")
    plt.close(figure)


def run_exercise_5() -> Tuple[pd.Series, pd.DataFrame]:
    """Executa a rotina analítica do Exercício 5."""
    wine_dataframe = load_clean_wine_dataset()
    descriptive_df, mean_cv_per_feature = (
        compute_descriptive_statistics_by_cultivar(wine_dataframe)
    )

    top_3_cv_variables = mean_cv_per_feature.head(3).index.tolist()
    outlier_df = detect_outliers_iqr_by_cultivar(
        wine_dataframe, top_3_cv_variables
    )

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "exercicio5_top3_cv_boxplots.png"
    plot_top3_cv_boxplots(wine_dataframe, top_3_cv_variables, figure_path)

    print("=== EXERCÍCIO 5: MEDIDAS DE POSIÇÃO, DISPERSÃO E OUTLIERS ===")
    print("\n--- Ranking de Variáveis por Coeficiente de Variação Médio (%) ---")
    for rank_idx, (feature_name, cv_value) in enumerate(
        mean_cv_per_feature.items(), start=1
    ):
        print(f"{rank_idx:2d}. {feature_name:<28}: CV Médio = {cv_value:6.2f}%")

    print(
        f"\nVariável com maior CV médio: {top_3_cv_variables[0]} ({mean_cv_per_feature.iloc[0]:.2f}%)"
    )
    print(f"Top 3 variáveis com maior CV médio: {', '.join(top_3_cv_variables)}")

    print("\n--- Detecção de Outliers Intragrupo (Regra 1,5×IQR) ---")
    for _, outlier_row in outlier_df.iterrows():
        print(
            f"Variável: {outlier_row['variavel']:<20} | {outlier_row['cultivar']:<10} | "
            f"Q1={outlier_row['q1']:5.2f} | Q3={outlier_row['q3']:5.2f} | "
            f"Limite Sup={outlier_row['limite_superior']:5.2f} | "
            f"Outliers={outlier_row['quantidade_outliers']:2d} {outlier_row['valores_outliers']}"
        )

    # Verificação de homogeneidade global
    pivoted_cv = descriptive_df.pivot(
        index="variavel", columns="cultivar", values="cv_percentual"
    )
    lowest_cv_distribution = pivoted_cv.idxmin(axis=1).value_counts()
    print("\n--- Contagem de Variáveis em que cada Cultivar teve o menor CV ---")
    for cultivar_label, count_val in lowest_cv_distribution.items():
        print(f"  {cultivar_label}: {count_val} variáveis com menor CV")

    print(f"\nFigura gerada e gravada em: {figure_path}\n")

    return mean_cv_per_feature, outlier_df


if __name__ == "__main__":
    run_exercise_5()
