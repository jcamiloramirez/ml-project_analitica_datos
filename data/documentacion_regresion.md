## Documentación: Base de Datos de Regresión (House Prices)

**a) Nombre de la base de datos:** Housing.csv

**b) Fuente (URL):** https://www.kaggle.com/datasets/yasserh/housing-prices-dataset

**c) Descripción general del problema:** La fijación del precio de venta de una propiedad en el mercado inmobiliario es un proceso altamente subjetivo y dependiente de múltiples factores físicos y de ubicación. El problema radica en la necesidad de tasadores, compradores y vendedores de tener una estimación justa, objetiva y basada en datos reales sobre el valor de una vivienda, evitando la especulación y sobrevaloración del mercado.

**d) Objetivo del análisis:** Construir un modelo predictivo de regresión que permita estimar el precio final de venta de una vivienda a partir de sus características estructurales (como el área y cantidad de habitaciones) y sus comodidades adicionales.

**e) Variable objetivo (variable respuesta):** price (Numérica continua - Representa el precio final de venta de la vivienda en el mercado).

**f) Diccionario de variables:**
* **price**: Precio de venta de la casa. *(Numérica continua)*.
* **rea**: Tamaño total del lote de la vivienda en pies cuadrados o metros cuadrados. *(Numérica continua)*.
* **edrooms**: Cantidad de habitaciones o dormitorios en la casa. *(Numérica discreta)*.
* **athrooms**: Cantidad de baños disponibles. *(Numérica discreta)*.
* **stories**: Número de pisos o niveles que tiene la propiedad. *(Numérica discreta)*.
* **mainroad**: Indica si la propiedad está conectada a una vía principal (yes/no). *(Categórica nominal)*.
* **guestroom**: Indica si la casa cuenta con una habitación para huéspedes (yes/no). *(Categórica nominal)*.
* **asement**: Indica si la casa tiene sótano (yes/no). *(Categórica nominal)*.
* **hotwaterheating**: Indica si la casa cuenta con sistema de calentador de agua (yes/no). *(Categórica nominal)*.
* **irconditioning**: Indica si la casa tiene sistema de aire acondicionado central (yes/no). *(Categórica nominal)*.
* **parking**: Número de espacios de parqueo disponibles dentro de la propiedad. *(Numérica discreta)*.
* **prefarea**: Indica si la casa está ubicada en una zona residencial preferencial o de alta demanda (yes/no). *(Categórica nominal)*.
* **urnishingstatus**: Estado de amueblamiento de la vivienda (furnished = amueblado, semi-furnished = semi-amueblado, unfurnished = sin muebles). *(Categórica ordinal)*.

**g) Número de observaciones:** 545 filas.

**h) Número de variables:** 13 columnas (1 variable objetivo + 12 variables predictoras).

**i) Posibles hipótesis de estudio:**
1. **Efecto del tamaño:** Se espera que exista una relación predictiva fuerte y positiva entre la variable rea y la variable objetivo price, siendo el tamaño del lote el factor base de mayor peso en la valoración de la propiedad, independientemente del algoritmo utilizado.
2. **Prima por comodidades:** Las casas que cuentan con aire acondicionado (irconditioning = yes) y están en una zona preferencial (prefarea = yes) tendrán un precio de venta promedio estadísticamente superior al de casas similares sin estas características.
3. **Efecto de rendimientos decrecientes en habitaciones:** Se hipotetiza que el incremento de precio al pasar de 1 a 2 baños (athrooms) será porcentualmente mayor que el incremento al pasar de 3 a 4, mostrando que ciertas comodidades añaden valor de forma no perfectamente lineal.
