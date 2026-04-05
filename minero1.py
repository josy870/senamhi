import os
import time
import pandas as pd
from datetime import datetime, timedelta

# --- 1. BASE DE DATOS GEOGRÁFICA (Resumida para el ejemplo) ---
# --- BASE DE DATOS GEOGRÁFICA (VERSIÓN EXTENDIDA) ---
geografia_peru = {
    "amazonas": {
        "chachapoyas": ["chachapoyas", "asuncion", "balsas", "chuquibamba", "huancas", "leymebamba"],
        "bagua": ["bagua", "aramango", "copallin", "el parco", "imaza"],
        "utcubamba": ["bagua grande", "cajaruro", "cumbalumba", "el milagro", "jamalca"]
    },
    "ancash": {
        "huaraz": ["huaraz", "cochas", "huanchay", "independencia", "pira", "tarica"],
        "santa": ["chimbote", "caceres del peru", "coishco", "moro", "nuevo chimbote", "samanco"],
        "huari": ["huari", "anra", "cajay", "chavin de huantar", "huacachi"]
    },
    "apurimac": {
        "abancay": ["abancay", "chacoche", "circarca", "curahuasi", "huanipaca", "tamburco"],
        "andahuaylas": ["andahuaylas", "andarapa", "chiara", "huancarama", "pacucha", "talavera"]
    },
    "arequipa": {
        "arequipa": ["arequipa", "alto selva alegre", "cayma", "cerro colorado", "jacobo hunter", "mariano melgar", "miraflores", "paucarpata", "sachaca", "socabaya", "tiabaya", "yanahuara", "yura"],
        "caylloma": ["chivay", "cabanaconde", "callalli", "coporaque", "huambo", "maca", "yanque"],
        "camana": ["camana", "jose maria quimper", "marian nicolas valcarcel", "mariscal caceres"]
    },
    "ayacucho": {
        "huamanga": ["ayacucho", "acocro", "ancos", "carmen alto", "chiara", "jesus nazareno", "san juan bautista", "tambillo"],
        "huanta": ["huanta", "ayahuanco", "huamanguilla", "iglesiachayo", "luricocha", "santillana"],
        "lucanas": ["puquio", "aucara", "carmen salcedo", "chaviña", "chipao", "lucanas"]
    },
    "cajamarca": {
        "cajamarca": ["cajamarca", "asuncion", "baños del inca", "chetilla", "cospan", "enacañada", "jesus", "llacanora", "magdalena"],
        "jaen": ["jaen", "bellavista", "chontalí", "colapas", "huabal", "las pirias", "pomahuaca"],
        "chota": ["chota", "anguia", "chadin", "chiguirip", "chimban", "choropampa", "cochabamba"]
    },
    "callao": {
        "callao": ["callao", "bellavista", "carmen de la legua reynoso", "la perla", "la punta", "ventanilla", "mi peru"]
    },
    "cusco": {
        "cusco": ["cusco", "ccorcca", "poroy", "san jeronimo", "san sebastian", "santiago", "saylla", "wanchaq"],
        "urubamba": ["urubamba", "chinchero", "huayllabamba", "machupicchu", "maras", "ollantaytambo", "yucay"],
        "la convencion": ["quillabamba", "echarate", "huayopata", "maranura", "ocobamba", "santa ana", "santa teresa", "vilcabamba"],
        "canchis": ["sicuani", "checacupe", "combapata", "marangani", "pitumarca", "san pablo"]
    },
    "huancavelica": {
        "huancavelica": ["huancavelica", "acobambilla", "acoria", "conayca", "cuenca", "izcuchaca", "manta", "palca", "yauli"],
        "tayacaja": ["pampas", "acostambo", "acraquia", "ahuaycha", "colcabamba", "daniel hernandez", "huachocolpa"]
    },
    "huanuco": {
        "huanuco": ["huanuco", "amarilis", "chinchao", "churubamba", "margos", "pillco marca", "quisqui", "yacus"],
        "leoncio prado": ["tingo maria", "daniel alomia robles", "hermilio valdizan", "jose crespo y castillo", "luyando", "rupa-rupa"]
    },
    "ica": {
        "ica": ["ica", "la tinguiña", "los aquijes", "ocucaje", "pachacutec", "parcona", "pueblo nuevo", "salas", "san jose de los molinos", "san juan bautista", "subtanjalla", "tate", "yauca del rosario"],
        "pisco": ["pisco", "huancano", "humay", "independencia", "paracas", "san clemente", "san andres", "tupac amaru inca"],
        "chincha": ["chincha alta", "alto laran", "chavin", "chincha baja", "el carmen", "grocio prado", "pueblo nuevo", "sunampe"]
    },
    "junin": {
        "huancayo": ["huancayo", "carhuacallanga", "chacapampa", "chicche", "chilca", "chongos alto", "el tambo", "pilcomayo", "san agustin", "sapallanga"],
        "chanchamayo": ["la merced", "perene", "pichanaqui", "san luis de shuaro", "san ramon", "vitoc"],
        "satipo": ["satipo", "coviriali", "llaylla", "mazamari", "pampa hermosa", "pangoa", "rio negro"]
    },
    "la libertad": {
        "trujillo": ["trujillo", "el porvenir", "florencia de mora", "huanchaco", "la esperanza", "laredo", "moche", "poroto", "salaverry", "simbal", "victor larco herrera"],
        "ascope": ["ascope", "chicama", "chocope", "magdalena de cao", "paijan", "razuri", "santiago de cao"],
        "pacasmayo": ["san pedro de lloc", "guadalupe", "jequetepeque", "pacasmayo", "san jose"]
    },
    "lambayeque": {
        "chiclayo": ["chiclayo", "chongoyape", "eten", "eten puerto", "jose leonardo ortiz", "la victoria", "lagunas", "monsefu", "nueva arica", "oyotun", "picsi", "pimentel", "reque", "santa rosa", "zaña"],
        "lambayeque": ["lambayeque", "chochope", "illimo", "jayanca", "mochuci", "morrope", "motupe", "olmos", "pacora", "salas", "san jose", "tucume"],
        "ferreñafe": ["ferreñafe", "cañaris", "incahuasi", "mesones muro", "pitipo", "pueblo nuevo"]
    },
    "lima": {
        "lima": ["lima cercado", "ate", "barranco", "breña", "carabayllo", "chaclacayo", "chorrillos", "cieneguilla", "comas", "el agustino", "independencia", "jesus maria", "la molina", "la victoria", "lince", "los olivos", "lurigancho", "lurin", "magdalena del mar", "miraflores", "pachacamac", "pucusana", "pueblo libre", "puente piedra", "punta hermosa", "punta negra", "rimac", "san bartolo", "san borja", "san isidro", "san juan de lurigancho", "san juan de miraflores", "san luis", "san martin de porres", "san miguel", "santa anita", "santa maria del mar", "santa rosa", "surco", "surquillo", "villa el salvador", "villa maria del triunfo"],
        "cañete": ["san vicente de cañete", "asia", "calango", "cerro azul", "chilca", "coayllo", "imperial", "lunahuana", "mala", "nuevo imperial", "pacaran", "quilmana", "san antonio", "san luis", "santa cruz de flores", "zuñiga"],
        "huaura": ["huacho", "ambar", "caleta de carquin", "checras", "hualmay", "huaura", "leoncio prado", "paccho", "santa leonor", "santa maria", "sayan", "vegueta"],
        "huarochiri": ["matucana", "antioquia", "callahuanca", "carampoma", "chicla", "cuenca", "huachupampa", "huanza", "huarochiri", "lahuaytambo", "langa", "laraos", "mariatana", "ricardo palma", "san andres de tupicocha", "san bartolome", "san damian", "san juan de iris", "san juan de tantaranche", "san lorenzo de quinti", "san mateo", "san mateo de otao", "san pedro de casta", "san pedro de huancayre", "sangallaya", "santa cruz de cocachacra", "santa eulalia", "santiago de anchucaya", "santiago de tuna", "santo domingo de los olleros", "surco"]
    },
    "loreto": {
        "maynas": ["iquitos", "alto nanay", "belen", "indiana", "las amazonas", "mazan", "napo", "punchana", "torres causana"],
        "alto amazonas": ["yurimaguas", "balsapuerto", "jeberos", "lagunas", "santa cruz", "teniente cesar lopez rojas"]
    },
    "madre de dios": {
        "tambopata": ["puerto maldonado", "inambari", "las piedras", "laberinto"],
        "manu": ["salvacion", "fitzcarrald", "madre de dios", "huepetuhe"]
    },
    "moquegua": {
        "mariscal nieto": ["moquegua", "carumas", "cuchumbaya", "samegua", "san cristobal", "torata"],
        "ilo": ["ilo", "el algarrobico", "pacocha"]
    },
    "pasco": {
        "pasco": ["cerro de pasco", "chaupimarca", "huachon", "huariaca", "huayllay", "ninacaca", "pallanchacra", "paucartambo", "san fco de asis de yarusyacan", "simon bolivar", "ticlayan", "tinyahuarco", "vicco", "yanacancha"],
        "oxapampa": ["oxapampa", "chontabamba", "huancabamba", "palcazu", "pozuzo", "puerto bermudez", "villa rica", "constitucion"]
    },
    "piura": {
        "piura": ["piura", "castilla", "catacaos", "cura mori", "el tallan", "la arena", "la union", "las lomas", "tambogrande", "veintiseis de octubre"],
        "sullana": ["sullana", "bellavista", "ignacio escudero", "lancones", "marcavelica", "miguel checa", "querecotillo", "salitral"],
        "talara": ["parariñas", "el alto", "la brea", "lobitos", "los organos", "mancora"],
        "paita": ["paita", "amotope", "arenal", "colan", "la huaca", "tamarindo", "vichayal"]
    },
    "puno": {
        "puno": ["puno", "acora", "amantaní", "atuncolla", "capachica", "chucuito", "coata", "huata", "mañazo", "paucarcolla", "pichacani", "plateria", "san antonio", "tiquillaca", "vilque"],
        "san roman": ["juliaca", "cabana", "cabanillas", "caracoto"]
    },
    "san martin": {
        "moyobamba": ["moyobamba", "calzada", "habana", "jepelacio", "soritor", "yantalo"],
        "san martin": ["tarapoto", "alberto levek", "cacaotazo", "chazuta", "chipurana", "el porvenir", "huimbayoc", "juan guerra", "la banda de shilcayo", "morales", "papaplaya", "san antonio", "sauce", "shapaja"],
        "tocache": ["tocache", "nuevo progreso", "polvora", "shunte", "uchiza"]
    },
    "tacna": {
        "tacna": ["tacna", "alto de la alianza", "calana", "ciudad nueva", "coronel gregorio albarracin lanchipa", "inclan", "pachia", "palca", "pocollay", "sama"],
        "tarata": ["tarata", "chucatamani", "estique", "estique-pampa", "sitajara", "susapaya", "tarucachi", "ticaco"]
    },
    "tumbes": {
        "tumbes": ["tumbes", "corrales", "la cruz", "pampas de hospital", "san jacinto", "san juan de la virgen"],
        "zarumilla": ["zarumilla", "aguas verdes", "matapalo", "papayal"],
        "contralmirante villar": ["zorritos", "casitas", "canoas de punta sal"]
    },
    "ucayali": {
        "coronel portillo": ["pucallpa", "calleria", "campoverde", "iparia", "masisea", "nueva requena", "yarinacocha", "manantay"],
        "padre abad": ["aguaytia", "irazola", "curimana", "neshuya", "alexander von humboldt"]
    }
}
carpeta_base = "data_descargada"

# --- 2. MÓDULO: MINERO DE CLIMA (SENAMHI) ---
def procesar_clima():
    print("\n🌤️ Detectado: Portal Meteorológico.")
    departamento = input("¿Qué departamento deseas descargar? (Ej. Lima, Arequipa): ").strip().lower()
    
    if departamento not in geografia_peru:
        print(f"❌ Error: El departamento '{departamento}' no está en nuestra base de datos actual.")
        return

    print(f"\nGenerando estructura y descargando datos para: {departamento.upper()}")
    
    provincias = geografia_peru[departamento]
    for provincia, distritos in provincias.items():
        for distrito in distritos:
            # Crear ruta: data_descargada/clima/lima/lima/miraflores
            ruta_destino = os.path.join(carpeta_base, "clima", departamento, provincia, distrito)
            os.makedirs(ruta_destino, exist_ok=True)
            
            # Simular la descarga de datos de SENAMHI
            print(f"  -> Extrayendo datos de: {distrito.capitalize()}...")
            # Aquí iría tu código de BeautifulSoup para raspar la web...
            time.sleep(0.3) 
            
            # Crear un archivo CSV de confirmación
            ruta_archivo = os.path.join(ruta_destino, f"{distrito}_historico.csv")
            pd.DataFrame({"Mensaje": ["Datos climáticos listos"]}).to_csv(ruta_archivo, index=False)

    print("\n✅ ¡Descarga meteorológica completada con éxito!")

# --- 3. MÓDULO: MINERO DE NOTICIAS ---
def procesar_noticias(url):
    print("\n📰 Detectado: Portal de Noticias.")
    print(f"Analizando el sitio: {url}")
    print("Iniciando algoritmo de extracción histórica (1 año)...")
    
    # Crear carpeta para noticias
    ruta_noticias = os.path.join(carpeta_base, "noticias")
    os.makedirs(ruta_noticias, exist_ok=True)
    
    # Simular que el código está paginando por 12 meses
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    total_noticias = 0
    for mes in meses:
        print(f"  -> Raspando titulares de {mes} 2025...")
        # Aquí iría la lógica compleja de paginación del sitio de noticias
        time.sleep(0.5) 
        total_noticias += 150 # Simulamos que sacamos 150 noticias por mes
        
    print(f"\n✅ ¡Extracción completada! Se minaron aprox. {total_noticias} noticias del último año.")

# --- 4. CEREBRO CENTRAL (El Enrutador) ---
def iniciar_programa():
    print("="*50)
    print("  MINERO DE DATOS AUTOMÁTICO v2.0")
    print("="*50)
    
    while True:
        url = input("\n🔗 Pega el link a minar (o escribe 'salir' para terminar): ").strip().lower()
        
        if url == 'salir':
            print("Apagando el sistema. ¡Hasta pronto!")
            break
            
        # Lógica de detección de página
        if "senamhi" in url or "clima" in url:
            procesar_clima()
        
        elif "noticia" in url or "comercio" in url or "republica" in url or "rpp" in url:
            procesar_noticias(url)
            
        else:
            print("⚠️ Enlace no reconocido. Asegúrate de que sea un portal de noticias o de clima soportado.")

# Ejecutar el programa
if __name__ == "__main__":
    iniciar_programa()