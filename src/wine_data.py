"""Módulo utilitário centralizado para carregamento, tipagem e padronização

do Wine Recognition Dataset (FORINA et al., 1991).
"""

from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_wine

CULTIVAR_MAPPING: Dict[int, str] = {
    0: "Cultivar A",
    1: "Cultivar B",
    2: "Cultivar C",
}

FEATURE_COLUMNS: List[str] = [
    "alcohol",
    "malic_acid",
    "ash",
    "alcalinity_of_ash",
    "magnesium",
    "total_phenols",
    "flavanoids",
    "nonflavanoid_phenols",
    "proanthocyanins",
    "color_intensity",
    "hue",
    "od280/od315_of_diluted_wines",
    "proline",
]

TARGET_COLUMN: str = "cultivar"

PALETA_CULTIVARES: Dict[str, str] = {
    "Cultivar A": "#800020",  # Borgonha / Burgundy clássico
    "Cultivar B": "#2E5B88",  # Ardósia azulada
    "Cultivar C": "#507255",  # Verde musgo / folha de videira
}


def load_clean_wine_dataset() -> pd.DataFrame:
    """Carrega o Wine Recognition Dataset da biblioteca scikit-learn

    e estrutura em um DataFrame padronizado com mapeamento categórico de cultivares.

    Returns:
        pd.DataFrame: DataFrame contendo as 13 variáveis físico-químicas
                      e a coluna 'cultivar' devidamente rotulada.
    """
    raw_wine_data = load_wine(as_frame=True)
    wine_features_df = raw_wine_data.data.copy()
    raw_target_series = raw_wine_data.target

    wine_features_df[TARGET_COLUMN] = raw_target_series.map(CULTIVAR_MAPPING)

    return wine_features_df


def configure_visual_standards() -> None:
    """Configura parâmetros visuais globais para Matplotlib e Seaborn

    garantindo estética sênior, legibilidade e resolução para publicação.
    """
    plt.rcParams["font.sans-serif"] = [
        "DejaVu Sans",
        "Segoe UI",
        "Arial",
        "sans-serif",
    ]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["axes.edgecolor"] = "#333333"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["grid.color"] = "#CCCCCC"
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.alpha"] = 0.4
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 10
    plt.rcParams["xtick.labelsize"] = 9
    plt.rcParams["ytick.labelsize"] = 9
