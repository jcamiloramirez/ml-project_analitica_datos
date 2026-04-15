import sqlite3
import pandas as pd
import os

# --- 1. CONFIGURACIÓN DE LA CONEXIÓN ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
db_path = os.path.join(project_root, "database", "analitica_data.db")

def display_sql(query, conn):
    """Ejecuta una consulta SQL y la muestra formateada usando Pandas."""
    try:
        resultado = pd.read_sql_query(query, conn)
        print(resultado.to_string(
            index=False, 
            float_format=lambda x: f"{x:,.2f}"
        ))
    except Exception as e:
        print(f"[!] Error ejecutando consulta: {e}")

def ejecutar_consultas():
    if not os.path.exists(db_path):
        print(f"[!] ERROR: No se encontró la BD en {db_path}. Ejecuta setup_sqlite.py primero.")
        return

    conn = sqlite3.connect(db_path)
    
    print("=========================================")
    print(" 5 CONSULTAS SQL - HOUSING (KING COUNTY) ")
    print("=========================================")
    
    # 1. Conteo Total
    print("\n1. Conteo total de registros de vivienda:")
    display_sql("SELECT COUNT(*) AS Total_Casas FROM housing;", conn)

    # 2. Análisis de Extremos
    q2 = """
    SELECT 
        MIN(price) AS Precio_Min, MAX(price) AS Precio_Max, AVG(price) AS Precio_Prom,
        MIN(sqft_living) AS Area_Min, MAX(sqft_living) AS Area_Max, AVG(sqft_living) AS Area_Prom 
    FROM housing;
    """
    print("\n2. Análisis de extremos en Precio y Área Habitable (sqft_living):")
    display_sql(q2, conn)

    # 3. Agrupación por Calidad de Construcción
    q3 = """
    SELECT grade AS Calidad_Construccion, COUNT(*) AS Cantidad, AVG(price) AS Precio_Promedio 
    FROM housing GROUP BY grade ORDER BY grade DESC;
    """
    print("\n3. Agrupación por nivel de construcción (Grade) y precio promedio:")
    display_sql(q3, conn)

    # 4. Filtro: Propiedades de lujo
    q4 = """
    SELECT price, bedrooms, bathrooms, sqft_living, waterfront 
    FROM housing WHERE price > 2000000 AND waterfront = 1 LIMIT 5;
    """
    print("\n4. Filtro: Top 5 Propiedades de lujo (>2M) con vista al agua:")
    display_sql(q4, conn)

    # 5. Agrupación + Filtro
    q5 = """
    SELECT bedrooms AS Habitaciones, AVG(price) AS Precio_Promedio 
    FROM housing GROUP BY bedrooms HAVING COUNT(*) > 50 ORDER BY Habitaciones ASC;
    """
    print("\n5. Precio promedio por habitaciones (solo grupos con n > 50):")
    display_sql(q5, conn)

    print("\n=========================================")
    print(" 5 CONSULTAS SQL - CREDIT (CLASIFICACIÓN) ")
    print("=========================================")

    # 1. Conteo
    print("\n1. Conteo total de clientes:")
    display_sql("SELECT COUNT(*) AS Total_Clientes FROM credit;", conn)

    # 2. Análisis de Extremos
    q7 = """
    SELECT 
        MIN(LIMIT_BAL) AS Limite_Min, MAX(LIMIT_BAL) AS Limite_Max, AVG(LIMIT_BAL) AS Limite_Prom,
        MIN(AGE) AS Edad_Min, MAX(AGE) AS Edad_Max, AVG(AGE) AS Edad_Prom 
    FROM credit;
    """
    print("\n2. Análisis de extremos en Límite de Crédito y Edad:")
    display_sql(q7, conn)

    # 3. Agrupación por Variable Objetivo
    q8 = """
    SELECT default_payment AS 'Status_Default', COUNT(*) AS Cantidad, AVG(LIMIT_BAL) AS Limite_Medio 
    FROM credit GROUP BY default_payment;
    """
    print("\n3. Distribución de Default y su relación con el límite otorgado:")
    display_sql(q8, conn)

    # 4. Filtro: Clientes con pagos muy retrasados
    q9 = """
    SELECT LIMIT_BAL, EDUCATION, AGE, PAY_1 
    FROM credit WHERE PAY_1 > 2 AND default_payment = 1 LIMIT 5;
    """
    print("\n4. Filtro: 5 Clientes en default con retrasos altos (>2 meses) en PAY_1:")
    display_sql(q9, conn)

    # 5. Agrupación + Filtro Educativo
    q10 = """
    SELECT EDUCATION AS Nivel_Educativo, AVG(LIMIT_BAL) AS Limite_Promedio 
    FROM credit GROUP BY EDUCATION ORDER BY Limite_Promedio DESC;
    """
    print("\n5. Límite de crédito promedio por Nivel Educativo:")
    display_sql(q10, conn)

    conn.close()
    print("\n[+] Consultas finalizadas. Conexión cerrada.")

if __name__ == "__main__":
    ejecutar_consultas()