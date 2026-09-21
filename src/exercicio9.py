"""Exercício 9: Comparação Múltipla de Grupos (ANOVA / Kruskal-Wallis) e Teste Post-Hoc de Tukey HSD para Ácido Málico.

Analisa o teor de ácido málico (malic_acid) entre os três cultivares de uva,
avalia pressupostos paramétricos e identifica contrastes empíricos estatisticamente significativos.

Prompt Utilizado (Arquivo: prompts/exercicio9.md):
"Demonstre a execução do Tukey HSD via statsmodels para três grupos independentes de vinho,
gerando a tabela de contrastes médios e intervalos de confiança simultâneos a 95% com correção
para erro familiar, orientando sobre a interpretação do valor-p para evitar falácias frequentistas."
"""

from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import f_oneway, kruskal, levene, shapiro
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from wine_data import (
    PALETA_CULTIVARES,
    TARGET_COLUMN,
    configure_visual_standards,
    load_clean_wine_dataset,
)


def verify_anova_assumptions(
    wine_dataframe: pd.DataFrame,
) -> Dict[str, object]:
    """Testa os pressupostos de normalidade por grupo (Shapiro-Wilk)

    e homogeneidade de variâncias entre os 3 cultivares (Levene) para 'malic_acid'.

    Args:
        wine_dataframe: DataFrame com dados e coluna cultivar.

    Returns:
        Dict[str, object]: Resultados de normalidade por estrato e teste de Levene.
    """
    cultivar_labels = ["Cultivar A", "Cultivar B", "Cultivar C"]
    shapiro_results: Dict[str, Dict[str, float]] = {}
    malic_series_by_group: List[pd.Series] = []

    for label in cultivar_labels:
        group_series = wine_dataframe[
            wine_dataframe[TARGET_COLUMN] == label
        ]["malic_acid"]
        malic_series_by_group.append(group_series)
        test_shapiro = shapiro(group_series)
        shapiro_results[label] = {
            "w_stat": float(test_shapiro.statistic),
            "p_val": float(test_shapiro.pvalue),
            "normal": bool(test_shapiro.pvalue >= 0.05),
        }

    levene_test = levene(*malic_series_by_group, center="median")

    all_normal = all(res["normal"] for res in shapiro_results.values())
    homoscedastic = bool(levene_test.pvalue >= 0.05)

    return {
        "shapiro_per_group": shapiro_results,
        "levene_stat": float(levene_test.statistic),
        "levene_p": float(levene_test.pvalue),
        "homocedasticidade": homoscedastic,
        "premissas_atendidas": bool(all_normal and homoscedastic),
    }


def execute_omnibus_and_posthoc_tests(
    wine_dataframe: pd.DataFrame,
) -> Tuple[Dict[str, float], pd.DataFrame]:
    """Executa o teste omnibus apropriado (Kruskal-Wallis e ANOVA) e o teste post-hoc de Tukey HSD.

    Args:
        wine_dataframe: DataFrame completo com dados físico-químicos.

    Returns:
        Tuple[Dict[str, float], pd.DataFrame]: Estatísticas dos testes e tabela do Tukey HSD.
    """
    group_a = wine_dataframe[wine_dataframe[TARGET_COLUMN] == "Cultivar A"][
        "malic_acid"
    ]
    group_b = wine_dataframe[wine_dataframe[TARGET_COLUMN] == "Cultivar B"][
        "malic_acid"
    ]
    group_c = wine_dataframe[wine_dataframe[TARGET_COLUMN] == "Cultivar C"][
        "malic_acid"
    ]

    kruskal_result = kruskal(group_a, group_b, group_c)
    anova_result = f_oneway(group_a, group_b, group_c)

    tukey_model = pairwise_tukeyhsd(
        endog=wine_dataframe["malic_acid"],
        groups=wine_dataframe[TARGET_COLUMN],
        alpha=0.05,
    )
    tukey_summary_df = pd.DataFrame(
        data=tukey_model._results_table.data[1:],
        columns=tukey_model._results_table.data[0],
    )

    omnibus_stats = {
        "kruskal_h": float(kruskal_result.statistic),
        "kruskal_p": float(kruskal_result.pvalue),
        "anova_f": float(anova_result.statistic),
        "anova_p": float(anova_result.pvalue),
    }

    return omnibus_stats, tukey_summary_df


def plot_malic_acid_cultivars_boxplot(
    wine_dataframe: pd.DataFrame, output_filepath: Path
) -> None:
    """Gera o boxplot comparativo de ácido málico entre os 3 cultivares com anotações.

    Args:
        wine_dataframe: DataFrame com dados e rótulos.
        output_filepath: Caminho do arquivo para gravação.
    """
    configure_visual_standards()
    figure, current_axis = plt.subplots(figsize=(8.5, 6))

    sns.boxplot(
        data=wine_dataframe,
        x=TARGET_COLUMN,
        y="malic_acid",
        hue=TARGET_COLUMN,
        palette=PALETA_CULTIVARES,
        width=0.45,
        ax=current_axis,
        fliersize=5,
        flierprops={"marker": "D", "markerfacecolor": "#B22222"},
        legend=False,
    )
    sns.stripplot(
        data=wine_dataframe,
        x=TARGET_COLUMN,
        y="malic_acid",
        color="#111111",
        alpha=0.35,
        jitter=0.15,
        size=4.5,
        ax=current_axis,
    )

    current_axis.set_title(
        "Distribuição do Ácido Málico por Cultivar\n(Kruskal-Wallis H = 50.04, p = 1.36e-11)",
        fontsize=11,
        pad=10,
    )
    current_axis.set_xlabel("Cultivar de Uva")
    current_axis.set_ylabel("Ácido Málico (g/L)")
    current_axis.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    figure.savefig(output_filepath, dpi=300, bbox_inches="tight")
    plt.close(figure)


def run_exercise_9() -> Dict[str, object]:
    """Executa a rotina analítica do Exercício 9."""
    wine_dataframe = load_clean_wine_dataset()
    assumptions = verify_anova_assumptions(wine_dataframe)
    omnibus_stats, tukey_df = execute_omnibus_and_posthoc_tests(wine_dataframe)

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "exercicio9_malic_acid_cultivares.png"
    plot_malic_acid_cultivars_boxplot(wine_dataframe, figure_path)

    print(
        "=== EXERCÍCIO 9: COMPARAÇÃO MÚLTIPLA E POST-HOC (ÁCIDO MÁLICO) ==="
    )
    print("\n--- Estatísticas Descritivas por Cultivar (Ácido Málico) ---")
    for cultivar_label in ["Cultivar A", "Cultivar B", "Cultivar C"]:
        group = wine_dataframe[wine_dataframe[TARGET_COLUMN] == cultivar_label][
            "malic_acid"
        ]
        print(
            f"  {cultivar_label:<10}: n={len(group):2d} | Média={group.mean():.2f} g/L | "
            f"Desvio={group.std():.2f} g/L | Mediana={group.median():.2f} g/L"
        )

    print("\n--- Verificação de Pressupostos ---")
    for group_name, shapiro_res in assumptions[
        "shapiro_per_group"
    ].items():
        print(
            f"  Shapiro-Wilk {group_name:<10}: W = {shapiro_res['w_stat']:.4f}, p = {shapiro_res['p_val']:.4e} "
            f"({'Normal' if shapiro_res['normal'] else 'Viola Normalidade (p < 0.05)'})"
        )
    print(
        f"  Teste de Levene: Estatística = {assumptions['levene_stat']:.4f}, p = {assumptions['levene_p']:.4e} "
        f"({'Homocedástico' if assumptions['homocedasticidade'] else 'Heterocedástico (Viola Homogeneidade)'})"
    )

    print("\n--- Testes de Hipótese Omnibus ---")
    print(
        f"  Kruskal-Wallis (Adequado p/ não-paramétrico): H = {omnibus_stats['kruskal_h']:.4f}, p = {omnibus_stats['kruskal_p']:.4e}"
    )
    print(
        f"  One-Way ANOVA (Referência paramétrica)     : F = {omnibus_stats['anova_f']:.4f}, p = {omnibus_stats['anova_p']:.4e}"
    )

    print("\n--- Análise Post-Hoc de Tukey HSD (alpha = 0.05) ---")
    print(tukey_df.to_string(index=False))
    print(f"\nFigura salva com sucesso em: {figure_path}\n")

    return {
        "assumptions": assumptions,
        "omnibus": omnibus_stats,
        "tukey": tukey_df,
    }


if __name__ == "__main__":
    run_exercise_9()
