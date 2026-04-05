# Senamhi Scraper 🌦️

Este proyecto es un scraper desarrollado en Python para extraer datos meteorológicos de las estaciones del **SENAMHI**.

## 🚀 Instalación y Uso

Sigue estos pasos para configurar el entorno y ejecutar el scraper:

### 1. Preparar el proyecto
Crea una carpeta para el proyecto y sitúate dentro de ella:
```bash
mkdir Senamhi_scraper
cd Senamhi_scraper
```
### 2. Configurar el entorno virtual
Es recomendable usar un entorno virtual para mantener las dependencias aisladas:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```
### 3. Instalar dependencias
Instala las librerías necesarias para el funcionamiento del script:

```bash
pip install requests pandas beautifulsoup4
```
### 4. Ejecución
Una vez configurado todo, puedes ejecutar el código principal. El script utiliza la siguiente URL base para la extracción de datos de Loreto:

text
https://www.senamhi.gob.pe/main.php?dp=loreto&p=estaciones
```bash
python tu_script.py
```
🛠️ Tecnologías utilizadas
Python: Lenguaje principal.

Requests: Para realizar las peticiones HTTP al sitio del SENAMHI.

BeautifulSoup4: Para parsear el contenido HTML.

Pandas: Para la estructuración y limpieza de los datos extraídos.
