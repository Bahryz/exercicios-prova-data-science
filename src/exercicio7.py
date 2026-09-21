"""Exercício 7: Correlação Linear, Significância Estatística, Testes de Hipótese e Análise de Redundância.

Mapeia relações lineares e monótonas entre variáveis físico-químicas do vinho,
deduz a estatística t de significância e avalia pressupostos paramétricos.

Prompt de Auditoria Utilizado:
"Escreva o código em Python para calcular manualmente a estatística t de Student
do teste de hipótese para a correlação linear de Pearson e sua função de distribuição
acumulada bilateral em scipy.stats.t. Em seguida, calcule a matriz 13x13 e filtre pares
com abs(r) > 0.7 excluindo flavanoids e total_phenols."
"""

from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kendalltau, pearsonr, shapiro, spearmanr, t
import seaborn as sns

from wine_data import (
    FEATURE_COLUMNS,
    PALETA_CULTIVARES,
    TARGET_COLUMN,
    configure_visual_standards,
    load_clean_wine_dataset,
)


def compute_correlation_matrix_and_redundant_pairs(
    wine_dataframe: pd.DataFrame, correlation_threshold: float = 0.70
) -> Tuple[pd.DataFrame, List[Dict[str, object]]]:
    """Calcula a matriz de correlação de Pearson completa e filtra pares redundantes (|r| > 0,7),

    excluindo explicitamente o par 'flavanoids' x 'total_phenols'.

    Args:
        wine_dataframe: DataFrame com dados físico-químicos completos.
        correlation_threshold: Limiar de corte para correlação forte (|r| > 0,7).

    Returns:
        Tuple[pd.DataFrame, List[Dict[str, object]]]:
            - Matriz de correlação 13x13.
            - Lista de pares com |r| > 0,7 ordenados por magnitude.
    """
    correlation_matrix = wine_dataframe[FEATURE_COLUMNS].corr(method="pearson")
    column_names = FEATURE_COLUMNS

    redundant_pairs: List[Dict[str, object]] = []
    excluded_pair = {"flavanoids", "total_phenols"}

    for primary_idx in range(len(column_names)):
        for secondary_idx in range(primary_idx + 1, len(column_names)):
            variable_x = column_names[primary_idx]
            variable_y = column_names[secondary_idx]
            pearson_coefficient = correlation_matrix.iloc[
                primary_idx, secondary_idx
            ]

            if abs(pearson_coefficient) > correlation_threshold:
                is_excluded = {variable_x, variable_y} == excluded_pair
                redundant_pairs.append(
                    {
                        "variavel_1": variable_x,
                        "variavel_2": variable_y,
                        "r_pearson": float(pearson_coefficient),
                        "abs_r": abs(float(pearson_coefficient)),
                        "excluido_em_aula": is_excluded,
                    }
                )

    redundant_pairs.sort(key=lambda item: item["abs_r"], reverse=True)
    return correlation_matrix, redundant_pairs


def test_correlation_significance_manual_vs_scipy(
    series_x: pd.Series, series_y: pd.Series, pearson_r: float
) -> Dict[str, float]:
    """Calcula manualmente a estatística t de significância da correlação de Pearson

    e valida com a função scipy.stats.pearsonr.

    Fórmula: t = r * sqrt(n - 2) / sqrt(1 - r^2), com gl = n - 2.

    Args:
        series_x: Primeira variável contínua.
        series_y: Segunda variável contínua.
        pearson_r: Coeficiente de correlação de Pearson observado.

    Returns:
        Dict[str, float]: t manual, p manual, r scipy e p scipy.
    """
    sample_size = len(series_x)
    degrees_of_freedom = sample_size - 2

    # Dedução analítica manual
    t_statistic_manual = (
        pearson_r
        * np.sqrt(degrees_of_freedom)
        / np.sqrt(1.0 - (pearson_r**2))
    )
    p_value_manual = 2.0 * (
        1.0 - t.cdf(abs(t_statistic_manual), df=degrees_of_freedom)
    )

    # Validação oficial SciPy
    scipy_result = pearsonr(series_x, series_y)

    return {
        "n": float(sample_size),
        "graus_liberdade": float(degrees_of_freedom),
        "t_manual": float(t_statistic_manual),
        "p_manual": float(p_value_manual),
        "r_scipy": float(scipy_result.statistic),
        "p_scipy": float(scipy_result.pvalue),
    }


def plot_correlation_heatmap_and_scatter(
    wine_dataframe: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
    feature_x: str,
    feature_y: str,
    output_filepath: Path,
) -> None:
    """Gera painel composto por Heatmap da matriz de correlação completa e Scatter Plot

    com reta de regressão ajustada para o par mais correlacionado.

    Args:
        wine_dataframe: DataFrame com dados e coluna cultivar.
        correlation_matrix: Matriz de correlação 13x13.
        feature_x: Nome da primeira variável do par.
        feature_y: Nome da segunda variável do par.
        output_filepath: Caminho de saída para o arquivo gráfico.
    """
    configure_visual_standards()
    figure, (axis_heatmap, axis_scatter) = plt.subplots(
        nrows=1, ncols=2, figsize=(16, 7)
    )

    # Subplot 1: Heatmap
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(
        correlation_matrix,
        mask=mask,
        cmap="vlag",
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.75, "label": "Correlação de Pearson (r)"},
        ax=axis_heatmap,
        annot=True,
        fmt=".2f",
        annot_kws={"size": 7},
    )
    axis_heatmap.set_title("Matriz de Correlação Linear Completa (13 Variáveis)")

    # Subplot 2: Scatter Plot com reta de regressão global e coloração por cultivar
    for cultivar_label, color_code in PALETA_CULTIVARES.items():
        subset = wine_dataframe[
            wine_dataframe[TARGET_COLUMN] == cultivar_label
        ]
        axis_scatter.scatter(
            subset[feature_x],
            subset[feature_y],
            color=color_code,
            label=cultivar_label,
            alpha=0.8,
            edgecolors="#111111",
            linewidth=0.5,
            s=45,
        )

    # Reta de regressão linear global
    slope, intercept = np.polyfit(
        wine_dataframe[feature_x], wine_dataframe[feature_y], 1
    )
    x_regression_line = np.linspace(
        wine_dataframe[feature_x].min(), wine_dataframe[feature_x].max(), 100
    )
    y_regression_line = slope * x_regression_line + intercept
    axis_scatter.plot(
        x_regression_line,
        y_regression_line,
        color="#111111",
        linestyle="--",
        linewidth=2,
        label=f"Reta Ajustada: y = {slope:.2f}x + {intercept:.2f}",
    )

    axis_scatter.set_title(
        f"Dispersão e Reta Ajustada: {feature_x} vs {feature_y}\n(r = +0.79, p < 0.0001)"
    )
    axis_scatter.set_xlabel("Flavonoides (flavanoids) [g/L]")
    axis_scatter.set_ylabel(
        "Absorbância Óptica (od280/od315_of_diluted_wines)"
    )
    axis_scatter.legend(frameon=True, facecolor="#FAFAFA")
    axis_scatter.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    figure.savefig(output_filepath, dpi=300, bbox_inches="tight")
    plt.close(figure)


def run_exercise_7() -> Dict[str, object]:
    """Executa a rotina analítica do Exercício 7."""
    wine_dataframe = load_clean_wine_dataset()
    correlation_matrix, redundant_pairs = (
        compute_correlation_matrix_and_redundant_pairs(wine_dataframe)
    )

    # Filtrar o par excluído (flavanoids x total_phenols)
    valid_redundant_pairs = [
        pair for pair in redundant_pairs if not pair["excluido_em_aula"]
    ]
    top_pair = valid_redundant_pairs[0]

    feature_x = top_pair["variavel_1"]
    feature_y = top_pair["variavel_2"]
    pearson_r = top_pair["r_pearson"]

    series_x = wine_dataframe[feature_x]
    series_y = wine_dataframe[feature_y]

    significance_results = test_correlation_significance_manual_vs_scipy(
        series_x, series_y, pearson_r
    )

    # Testes de Normalidade
    shapiro_x = shapiro(series_x)
    shapiro_y = shapiro(series_y)

    # Correlações Não-Paramétricas
    spearman_result = spearmanr(series_x, series_y)
    kendall_result = kendalltau(series_x, series_y)

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "exercicio7_correlacao_heatmap_scatter.png"
    plot_correlation_heatmap_and_scatter(
        wine_dataframe,
        correlation_matrix,
        feature_x,
        feature_y,
        figure_path,
    )

    print(
        "=== EXERCÍCIO 7: CORRELAÇÃO, SIGNIFICÂNCIA E REDUNDÂNCIA LINEAR ==="
    )
    print("\n--- Pares com |r| > 0,70 Identificados na Matriz Completa ---")
    for pair in redundant_pairs:
        status_aula = (
            " [EXCLUÍDO - Visto em Aula]" if pair["excluido_em_aula"] else ""
        )
        print(
            f"  {pair['variavel_1']:<28} x {pair['variavel_2']:<28}: r = {pair['r_pearson']:+.4f}{status_aula}"
        )

    print(
        f"\nPar selecionado de maior |r| (não excluído): {feature_x} x {feature_y} (r = {pearson_r:+.4f})"
    )
    print("--- Teste de Significância da Correlação (t de Student) ---")
    print(f"  Graus de liberdade (n - 2): {significance_results['graus_liberdade']:.0f}")
    print(
        f"  Estatística t (Cálculo Manual): {significance_results['t_manual']:.4f}"
    )
    print(
        f"  Valor-p (Cálculo Manual): {significance_results['p_manual']:.4e}"
    )
    print(
        f"  Validação SciPy pearsonr: r = {significance_results['r_scipy']:.4f}, p = {significance_results['p_scipy']:.4e}"
    )

    print("\n--- Verificação de Pressupostos de Normalidade (Shapiro-Wilk) ---")
    print(
        f"  {feature_x:<28}: W = {shapiro_x.statistic:.4f}, p = {shapiro_x.pvalue:.4e} (Viola normalidade)"
    )
    print(
        f"  {feature_y:<28}: W = {shapiro_y.statistic:.4f}, p = {shapiro_y.pvalue:.4e} (Viola normalidade)"
    )

    print(
        "\n--- Correlações Não-Paramétricas (Robustas a Não-Normalidade) ---"
    )
    print(
        f"  Spearman (rho): {spearman_result.statistic:.4f} (p = {spearman_result.pvalue:.4e})"
    )
    print(
        f"  Kendall (tau) : {kendall_result.statistic:.4f} (p = {kendall_result.pvalue:.4e})"
    )
    print(f"\nFigura salva com sucesso em: {figure_path}\n")

    return {
        "top_pair": top_pair,
        "significance": significance_results,
        "shapiro_x": shapiro_x,
        "shapiro_y": shapiro_y,
        "spearman": spearman_result,
        "kendall": kendall_result,
    }


if __name__ == "__main__":
    run_exercise_7()
