import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def draw_plot():
    # Cargar datos (colocar epa-sea-level.csv en la misma carpeta)
    df = pd.read_csv('epa-sea-level.csv')

    # Asegurar nombres esperados (FreeCodeCamp usa 'Year' y 'CSIRO Adjusted Sea Level')
    # Si tu CSV tiene otros nombres, cámbialos acá.
    x_all = df['Year'].values.reshape(-1, 1)
    y_all = df['CSIRO Adjusted Sea Level'].values

    # Modelo 1: regresión con todos los datos
    model_all = LinearRegression()
    model_all.fit(x_all, y_all)

    # Predecir desde el primer año del dataset hasta 2050 (inclusive)
    years_all = np.arange(df['Year'].min(), 2051).reshape(-1, 1)
    preds_all = model_all.predict(years_all)

    # Modelo 2: regresión usando datos desde el año 2000 en adelante
    df_recent = df[df['Year'] >= 2000]
    x_recent = df_recent['Year'].values.reshape(-1, 1)
    y_recent = df_recent['CSIRO Adjusted Sea Level'].values

    model_recent = LinearRegression()
    model_recent.fit(x_recent, y_recent)

    years_recent = np.arange(2000, 2051).reshape(-1, 1)
    preds_recent = model_recent.predict(years_recent)

    # Dibujar gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    # scatter de datos originales
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', s=20, label='Observations')

    # líneas de predicción
    ax.plot(years_all.flatten(), preds_all, color='red', linewidth=2, label='Fit: all data')
    ax.plot(years_recent.flatten(), preds_recent, color='green', linewidth=2, label='Fit: from 2000')

    # etiquetas y título
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
    ax.set_title('Rise in Sea Level')
    ax.legend()

    plt.tight_layout()

    # Guardar figura
    fig.savefig('sea_level_plot.png')

    # (opcional) imprimir predicción 2050 para control
    pred_2050_all = model_all.predict(np.array([[2050]]))[0]
    pred_2050_recent = model_recent.predict(np.array([[2050]]))[0]
    print(f"Predicción 2050 (modelo con todos los datos): {pred_2050_all:.3f}")
    print(f"Predicción 2050 (modelo desde 2000): {pred_2050_recent:.3f}")

    return fig

if __name__ == "__main__":
    draw_plot()
    print("sea_level_plot.png guardado.")
