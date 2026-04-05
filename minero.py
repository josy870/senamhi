import requests
import pandas as pd
import os
import time

# 1. Crear carpeta para almacenar los datos descargados
carpeta_destino = "data_departamentos"
os.makedirs(carpeta_destino, exist_ok=True)

# 2. Lista completa de departamentos del Perú
departamentos = [
    "Amazonas", "Ancash", "Apurimac", "Arequipa", "Ayacucho", "Cajamarca",
    "Callao", "Cusco", "Huancavelica", "Huanuco", "Ica", "Junin", "La Libertad",
    "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco",
    "Piura", "Puno", "San Martin", "Tacna", "Tumbes", "Ucayali"
]

def minar_datos_departamento(departamento):
    print(f"Iniciando extracción para el departamento de: {departamento}...")
    
    # URL base (Esta URL dependerá del portal exacto de SENAMHI que usemos)
    # Ejemplo genérico simulando un endpoint que acepta el nombre del departamento
    url = f"https://api.senamhi.gob.pe/datos?region={departamento.lower()}"
    
    try:
        # AQUI VA LA CONEXIÓN REAL:
        # response = requests.get(url)
        # data = response.json() 
        
        # SIMULACIÓN de los datos que extraeríamos para probar el script
        data_extraida = {
            "Fecha": ["2026-04-01", "2026-04-02", "2026-04-03"],
            "Temp_Max": [25.5, 26.1, 24.8],
            "Temp_Min": [18.2, 17.8, 18.0],
            "Precipitacion_mm": [0.0, 1.2, 0.5]
        }
        
        # 3. Transformar la data usando Pandas y exportarla a CSV
        df = pd.DataFrame(data_extraida)
        ruta_archivo = os.path.join(carpeta_destino, f"{departamento.lower()}_clima.csv")
        
        df.to_csv(ruta_archivo, index=False)
        print(f"✓ Datos guardados exitosamente en: {ruta_archivo}\n")
        
    except Exception as e:
        print(f"Error al descargar información de {departamento}: {e}\n")

# 4. Ejecutar el ciclo de minería
print("--- INICIANDO MINERO DE SENAMHI ---")
for dep in departamentos:
    minar_datos_departamento(dep)
    # Es una buena práctica poner una pausa de 1 o 2 segundos entre descargas
    # para evitar bloquear el servidor del gobierno (Rate Limiting).
    time.sleep(1.5) 

print("¡Extracción completada al 100%!")