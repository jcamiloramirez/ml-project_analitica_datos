## Documentación: Base de Datos de Regresión (House Sales - King County)

**a) Nombre de la base de datos:**  
dataset_regresion.csv (Originalmente: kc_house_data.csv)

---

**b) Fuente (URL):**  
https://www.kaggle.com/datasets/harlfoxem/housesalesprediction

---

**c) Descripción general del problema:**  
El precio de las viviendas en mercados inmobiliarios reales depende de una combinación de factores estructurales, de calidad y de localización geográfica. En particular, la ubicación de la propiedad, sus características físicas y su estado influyen significativamente en su valor de mercado.

El problema consiste en modelar la relación entre estas variables y el precio de venta de las viviendas en el condado de King (Seattle, EE.UU.), a partir de datos reales de transacciones inmobiliarias. Este problema permite analizar cómo diferentes atributos contribuyen a la formación del precio en un contexto urbano real.

---

**d) Objetivo del análisis:**  
Construir un modelo de regresión que permita predecir el precio de una vivienda a partir de sus características estructurales, de calidad y de ubicación, identificando los factores más influyentes en la determinación del valor inmobiliario.

---

**e) Variable objetivo (variable respuesta):**  
price *(Numérica continua: Representa el precio de venta de la vivienda en dólares).*

---

**f) Diccionario de variables:**

* **id**: Identificador único de la propiedad. *(No predictiva; debe excluirse del modelo).*

* **date**: Fecha de la venta de la propiedad. *(Categórica temporal; puede transformarse en variables como año o mes).*

---

**Características estructurales:**

* **bedrooms**: Número de habitaciones. *(Numérica discreta).*

* **bathrooms**: Número de baños. *(Numérica continua).*

* **sqft_living**: Área habitable interior en pies cuadrados. *(Numérica continua).*

* **sqft_lot**: Tamaño total del lote. *(Numérica continua).*

* **floors**: Número de pisos. *(Numérica continua/discreta).*

* **waterfront**: Indica si la propiedad tiene vista al agua (0 = no, 1 = sí). *(Categórica nominal binaria).*

* **view**: Índice de calidad de la vista de la propiedad. *(Numérica discreta ordinal).*

* **condition**: Estado general de la propiedad. *(Numérica discreta ordinal).*

* **grade**: Calidad de construcción y diseño. *(Numérica discreta ordinal).*

---

**Distribución del espacio:**

* **sqft_above**: Área habitable por encima del nivel del suelo. *(Numérica continua).*

* **sqft_basement**: Área del sótano. *(Numérica continua).*

---

**Ubicación:**

* **zipcode**: Código postal de la propiedad. *(Categórica nominal).*

* **lat**: Latitud geográfica. *(Numérica continua).*

* **long**: Longitud geográfica. *(Numérica continua).*

---

**Información temporal de la propiedad:**

* **yr_built**: Año de construcción. *(Numérica discreta).*

* **yr_renovated**: Año de última renovación (0 si no ha sido renovada). *(Numérica discreta).*

---

**Información de vecindario:**

* **sqft_living15**: Área promedio de viviendas cercanas. *(Numérica continua).*

* **sqft_lot15**: Tamaño promedio de lotes cercanos. *(Numérica continua).*

---

**g) Número de observaciones:**  
21,613 registros.

---

**h) Número de variables:**  
21 columnas (1 variable objetivo + variables predictoras + identificador).

---

**i) Posibles hipótesis de estudio:**

1. **Efecto del área habitable:**  
Se espera que exista una relación positiva entre el área habitable (`sqft_living`) y el precio (`price`), siendo uno de los principales determinantes del valor de la propiedad.

---

2. **Importancia de la ubicación geográfica:**  
Se plantea que las variables de localización (`lat`, `long`, `zipcode`) tienen un impacto significativo en el precio, reflejando diferencias en la valorización del suelo según la zona.

---

3. **Efecto de la calidad estructural:**  
Se hipotetiza que propiedades con mayor calidad de construcción (`grade`) y mejor condición (`condition`) presentan precios más altos.

---

4. **Impacto de amenidades premium:**  
Se espera que características como `waterfront` o mejores valores en `view` incrementen significativamente el precio de la vivienda.

---

5. **Efecto de la antigüedad y renovación:**  
Se plantea que viviendas más antiguas (`yr_built`) tienden a tener menor precio, salvo que hayan sido renovadas (`yr_renovated`), lo que puede mitigar o revertir este efecto.

---

6. **Influencia del entorno:**  
Se hipotetiza que las características del vecindario (`sqft_living15`, `sqft_lot15`) influyen en el precio de la vivienda, reflejando efectos de entorno y comparación con propiedades cercanas.