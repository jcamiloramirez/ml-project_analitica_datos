import sqlite3
import pandas as pd
import os

# --- 1. CONFIGURACIÓN DE RUTAS DINÁMICAS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Rutas hacia la capa Interim y la Base de Datos
interim_housing = os.path.join(project_root, "data", "interim", "dataset_regresion_interim.csv")
interim_credit = os.path.join(project_root, "data", "interim", "dataset_clasificacion_interim.csv")

# Aseguramos que la carpeta database exista
db_dir = os.path.join(project_root, "database")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "analitica_data.db")

def crear_base_datos():
    print("=========================================")
    print(" INICIANDO PASO 1: CREACIÓN DE SQLITE    ")
    print("=========================================\n")
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"[+] Conectado a la base de datos en:\n    {db_path}\n")

        # Cargar Regresión (King County)
        if os.path.exists(interim_housing):
            df_housing = pd.read_csv(interim_housing)
            df_housing.to_sql("housing", conn, if_exists="replace", index=False)
            print("[+] Tabla 'housing' (King County) actualizada e importada.")
        else:
            print(f"[!] ADVERTENCIA: No se encontró {interim_housing}")

        # Cargar Clasificación (Credit Default)
        if os.path.exists(interim_credit):
            df_credit = pd.read_csv(interim_credit)
            df_credit.to_sql("credit", conn, if_exists="replace", index=False)
            print("[+] Tabla 'credit' (Credit Card) actualizada e importada.\n")
        else:
             print(f"[!] ADVERTENCIA: No se encontró {interim_credit}")
        
    except Exception as e:
        print(f"[!] ERROR durante la importación de datos:\n{e}")
    finally:
        if conn:
            conn.close()
            print("[+] Conexión a SQLite cerrada. Estructura de BD lista.")

if __name__ == "__main__":
    crear_base_datos()