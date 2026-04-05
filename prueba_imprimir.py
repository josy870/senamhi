import os
import time
import pandas as pd
from datetime import datetime, timedelta

# --- 1. BASE DE DATOS GEOGRÁFICA (Resumida para el ejemplo) ---
# --- BASE DE DATOS GEOGRÁFICA (VERSIÓN EXTENDIDA) ---
geografia_peru = {
    "amazonas": {
        "chachapoyas": ["chachapoyas", "asuncion", "balsas", "cheto", "chiliquin", "chuquibamba", "granada", "huancas", "la jalca", "leymebamba", "levanto", "magdalena", "mariscal castilla", "molinopampa", "montevideo", "olleros", "quinjalca", "san francisco de daguas", "san isidro de maino", "soloco", "sonche"],
        "bagua": ["bagua", "aramango", "copallin", "el parco", "imaza", "la peca"],
        "bongara": ["jumbilla", "chisquilla", "churuja", "corosha", "cuispes", "florida", "jazan", "recta", "san carlos", "shipasbamba", "valera", "yambrasbamba"],
        "condorcanqui": ["nieva", "el cenepa", "rio santiago"],
        "luya": ["lamud", "camporredondo", "cocabamba", "colcamar", "conila", "inguilpata", "longuita", "lonya chico", "luya", "luya viejo", "maria", "ocalli", "ocumal", "pisuquia", "providencia", "san cristobal", "san francisco del yeso", "san jeronimo", "san juan de lopecancha", "santa catalina", "santo tomas", "tingo", "trita"],
        "rodriguez de mendoza": ["san nicolas", "chirimoto", "cochamal", "huambo", "limabamba", "longar", "mariscal benavides", "milpuc", "omia", "santa rosa", "totora", "vista alegre"],
        "utcubamba": ["bagua grande", "cajaruro", "cumba", "el milagro", "jamalca", "lonya grande", "yamon"]
    },
    "ancash": {
        "aija": ["aija", "coris", "huacllan", "la merced", "succha"],
        "antonio raymondi": ["llamellin", "aczo", "chaccho", "chingas", "mirgas", "san juan de rontoy"],
        "asuncion": ["chacas", "acochaca"],
        "bolognesi": ["chiquian", "abelardo galvez", "aquia", "cajacay", "canis", "colquioc", "huallanca", "huasta", "huayllacayan", "la primavera", "mangas", "pacllon", "san miguel de corpanqui", "ticllos", "antonio raymondi"],
        "carhuaz": ["carhuaz", "acopampa", "amashca", "anta", "ataquero", "marcara", "pariahuanca", "san miguel de aco", "shilla", "tinco", "yungar"],
        "carlos fermin fitzcarrald": ["san luis", "san nicolas", "yauya"],
        "casma": ["casma", "buena vista alta", "comandante noel", "yautan"],
        "corongo": ["corongo", "aco", "bambas", "cusca", "la pampa", "yanac", "yupan"],
        "huaraz": ["huaraz", "cochabamba", "colcabamba", "huanchay", "independencia", "jangas", "la libertad", "olleros", "pampas grande", "pariacoto", "pira", "tarica"],
        "huari": ["huari", "anra", "cajay", "chavin de huantar", "huacachi", "huacchis", "huachis", "huantar", "masin", "paucas", "ponto", "rahuapampa", "rapayan", "san marcos", "san pedro de chana", "uco"],
        "huarmey": ["huarmey", "cochapeti", "culebras", "huayan", "malvas"],
        "huaylas": ["caraz", "huallanca", "huata", "huaylas", "mato", "pamparomas", "pueblo libre", "santa cruz", "santo toribio", "yuracmarca"],
        "mariscal luzuriaga": ["piscobamba", "casca", "eleazar guzman barron", "fidel olivas escudero", "llama", "llumpa", "lucma", "musga"],
        "ocros": ["ocros", "acas", "cajamarquilla", "carhuapampa", "cochas", "congas", "llipa", "san cristobal de rajan", "san pedro", "santiago de chilcas"],
        "pallasca": ["cabana", "bolognesi", "conchucos", "huacaschuque", "huandoval", "lacabamba", "llapo", "pallasca", "pampas", "santa rosa", "tauca"],
        "pomabamba": ["pomabamba", "huayllan", "quinuabamba", "parobamba"],
        "recuay": ["recuay", "catac", "cotaparaco", "huayllapampa", "llacllin", "marca", "pampas chico", "pararin", "tapacocha", "ticapampa"],
        "santa": ["chimbote", "caceres del peru", "coishco", "macate", "moro", "nepeña", "nuevo chimbote", "samanco", "santa"],
        "sihuas": ["sihuas", "acobamba", "alfonso ugarte", "cashapampa", "chingalpo", "huayllabamba", "quiches", "ragash", "san juan", "sicsibamba"],
        "yungay": ["yungay", "cascapara", "mancos", "matacoto", "quillo", "ranrahirca", "shupluy", "yanama"]
    },
    "apurimac": {
        "abancay": ["abancay", "chacoche", "circa", "curahuasi", "huanipaca", "lambrama", "pichirhua", "san pedro de cachora", "tamburco"],
        "andahuaylas": ["andahuaylas", "andarapa", "chiara", "huancarama", "huancaray", "huayana", "jose maria arguedas", "kaquiabamba", "kishuara", "pacobamba", "pacucha", "pampachiri", "pomacocha", "san antonio de cachi", "san jeronimo", "san miguel de chaccrampa", "santa maria de chicmo", "talavera", "tumay huaraca", "turpo"],
        "antabamba": ["antabamba", "el oro", "huaquirca", "juan espinoza medrano", "oropesa", "pachaconas", "sabaino"],
        "aymaraes": ["chalhuanca", "capaya", "caraybamba", "chapimarca", "colcabamba", "cotaruse", "ihuayllo", "justo apu sahuaraura", "lucre", "pocohuanca", "san juan de chacña", "sañayca", "soraya", "tapairihua", "tintay"],
        "cotabambas": ["tambobamba", "chalhuahuacho", "cotabambas", "coyllurqui", "haquira", "mara"],
        "chincheros": ["chincheros", "anco-huallo", "cocharcas", "el porvenir", "huaccana", "los chankas", "ocobamba", "ongoy", "ranracancha", "rocchacc", "uranmarca"],
        "grau": ["chuquibambilla", "curasco", "curpahuasi", "gamarra", "huayllati", "mamara", "micaela bastidas", "pataypampa", "progreso", "san antonio", "santa", "turpay", "vilcabamba", "virundo"]
    },
   "arequipa": {
        "arequipa": ["arequipa", "alto selva alegre", "cayma", "cerro colorado", "characato", "chiguata", "jacobo hunter", "la joya", "mariano melgar", "miraflores", "molleabaya", "paucarpata", "pocsi", "polobaya", "quequeña", "sabandia", "sachaca", "san juan de siguas", "san juan de tarucani", "santa isabel de siguas", "santa rita de siguas", "socabaya", "tiabaya", "uchumayo", "vitor", "yanahuara", "yarabamba", "yura"],
        "camana": ["camana", "jose maria quimper", "mariano nicolas valcarcel", "mariscal caceres", "nicolas de pierola", "ocoña", "quilca", "samuel pastor"],
        "caraveli": ["caraveli", "acari", "atico", "atiquipa", "bella union", "cahuacho", "chala", "chaparra", "huanuhuanu", "jaqui", "lomas", "quicacha", "yauca"],
        "castilla": ["aplao", "andagua", "ayo", "chachas", "chilcaymarca", "choco", "huancarqui", "machaguay", "orcopampa", "pampacolca", "piñon", "uraca", "uñon", "viraco"],
        "caylloma": ["chivay", "achoma", "cabanaconde", "callalli", "caylloma", "coporaque", "huambo", "huanca", "ichupampa", "lari", "lluta", "maca", "madrigal", "majes", "san antonio de chuca", "sibayo", "tapay", "tisco", "tuti", "yanque"],
        "condesuyos": ["chuquibamba", "andaray", "cayarani", "chichas", "iray", "rio grande", "salamanca", "yanaquihua"],
        "islay": ["mollendo", "cocachacra", "dean valdivia", "islay", "mejia", "punta de bombon"],
        "la union": ["cotahuasi", "alca", "charcana", "huaynacotas", "pampamarca", "puyca", "quechualla", "sayla", "tauria", "tomepampa", "toro"]
    },
    "ayacucho": {
        "cangallo": ["cangallo", "chuschi", "los morochucos", "maria parado de bellido", "paras", "totos"],
        "huamanga": ["ayacucho", "acocro", "acos vinchos", "andres avelino caceres dorregaray", "carmen alto", "chiara", "jesus nazareno", "ocros", "pacaycasa", "quinua", "san jose de ticllas", "san juan bautista", "santiago de pischa", "socos", "tambillo", "vinchos"],
        "huanca sancos": ["sancos", "carapo", "sacsamarca", "santiago de lucanamarca"],
        "huanta": ["huanta", "ayahuanco", "chaca", "canayre", "huamanguilla", "iguain", "llochegua", "luricocha", "pucacolpa", "santillana", "sivia", "uchuraccay"],
        "la mar": ["san miguel", "anchihuay", "anco", "ayna", "chilcas", "chungui", "luis carranza", "oronccoy", "samugari", "santa rosa", "tambo"],
        "lucanas": ["puquio", "aucara", "cabana", "carmen salcedo", "chaviña", "chipao", "huac-huas", "laramate", "leoncio prado", "llauta", "lucanas", "ocaña", "otoca", "saisa", "san cristobal", "san juan", "san pedro", "san pedro de palco", "sancos", "santa ana de huaycahuacho", "totora"],
        "parinacochas": ["coracora", "chumpi", "coronel castañeda", "pacapausa", "pullo", "puyusca", "san francisco de ravacayco", "upahuacho"],
        "paucar del sara sara": ["pausa", "colta", "corculla", "lampa", "marcabamba", "oyolo", "pararca", "san javier de alpabamba", "san jose de ushua", "sara sara"],
        "sucre": ["querobamba", "belen", "chalcos", "chilcayoc", "huacaña", "morcolla", "paico", "san pedro de larcay", "san salvador de quije", "santiago de paucaray", "soras"],
        "victor fajardo": ["huancapi", "alcamenca", "apongo", "asquipata", "canaria", "cayara", "colca", "huamanquiquia", "huancaraylla", "huaya", "sarhua", "vilcanchos"],
        "vilcas huaman": ["vilcas huaman", "accomarca", "carhuanca", "concepcion", "huambalpa", "independencia", "saurama", "vischongo"]
    },
    "cajamarca": {
        "cajabamba": ["cajabamba", "cachachi", "condebamba", "sitacocha"],
        "cajamarca": ["cajamarca", "asuncion", "baños del inca", "chetilla", "cospan", "encañada", "jesus", "llacanora", "magdalena", "matara", "namora", "san juan"],
        "celendin": ["celendin", "chumuch", "cortegana", "huasmin", "jorge chavez", "jose galvez", "la libertad de pallan", "miguel iglesias", "oxamarca", "sorochuco", "sucre", "utco"],
        "chota": ["chota", "anguia", "chadin", "chalamarca", "chiguirip", "chimban", "choropampa", "cochabamba", "conchan", "huambos", "lajas", "llallan", "miracosta", "paccha", "pion", "querocoto", "san juan de licupis", "tacabamba", "tocmoche"],
        "contumaza": ["contumaza", "chilete", "cupisnique", "guzmango", "san benito", "santa cruz de toled", "tantarica", "yonan"],
        "cutervo": ["cutervo", "callayuc", "choros", "cujillo", "la ramada", "pimpingos", "querocotillo", "san andres de cutervo", "san juan de cutervo", "san luis de lucma", "santa cruz", "santo domingo de la capilla", "santo tomas", "socota", "toribio casanova"],
        "hualgayoc": ["bambamarca", "chugur", "hualgayoc"],
        "jaen": ["jaen", "bellavista", "chontali", "colasay", "huabal", "las pirias", "pomahuaca", "pucara", "sallique", "san felipe", "san jose del alto", "santa rosa"],
        "san ignacio": ["san ignacio", "chirinos", "huarango", "la coipa", "namballe", "san jose de lourdes", "tabaconas"],
        "san marcos": ["pedro galvez", "chancay", "eduardo villanueva", "gregorio pita", "ichocan", "jose manuel quiroz", "jose sabogal"],
        "san miguel": ["san miguel", "bolivar", "calquis", "catilluc", "el prado", "florida", "llapa", "nanchoc", "niepos", "san gregorio", "san silvestre de cochan", "tongod", "union agua blanca"],
        "san pablo": ["san pablo", "san bernardino", "san luis", "tumbaden"],
        "santa cruz": ["santa cruz", "andabamba", "catache", "chancaybaños", "la esperanza", "ninabamba", "pulan", "saucepampa", "sexi", "uticyacu", "yauyucan"]
    },
    "callao": {
        "callao": ["callao", "bellavista", "carmen de la legua reynoso", "la perla", "la punta", "ventanilla", "mi peru"]
    },
    "cusco": {
        "acomayo": ["acomayo", "acopia", "acos", "mosoc llacta", "pomacanchi", "rondocan", "sangarara"],
        "anta": ["anta", "ancahuasi", "cachimayo", "chinchaypujio", "huarocondo", "limatambo", "mollepata", "pucyura", "zurite"],
        "calca": ["calca", "coya", "lamay", "lares", "pisac", "san salvador", "taray", "yanatile"],
        "canas": ["yanaoca", "checca", "kunturkanki", "langui", "layo", "pampamarca", "quehue", "tupac amaru"],
        "canchis": ["sicuani", "checacupe", "combapata", "marangani", "pitumarca", "san pablo", "san pedro", "tinta"],
        "chumbivilcas": ["santo tomas", "capacmarca", "chamaca", "colquemarca", "livitaca", "llusco", "quiñota", "velille"],
        "cusco": ["cusco", "ccorcca", "poroy", "san jeronimo", "san sebastian", "santiago", "saylla", "wanchaq"],
        "espinar": ["yauri", "alto pichigua", "condoroma", "coporaque", "ocoruro", "pallpata", "pichigua", "suyckutambo"],
        "la convencion": ["santa ana", "cielo punco", "echarate", "huayopata", "incahuasi", "kimbiri", "kumpirushiato", "manitea", "maranura", "megantoni", "ocobamba", "pichari", "quellouno", "santa teresa", "union ashaninka", "vilcabamba", "villa kintiarina", "villa virgen"],
        "paruro": ["paruro", "accha", "ccapi", "colcha", "huanoquite", "omacha", "paccaritambo", "pillpinto", "yaurisque"],
        "paucartambo": ["paucartambo", "caicay", "challabamba", "colquepata", "huancarani", "kosñipata"],
        "quispicanchi": ["urcos", "andahuaylillas", "camanti", "ccarhuayo", "ccatca", "cusipata", "huaro", "lucre", "marcapata", "ocongate", "oropesa", "quiquijana"],
        "urubamba": ["urubamba", "chinchero", "huayllabamba", "machupicchu", "maras", "ollantaytambo", "yucay"]
    },
    "huancavelica": {
        "acobamba": ["acobamba", "andabamba", "anta", "caja", "marcas", "paucara", "pomacocha", "rosario"],
        "angaraes": ["lircay", "anchonga", "callanmarca", "ccochaccasa", "chincho", "congalla", "huanca-huanca", "huayllay grande", "julcamarca", "san antonio de antaparco", "santo tomas de pata", "secclla"],
        "castrovirreyna": ["castrovirreyna", "arma", "aurahua", "capillas", "chupamarca", "cocas", "huachos", "huamatambo", "mollepampa", "san juan", "santa ana", "tantara", "ticrapo"],
        "churcampa": ["churcampa", "anco", "chinchihuasi", "cosme", "el carmen", "la merced", "locroja", "pachamarca", "paucarbamba", "san miguel de mayocc", "san pedro de coris"],
        "huancavelica": ["huancavelica", "acobambilla", "acoria", "ascencion", "conayca", "cuenca", "huachocolpa", "huayllahuara", "izcuchaca", "laria", "manta", "mariscal caceres", "moya", "nuevo occoro", "palca", "pilchaca", "vilca", "yauli"],
        "huaytara": ["huaytara", "ayavi", "cordova", "huayacundo arma", "laramarca", "ocoyo", "pilpichaca", "querco", "quito-arma", "san antonio de cusicancha", "san francisco de sangayaico", "san isidro", "santiago de chocorvos", "santiago de quirahuara", "santo domingo de capillas", "tambo"],
        "tayacaja": ["pampas", "acostambo", "acraquia", "ahuaycha", "andaymarca", "colcabamba", "daniel hernandez", "huachocolpa", "huaribamba", "ñahuimpuquio", "pazos", "pichos", "quishuar", "roble", "salcabamba", "salcahuasi", "san marcos de rocchac", "surcubamba", "tintay puncu"]
    }, 
    "huanuco": {
        "ambo": ["ambo", "cayna", "colpas", "conchamarca", "huacar", "san francisco", "san rafael", "tomay kichwa"],
        "dos de mayo": ["la union", "chuquis", "marias", "pachas", "quivilla", "ripan", "shunqui", "sillapata", "yanas"],
        "huacaybamba": ["huacaybamba", "canchabamba", "cochabamba", "pinra"],
        "huamalies": ["llata", "arancay", "chavin de pariarca", "jacas grande", "jircan", "miraflores", "monzon", "punchao", "puños", "singa", "tantamayo"],
        "huanuco": ["huanuco", "amarilis", "chinchao", "churubamba", "margos", "pillco marca", "quisqui", "san francisco de cayran", "san pablo de pillao", "san pedro de chaulan", "santa maria del valle", "yacus", "yarumayo"],
        "lauricocha": ["jesus", "baños", "jivia", "queropalca", "rondos", "san francisco de asis", "san miguel de cauri"],
        "leoncio prado": ["rupa-rupa", "castillo grande", "daniel alomia robles", "hermilio valdizan", "jose crespo y castillo", "luyando", "mariano damaso beraun", "pucayacu", "pueblo nuevo", "santo domingo de anda"],
        "marañon": ["huacrachuco", "cholon", "la morada", "san buenaventura", "santa rosa de alto yanajanca"],
        "pachitea": ["panao", "chaglla", "molino", "umari"],
        "puerto inca": ["puerto inca", "codo del pozuzo", "honoria", "tournavista", "yuyapichis"],
        "yarowilca": ["chavinillo", "aparicio pomares", "cahuac", "chacabamba", "jacas chico", "obas", "pampamarca"]
    },
    "ica": {
        "chincha": ["chincha alta", "alto laran", "chavin", "chincha baja", "el carmen", "grocio prado", "pueblo nuevo", "san juan de yanac", "san pedro de huacarpana", "sunampe", "tambo de mora"],
        "ica": ["ica", "la tinguiña", "los aquijes", "ocucaje", "pachacutec", "parcona", "pueblo nuevo", "salas", "san jose de los molinos", "san juan bautista", "santiago", "subtanjalla", "tate", "yauca del rosario"],
        "nasca": ["nasca", "changuillo", "el ingenio", "marcona", "vista alegre"],
        "palpa": ["palpa", "llipata", "rio grande", "santa cruz", "tibillo"],
        "pisco": ["pisco", "huancano", "humay", "independencia", "paracas", "san andres", "san clemente", "tupac amaru inca"]
    },
    "junin": {
        "chanchamayo": ["chanchamayo", "perene", "pichanaqui", "san luis de shuaro", "san ramon", "vitoc"],
        "chupaca": ["chupaca", "ahuac", "chongos bajo", "huachac", "huamancaca chico", "san juan de iscos", "san juan de jarpa", "tres de diciembre", "yanacancha"],
        "concepcion": ["concepcion", "aco", "andamarca", "chambara", "cochas", "comas", "heroinas toledo", "manzanares", "mariscal castilla", "matahuasi", "mito", "nueve de julio", "orcotuna", "san jose de quero", "santa rosa de ocopa"],
        "huancayo": ["huancayo", "carhuacallanga", "chacapampa", "chicche", "chilca", "chongos alto", "chupuro", "colca", "cullhuas", "el tambo", "huacrapuquio", "hualhuas", "huancan", "huasicancha", "huayucachi", "ingenio", "pariahuanca", "pilcomayo", "pucara", "quichuay", "quilcas", "san agustin", "san jeronimo de tunan", "santo domingo de acobamba", "saño", "sapallanga", "sicaya", "viques"],
        "jauja": ["jauja", "apata", "arolla", "ataura", "canchayllo", "curicaca", "el mantaro", "huamali", "huaripampa", "huertas", "janjaillo", "julcan", "leonor ordoñez", "llocllapampa", "marco", "masma", "masma chicche", "molinos", "monobamba", "muqui", "muquiyauyo", "paca", "paccha", "pancan", "parco", "pomacancha", "ricran", "san lorenzo", "san pedro de chunan", "sincos", "tunan marca", "yauli", "yauyos"],
        "junin": ["junin", "carhuamayo", "ondores", "ulcumayo"],
        "satipo": ["satipo", "coviriali", "llaylla", "mazamari", "pampa hermosa", "pangoa", "rio negro", "rio tambo", "vizcatan del ene"],
        "tarma": ["tarma", "acobamba", "huaricolca", "huasahuasi", "la union", "palca", "palcamayo", "san pedro de cajas", "tapo"],
        "yauli": ["la oroya", "chacapalpa", "huay-huay", "marcapomacocha", "morococha", "paccha", "santa barbara de carhuacayan", "santa rosa de sacco", "suitucancha", "yauli"]
    },
    "la libertad": {
        "ascope": ["ascope", "casa grande", "chicama", "chocope", "magdalena de cao", "paijan", "razuri", "santiago de cao"],
        "bolivar": ["bolivar", "bambamarca", "condormarca", "longotea", "uchumarca", "ucuncha"],
        "chepen": ["chepen", "pacanga", "pueblo nuevo"],
        "gran chimu": ["cascas", "lucma", "marmot", "sayapullo"],
        "julcan": ["julcan", "calamarca", "carabamba", "huaso"],
        "otuzco": ["otuzco", "agallpampa", "charat", "huaranchal", "la cuesta", "mache", "paranday", "salpo", "sinsicap", "usquil"],
        "pacasmayo": ["san pedro de lloc", "guadalupe", "jequetepeque", "pacasmayo", "san jose"],
        "pataz": ["tayabamba", "buldibuyo", "chillia", "huancaspata", "huaylillas", "huayo", "ongon", "parcoy", "pataz", "pias", "santiago de challas", "taurija", "urpay"],
        "sanchez carrion": ["huamachuco", "chugay", "cochorco", "curgos", "marcabal", "sanagoran", "sarin", "sartimbamba"],
        "santiago de chuco": ["santiago de chuco", "angasmarca", "cachicadan", "mollebamba", "mollepata", "quiruvilca", "santa cruz de chuca", "sitabamba"],
        "trujillo": ["trujillo", "el porvenir", "florencia de mora", "huanchaco", "la esperanza", "laredo", "moche", "poroto", "salaverry", "simbal", "victor larco herrera"],
        "viru": ["viru", "chao", "guadalupito"]
    },
    "lambayeque": {
        "chiclayo": ["chiclayo", "cayalti", "chongoyape", "eten", "eten puerto", "jose leonardo ortiz", "la victoria", "lagunas", "monsefu", "nueva arica", "oyotun", "patapo", "picsi", "pimentel", "pomalca", "pucala", "reque", "santa rosa", "tuman", "zaña"],
        "ferreñafe": ["ferreñafe", "cañaris", "incahuasi", "mesones muro", "pitipo", "pueblo nuevo"],
        "lambayeque": ["lambayeque", "chochope", "illimo", "jayanca", "mochumi", "morrope", "motupe", "olmos", "pacora", "salas", "san jose", "tucume"]
    },
   "lima": {
        "barranca": ["barranca", "paramonga", "pativilca", "puerto supe", "supe"],
        "cajatambo": ["cajatambo", "copa", "gorgor", "huancapon", "manas"],
        "canta": ["canta", "arahuay", "huamantanga", "huaros", "lachaqui", "san buenaventura", "santa rosa de quives"],
        "cañete": ["san vicente de cañete", "asia", "calango", "cerro azul", "chilca", "coayllo", "imperial", "lunahuana", "mala", "nuevo imperial", "pacaran", "quilmana", "san antonio", "san luis", "santa cruz de flores", "zuñiga"],
        "huaral": ["huaral", "atavillos alto", "atavillos bajo", "aucallama", "chancay", "ihuari", "lampian", "pacaraos", "san miguel de acos", "santa cruz de andamarca", "sumbilca", "veintisiete de noviembre"],
        "huarochiri": ["matucana", "antioquia", "callahuanca", "carampoma", "chicla", "cuenca", "huachupampa", "huanza", "huarochiri", "lahuaytambo", "langa", "laraos", "mariatana", "ricardo palma", "san andres de tupicocha", "san antonio", "san bartolome", "san damian", "san juan de iris", "san juan de tantaranche", "san lorenzo de quinti", "san mateo", "san mateo de otao", "san pedro de casta", "san pedro de huancayre", "sangallaya", "santa cruz de cocachacra", "santa eulalia", "santiago de anchucaya", "santiago de tuna", "santo domingo de los olleros", "surco"],
        "huaura": ["huacho", "ambar", "caleta de carquin", "checras", "hualmay", "huaura", "leoncio prado", "paccho", "santa leonor", "santa maria", "sayan", "vegueta"],
        "lima": ["lima cercado", "ancon", "ate", "barranco", "breña", "carabayllo", "chaclacayo", "chorrillos", "cieneguilla", "comas", "el agustino", "independencia", "jesus maria", "la molina", "la victoria", "lince", "los olivos", "lurigancho", "lurin", "magdalena del mar", "miraflores", "pachacamac", "pucusana", "pueblo libre", "puente piedra", "punta hermosa", "punta negra", "rimac", "san bartolo", "san borja", "san isidro", "san juan de lurigancho", "san juan de miraflores", "san luis", "san martin de porres", "san miguel", "santa anita", "santa maria del mar", "santa rosa", "surco", "surquillo", "villa el salvador", "villa maria del triunfo"],
        "oyon": ["oyon", "andajes", "caujul", "cochamarca", "navan", "pachangara"],
        "yauyos": ["yauyos", "alis", "ayauca", "ayaviri", "azangaro", "cacra", "carania", "catahuasi", "chocos", "cochas", "colonia", "hongos", "huampara", "huancaya", "huangascar", "huantan", "huañec", "laraos", "lincha", "madean", "miraflores", "omas", "putinza", "quinches", "quinocay", "san joaquin", "san pedro de pilas", "tanta", "tauripampa", "tomas", "tupe", "viñac", "vitis"]
    },
    "loreto": {
        "alto amazonas": ["yurimaguas", "balsapuerto", "jeberos", "lagunas", "santa cruz", "teniente cesar lopez rojas"],
        "datem del marañon": ["barranca", "cahuapanas", "manseriche", "morona", "pastaza", "andoas"],
        "loreto": ["nauta", "parinari", "tigre", "trompeteros", "urarinas"],
        "mariscal ramon castilla": ["ramon castilla", "pebas", "yavari", "san pablo"],
        "maynas": ["iquitos", "alto nanay", "belen", "fernando lores", "indiana", "las amazonas", "mazan", "napo", "punchana", "san juan bautista", "torres causana"],
        "putumayo": ["putumayo", "rosa panduro", "teniente manuel clavero", "yaguas"],
        "requena": ["requena", "alto tapiche", "capelo", "emilio san martin", "jenaro herrera", "maquia", "puinahua", "saquena", "soplin", "tapiche", "yaquerana"],
        "ucayali": ["contamana", "inahuaya", "padre marquez", "pampa hermosa", "sarayacu", "vargas guerra"]
    },
    "madre de dios": {
        "manu": ["manu", "fitzcarrald", "huepetuhe", "madre de dios"],
        "tahuamanu": ["iñapari", "iberia", "tahuamanu"],
        "tambopata": ["tambopata", "inambari", "laberinto", "las piedras"]
    },
    "moquegua": {
        "general sanchez cerro": ["omate", "chojata", "coalaque", "ichuña", "la capilla", "lloque", "matalaque", "puquina", "quinistaquillas", "ubinas", "yunga"],
        "ilo": ["ilo", "el algarrobal", "pacocha"],
        "mariscal nieto": ["moquegua", "carumas", "cuchumbaya", "samegua", "san cristobal", "torata"]
    },
    "pasco": {
        "daniel alcides carrion": ["yanahuanca", "chacayan", "goyllarisquizga", "paucar", "san pedro de pillao", "santa ana de tusi", "tapuc", "vilcabamba"],
        "oxapampa": ["oxapampa", "chontabamba", "constitucion", "huancabamba", "palcazu", "pozuzo", "puerto bermudez", "villa rica"],
        "pasco": ["chaupimarca", "huachon", "huariaca", "huayllay", "ninacaca", "pallanchacra", "paucartambo", "san francisco de asis de yarusyacan", "simon bolivar", "ticlacayan", "tinyahuarco", "vicco", "yanacancha"]
    },
    "piura": {
        "ayabaca": ["ayabaca", "frias", "jilili", "lagunas", "montero", "pacaipampa", "paimas", "sapillica", "sicchez", "suyo"],
        "huancabamba": ["huancabamba", "canchaque", "el carmen de la frontera", "huarmaca", "lalaquiz", "san miguel de el faique", "sondor", "sondorillo"],
        "morropon": ["chulucanas", "buenos aires", "chalaco", "la matanza", "morropon", "salitral", "san juan de bigote", "santa catalina de mossa", "santo domingo", "yamango"],
        "paita": ["paita", "amotape", "arenal", "colan", "la huaca", "tamarindo", "vichayal"],
        "piura": ["piura", "castilla", "catacaos", "cura mori", "el tallan", "la arena", "la union", "las lomas", "tambogrande", "veintiseis de octubre"],
        "sechura": ["sechura", "bellavista de la union", "bernal", "cristo nos valga", "rinconada llicuar", "vice"],
        "sullana": ["sullana", "bellavista", "ignacio escudero", "lancones", "marcavelica", "miguel checa", "querecotillo", "salitral"],
        "talara": ["pariñas", "el alto", "la brea", "lobitos", "los organos", "mancora"]
    },
    "puno": {
        "puno": ["puno", "acora", "amantaní", "atuncolla", "capachica", "chucuito", "coata", "huata", "mañazo", "paucarcolla", "pichacani", "plateria", "san antonio", "tiquillaca", "vilque"],
        "azangaro": ["azangaro", "achaya", "arapa", "asillo", "caminaca", "chupa", "jose domingo choquehuanca", "muñani", "potoni", "samán", "san anton", "san jose", "san juan de salinas", "santiago de pupuja", "tirapata"],
        "carabaya": ["macusani", "ayapata", "coasa", "corani", "crucero", "ituata", "ollachea", "san gaban", "usicayos"],
        "chucuito": ["juli", "desaguadero", "huacullani", "kelluyo", "pisacoma", "pomata", "zepita"],
        "el collao": ["ilave", "capazo", "pilcuyo", "santa rosa", "conduriri"],
        "huancane": ["huancane", "cojata", "huatasani", "inchupalla", "pusi", "rosaspata", "taraco", "vilque chico"],
        "lampa": ["lampa", "cabanilla", "calapuja", "nicasio", "ocuviri", "palca", "paratia", "pucara", "santa lucia", "vilavila"],
        "melgar": ["ayaviri", "antauta", "cupi", "llalli", "macari", "nuñoa", "orurillo", "santa rosa", "umachiri"],
        "moho": ["moho", "conima", "huayrapata", "tilali"],
        "san antonio de putina": ["putina", "ananea", "pedro vilca apaza", "quilcapuncu", "sina"],
        "san roman": ["juliaca", "cabana", "cabanillas", "caracoto"],
        "sandia": ["sandia", "cuyocuyo", "phara", "patambuco", "quiaca", "san juan del oro", "san pedro de putina punco", "alto inambari"],
        "yunguyo": ["yunguyo", "anapia", "copani", "cuturapi", "ollaraya", "tinicachi", "unicachi"]
    },
    "san martin": {
        "bellavista": ["bellavista", "alto biavo", "bajo biavo", "huallaga", "san pablo", "san rafael"],
        "el dorado": ["san jose de sisa", "agua blanca", "san martin", "santa rosa", "shatoja"],
        "huallaga": ["saposoa", "alto saposoa", "el eslabon", "piscoyacu", "sacanche", "tingo de saposoa"],
        "lamas": ["lamas", "alonso de alvarado", "barranquita", "caynarachi", "cuñumbuqui", "pinto recodo", "rumisapa", "san roque de cumbaza", "shanao", "tabalosos", "zapatero"],
        "mariscal caceres": ["juanjui", "campanilla", "huicungo", "pachiza", "pajarillo"],
        "moyobamba": ["moyobamba", "calzada", "habana", "jepelacio", "soritor", "yantalo"],
        "picota": ["picota", "buenos aires", "caspizapa", "pilluana", "pucacaca", "san cristobal", "san hilarion", "shamboyacu", "tingo de ponasa", "tres unidos"],
        "rioja": ["rioja", "awajun", "elias soplin vargas", "nueva cajamarca", "pardo miguel", "posic", "san fernando", "yuracyacu"],
        "san martin": ["tarapoto", "alberto leveau", "cacatachi", "chazuta", "chipurana", "el porvenir", "huimbayoc", "juan guerra", "la banda de shilcayo", "morales", "papaplaya", "san antonio", "sauce", "shapaja"],
        "tocache": ["tocache", "nuevo progreso", "polvora", "santa lucia", "shunte", "uchiza"]
    },
    "tacna": {
        "candarave": ["candarave", "cairani", "camilaca", "curibaya", "huanuara", "quilahuani"],
        "jorge basadre": ["locumba", "ilabaya", "ite"],
        "tacna": ["tacna", "alto de la alianza", "calana", "ciudad nueva", "coronel gregorio albarracin lanchipa", "inclan", "la yarada los palos", "pachia", "palca", "pocollay", "sama"],
        "tarata": ["tarata", "estique", "estique pampa", "heroes albarracin", "sitajara", "susapaya", "tarucachi", "ticaco"]
    },
    "tumbes": {
        "contralmirante villar": ["zorritos", "canoas de punta sal", "casitas"],
        "tumbes": ["tumbes", "corrales", "la cruz", "pampas de hospital", "san jacinto", "san juan de la virgen"],
        "zarumilla": ["zarumilla", "aguas verdes", "matapalo", "papayal"]
    },
    "ucayali": {
        "atalaya": ["raimondi", "sepahua", "tahuania", "yurua"],
        "coronel portillo": ["calleria", "campoverde", "iparia", "manantay", "masisea", "nueva requena", "yarinacocha"],
        "padre abad": ["padre abad", "alexander von humboldt", "boqueron", "curimana", "huipoca", "irazola", "neshuya"],
        "purus": ["purus"]
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