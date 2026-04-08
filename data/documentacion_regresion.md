## Documentación: Base de Datos de Regresión (House Prices)

**a) Nombre de la base de datos:** dataset_regresion.csv (Originalmente: Housing.csv)

---

**b) Fuente (URL):** https://www.kaggle.com/datasets/yasserh/housing-prices-dataset

---

**c) Descripción general del problema:** La fijación del precio de una propiedad en el mercado inmobiliario es un proceso complejo que depende de múltiples factores estructurales y de entorno. El problema consiste en modelar la relación matemática entre dichas características y el precio final de venta, con el fin de comprender los determinantes del valor inmobiliario y facilitar su estimación mediante un enfoque objetivo basado en datos reales.

---

**d) Objetivo del análisis:** Construir un modelo de regresión que permita aproximar la función que relaciona el precio de la vivienda con sus variables explicativas, identificando la contribución individual y conjunta de cada característica en la variabilidad del precio de mercado.

---

**e) Variable objetivo (variable respuesta):** price *(Numérica continua: Representa el precio final de venta de la vivienda).*

---

**f) Diccionario de variables:**

**Características Estructurales:**
* **area**: Tamaño total del lote de la vivienda en pies cuadrados. *(Numérica continua).*
* **bedrooms**: Cantidad de habitaciones o dormitorios en la casa. *(Numérica discreta).*
* **bathrooms**: Cantidad de baños disponibles. *(Numérica discreta).*
* **stories**: Número de pisos o niveles que tiene la propiedad. *(Numérica discreta).*
* **parking**: Número de espacios de parqueo disponibles dentro de la propiedad. *(Numérica discreta).*

**Amenidades y Servicios**
* **mainroad**: Indica si la propiedad está conectada a una vía principal (yes/no). *(Categórica nominal).*
* **guestroom**: Indica si la casa cuenta con una habitación para huéspedes (yes/no). *(Categórica nominal).*
* **basement**: Indica si la casa tiene sótano (yes/no). *(Categórica nominal).*
* **hotwaterheating**: Indica si la casa cuenta con sistema de calentador de agua (yes/no). *(Categórica nominal).*
* **airconditioning**: Indica si la casa tiene sistema de aire acondicionado central (yes/no). *(Categórica nominal).*
* **prefarea**: Indica si la casa está ubicada en una zona residencial de alta demanda (yes/no). *(Categórica nominal).*

**Estado de la Propiedad:**
* **furnishingstatus**: Estado de amueblamiento de la vivienda (furnished, semi-furnished, unfurnished). *(Categórica nominal).*

---

**g) Número de observaciones:** 545 filas.

---

**h) Número de variables:** 13 columnas (1 variable objetivo + 12 variables predictoras).

---

**i) Posibles hipótesis de estudio:**

1. **Efecto del tamaño (Factor Dominante):** Se espera que exista una relación predictiva fuerte y positiva entre la variable `area` y la variable objetivo `price`, siendo el tamaño del lote el factor base de mayor peso en la valoración de la propiedad.

2. **Preferencia por la verticalidad:** Se plantea que, incluso manteniendo constante el tamaño total del lote, las casas con mayor número de pisos (`stories`) registrarán un precio superior, indicando una preferencia del mercado por construcciones verticales o una mejor optimización del espacio.

3. **Efecto de rendimientos decrecientes en baños:** Se hipotetiza que el efecto del número de baños sobre el precio presenta rendimientos decrecientes; el incremento marginal en el valor de la vivienda será porcentualmente mayor al añadir el segundo baño que al añadir el cuarto.
