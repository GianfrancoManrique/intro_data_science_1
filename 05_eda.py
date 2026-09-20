"""
EDA del caso de estudio de Lima Metropolitana

Objetivo:
- Describir distribuciones univariadas
- Explorar relaciones bivariadas
- Revisar patrones multivariados
- Generar salidas gráficas para interpretación inicial
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "processed" / "datos_temporales.csv"
RESULTS_DIR = ROOT / "results" / "eda"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def save_chart(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / name, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    print("=" * 80)
    print("INICIANDO EDA")
    print("=" * 80)

    df = pd.read_csv(DATA_PATH)
    df = df[df["ANIO"] < 2026].copy()
    print(f"Dataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")

    numeric_cols = [
        "POBLACION_TOTAL",
        "PORC_NBI",
        "TOTAL_DELITOS",
        "TASA_DELITOS_10K",
    ]

    for col in numeric_cols:
        if col not in df.columns:
            raise KeyError(f"La columna requerida no existe: {col}")

    # 1. Estadísticas descriptivas
    stats = df[numeric_cols].describe().T
    stats.to_csv(RESULTS_DIR / "estadisticas_descriptivas.csv")
    print("\nEstadísticas descriptivas guardadas en results/eda/estadisticas_descriptivas.csv")

    # 2. Distribuciones univariadas
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    for ax, col in zip(axes.flat, numeric_cols):
        sns.histplot(df[col], bins=25, kde=True, ax=ax)
        ax.set_title(f"Distribución de {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frecuencia")
    save_chart(fig, "distribuciones_univariadas.png")

    # 3. Boxplots para outliers
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    for ax, col in zip(axes, numeric_cols):
        sns.boxplot(x=df[col], ax=ax, color="#4C72B0")
        ax.set_title(f"Boxplot de {col}")
        ax.set_xlabel(col)
    save_chart(fig, "boxplots_outliers.png")

    # 4. Análisis temporal general
    temporal = (
        df.groupby("ANIO", as_index=False)
        .agg(
            TOTAL_DELITOS=("TOTAL_DELITOS", "sum"),
            TASA_PROMEDIO_10K=("TASA_DELITOS_10K", "mean"),
            POBLACION_TOTAL=("POBLACION_TOTAL", "sum"),
            PORC_NBI_PROMEDIO=("PORC_NBI", "mean"),
        )
        .sort_values("ANIO")
    )

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.lineplot(data=temporal, x="ANIO", y="TOTAL_DELITOS", ax=axes[0, 0], marker="o")
    axes[0, 0].set_title("Total de delitos por año")

    sns.lineplot(data=temporal, x="ANIO", y="TASA_PROMEDIO_10K", ax=axes[0, 1], marker="o")
    axes[0, 1].set_title("Tasa promedio de delitos por 10k por año")

    sns.lineplot(data=temporal, x="ANIO", y="POBLACION_TOTAL", ax=axes[1, 0], marker="o")
    axes[1, 0].set_title("Población total por año")

    sns.lineplot(data=temporal, x="ANIO", y="PORC_NBI_PROMEDIO", ax=axes[1, 1], marker="o")
    axes[1, 1].set_title("% NBI promedio por año")
    save_chart(fig, "analisis_temporal.png")

    # 5. Relación bivariada: porcentaje NBI vs tasa de delitos
    district_summary = (
        df.groupby("DISTRITO", as_index=False)
        .agg(
            POBLACION_TOTAL=("POBLACION_TOTAL", "mean"),
            PORC_NBI=("PORC_NBI", "mean"),
            TOTAL_DELITOS=("TOTAL_DELITOS", "sum"),
            TASA_DELITOS_10K=("TASA_DELITOS_10K", "mean"),
        )
        .sort_values("TASA_DELITOS_10K", ascending=False)
    )

    fig = plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=district_summary,
        x="PORC_NBI",
        y="TASA_DELITOS_10K",
        size="TOTAL_DELITOS",
        hue="TOTAL_DELITOS",
        palette="viridis",
        sizes=(40, 300),
        alpha=0.8,
    )
    plt.title("% NBI vs tasa de delitos por distrito")
    plt.xlabel("% NBI")
    plt.ylabel("Tasa delitos por 10,000 habitantes")
    save_chart(fig, "scatter_nbi_vs_tasa.png")

    # 6. Correlación y matrix multivariada
    corr = df[numeric_cols].corr(method="pearson")
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0, ax=ax)
    ax.set_title("Matriz de correlación")
    save_chart(fig, "matriz_correlacion.png")

    # 7. Pairplot para inspección multivariada
    pair_df = district_summary[["POBLACION_TOTAL", "PORC_NBI", "TOTAL_DELITOS", "TASA_DELITOS_10K"]].copy()
    pairplot = sns.pairplot(pair_df, diag_kind="kde", height=2.2)
    pairplot.fig.suptitle("Pairplot de variables clave", y=1.02)
    pairplot.fig.savefig(RESULTS_DIR / "pairplot_variables.png", dpi=300, bbox_inches="tight")
    plt.close(pairplot.fig)

    # 8. Top 10 distritos por tasa
    top10 = district_summary.head(10)
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(data=top10, x="TASA_DELITOS_10K", y="DISTRITO", palette="magma", ax=ax)
    ax.set_title("Top 10 distritos con mayor tasa de delitos")
    ax.set_xlabel("Tasa de delitos por 10,000 habitantes")
    ax.set_ylabel("Distrito")
    save_chart(fig, "top10_tasa_por_distrito.png")

    print("\nArchivos generados:")
    for path in sorted(RESULTS_DIR.iterdir()):
        print(f"- {path.name}")

    print("\n" + "=" * 80)
    print("EDA COMPLETADO")
    print("=" * 80)


if __name__ == "__main__":
    main()
