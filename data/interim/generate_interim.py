import pandas as pd
import os

# Determina la ubicación exacta de este script (tu carpeta actual)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas de lectura: sube un nivel (..) y entra a 'raw'
raw_housing_path = os.path.join(script_dir, "..", "raw", "dataset_regresion.csv")
raw_credit_path = os.path.join(script_dir, "..", "raw", "dataset_clasificacion.csv")

# Rutas de escritura: guarda en el mismo directorio donde está el script
interim_housing_path = os.path.join(script_dir, "dataset_regresion_interim.csv")
interim_credit_path = os.path.join(script_dir, "dataset_clasificacion_interim.csv")

def process_housing_interim():
    print("Procesando dataset de regresión (Housing)...")
    if not os.path.exists(raw_housing_path):
        print(f"Error: No se encontró el archivo original en {raw_housing_path}")
        return

    df = pd.read_csv(raw_housing_path)
    
    # Mapeo binario (yes/no a 1/0)
    # Justificación: Los gráficos de correlación (como mapas de calor) en el EDA requieren valores numéricos. 
    # Esta transformación adecúa la estructura sin alterar la distribución ni eliminar datos atípicos.
    binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({'yes': 1, 'no': 0})
    
    df.to_csv(interim_housing_path, index=False)
    print(f"Archivo guardado: {interim_housing_path}")

def process_credit_interim():
    print("Procesando dataset de clasificación (Credit)...")
    if not os.path.exists(raw_credit_path):
        print(f"Error: No se encontró el archivo original en {raw_credit_path}")
        return

    df = pd.read_csv(raw_credit_path)

    # Eliminación de identificador
    # Justificación: 'ID' es un índice secuencial carente de valor analítico que distorsiona las matrices de correlación.
    if 'ID' in df.columns:
        df.drop('ID', axis=1, inplace=True)

    # Renombrar variable objetivo
    # Justificación: Los puntos en el nombre generan errores de sintaxis en consultas SQL y funciones de librerías como seaborn.
    if 'default.payment.next.month' in df.columns:
        df.rename(columns={'default.payment.next.month': 'default_payment'}, inplace=True)

    # Consolidación de categorías
    # Justificación: Agrupa valores indocumentados (0, 5, 6) en una categoría general (4 y 3) para facilitar la lectura 
    # de histogramas y boxplots, sin modificar las variables numéricas continuas (edad, montos).
    df['EDUCATION'] = df['EDUCATION'].replace([0, 5, 6], 4)
    df['MARRIAGE'] = df['MARRIAGE'].replace(0, 3)

    df.to_csv(interim_credit_path, index=False)
    print(f"Archivo guardado: {interim_credit_path}")

if __name__ == "__main__":
    process_housing_interim()
    process_credit_interim()