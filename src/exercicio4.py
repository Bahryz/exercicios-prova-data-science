"""Exercício 4: Amostragem Estratificada e Teorema Central do Limite (TCL).

Demonstra a representatividade da amostragem estratificada e a convergência
da distribuição das médias amostrais para a variável prolina (proline).
"""

from pathlib import Path
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from wine_data import (
    FEATURE_COLUMNS,
    PALETA_CULTIVARES,
    TARGET_COLUMN,
    configure_visual_standards,
    load_clean_wine_dataset,
)


def extract_stratified_sample(
    wine_dataframe: pd.DataFrame,
    sample_fraction: float = 0.20,
    random_seed: int = 42,
) -> pd.DataFrame:
    """Extrai uma amostra estratificada por cultivar mantendo as proporções originais.

    Args:
        wine_dataframe: DataFrame populacional completo (178 observações).
        sample_fraction: Fração amostral desejada para cada estrato (padrão 20%).
        random_seed: Semente pseudoaleatória para reprodutibilidade.

    Returns:
        pd.DataFrame: Subconjunto amostral estratificado.
    """
    _, stratified_sample_df = train_test_split(
        wine_dataframe,
        test_size=sample_fraction,
        stratify=wine_dataframe[TARGET_COLUMN],
        random_state=random_seed,
    )
    return stratified_sample_df.copy()


def simulate_central_limit_theorem(
    population_series: pd.Series,
    sample_size: int,
    resample_iterations: int = 1000,
    random_seed: int = 42,
) -> np.ndarray:
    """Simula a distribuição amostral da média via reamostragem com reposição.

    Args:
        population_series: Série com os valores populacionais da variável.
        sample_size: Tamanho de cada amostra aleatória extraída (n).
        resample_iterations: Quantidade de reamostragens executadas (B = 1000).
        random_seed: Semente pseudoaleatória.

    Returns:
        np.ndarray: Vetor unidimensional com as médias calculadas de cada iteração.
    """
    random_generator = np.random.default_rng(random_seed)
    population_values = population_series.to_numpy()

    simulated_means = np.empty(resample_iterations, dtype=np.float64)
    for iteration_index in range(resample_iterations):
        resampled_batch = random_generator.choice(
            population_values, size=sample_size, replace=True
        )
        simulated_means[iteration_index] = np.mean(resampled_batch)

    return simulated_means


def plot_sampling_and_clt_analysis(
    population_proline: pd.Series,
    sample_proline: pd.Series,
    bootstrap_means: np.ndarray,
    theoretical_standard_error: float,
    output_filepath: Path,
) -> None:
    """Gera visualização comparativa de histogramas e a distribuição do TCL.

    Args:
        population_proline: Valores de prolina da população completa.
        sample_proline: Valores de prolina da amostra estratificada de 20%.
        bootstrap_means: Vetor das 1.000 médias reamostradas.
        theoretical_standard_error: Erro-padrão teórico (sigma / sqrt(n)).
        output_filepath: Caminho do arquivo para gravação da figura.
    """
    configure_visual_standards()
    figure, (axis_distribution, axis_clt) = plt.subplots(
        nrows=1, ncols=2, figsize=(13, 5.5)
    )

    # Subplot 1: População vs Amostra Estratificada
    axis_distribution.hist(
        population_proline,
        bins=15,
        density=True,
        alpha=0.55,
        color="#2E5B88",
        label=f"População (N={len(population_proline)})",
        edgecolor="#1D3854",
    )
    axis_distribution.hist(
        sample_proline,
        bins=10,
        density=True,
        alpha=0.65,
        color="#800020",
        label=f"Amostra Estratificada 20% (n={len(sample_proline)})",
        edgecolor="#4A0012",
    )
    axis_distribution.set_title(
        "Distribuição da Prolina: População vs Amostra Estratificada"
    )
    axis_distribution.set_xlabel("Concentração de Prolina (mg/L)")
    axis_distribution.set_ylabel("Densidade de Probabilidade")
    axis_distribution.legend(frameon=True, facecolor="#FAFAFA")
    axis_distribution.grid(True, linestyle="--", alpha=0.3)

    # Subplot 2: Histograma das 1.000 Médias Amostrais (TCL)
    observed_standard_error = float(np.std(bootstrap_means, ddof=1))
    mean_of_means = float(np.mean(bootstrap_means))

    axis_clt.hist(
        bootstrap_means,
        bins=25,
        density=True,
        color="#507255",
        alpha=0.75,
        edgecolor="#2D4030",
        label="1.000 Médias Amostrais",
    )
    axis_clt.axvline(
        mean_of_means,
        color="#800020",
        linestyle="--",
        linewidth=2,
        label=f"Média das Médias: {mean_of_means:.1f} mg/L",
    )
    axis_clt.axvline(
        population_proline.mean(),
        color="#111111",
        linestyle=":",
        linewidth=2,
        label=f"Média Populacional: {population_proline.mean():.1f} mg/L",
    )
    axis_clt.set_title(
        f"Convergência do TCL (n={len(sample_proline)}, B=1.000)\n"
        f"EP Obs: {observed_standard_error:.2f} mg/L | EP Teórico: {theoretical_standard_error:.2f} mg/L"
    )
    axis_clt.set_xlabel("Média Amostral da Prolina (mg/L)")
    axis_clt.set_ylabel("Densidade de Frequência")
    axis_clt.legend(frameon=True, facecolor="#FAFAFA")
    axis_clt.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    figure.savefig(output_filepath, dpi=300)
    plt.close(figure)


def run_exercise_4() -> Dict[str, float]:
    """Executa a rotina analítica completa do Exercício 4."""
    wine_dataframe = load_clean_wine_dataset()
    stratified_sample_dataframe = extract_stratified_sample(
        wine_dataframe, sample_fraction=0.20, random_seed=42
    )

    sample_size = len(stratified_sample_dataframe)
    population_proline_series = wine_dataframe["proline"]
    sample_proline_series = stratified_sample_dataframe["proline"]

    population_mean = float(population_proline_series.mean())
    population_std_ddof0 = float(population_proline_series.std(ddof=0))
    sample_mean = float(sample_proline_series.mean())
    sample_std = float(sample_proline_series.std(ddof=1))

    simulated_means = simulate_central_limit_theorem(
        population_proline_series,
        sample_size=sample_size,
        resample_iterations=1000,
        random_seed=42,
    )

    theoretical_se = population_std_ddof0 / np.sqrt(sample_size)
    observed_se = float(np.std(simulated_means, ddof=1))
    reduction_factor = population_std_ddof0 / theoretical_se

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_path = output_dir / "exercicio4_proline_distribuicao_tcl.png"

    plot_sampling_and_clt_analysis(
        population_proline_series,
        sample_proline_series,
        simulated_means,
        theoretical_se,
        figure_path,
    )

    print("=== EXERCÍCIO 4: AMOSTRAGEM ESTRATIFICADA E TEOREMA CENTRAL DO LIMITE ===")
    print(f"Tamanho da População (N): {len(wine_dataframe)}")
    print(f"Tamanho da Amostra Estratificada (n): {sample_size}")
    print(
        f"Contagem por Cultivar na Amostra: {stratified_sample_dataframe[TARGET_COLUMN].value_counts().to_dict()}"
    )
    print(
        f"Média Populacional de Prolina: {population_mean:.2f} mg/L (Desvio-Padrão: {population_std_ddof0:.2f} mg/L)"
    )
    print(
        f"Média Amostral de Prolina (20%): {sample_mean:.2f} mg/L (Desvio-Padrão: {sample_std:.2f} mg/L)"
    )
    print(f"Erro-Padrão Teórico (sigma / sqrt(n)): {theoretical_se:.2f} mg/L")
    print(f"Erro-Padrão Observado (1.000 reamostragens): {observed_se:.2f} mg/L")
    print(
        f"Fator de Redução da Dispersão (sqrt(n)): {reduction_factor:.2f} vezes"
    )
    print(f"Figura salva com sucesso em: {figure_path}\n")

    return {
        "population_mean": population_mean,
        "population_std": population_std_ddof0,
        "sample_mean": sample_mean,
        "sample_std": sample_std,
        "theoretical_se": theoretical_se,
        "observed_se": observed_se,
        "reduction_factor": reduction_factor,
    }


if __name__ == "__main__":
    run_exercise_4()
