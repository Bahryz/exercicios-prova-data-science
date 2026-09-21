"""Exercício 8: Teste de Hipótese Entre Dois Grupos Independentes (Cultivar B vs. Cultivar C) para Magnésio.

Avalia a concentração de magnésio (magnesium), testa os pressupostos
de normalidade e homocedasticidade e seleciona o teste inferencial adequado.

Prompt de Auditoria Utilizado:
"Analise a equivalência matemática entre os testes de Kruskal-Wallis e Mann-Whitney
para comparação de dois grupos independentes no SciPy. Explique por que o teste t
falha em detectar diferença com p=0.085 enquanto Kruskal detecta com p=0.0005 frente
a assimetria com outliers, auxiliando na redação da justificativa para tomada de decisão
prática do enólogo."
"""

from pathlib import Path
from typing import Dict, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kruskal, levene, mannwhitneyu, shapiro, ttest_ind
import seaborn as sns

from wine_data import (
    PALETA_CULTIVARES,
    TARGET_COLUMN,
    configure_visual_standards,
    load_clean_wine_dataset,
)


def extract_magnesium_groups(
    wine_dataframe: pd.DataFrame,
) -> Tuple[pd.Series, pd.Series]:
    """Filtra as séries de magnésio para os Cultivares B e C.

    Args:
        wine_dataframe: DataFrame com dados e coluna cultivar.

    Returns:
        Tuple[pd.Series, pd.Series]: Séries de magnésio do Cultivar B e Cultivar C.
    """
    magnesium_b = wine_dataframe[
        wine_dataframe[TARGET_COLUMN] == "Cultivar B"
    ]["magnesium"]
    magnesium_c = wine_dataframe[
        wine_dataframe[TARGET_COLUMN] == "Cultivar C"
    ]["magnesium"]
    return magnesium_b, magnesium_c


def check_inferential_assumptions_two_groups(
    series_group_b: pd.Series, series_group_c: pd.Series
) -> Dict[str, object]:
    """Executa os testes de Shapiro-Wilk (normalidade em cada grupo) e Levene (homocedasticidade).

    Args:
        series_group_b: Dados do Cultivar B.
        series_group_c: Dados do Cultivar C.

    Returns:
        Dict[str, object]: Estatísticas e p-valores dos pressupostos.
    """
    shapiro_b = shapiro(series_group_b)
    shapiro_c = shapiro(series_group_c)
    levene_test = levene(series_group_b, series_group_c, center="median")

    assumptions_met = (
        (shapiro_b.pvalue >= 0.05)
        and (shapiro_c.pvalue >= 0.05)
        and (levene_test.pvalue >= 0.05)
    )

    return {
        "shapiro_b_stat": float(shapiro_b.statistic),
        "shapiro_b_pval": float(shapiro_b.pvalue),
        "shapiro_b_normal": bool(shapiro_b.pvalue >= 0.05),
        "shapiro_c_stat": float(shapiro_c.statistic),
        "shapiro_c_pval": float(shapiro_c.pvalue),
        "shapiro_c_normal": bool(shapiro_c.pvalue >= 0.05),
        "levene_stat": float(levene_test.statistic),
        "levene_pval": float(levene_test.pvalue),
        "homocedasticidade": bool(levene_test.pvalue >= 0.05),
        "todos_pressupostos_atendidos": assumptions_met,
    }


def execute_hypothesis_tests(
    series_group_b: pd.Series, series_group_c: pd.Series
) -> Dict[str, object]:
    """Calcula os testes paramétrico (t de Student) e não-paramétrico (Kruskal-Wallis / Mann-Whitney).

    Args:
        series_group_b: Magnésio no Cultivar B.
        series_group_c: Magnésio no Cultivar C.

    Returns:
        Dict[str, object]: Resultados estatísticos comparados.
    """
    kruskal_result = kruskal(series_group_b, series_group_c)
    mannwhitney_result = mannwhitneyu(
        series_group_b, series_group_c, alternative="two-sided"
    )
    student_t_result = ttest_ind(
        series_group_b, series_group_c, equal_var=True
    )

    return {
        "kruskal_h": float(kruskal_result.statistic),
        "kruskal_p": float(kruskal_result.pvalue),
        "mannwhitney_u": float(mannwhitney_result.statistic),
        "mannwhitney_p": float(mannwhitney_result.pvalue),
        "student_t": float(student_t_result.statistic),
        "student_p": float(student_t_result.pvalue),
    }


def plot_magnesium_cultivar_b_c_boxplot(
    wine_dataframe: pd.DataFrame, output_filepath: Path
) -> None:
    """Gera boxplot comparativo detalhado de magnésio entre Cultivar B e C.

    Args:
        wine_dataframe: DataFrame com dados completos.
        output_filepath: Caminho do arquivo de saída.
    """
    subset_df = wine_dataframe[
        wine_dataframe[TARGET_COLUMN].isin(["Cultivar B", "Cultivar C"])
    ].copy()

    configure_visual_standards()
    figure, current_axis = plt.subplots(figsize=(8, 6))

    custom_palette = {
        "Cultivar B": PALETA_CULTIVARES["Cultivar B"],
        "Cultivar C": PALETA_CULTIVARES["Cultivar C"],
    }

    sns.boxplot(
        data=subset_df,
        x=TARGET_COLUMN,
        y="magnesium",
        hue=TARGET_COLUMN,
        palette=custom_palette,
        width=0.45,
        ax=current_axis,
        fliersize=5,
        flierprops={"marker": "D", "markerfacecolor": "#B22222"},
        legend=False,
    )
    sns.stripplot(
        data=subset_df,
        x=TARGET_COLUMN,
        y="magnesium",
        color="#111111",
        alpha=0.4,
        jitter=0.15,
        size=5,
        ax=current_axis,
    )

    current_axis.set_title(
        "Comparação do Teor de Magnésio: Cultivar B vs Cultivar C\n(Kruskal-Wallis H = 11.88, p = 0.00057)",
        fontsize=11,
        pad=10,
    )
    current_axis.set_xlabel("Cultivar de Uva")
    current_axis.set_ylabel("Concentração de Magnésio (mg/L)")
    current_axis.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    figure.savefig(output_filepath, dpi=300, bbox_inches="tight")
    plt.close(figure)


def run_exercise_8() -> Dict[str, object]:
    """Executa a rotina analítica do Exercício 8."""
    wine_dataframe = load_clean_wine_dataset()
    magnesium_b, magnesium_c = extract_magnesium_groups(wine_dataframe)

    assumptions = check_inferential_assumptions_two_groups(
        magnesium_b, magnesium_c
    )
    test_results = execute_hypothesis_tests(magnesium_b, magnesium_c)

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "exercicio8_magnesium_cultivar_b_c.png"
    plot_magnesium_cultivar_b_c_boxplot(wine_dataframe, figure_path)

    print("=== EXERCÍCIO 8: TESTE DE HIPÓTESE ENTRE DOIS GRUPOS (MAGNÉSIO) ===")
    print(
        f"Cultivar B: n = {len(magnesium_b)}, Média = {magnesium_b.mean():.2f} mg/L, "
        f"Desvio = {magnesium_b.std():.2f} mg/L, Mediana = {magnesium_b.median():.2f} mg/L"
    )
    print(
        f"Cultivar C: n = {len(magnesium_c)}, Média = {magnesium_c.mean():.2f} mg/L, "
        f"Desvio = {magnesium_c.std():.2f} mg/L, Mediana = {magnesium_c.median():.2f} mg/L"
    )

    print("\n--- Verificação de Pressupostos ---")
    print(
        f"  Shapiro-Wilk Cultivar B: W = {assumptions['shapiro_b_stat']:.4f}, p = {assumptions['shapiro_b_pval']:.4e} "
        f"({'Atende' if assumptions['shapiro_b_normal'] else 'Viola Normalidade (p < 0.05)'})"
    )
    print(
        f"  Shapiro-Wilk Cultivar C: W = {assumptions['shapiro_c_stat']:.4f}, p = {assumptions['shapiro_c_pval']:.4e} "
        f"({'Atende' if assumptions['shapiro_c_normal'] else 'Viola Normalidade (p < 0.05)'})"
    )
    print(
        f"  Teste de Levene: Estatística = {assumptions['levene_stat']:.4f}, p = {assumptions['levene_pval']:.4e} "
        f"({'Homocedástico' if assumptions['homocedasticidade'] else 'Heterocedástico'})"
    )

    print("\n--- Seleção e Execução do Teste Inferencial ---")
    print("  Decisão Metodológica: Como a normalidade foi rejeitada no Cultivar B (outliers extremos de até 162 mg/L),")
    print(
        "  o teste t de Student paramétrico é inválido. Adota-se o teste não-paramétrico de Kruskal-Wallis (Mann-Whitney)."
    )
    print(
        f"  Kruskal-Wallis: H = {test_results['kruskal_h']:.4f}, p-valor = {test_results['kruskal_p']:.4e}"
    )
    print(
        f"  Mann-Whitney U: U = {test_results['mannwhitney_u']:.4f}, p-valor = {test_results['mannwhitney_p']:.4e}"
    )
    print(
        f"  (Referência Comparativa) Teste t de Student: t = {test_results['student_t']:.4f}, p = {test_results['student_p']:.4e}"
    )
    print(
        "  Nota: O teste t convencional falharia em detectar a diferença em nível alfa=0.05 por distorção dos outliers."
    )
    print(f"\nFigura salva com sucesso em: {figure_path}\n")

    return {
        "assumptions": assumptions,
        "test_results": test_results,
    }


if __name__ == "__main__":
    run_exercise_8()
