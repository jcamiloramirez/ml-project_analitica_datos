import pandas as pd
import os

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Ubicación exacta de este script (dentro de src/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Definición de la raíz del proyecto (un nivel arriba de src/)
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Ruta de entrada: data/raw/dataset_clasificacion.csv
raw_path = os.path.join(project_root, "data", "raw", "dataset_clasificacion.csv")

# Ruta de salida: data/interim/dataset_clasificacion_interim.csv
interim_path = os.path.join(project_root, "data", "interim", "dataset_clasificacion_interim.csv")

def process_credit_interim():
    print("==================================================")
    print(" INICIANDO LIMPIEZA - CLASIFICACIÓN ")
    print("==================================================\n")

    # Verificar si el archivo raw existe
    if not os.path.exists(raw_path):
        print(f"[!] Error: No se encontró el archivo original en {raw_path}")
        return

    # Carga de datos
    df = pd.read_csv(raw_path)
    print(f"[+] Dataset cargado. Dimensiones originales: {df.shape}")

    # --- 2. TRANSFORMACIONES ESTRUCTURALES ---

    # 1. Eliminación de identificador
    # Justificación: 'ID' es un índice secuencial carente de valor analítico que distorsiona las matrices de correlación.
    if 'ID' in df.columns:
        df.drop('ID', axis=1, inplace=True)
        print("  -> [OK] Columna 'ID' eliminada.")

    # 2. Renombrar variables (Objetivo y Consistencia)
    # Justificación: Se renombra la variable objetivo por sintaxis de SQL/Seaborn 
    # y PAY_0 a PAY_1 para mantener la coherencia secuencial con el resto del historial.
    rename_dict = {
        'default.payment.next.month': 'default_payment',
        'PAY_0': 'PAY_1'
    }
    # Solo renombramos si las columnas existen para evitar errores
    df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns}, inplace=True)
    print("  -> [OK] Variables 'default_payment' y 'PAY_1' actualizadas.")

    # 3. Consolidación de categorías (Educación)
    # Justificación: Agrupa valores indocumentados (0, 5, 6) en una categoría general (4) para facilitar la lectura 
    # de histogramas y boxplots.
    if 'EDUCATION' in df.columns:
        df['EDUCATION'] = df['EDUCATION'].replace([0, 5, 6], 4)
        print("  -> [OK] Categorías de EDUCATION normalizadas (0,5,6 -> 4).")

    # 4. Consolidación de categorías (Estado Civil)
    # Justificación: El valor 0 no está documentado; se agrupa en la categoría 3 (otros).
    if 'MARRIAGE' in df.columns:
        df['MARRIAGE'] = df['MARRIAGE'].replace(0, 3)
        print("  -> [OK] Categorías de MARRIAGE normalizadas (0 -> 3).")

    # Nota: Los valores monetarios y de edad se mantienen intactos para el análisis de outliers en el EDA.
    print("  -> [OK] Distribuciones numéricas preservadas para el EDA.")

    # --- 3. EXPORTACIÓN ---

    # Asegurarnos de que la carpeta interim exista
    interim_dir = os.path.dirname(interim_path)
    if not os.path.exists(interim_dir):
        os.makedirs(interim_dir)
        print(f"[+] Carpeta creada: {interim_dir}")

    # Guardar el archivo interim
    df.to_csv(interim_path, index=False)
    print(f"\n[+] Proceso finalizado. Archivo guardado en:\n    {interim_path}")
    print(f"[+] Dimensiones finales para el EDA: {df.shape}")

if __name__ == "__main__":
    process_credit_interim()