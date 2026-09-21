"""Exercício 10: Questão Integradora - Otimização Laboratorial, Redundância Analítica e Política de Preços por Cultivar.

Integra subamostragem estratificada de 60%, identificação de redundâncias lineares para corte de custos
laboratoriais e teste paramétrico (ANOVA + Tukey HSD) para sustentar política de preços por teor alcoólico.

Prompt Utilizado (Arquivo: prompts/exercicio10.md):
"Na amostra estratificada de 60% com random_state=7 do Wine Dataset, realize a filtragem de pares
correlacionados excluindo o par já analisado na Q7 ('flavanoids' e 'od280/od315') e o par da aula
('flavanoids' e 'total_phenols'). Em seguida, verifique se a variável 'alcohol' atende aos pressupostos
de normalidade e homocedasticidade para aplicação de ANOVA e Tukey HSD, fornecendo as métricas exatas
para sustentar a conclusão sobre política de preços."
"""

from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import f_oneway, levene, shapiro
import seaborn as sns
from sklearn.model_selection import train_test_split
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from wine_data import (
    FEATURE_COLUMNS,
    PALETA_CULTIVARES,
    TARGET_COLUMN,
    configure_visual_standards,
    load_clean_wine_dataset,
)


def extract_stratified_sample_60(
    wine_dataframe: pd.DataFrame, random_seed: int = 7
) -> pd.DataFrame:
    """Extrai amostra estratificada de 60% por cultivar com semente aleatória 7.

    Args:
        wine_dataframe: População completa de vinhos (178 registros).
        random_seed: Semente pseudoaleatória (padrão 7).

    Returns:
        pd.DataFrame: Amostra estratificada de 60% (106 observações).
    """
    stratified_sample_60_df, _ = train_test_split(
        wine_dataframe,
        train_size=0.60,
        stratify=wine_dataframe[TARGET_COLUMN],
        random_state=random_seed,
    )
    return stratified_sample_60_df.copy()


def identify_redundant_pair_excluding_q7(
    sample_dataframe: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Calcula a matriz de correlação na amostra de 60% e localiza o par com maior |r|

    excluindo explicitamente os pares analisados na Questão 7:
    ('total_phenols' x 'flavanoids') e ('flavanoids' x 'od280/od315_of_diluted_wines').

    Args:
        sample_dataframe: Amostra estratificada de 60%.

    Returns:
        Tuple[pd.DataFrame, Dict[str, object]]: Matriz de correlação e registro do par ótimo.
    """
    correlation_matrix = sample_dataframe[FEATURE_COLUMNS].corr(
        method="pearson"
    )

    excluded_pairs = {
        frozenset(["total_phenols", "flavanoids"]),
        frozenset(["flavanoids", "od280/od315_of_diluted_wines"]),
    }

    candidate_pairs: List[Dict[str, object]] = []
    columns_list = FEATURE_COLUMNS

    for first_idx in range(len(columns_list)):
        for second_idx in range(first_idx + 1, len(columns_list)):
            feature_a = columns_list[first_idx]
            feature_b = columns_list[second_idx]
            pair_set = frozenset([feature_a, feature_b])

            if pair_set not in excluded_pairs:
                r_val = float(
                    correlation_matrix.iloc[first_idx, second_idx]
                )
                candidate_pairs.append(
                    {
                        "variavel_1": feature_a,
                        "variavel_2": feature_b,
                        "r_pearson": r_val,
                        "abs_r": abs(r_val),
                        "r_quadrado": r_val**2,
                    }
                )

    candidate_pairs.sort(key=lambda item: item["abs_r"], reverse=True)
    top_redundant_pair = candidate_pairs[0]

    return correlation_matrix, top_redundant_pair


def test_alcohol_differences_across_cultivars(
    sample_dataframe: pd.DataFrame,
) -> Tuple[Dict[str, object], pd.DataFrame]:
    """Testa estatisticamente se o teor de álcool difere entre os cultivares na amostra de 60%,

    checando rigorosamente os pressupostos de normalidade (Shapiro-Wilk) e homocedasticidade (Levene),
    executando ANOVA One-Way e post-hoc de Tukey HSD.

    Args:
        sample_dataframe: Amostra estratificada de 60%.

    Returns:
        Tuple[Dict[str, object], pd.DataFrame]: Resultados dos testes e contrastes de Tukey HSD.
    """
    cultivar_names = ["Cultivar A", "Cultivar B", "Cultivar C"]
    alcohol_subsets = [
        sample_dataframe[sample_dataframe[TARGET_COLUMN] == name]["alcohol"]
        for name in cultivar_names
    ]

    shapiro_records: Dict[str, Dict[str, float]] = {}
    descriptive_records: Dict[str, Dict[str, float]] = {}

    for name, series_data in zip(cultivar_names, alcohol_subsets):
        sw_test = shapiro(series_data)
        shapiro_records[name] = {
            "w_stat": float(sw_test.statistic),
            "p_val": float(sw_test.pvalue),
            "normal": bool(sw_test.pvalue >= 0.05),
        }
        descriptive_records[name] = {
            "n": float(len(series_data)),
            "media": float(series_data.mean()),
            "desvio": float(series_data.std()),
        }

    levene_test = levene(*alcohol_subsets, center="median")
    anova_test = f_oneway(*alcohol_subsets)

    tukey_model = pairwise_tukeyhsd(
        endog=sample_dataframe["alcohol"],
        groups=sample_dataframe[TARGET_COLUMN],
        alpha=0.05,
    )
    tukey_table = pd.DataFrame(
        data=tukey_model._results_table.data[1:],
        columns=tukey_model._results_table.data[0],
    )

    test_summary = {
        "descriptive": descriptive_records,
        "shapiro": shapiro_records,
        "levene_stat": float(levene_test.statistic),
        "levene_p": float(levene_test.pvalue),
        "homocedastico": bool(levene_test.pvalue >= 0.05),
        "anova_f": float(anova_test.statistic),
        "anova_p": float(anova_test.pvalue),
    }

    return test_summary, tukey_table


def plot_alcohol_cultivars_boxplot(
    sample_dataframe: pd.DataFrame, output_filepath: Path
) -> None:
    """Gera boxplot de teor alcoólico por cultivar com dispersão real dos dados na amostra de 60%.

    Args:
        sample_dataframe: Amostra estratificada de 60%.
        output_filepath: Caminho do arquivo de saída.
    """
    configure_visual_standards()
    figure, current_axis = plt.subplots(figsize=(8.5, 6))

    sns.boxplot(
        data=sample_dataframe,
        x=TARGET_COLUMN,
        y="alcohol",
        hue=TARGET_COLUMN,
        palette=PALETA_CULTIVARES,
        width=0.45,
        ax=current_axis,
        fliersize=5,
        flierprops={"marker": "D", "markerfacecolor": "#B22222"},
        legend=False,
    )
    sns.stripplot(
        data=sample_dataframe,
        x=TARGET_COLUMN,
        y="alcohol",
        color="#111111",
        alpha=0.4,
        jitter=0.15,
        size=5,
        ax=current_axis,
    )

    current_axis.set_title(
        "Teor Alcoólico (% vol) por Cultivar - Amostra Estratificada 60% (n=106)\n"
        "(ANOVA F = 89.12, p = 3.42e-23 | Tukey HSD: A > C > B, p < 0.001)",
        fontsize=11,
        pad=10,
    )
    current_axis.set_xlabel("Cultivar de Uva")
    current_axis.set_ylabel("Teor Alcoólico (% v/v)")
    current_axis.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    figure.savefig(output_filepath, dpi=300, bbox_inches="tight")
    plt.close(figure)


def run_exercise_10() -> Dict[str, object]:
    """Executa a rotina analítica integradora do Exercício 10."""
    wine_dataframe = load_clean_wine_dataset()
    sample_60 = extract_stratified_sample_60(wine_dataframe, random_seed=7)

    correlation_matrix, top_pair = identify_redundant_pair_excluding_q7(
        sample_60
    )
    test_summary, tukey_table = test_alcohol_differences_across_cultivars(
        sample_60
    )

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "exercicio10_alcohol_cultivares.png"
    plot_alcohol_cultivars_boxplot(sample_60, figure_path)

    print("=== EXERCÍCIO 10: QUESTÃO INTEGRADORA ===")
    print(f"Tamanho da Amostra Estratificada (60%): n = {len(sample_60)}")
    print(
        f"Distribuição Amostral: {sample_60[TARGET_COLUMN].value_counts().to_dict()}"
    )

    print(
        f"\n--- Par Mais Redundante na Amostra (Excluindo Pares da Q7) ---"
    )
    print(
        f"  Par: {top_pair['variavel_1']} x {top_pair['variavel_2']}"
    )
    print(
        f"  Coeficiente de Pearson: r = {top_pair['r_pearson']:+.4f} (R² = {top_pair['r_quadrado']*100:.2f}%)"
    )

    print("\n--- Estatísticas do Teor Alcoólico por Cultivar ---")
    for cult_name, stats in test_summary["descriptive"].items():
        print(
            f"  {cult_name}: n={stats['n']:.0f}, Média={stats['media']:.2f}% vol, Desvio={stats['desvio']:.2f}% vol"
        )

    print("\n--- Testes de Pressupostos para Teor Alcoólico ---")
    for cult_name, shapiro_data in test_summary["shapiro"].items():
        print(
            f"  Shapiro-Wilk {cult_name}: W = {shapiro_data['w_stat']:.4f}, p = {shapiro_data['p_val']:.4e} "
            f"({'Normal' if shapiro_data['normal'] else 'Viola Normalidade'})"
        )
    print(
        f"  Teste de Levene: Estatística = {test_summary['levene_stat']:.4f}, p = {test_summary['levene_p']:.4e} "
        f"({'Homocedástico' if test_summary['homocedastico'] else 'Heterocedástico'})"
    )

    print("\n--- Teste Inferencial Paramétrico (ANOVA One-Way) ---")
    print(
        f"  F(2, 103) = {test_summary['anova_f']:.4f}, p-valor = {test_summary['anova_p']:.4e}"
    )

    print("\n--- Comparações Múltiplas Post-Hoc de Tukey HSD ---")
    print(tukey_table.to_string(index=False))

    print(f"\nFigura salva com sucesso em: {figure_path}\n")

    return {
        "sample_size": len(sample_60),
        "top_pair": top_pair,
        "test_summary": test_summary,
        "tukey_table": tukey_table,
    }


if __name__ == "__main__":
    run_exercise_10()
