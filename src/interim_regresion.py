import pandas as pd
import os

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Ubicación exacta de este script (dentro de src/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Definición de la raíz del proyecto (un nivel arriba de src/)
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Ruta de entrada: data/raw/dataset_regresion.csv
raw_path = os.path.join(project_root, "data", "raw", "dataset_regresion.csv")

# Ruta de salida: data/interim/dataset_regresion_interim.csv
interim_path = os.path.join(project_root, "data", "interim", "dataset_regresion_interim.csv")

def process_king_county_data():
    print("==================================================")
    print(" INICIANDO LIMPIEZA ESTRUCTURAL - REGRESIÓN ")
    print("==================================================\n")

    # Verificar existencia del archivo de origen
    if not os.path.exists(raw_path):
        print(f"[!] Error: No se encontró el archivo en {raw_path}")
        return

    # Carga de datos
    df = pd.read_csv(raw_path)
    print(f"[+] Dataset cargado. Dimensiones originales: {df.shape}")

    # --- 2. TRANSFORMACIONES ESTRUCTURALES ---

    # 1. Eliminación de identificadores (ID)
    # Justificación: El ID no aporta valor predictivo y genera ruido en el análisis de correlación.
    if 'id' in df.columns:
        df.drop(columns=['id'], inplace=True)
        print("  -> [OK] Columna 'id' eliminada.")

    # 2. Procesamiento de Fechas
    # Justificación: Convertir la cadena de texto original a componentes temporales 
    # numéricos permite analizar la estacionalidad de los precios.
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['sale_year'] = df['date'].dt.year
        df['sale_month'] = df['date'].dt.month
        # Mantener la fecha en formato estándar YYYY-MM-DD
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        print("  -> [OK] Variables 'sale_year' y 'sale_month' creadas.")

    # 3. Cambio de tipo para Códigos Postales (Zipcode)
    # Justificación: El código postal es una variable categórica. Al convertirlo a texto, 
    # evitamos cálculos matemáticos erróneos (como promedios de zonas).
    if 'zipcode' in df.columns:
        df['zipcode'] = df['zipcode'].astype(str)
        print("  -> [OK] Variable 'zipcode' convertida a tipo categórico (string).")

    # 4. Creación de variable para Renovaciones
    # Justificación: La variable original tiene demasiados ceros. Una variable binaria 
    # (Renovada vs No Renovada) es más útil para el análisis visual.
    if 'yr_renovated' in df.columns:
        df['is_renovated'] = df['yr_renovated'].apply(lambda x: 1 if x > 0 else 0)
        print("  -> [OK] Variable binaria 'is_renovated' generada.")

    # Nota: Los valores atípicos se mantienen para ser analizados visualmente en el EDA.
    print("  -> [OK] Distribución estadística preservada (outliers intactos).")

    # --- 3. EXPORTACIÓN ---

    # Asegurar que la carpeta interim exista
    interim_dir = os.path.dirname(interim_path)
    if not os.path.exists(interim_dir):
        os.makedirs(interim_dir)
        print(f"[+] Carpeta creada: {interim_dir}")

    # Guardar archivo interim
    df.to_csv(interim_path, index=False)
    print(f"\n[+] Proceso finalizado. Archivo guardado en:\n    {interim_path}")
    print(f"[+] Dimensiones finales para el EDA: {df.shape}")

if __name__ == "__main__":
    process_king_county_data()