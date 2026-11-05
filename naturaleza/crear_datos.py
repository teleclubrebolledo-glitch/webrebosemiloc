#!/usr/bin/env python3
"""Fauna y flora de Rebolledo de la Torre y su entorno (Geoparque Las Loras, páramos del norte de Burgos). Datos orientativos escritos a mano.
★ = especie citada por fuentes del Geoparque Las Loras (aves de los cortados: buitre leonado y negro, águila real, halcón peregrino, cuervo, chova piquirroja, grajilla, corneja, urraca, agateador;
bosques de quejigo, melojo y coscoja). El resto son especies propias de la meseta norte y de los cortados calizos: contrastar con guías y con observaciones locales."""
import json
from pathlib import Path
SALIDA = Path(__file__).parent / "datos.json"

# nombre, científico, grupo, meses de presencia, dónde, cómo reconocerla, dato, estrella
AVES = [
 ("Buitre leonado", "Gyps fulvus", "rapaz", "1-12", "Cortados calizos; planea sobre los páramos", "Grande (2,5 m de envergadura), pardo claro, cuello claro y alas con bordes negros", "Come carroña y es clave para limpiar el campo. Anida en repisas de roca.", 1),
 ("Buitre negro", "Aegypius monachus", "rapaz", "1-12", "Cortados y bosques cercanos", "Aún mayor (hasta 3 m), casi negro, cabeza clara", "Raro y protegido; sus colonias son muy sensibles a las molestias.", 1),
 ("Alimoche", "Neophron percnopterus", "rapaz", "3-9", "Cortados y barrancos", "Blanco con puntas de ala negras, cara amarilla, cola en cuña", "Viene de África en primavera y se marcha a final del verano.", 0),
 ("Águila real", "Aquila chrysaetos", "rapaz", "1-12", "Cortados, páramos y bosque", "Muy grande, marrón oscuro, nuca dorada", "Cada pareja controla un territorio enorme.", 1),
 ("Halcón peregrino", "Falco peregrinus", "rapaz", "1-12", "Cortados", "Dorso gris azulado, pecho claro barrado, «bigotera» negra", "En picado supera los 300 km/h: el animal más rápido del planeta.", 1),
 ("Cernícalo vulgar", "Falco tinnunculus", "rapaz", "1-12", "Campos, pueblos y campanarios", "Pequeño, rojizo, se queda quieto en el aire «cerneándose»", "Caza topillos en los cultivos.", 0),
 ("Milano real", "Milvus milvus", "rapaz", "10-3", "Campos abiertos", "Cola larga muy ahorquillada, cabeza clara", "Invernan muchos en la meseta; se junta con los buitres en las carroñas.", 0),
 ("Aguilucho cenizo", "Circus pygargus", "rapaz", "4-8", "Campos de cereal", "Macho gris con rayas negras en el ala; hembra parda", "Anida en el suelo, entre el trigo: se protegen los nidos antes de cosechar.", 0),
 ("Cuervo", "Corvus corax", "córvido", "1-12", "Cortados y páramos", "El mayor córvido, negro, cola en cuña, grazna grave", "Inteligente y longevo.", 1),
 ("Chova piquirroja", "Pyrrhocorax pyrrhocorax", "córvido", "1-12", "Cortados y pueblos de piedra", "Negra con pico y patas rojos", "Vuela en bandos acrobáticos; anida en grietas y torres.", 1),
 ("Grajilla", "Coloeus monedula", "córvido", "1-12", "Pueblos, iglesias y cortados", "Pequeña, negra con nuca gris y ojo claro", "Muy sociable; anida en campanarios y tejados.", 1),
 ("Corneja negra", "Corvus corone", "córvido", "1-12", "Campos y pueblos", "Negra, pico fuerte, grazna seco", "Lista y oportunista.", 1),
 ("Urraca", "Pica pica", "córvido", "1-12", "Campos, setos y pueblos", "Blanco y negro con cola larga y reflejos azules", "Sus nidos de ramas, con cúpula, se ven en los árboles.", 1),
 ("Arrendajo", "Garrulus glandarius", "córvido", "1-12", "Robledales y encinares", "Pardo rosado con alas azules y blancas", "Entierra bellotas y así siembra robles.", 0),
 ("Cigüeña blanca", "Ciconia ciconia", "ave de pueblo", "2-8", "Campanarios y postes", "Blanca con alas negras y pico y patas rojos", "Muchas ya no migran a África y se quedan todo el año.", 0),
 ("Golondrina común", "Hirundo rustica", "ave de pueblo", "3-10", "Cuadras, porches y pueblos", "Cola con largas puntas, vientre claro, garganta rojiza", "Hace el nido de barro bajo los aleros; vuelve cada primavera al mismo sitio.", 0),
 ("Avión roquero", "Ptyonoprogne rupestris", "ave de roca", "3-10", "Cortados", "Pardo, cola cuadrada con manchas blancas", "Nidifica pegado a la pared de roca.", 0),
 ("Vencejo común", "Apus apus", "ave de pueblo", "5-8", "Cielo sobre los pueblos", "Todo oscuro, alas de hoz, chilla en grupos", "Pasa casi toda la vida volando: duerme y come en el aire.", 0),
 ("Abubilla", "Upupa epops", "ave de campo", "3-9", "Linderos, huertas y praderas", "Cresta de plumas, pico curvo, alas listadas", "Su «up-up-up» se oye en primavera.", 0),
 ("Perdiz roja", "Alectoris rufa", "ave de campo", "1-12", "Campos y matorral bajo", "Collar negro, flancos rayados, patas rojas", "Corre más que vuela.", 0),
 ("Codorniz común", "Coturnix coturnix", "ave de campo", "5-9", "Cereal y prados", "Pequeña y críptica, se oye más que se ve («pica-pa-pic»)", "Pasa el invierno en África.", 0),
 ("Alondra común", "Alauda arvensis", "ave de campo", "1-12", "Campos abiertos", "Parda con pequeña cresta; canta sin parar subiendo en vertical", "Su canto es de los más típicos de primavera.", 0),
 ("Calandria", "Melanocorypha calandra", "ave de campo", "1-12", "Cereal y páramo", "Grande, con manchas negras en el cuello", "Típica de los páramos cerealistas.", 0),
 ("Triguero", "Emberiza calandra", "ave de campo", "1-12", "Cultivos, setos y cables", "Gordito y pardo, canta como unas llaves que tintinean", "Se posa en lo más alto de los cables.", 0),
 ("Roquero solitario", "Monticola solitarius", "ave de roca", "1-12", "Cortados", "Macho azul pizarra, hembra parda", "Canta desde lo alto de las rocas.", 0),
 ("Mochuelo común", "Athene noctua", "nocturna", "1-12", "Pueblos, tapias y majadas", "Pequeño, mirada seria, de día se ve en muros", "Cría en huecos de piedra.", 0),
 ("Lechuza común", "Tyto alba", "nocturna", "1-12", "Campanarios y pajares", "Cara en forma de corazón, blanca por debajo", "Un par de lechuzas se come miles de ratones al año.", 0),
 ("Búho real", "Bubo bubo", "nocturna", "1-12", "Cortados y barrancos", "El mayor búho, con «orejas»", "Su «uuh-hu» grave se oye en invierno.", 0),
 ("Pito real", "Picus sharpei", "ave de bosque", "1-12", "Robledales, encinares y fresnedas", "Verde con cabeza roja; ríe al volar", "Busca hormigas en el suelo.", 0),
 ("Petirrojo", "Erithacus rubecula", "ave de bosque", "10-3", "Huertas, setos y bosques", "Pecho y cara naranja", "En invierno se acerca a los huertos y casas.", 0),
]
MAMIFEROS = [
 ("Corzo", "Capreolus capreolus", "Bosques y linderos; al amanecer y al atardecer", "Pequeño ciervo, sin cola visible, manchón blanco en la grupa", "Muy discreto; los machos llevan cuernas cortas."),
 ("Jabalí", "Sus scrofa", "Bosque y cultivos", "Cuerpo robusto, pelo oscuro y áspero", "Se delata por las «hozaduras» (tierra removida)."),
 ("Zorro", "Vulpes vulpes", "En cualquier sitio, sobre todo al anochecer", "Rojizo, cola espesa con punta blanca", "Caza topillos y conejos."),
 ("Lobo", "Canis lupus", "Montes y páramos; muy esquivo", "Mayor que un perro, cola recta y baja", "Presente en la comarca pero casi imposible de ver; respétalo y no lo busques."),
 ("Liebre ibérica", "Lepus granatensis", "Campos abiertos", "Orejas largas con punta negra, patas largas", "Duerme en una «encame» sobre el suelo."),
 ("Conejo", "Oryctolagus cuniculus", "Linderos y majanos", "Más pequeño que la liebre, orejas cortas", "Presa clave de águilas y zorros."),
 ("Tejón", "Meles meles", "Madrigueras en lindes y bosque; vida nocturna", "Cabeza blanca con dos rayas negras", "Excava madrigueras enormes y muy antiguas."),
 ("Garduña", "Martes foina", "Bosques, tapias y pueblos", "Marrón oscuro con babero blanco", "A veces entra en desvanes y motores."),
 ("Gineta", "Genetta genetta", "Bosques y barrancos; nocturna", "Cola anillada, cuerpo moteado, muy felina", "Casi nunca se ve; se delata en fotos de cámaras."),
 ("Gato montés", "Felis silvestris", "Bosque y matorral", "Como un gato atigrado grande, cola gruesa con anillos", "Muy esquivo y protegido."),
 ("Erizo europeo", "Erinaceus europaeus", "Huertas, setos y jardines", "Cubierto de púas", "Hiberna en invierno; deja un hueco libre en la valla."),
 ("Murciélagos", "varias especies", "Iglesias, cuevas, puentes; de noche", "Pequeños voladores nocturnos", "Comen toneladas de insectos; protégelos."),
]
REPTILES = [
 ("Lagarto ocelado", "Timon lepidus", "reptil", "Muros y pedregales soleados", "El mayor lagarto de la península; verde con manchas azules en los lados."),
 ("Lagartija ibérica", "Podarcis hispanicus", "reptil", "Piedras, tapias y huertas", "Pequeña, muy ágil, se calienta al sol."),
 ("Culebra bastarda", "Malpolon monspessulanus", "reptil", "Matorral y piedras", "Grande y de rápido movimiento; sus colmillos están al fondo de la boca y no es peligrosa para las personas."),
 ("Culebra de collar", "Natrix helvetica", "reptil", "Arroyos y charcas", "Collar claro tras la cabeza; nada muy bien. Inofensiva."),
 ("Víbora áspid", "Vipera aspis", "reptil", "Pedregales y bordes de bosque", "La única peligrosa de la zona: cabeza triangular, pupila vertical. Si ves una, déjala pasar y no la toques."),
 ("Sapo común", "Bufo spinosus", "anfibio", "Humedales, caminos con lluvia", "Piel áspera; se come muchos caracoles y babosas."),
 ("Rana común", "Pelophylax perezi", "anfibio", "Arroyos, charcas y balsas", "Verde brillante; canta en coro en verano."),
 ("Tritón jaspeado", "Triturus marmoratus", "anfibio", "Charcas y abrevaderos", "Verde con manchas negras; cría en agua limpia."),
]
INSECTOS = [
 ("Abejorros y abejas silvestres", "Cientos de especies que polinizan huertos y prados; sin ellas no hay manzanas."),
 ("Mariposas diurnas", "Macaón, vanesas, blancas de la col y blanquiverdes visitan flores desde mayo; los prados sin segar son su casa."),
 ("Luciérnagas", "En las noches calurosas de junio y julio brillan en linderos y prados: indican cielo y campo sin contaminar."),
 ("Libélulas y caballitos del diablo", "Siguen los arroyos y balsas; sus larvas viven en agua limpia."),
 ("Escarabajos peloteros", "Entierran el estiércol y mejoran el suelo del pasto."),
 ("Saltamontes y grillos", "Su canto marca los atardeceres de verano y alimentan a muchas aves."),
]
ARBOLES = [
 ("Quejigo", "Quercus faginea", "Roble de hoja algo coriácea que seca y queda en la rama; forma los bosques de las laderas.", 1),
 ("Roble melojo", "Quercus pyrenaica", "Hojas grandes y lobuladas con pelillos; vive en suelos silíceos y frescos.", 1),
 ("Coscoja", "Quercus coccifera", "Pequeño arbusto con hojas espinosas, en laderas secas soleadas.", 1),
 ("Encina", "Quercus ilex", "Siempre verde, bellotas dulces; es la base de muchos bosques de la meseta.", 0),
 ("Enebro", "Juniperus communis", "Arbusto de hojas punzantes y «gálbulas» azuladas; resiste el frío y la sequía.", 0),
 ("Espino albar", "Crataegus monogyna", "Setos con flores blancas en mayo y frutos rojos en otoño; refugio de pájaros.", 0),
 ("Endrino", "Prunus spinosa", "Espinoso, flor blanca antes que la hoja; sus endrinas dan el pacharán.", 0),
 ("Rosal silvestre", "Rosa canina", "Escaramujos rojos en otoño, ricos en vitamina C.", 0),
 ("Chopo y sauce", "Populus / Salix", "En arroyos y riberas; sujetan las orillas.", 0),
 ("Brezo y tomillo", "Calluna / Thymus", "Matorral bajo de laderas y páramos, muy melífero.", 0),
]
FLORA = [
 ("Narcisos", "Narcissus", "En primavera cubren claros y prados húmedos del norte de Burgos."),
 ("Orquídeas silvestres", "Orchidaceae", "Hay muchas especies pequeñas en prados y claros; no se arrancan nunca (protegidas)."),
 ("Amapolas, acianos y margaritas", "Papaver / Centaurea / Leucanthemum", "El color de los campos y linderos en mayo y junio."),
 ("Tomillo, cantueso y espliego", "Thymus / Lavandula", "Aromáticas del páramo que llenan de olor y abejas las laderas en verano."),
 ("Setas", "Fungi", "Salen tras las lluvias de otoño y primavera; mira la sección de la huerta antes de tocar ninguna."),
]
HABITATS = [
 ("Cortados y barrancos calizos", "Las paredes de las loras guardan buitres, águila real, halcón peregrino, chovas y cuervos; en las grietas, aviones roqueros y roqueros solitarios."),
 ("Páramos y campos de cereal", "Aves del campo (alondras, calandrias, trigueros, perdices, aguiluchos), liebres, zorros y mucha vida pequeña entre las lindes."),
 ("Bosques de quejigo, melojo y encina", "Corzos, jabalíes, tejones, gatos monteses, pitos, arrendajos y, en el suelo, setas y orquídeas."),
 ("Arroyos y riberas", "Chopos, sauces, ranas, tritones, culebras de collar, libélulas y aves que beben y se bañan."),
 ("Pueblos, huertas y tapias", "Cigüeñas, golondrinas, vencejos, mochuelos, lechuzas, murciélagos, erizos y lagartijas."),
]
datos = {"aviso": "Lista orientativa propia de la meseta norte y de los cortados de Las Loras; escrita a mano. Las especies con ★ aparecen citadas por fuentes del Geoparque Las Loras. Contrasta con guías de campo y con las observaciones de la gente del pueblo.",
         "aves": [dict(nombre=n, cientifico=s, grupo=g, meses=m, donde=d, rasgo=r, dato=x, geoparque=bool(e)) for n, s, g, m, d, r, x, e in AVES],
         "mamiferos": [dict(nombre=n, cientifico=s, donde=d, rasgo=r, dato=x) for n, s, d, r, x in MAMIFEROS],
         "reptiles": [dict(nombre=n, cientifico=s, grupo=g, donde=d, dato=x) for n, s, g, d, x in REPTILES],
         "insectos": [dict(nombre=n, dato=x) for n, x in INSECTOS],
         "arboles": [dict(nombre=n, cientifico=s, dato=x, geoparque=bool(e)) for n, s, x, e in ARBOLES],
         "flora": [dict(nombre=n, cientifico=s, dato=x) for n, s, x in FLORA],
         "habitats": [dict(nombre=n, dato=x) for n, x in HABITATS],
         "mirar": ["Mira desde lejos y con prismáticos: si el animal cambia de conducta, estás demasiado cerca.", "De marzo a julio las aves crían: ni te acerques a nidos ni a cortados con buitres.",
                   "Nada de drones cerca de cortados, nidos o rebaños.", "Perros atados en campo y monte: los nidos están en el suelo.", "No cojas ni plantas, ni setas, ni huevos, ni crías; no arranques orquídeas.",
                   "Si encuentras un animal herido, no lo cojas: avisa al 112 (en Castilla y León, al Centro de Recuperación de Fauna) o a los agentes medioambientales."]}
SALIDA.write_text(json.dumps(datos, ensure_ascii=False, indent=1))
print("escrito", SALIDA, len(AVES), "aves", len(MAMIFEROS), "mamíferos")
