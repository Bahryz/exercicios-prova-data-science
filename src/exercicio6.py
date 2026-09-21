"""Exercício 6: Forma da Distribuição, Assimetria (Skewness), Histogramas com KDE e Testes de Normalidade.

Avalia a morfologia distribucional de quatro compostos químicos chave do vinho
(magnesium, malic_acid, proanthocyanins e hue) para subsidiar a escolha entre média e mediana.

Prompt Utilizado (Arquivo: prompts/exercicio6.md):
"Verifique a sintaxe correta da função scipy.stats.skew com ajuste de viés (bias=False)
para amostras finitas e confirme o limiar convencional de Bulmer para classificação
de assimetria moderada vs severa (> 0.5 e > 1.0). Apresente também a parametrização
do teste de Shapiro-Wilk no SciPy."
"""

from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import shapiro, skew
import seaborn as sns

from wine_data import (
    FEATURE_COLUMNS,
    configure_visual_standards,
    load_clean_wine_dataset,
)


def calculate_distribution_shape_metrics(
    wine_dataframe: pd.DataFrame, target_features: List[str]
) -> pd.DataFrame:
    """Calcula o coeficiente de assimetria de Fisher-Pearson e a estatística

    de Shapiro-Wilk para as variáveis especificadas na população completa.

    Args:
        wine_dataframe: DataFrame populacional completo.
        target_features: Lista de variáveis químicas sob investigação.

    Returns:
        pd.DataFrame: Métricas de forma, valor-p de normalidade e classificação morfológica.
    """
    records: List[Dict[str, object]] = []

    for feature_name in target_features:
        feature_series = wine_dataframe[feature_name]
        skewness_coefficient = float(skew(feature_series, bias=False))
        shapiro_test = shapiro(feature_series)

        mean_value = float(feature_series.mean())
        median_value = float(feature_series.median())
        iqr_value = float(
            feature_series.quantile(0.75) - feature_series.quantile(0.25)
        )

        # Classificação de assimetria segundo Bulmer (1979)
        if skewness_coefficient > 0.5:
            classification = "Assimétrica à Direita (Positiva)"
            recommended_central_measure = "Mediana"
            justificativa = "Cauda alongada à direita; média inflacionada por valores extremos."
        elif skewness_coefficient < -0.5:
            classification = "Assimétrica à Esquerda (Negativa)"
            recommended_central_measure = "Mediana"
            justificativa = "Cauda alongada à esquerda; média subestimada por valores basais."
        else:
            classification = "Aproximadamente Simétrica"
            recommended_central_measure = "Média / Mediana equivalentes"
            justificativa = "Distribuição balanceada em torno do centro; média reflete adequadamente a concentração."

        records.append(
            {
                "variavel": feature_name,
                "assimetria": skewness_coefficient,
                "classificacao": classification,
                "media": mean_value,
                "mediana": median_value,
                "iqr": iqr_value,
                "shapiro_w": float(shapiro_test.statistic),
                "shapiro_p": float(shapiro_test.pvalue),
                "normalidade_aderente": bool(shapiro_test.pvalue >= 0.05),
                "medida_recomendada": recommended_central_measure,
                "justificativa": justificativa,
            }
        )

    return pd.DataFrame(records)


def plot_four_features_distribution_kde(
    wine_dataframe: pd.DataFrame,
    target_features: List[str],
    output_filepath: Path,
) -> None:
    """Plota painel 2x2 com histogramas e curvas de densidade estimada (KDE).

    Args:
        wine_dataframe: DataFrame populacional completo.
        target_features: Lista com as 4 variáveis analisadas.
        output_filepath: Caminho do arquivo de imagem a ser gravado.
    """
    configure_visual_standards()
    figure, axes_array = plt.subplots(nrows=2, ncols=2, figsize=(13, 9))
    flat_axes = axes_array.flatten()

    feature_labels_map = {
        "magnesium": "Magnésio (mg/L)",
        "malic_acid": "Ácido Málico (g/L)",
        "proanthocyanins": "Proantocianinas (g/L)",
        "hue": "Matiz / Tonalidade (Hue)",
    }

    colors = ["#2E5B88", "#800020", "#507255", "#93652E"]

    for index, feature_name in enumerate(target_features):
        current_axis = flat_axes[index]
        feature_series = wine_dataframe[feature_name]
        mean_val = float(feature_series.mean())
        median_val = float(feature_series.median())
        skew_val = float(skew(feature_series, bias=False))

        sns.histplot(
            feature_series,
            kde=True,
            stat="density",
            color=colors[index % len(colors)],
            ax=current_axis,
            bins=18,
            edgecolor="#222222",
            alpha=0.6,
            line_kws={"linewidth": 2},
        )

        current_axis.axvline(
            mean_val,
            color="#B22222",
            linestyle="--",
            linewidth=2,
            label=f"Média: {mean_val:.2f}",
        )
        current_axis.axvline(
            median_val,
            color="#111111",
            linestyle="-.",
            linewidth=2,
            label=f"Mediana: {median_val:.2f}",
        )

        current_axis.set_title(
            f"{feature_labels_map.get(feature_name, feature_name)} | Assimetria: {skew_val:+.3f}",
            fontsize=11,
            pad=10,
        )
        current_axis.set_xlabel("Valor da Variável")
        current_axis.set_ylabel("Densidade")
        current_axis.legend(frameon=True, facecolor="#FAFAFA")
        current_axis.grid(True, linestyle="--", alpha=0.3)

    figure.suptitle(
        "Morfologia das Distribuições: Histogramas e Densidade KDE das Variáveis Selecionadas",
        fontsize=13,
        fontweight="bold",
        y=0.99,
    )
    plt.tight_layout()
    figure.savefig(output_filepath, dpi=300, bbox_inches="tight")
    plt.close(figure)


def run_exercise_6() -> pd.DataFrame:
    """Executa a rotina analítica do Exercício 6."""
    wine_dataframe = load_clean_wine_dataset()
    selected_features = ["magnesium", "malic_acid", "proanthocyanins", "hue"]

    metrics_df = calculate_distribution_shape_metrics(
        wine_dataframe, selected_features
    )

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "exercicio6_distribuicoes_kde.png"
    plot_four_features_distribution_kde(
        wine_dataframe, selected_features, figure_path
    )

    print("=== EXERCÍCIO 6: FORMA DA DISTRIBUIÇÃO E TESTES DE NORMALIDADE ===")
    for _, row in metrics_df.iterrows():
        print(f"\nVariável: {row['variavel']}")
        print(
            f"  Assimetria: {row['assimetria']:+.4f} -> {row['classificacao']}"
        )
        print(f"  Média: {row['media']:.3f} | Mediana: {row['mediana']:.3f}")
        print(
            f"  Teste de Shapiro-Wilk: W = {row['shapiro_w']:.4f}, p-valor = {row['shapiro_p']:.4e} "
            f"({'Normal' if row['normalidade_aderente'] else 'Não-Normal (p < 0.05)'})"
        )
        print(f"  Medida Típica Indicada: {row['medida_recomendada']}")
        print(f"  Justificativa Técnica: {row['justificativa']}")

    print(f"\nFigura salva com sucesso em: {figure_path}\n")
    return metrics_df


if __name__ == "__main__":
    run_exercise_6()
