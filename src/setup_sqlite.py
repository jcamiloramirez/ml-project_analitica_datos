import sqlite3
import pandas as pd
import os

# --- RUTAS DINÁMICAS ---
# Ubicación de este script (dentro de src/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Sube un nivel a la raíz del proyecto
project_root = os.path.abspath(os.path.join(script_dir, ".."))

# Rutas hacia la capa Interim y la Base de Datos
interim_housing = os.path.join(project_root, "data", "interim", "dataset_regresion_interim.csv")
interim_credit = os.path.join(project_root, "data", "interim", "dataset_clasificacion_interim.csv")
db_path = os.path.join(project_root, "database", "analitica_data.db")

def crear_base_datos():
    print("=========================================")
    print(" INICIANDO PASO 1: GESTIÓN CON SQLITE ")
    print("=========================================\n")
    
    conn = sqlite3.connect(db_path)
    print(f"[+] Conectado a la base de datos en:\n    {db_path}\n")

    try:
        # Cargar Regresión (Interim)
        df_housing = pd.read_csv(interim_housing)
        df_housing.to_sql("housing", conn, if_exists="replace", index=False)
        print("[+] Tabla 'housing' creada e importada con éxito.")

        # Cargar Clasificación (Interim)
        df_credit = pd.read_csv(interim_credit)
        df_credit.to_sql("credit", conn, if_exists="replace", index=False)
        print("[+] Tabla 'credit' creada e importada con éxito.\n")
        
    except FileNotFoundError as e:
        print(f"[!] ERROR: No se encontró el archivo. Verifica las rutas.\n{e}")
        return None
    
    return conn

def ejecutar_consultas(conn):
    print("=========================================")
    print(" 5 CONSULTAS SQL - HOUSING (REGRESIÓN) ")
    print("=========================================")
    
    # 1. Conteo
    q1 = "SELECT COUNT(*) AS Total_Registros FROM housing;"
    print("\n1. Conteo total de propiedades:")
    display_sql(q1, conn)

    # 2. Análisis de Extremos (Justificación para IQR)
    q2 = """
    SELECT 
        MIN(price) AS Precio_Min, 
        MAX(price) AS Precio_Max, 
        AVG(price) AS Precio_Prom,
        MIN(area) AS Area_Min, 
        MAX(area) AS Area_Max, 
        AVG(area) AS Area_Prom 
    FROM housing;
    """
    print("\n2. Análisis de extremos en variables continuas (Previo a IQR):")
    display_sql(q2, conn)

    # 3. Agrupaciones
    q3 = "SELECT furnishingstatus AS Estado_Mobiliario, COUNT(*) AS Cantidad, AVG(price) AS Precio_Promedio FROM housing GROUP BY furnishingstatus;"
    print("\n3. Agrupación por estado de mobiliario (Conteo y Precio Promedio):")
    display_sql(q3, conn)

    # 4. Filtros
    q4 = "SELECT price, area, bedrooms, airconditioning FROM housing WHERE price > 8000000 AND airconditioning = 1 LIMIT 5;"
    print("\n4. Filtro: Top 5 Propiedades de lujo (Precio > 8M) con Aire Acondicionado:")
    display_sql(q4, conn)

    # 5. Agrupación + Filtro
    q5 = "SELECT bedrooms AS Habitaciones, AVG(price) AS Precio_Promedio FROM housing GROUP BY bedrooms HAVING COUNT(*) > 10 ORDER BY Precio_Promedio DESC;"
    print("\n5. Precio promedio por número de habitaciones (solo grupos con >10 propiedades):")
    display_sql(q5, conn)

    print("\n=========================================")
    print(" 5 CONSULTAS SQL - CREDIT (CLASIFICACIÓN) ")
    print("=========================================")

    # 1. Conteo
    q6 = "SELECT COUNT(*) AS Total_Clientes FROM credit;"
    print("\n1. Conteo total de clientes:")
    display_sql(q6, conn)

    # 2. Análisis de Extremos (Justificación para IQR)
    q7 = """
    SELECT 
        MIN(LIMIT_BAL) AS Limite_Min, 
        MAX(LIMIT_BAL) AS Limite_Max, 
        AVG(LIMIT_BAL) AS Limite_Prom,
        MIN(AGE) AS Edad_Min, 
        MAX(AGE) AS Edad_Max, 
        AVG(AGE) AS Edad_Prom 
    FROM credit;
    """
    print("\n2. Análisis de extremos en Límite de Crédito y Edad (Previo a IQR):")
    display_sql(q7, conn)

    # 3. Agrupaciones
    q8 = "SELECT default_payment AS Entro_en_Default, COUNT(*) AS Cantidad FROM credit GROUP BY default_payment;"
    print("\n3. Agrupación: Cantidad de clientes que entraron en Default vs No Default:")
    display_sql(q8, conn)

    # 4. Filtros
    q9 = "SELECT LIMIT_BAL, SEX, EDUCATION, AGE FROM credit WHERE LIMIT_BAL > 500000 AND default_payment = 1 LIMIT 5;"
    print("\n4. Filtro: 5 Clientes con Límite > 500,000 que ENTRARON en default:")
    display_sql(q9, conn)

    # 5. Agrupación + Filtro
    q10 = "SELECT EDUCATION AS Nivel_Educativo, AVG(LIMIT_BAL) AS Limite_Promedio FROM credit GROUP BY EDUCATION ORDER BY Limite_Promedio DESC;"
    print("\n5. Límite de crédito promedio agrupado por Nivel Educativo:")
    display_sql(q10, conn)

def display_sql(query, conn):
    # Usamos pandas para leer el resultado de la consulta SQL
    resultado = pd.read_sql_query(query, conn)
    
    # Imprimimos forzando el formato: separador de miles y 2 decimales fijos (sin notación e+)
    print(resultado.to_string(
        index=False, 
        float_format=lambda x: f"{x:,.2f}"
    ))

if __name__ == "__main__":
    conexion = crear_base_datos()
    if conexion:
        ejecutar_consultas(conexion)
        conexion.close()
        print("\n[+] Conexión a SQLite cerrada. Paso 1 completado exitosamente.")