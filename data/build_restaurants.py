# -*- coding: utf-8 -*-
import json, math, re

bounds_gj = json.load(open("data/bounds.geojson"))

def point_in_ring(lon, lat, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi):
            inside = not inside
        j = i
    return inside

districts = []
for feat in bounds_gj["features"]:
    if feat["properties"].get("level") == "8":
        name = feat["properties"]["name"]
        if name == "Ángeles":
            name = "Los Ángeles"
        rings = [poly[0] for poly in feat["geometry"]["coordinates"]]
        districts.append((name, rings))

def get_district(lat, lon):
    for name, rings in districts:
        for r in rings:
            if point_in_ring(lon, lat, r):
                return name
    best, best_d = "San Ramón", 999
    for name, rings in districts:
        r = rings[0]
        clon = sum(p[0] for p in r) / len(r)
        clat = sum(p[1] for p in r) / len(r)
        d = (lat - clat)**2 + (lon - clon)**2
        if d < best_d:
            best_d, best = d, name
    return best

def norm_name(s):
    if not s: return ""
    s = s.lower()
    # strip parenthetical alias
    s = re.sub(r"\([^)]*\)", " ", s)
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ñ","n"),("•",""),("'",""),("´",""),("-"," "),("&","and"),("/"," ")]:
        s = s.replace(a, b)
    s = re.sub(r"\b(restaurante|restaurant|rest|soda|bar|pizzeria|cafeteria|cafe|marisqueria|heladeria|panaderia|san ramon|de|la|el|los|las|y|and|express|expres|steak|house|ceviches|cevichito)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s

CURATED = [
    {
        "name": "Green Garden Trattoria",
        "category": "Italiana y Pizzería",
        "address": "100 m este y 100 m sur de Perimercados, San Ramón Centro",
        "lat": 10.0857, "lng": -84.4685, "coordsApprox": False,
        "phone": "+506 2445-3335",
        "delivery": "+506 8441-7564",
        "whatsapp": "+506 8441-7564",
        "hours": {
            "Mon": "11:00–21:00", "Tue": "Cerrado", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–16:00"
        },
        "rating": 4.8, "votes": 497,
        "description": "Trattoria italiana gourmet dirigida por chef con experiencia en Nueva York. Pastas frescas artesanales, pizzas gourmet, calzones, paninis y coctelería.",
        "menu": [
            {"item": "Spaghetti alla Carbonara artesanal", "price": "₡6,800"},
            {"item": "Lasagna Bolognesa al horno", "price": "₡6,500"},
            {"item": "Pizza Margherita Gourmet", "price": "₡6,900"},
            {"item": "Calzone Napolitano relleno", "price": "₡6,200"},
            {"item": "Fettuccine Alfredo con Pollo o Camarones", "price": "₡7,400"},
            {"item": "Panini Caprese en pan artesanal", "price": "₡4,900"}
        ],
        "website": "https://greengardensr.com"
    },
    {
        "name": "Savory a la Thai",
        "category": "Asiática y Sushi",
        "address": "1.5 km noroeste de la Iglesia de Piedades Norte (Calle Campos / Calle Zeledón)",
        "lat": 10.14935, "lng": -84.50537, "coordsApprox": False,
        "phone": "+506 6012-7722",
        "delivery": "+506 6012-7722",
        "whatsapp": "+506 6012-7722",
        "hours": {
            "Mon": "Cerrado", "Tue": "12:00–20:00", "Wed": "12:00–20:00",
            "Thu": "12:00–20:00", "Fri": "12:00–20:00", "Sat": "12:00–17:00", "Sun": "Cerrado"
        },
        "rating": 4.7, "votes": 528,
        "description": "Auténtica cocina tailandesa en las montañas de Piedades Norte dirigida por la chef Addie y Gerardo. Ingredientes frescos y orgánicos locales.",
        "menu": [
            {"item": "Pad Thai tradicional (pollo, cerdo o tofu)", "price": "₡4,800"},
            {"item": "Rollitos Primavera frescos (Spring Rolls)", "price": "₡3,200"},
            {"item": "Curry Verde Tailandés con leche de coco", "price": "₡5,200"},
            {"item": "Curry Rojo Massaman con arroz jazmín", "price": "₡5,400"},
            {"item": "Sopa Tom Yum picante y aromática", "price": "₡4,200"},
            {"item": "Té Helado Tailandés (Thai Iced Tea)", "price": "₡1,800"}
        ],
        "facebook": "https://www.facebook.com/Savory-A-La-Thai-1230624153677759"
    },
    {
        "name": "Octubre 29 Gastrobar",
        "category": "Bares y Cervecerías",
        "address": "100 m norte de la Estación de Bomberos (diagonal a Correos de Costa Rica), San Ramón Centro",
        "lat": 10.08835, "lng": -84.4673, "coordsApprox": False,
        "phone": "+506 2445-8282",
        "delivery": "+506 8330-4180",
        "whatsapp": "+506 8330-4180",
        "hours": {
            "Mon": "Cerrado", "Tue": "17:00–23:00", "Wed": "17:00–23:00",
            "Thu": "17:00–23:00", "Fri": "17:00–23:00", "Sat": "11:00–23:30", "Sun": "11:00–21:30"
        },
        "rating": 4.7, "votes": 380,
        "description": "Gastrobar moderno de cocina mediterránea, pizzas artesanales de masa delgada al horno de leña, tapas de autor, cerveza artesanal y coctelería.",
        "menu": [
            {"item": "Pizza Artesanal a la Leña Prosciutto & Rúcula", "price": "₡6,900"},
            {"item": "Tapas Mediterráneas Mixtas", "price": "₡5,400"},
            {"item": "Hamburguesa Octubre 29 de Autor", "price": "₡6,200"},
            {"item": "Sangría de la Casa / Moscow Mule", "price": "₡3,500"},
            {"item": "Cerveza Artesanal de barril", "price": "₡2,800"}
        ],
        "facebook": "https://www.facebook.com/octubre29gastrobar"
    },
    {
        "name": "Manada Coyote Brewery & Beer Garden",
        "category": "Bares y Cervecerías",
        "address": "600 m noreste de la Ermita de Volio, a orillas del Río Barranca, Volio de San Ramón",
        "lat": 10.1095, "lng": -84.4675, "coordsApprox": False,
        "phone": "+506 7293-4214",
        "delivery": "+506 7293-4214",
        "whatsapp": "+506 7293-4214",
        "hours": {
            "Mon": "Cerrado", "Tue": "Cerrado", "Wed": "Cerrado",
            "Thu": "Cerrado", "Fri": "15:00–22:00", "Sat": "12:00–22:00", "Sun": "12:00–21:00"
        },
        "rating": 4.8, "votes": 290,
        "description": "Cervecería artesanal familiar con Beer Garden al aire libre de 7,000 m² frente al Río Barranca. Pet-friendly, carnes ahumadas y parrilla.",
        "menu": [
            {"item": "Nachos a la parrilla (Pulled Pork, Brisket o Pollo)", "price": "₡4,200 – ₡6,000"},
            {"item": "Choripán Especial con tocineta y mozzarella", "price": "₡4,400"},
            {"item": "Brochetas de cerdo o pollo BBQ", "price": "₡3,500"},
            {"item": "Brochetas de camarón a la parrilla", "price": "₡4,500"},
            {"item": "Tacos de maíz con pulled pork ahumado (3 uds)", "price": "₡3,500"},
            {"item": "Cerveza Artesanal (Furia, Jauría, Sombra, Coyote Solo)", "price": "₡2,200"}
        ],
        "facebook": "https://www.facebook.com/manadacoyote"
    },
    {
        "name": "Filipos Mediterranean Fusion",
        "category": "Internacional y Fusión",
        "address": "180 m este de la Sede de Occidente UCR, cerca del campo ferial, San Ramón",
        "lat": 10.0868, "lng": -84.4765, "coordsApprox": False,
        "phone": "+506 6007-2299",
        "delivery": "+506 6007-2299",
        "whatsapp": "+506 6007-2299",
        "hours": {
            "Mon": "11:00–20:00", "Tue": "11:00–20:00", "Wed": "11:00–20:00",
            "Thu": "11:00–20:00", "Fri": "11:00–21:00", "Sat": "11:00–21:00", "Sun": "Cerrado"
        },
        "rating": 4.6, "votes": 210,
        "description": "Fusión mediterránea y costarricense cerca del campus de la UCR. Gyros griegos, falafel, ensaladas frescas, plato del día y sangría.",
        "menu": [
            {"item": "Gyro Griego tradicional (cerdo, pollo o mixto)", "price": "₡3,800"},
            {"item": "Wrap de Falafel Vegetariano con tzatziki", "price": "₡3,600"},
            {"item": "Plato del Día balanceado", "price": "₡3,500"},
            {"item": "Ensalada Mediterránea con queso feta", "price": "₡3,900"},
            {"item": "Copa de Sangría artesanal", "price": "₡2,500"}
        ]
    },
    {
        "name": "Restaurante Casona del Perezoso",
        "category": "Típica y Sodas",
        "address": "Ruta 702 camino a Los Ángeles, a 10 min del centro de San Ramón",
        "lat": 10.1155, "lng": -84.4712, "coordsApprox": True,
        "phone": "+506 6274-7474",
        "delivery": "+506 6274-7474",
        "whatsapp": "+506 6274-7474",
        "hours": {
            "Mon": "07:30–20:00", "Tue": "07:30–20:00", "Wed": "07:30–20:00",
            "Thu": "07:30–20:00", "Fri": "07:30–21:00", "Sat": "07:30–21:00", "Sun": "07:30–20:00"
        },
        "rating": 4.8, "votes": 319,
        "description": "Restaurante campestre y cafetería con mirador hacia las montañas, desayunos típicos, mariscos, carnes y pizzas. Ambiente familiar y pet-friendly.",
        "menu": [
            {"item": "Desayuno Típico Casona con gallo pinto y natilla", "price": "₡3,600"},
            {"item": "Casado Tradicional con carne en salsa o trucha", "price": "₡4,200"},
            {"item": "Arroz con Mariscos de la casa", "price": "₡5,800"},
            {"item": "Pizza Artesanal Familiar", "price": "₡6,900"},
            {"item": "Chifrijo Casona", "price": "₡3,800"}
        ],
        "facebook": "https://www.facebook.com/casonadelperezoso"
    },
    {
        "name": "Katana's Restaurante",
        "category": "Asiática y Sushi",
        "address": "100 m oeste del Banco Nacional, San Ramón Centro",
        "lat": 10.0869, "lng": -84.4718, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats",
        "whatsapp": None,
        "hours": {
            "Mon": "11:30–22:00", "Tue": "11:30–22:00", "Wed": "11:30–22:00",
            "Thu": "11:30–22:00", "Fri": "11:30–22:00", "Sat": "11:30–22:00", "Sun": "11:30–21:30"
        },
        "rating": 4.8, "votes": 296,
        "description": "Restaurante de fusión asiática y japonesa en el centro de San Ramón, reconocido por sus sushi rolls, poke bowls de salmón y platos orientales.",
        "menu": [
            {"item": "Katana Roll Especial (10 piezas)", "price": "₡4,900"},
            {"item": "Bowl Asiático de Salmón y Aguacate", "price": "₡5,400"},
            {"item": "Rollo Tempura Crunch", "price": "₡4,600"},
            {"item": "Arroz de Sushi con Pollo Teriyaki", "price": "₡4,500"},
            {"item": "Gyozas japonesas (6 uds)", "price": "₡3,200"}
        ]
    },
    {
        "name": "Ola Ola Ceviches",
        "category": "Marisquerías y Ceviches",
        "address": "Avenida Las Guarias (Av. 11), Barrio Los Parques, San Ramón",
        "lat": 10.09339, "lng": -84.47458, "coordsApprox": False,
        "phone": "+506 7014-4909",
        "delivery": "+506 7014-4909",
        "whatsapp": "+506 7014-4909",
        "hours": {
            "Mon": "12:00–21:30", "Tue": "12:00–21:30", "Wed": "12:00–21:30",
            "Thu": "12:00–21:30", "Fri": "12:00–22:00", "Sat": "12:00–22:00", "Sun": "12:00–21:30"
        },
        "rating": 4.8, "votes": 890,
        "description": "Uno de los restaurantes de mariscos y cevicherías mejor calificados de San Ramón. Ceviches frescos al estilo costero y peruano.",
        "menu": [
            {"item": "Ceviche Clásico de Pescado Blanco", "price": "₡3,900"},
            {"item": "Ceviche Mixto (Pescado, Camarón, Pulpo)", "price": "₡5,200"},
            {"item": "Ceviche Peruano en Leche de Tigre", "price": "₡4,800"},
            {"item": "Canasta de Patacones con Mariscos", "price": "₡5,600"},
            {"item": "Camarones Empanizados con papas", "price": "₡5,900"}
        ],
        "website": "https://olaolaceviches.com"
    },
    {
        "name": "Papi Parrillero",
        "category": "Carnes y Parrilla",
        "address": "75 m norte de la Bomba Chury, San Ramón Centro",
        "lat": 10.0835, "lng": -84.4694, "coordsApprox": False,
        "phone": "+506 7052-4567",
        "delivery": "+506 7052-4567",
        "whatsapp": "+506 7052-4567",
        "hours": {
            "Mon": "11:30–21:00", "Tue": "11:30–21:00", "Wed": "11:30–21:00",
            "Thu": "11:30–21:00", "Fri": "11:30–21:30", "Sat": "11:30–21:30", "Sun": "11:30–21:00"
        },
        "rating": 4.8, "votes": 274,
        "description": "Parrilladas al carbón, cortes de res, costillas BBQ, choripanes y patacones rellenos con servicio express directo y en Uber Eats.",
        "menu": [
            {"item": "Parrillada Personal al Carbón", "price": "₡6,500"},
            {"item": "Costilla de Cerdo BBQ con papas", "price": "₡5,900"},
            {"item": "Patacones Papi Parrillero con carne asada", "price": "₡4,800"},
            {"item": "Churrasco a la Parrilla 300g", "price": "₡7,900"},
            {"item": "Choripán Argentino al carbón", "price": "₡3,500"}
        ],
        "website": "https://papiparrillero.com"
    },
    {
        "name": "Kami Sushi Express",
        "category": "Asiática y Sushi",
        "address": "300 m oeste y 75 m norte de Emergencias del Hospital de San Ramón (Calle Ángeles)",
        "lat": 10.0908, "lng": -84.4755, "coordsApprox": False,
        "phone": "+506 8379-6679",
        "delivery": "+506 8379-6679",
        "whatsapp": "+506 8379-6679",
        "hours": {
            "Mon": "Cerrado", "Tue": "12:00–15:00, 18:00–21:00", "Wed": "12:00–15:00, 18:00–21:00",
            "Thu": "12:00–15:00, 18:00–21:00", "Fri": "12:00–15:00, 18:00–21:00", "Sat": "12:00–21:00", "Sun": "12:00–20:00"
        },
        "rating": 4.2, "votes": 323,
        "description": "Sushi artesanal y cocina japonesa con salón acogedor y servicio express rápido por WhatsApp en todo San Ramón.",
        "menu": [
            {"item": "California Roll (10 piezas)", "price": "₡3,800"},
            {"item": "Philadelphia Roll con salmón y queso crema", "price": "₡4,400"},
            {"item": "Kami Especial Tempura Roll", "price": "₡4,800"},
            {"item": "Combo Sushi 20 piezas mixto", "price": "₡8,200"},
            {"item": "Yakimeshi (arroz frito japonés)", "price": "₡4,100"}
        ]
    },
    {
        "name": "Restaurante Han Bin",
        "category": "Asiática y Sushi",
        "address": "Avenida 0, entre Calles 2 y 4 (25 m oeste de la esquina suroeste del Parque Central)",
        "lat": 10.08664, "lng": -84.47099, "coordsApprox": False,
        "phone": "+506 2445-5801",
        "delivery": "+506 2445-1003",
        "whatsapp": "+506 2445-5801",
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–22:30", "Sat": "11:00–22:30", "Sun": "11:00–22:00"
        },
        "rating": 4.5, "votes": 244,
        "description": "Clásico restaurante de comida china cantonesa e internacional a pasos del Parque Central de San Ramón. Porciones generosas y servicio express.",
        "menu": [
            {"item": "Arroz Cantonés Entero", "price": "₡4,600"},
            {"item": "Chop Suey Especial en Salsa", "price": "₡4,400"},
            {"item": "Pollo Agridulce Cantonés", "price": "₡4,800"},
            {"item": "Camarones Empanizados con papas", "price": "₡5,600"},
            {"item": "Sopa de Wantán Especial", "price": "₡3,600"}
        ]
    },
    {
        "name": "Restaurante Ta Gen",
        "category": "Asiática y Sushi",
        "address": "100 m norte de la Escuela Jorge Washington, San Ramón Centro",
        "lat": 10.08355, "lng": -84.47041, "coordsApprox": False,
        "phone": "+506 2447-9093",
        "delivery": "+506 2447-9093",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:30", "Tue": "11:00–21:30", "Wed": "11:00–21:30",
            "Thu": "11:00–21:30", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–21:30"
        },
        "rating": 4.3, "votes": 160,
        "description": "Restaurante tradicional de comida china con servicio en salón, para llevar y entregas a domicilio.",
        "menu": [
            {"item": "Arroz Frito Especial Ta Gen", "price": "₡4,500"},
            {"item": "Chow Mein con Pollo y Vegetales", "price": "₡4,400"},
            {"item": "Costilla de Cerdo Agridulce", "price": "₡5,100"},
            {"item": "Tacos Chinos (2 uds)", "price": "₡1,900"}
        ]
    },
    {
        "name": "Rincón San Ramón (Rincón Chino)",
        "category": "Asiática y Sushi",
        "address": "Costado norte del Parque Central de San Ramón",
        "lat": 10.08778, "lng": -84.47044, "coordsApprox": False,
        "phone": "+506 4033-7072",
        "delivery": "+506 7023-4131",
        "whatsapp": "+506 7023-4131",
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–22:00"
        },
        "rating": 3.8, "votes": 63,
        "description": "Restaurante chino frente al costado norte del Parque Central con servicio express directo.",
        "menu": [
            {"item": "Medio Arroz Cantonés + Chop Suey", "price": "₡3,900"},
            {"item": "Arroz Cantonés Familiar", "price": "₡5,500"},
            {"item": "Pollo con Brócoli en salsa de ostión", "price": "₡4,600"}
        ]
    },
    {
        "name": "Chiniticos San Ramón",
        "category": "Asiática y Sushi",
        "address": "San Ramón Centro (3GQG+6V5)",
        "lat": 10.0881, "lng": -84.4728, "coordsApprox": True,
        "phone": "+506 2447-7535",
        "delivery": "+506 2447-7535",
        "whatsapp": None,
        "hours": {
            "Mon": "10:00–20:00", "Tue": "10:00–20:00", "Wed": "10:00–20:00",
            "Thu": "10:00–20:00", "Fri": "10:00–21:00", "Sat": "10:00–21:00", "Sun": "10:00–19:00"
        },
        "rating": 3.4, "votes": 117,
        "description": "Comida china fusión costarricense para llevar y servicio express.",
        "menu": [
            {"item": "Combo Chinitico (Cantonés + Chop Suey + Taco)", "price": "₡3,500"},
            {"item": "Entero de Arroz Cantonés", "price": "₡4,200"}
        ]
    },
    {
        "name": "Ventanita China Express",
        "category": "Asiática y Sushi",
        "address": "San Ramón Centro, Alajuela",
        "lat": 10.0862, "lng": -84.4712, "coordsApprox": True,
        "phone": "+506 2445-0906",
        "delivery": "+506 2445-0906",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–22:00"
        },
        "rating": 3.7, "votes": 70,
        "description": "Ventanita de comida china rápida para llevar y entregas a domicilio en el centro de San Ramón.",
        "menu": [
            {"item": "Porción de Arroz Cantonés", "price": "₡2,800"},
            {"item": "Chop Suey en salsa o seco", "price": "₡2,900"}
        ]
    },
    {
        "name": "Restaurante Peruano Nazca",
        "category": "Internacional y Fusión",
        "address": "Costado sur del Gimnasio Rafael Rodríguez (contiguo al Polideportivo Gabelo Conejo)",
        "lat": 10.08516, "lng": -84.46892, "coordsApprox": False,
        "phone": "+506 2445-5005",
        "delivery": "+506 2445-1138",
        "whatsapp": "+506 2445-5005",
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–22:00"
        },
        "rating": 4.4, "votes": 425,
        "description": "Gastronomía peruana auténtica y mariscos: ceviches en leche de tigre, lomo saltado, jalea de mariscos y arroz chaufa.",
        "menu": [
            {"item": "Ceviche Peruano de Corvina", "price": "₡5,800"},
            {"item": "Lomo Saltado tradicional", "price": "₡6,900"},
            {"item": "Jalea Real de Mariscos", "price": "₡7,800"},
            {"item": "Arroz Chaufa de Mariscos", "price": "₡6,500"},
            {"item": "Ají de Gallina", "price": "₡5,900"},
            {"item": "Pisco Sour / Chicha Morada", "price": "₡3,200"}
        ]
    },
    {
        "name": "Los Nopales Restaurante Mexicano",
        "category": "Mexicana",
        "address": "175 m norte del Templo Parroquial (50 m este y 25 m sur de Ekono), San Ramón Centro",
        "lat": 10.0889, "lng": -84.4694, "coordsApprox": False,
        "phone": "+506 2445-3483",
        "delivery": "+506 2445-3483",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–21:30", "Sat": "11:00–21:30", "Sun": "18:00–21:30"
        },
        "rating": 4.5, "votes": 230,
        "description": "Restaurante mexicano tradicional muy querido en San Ramón. Tacos, sopa azteca, birria, burritos (con opciones vegetarianas y veganas).",
        "menu": [
            {"item": "Orden de Tacos al Pastor o Birria", "price": "₡4,200"},
            {"item": "Sopa Azteca tradicional con aguacate y queso", "price": "₡3,600"},
            {"item": "Burrito Los Nopales (res, pollo o vegetariano)", "price": "₡4,500"},
            {"item": "Quesabirrias con consomé", "price": "₡4,800"},
            {"item": "Guacamole fresco con totopos", "price": "₡3,200"}
        ]
    },
    {
        "name": "Hasta el Elote Taquería Mexicana",
        "category": "Mexicana",
        "address": "San Ramón Centro, Alajuela",
        "lat": 10.0868, "lng": -84.4695, "coordsApprox": True,
        "phone": None,
        "delivery": "Uber Eats",
        "whatsapp": None,
        "hours": {
            "Mon": "11:30–21:30", "Tue": "11:30–21:30", "Wed": "11:30–21:30",
            "Thu": "11:30–21:30", "Fri": "11:30–22:00", "Sat": "11:30–22:00", "Sun": "11:30–21:00"
        },
        "rating": 4.6, "votes": 115,
        "description": "Antojitos y comida mexicana auténtica: tacos al pastor, tacos de birria, quesabirrias, elotes locos y mangonadas.",
        "menu": [
            {"item": "Quesabirrias con consomé (3 uds)", "price": "₡4,500"},
            {"item": "Tacos al Pastor con piña y cilantro", "price": "₡3,900"},
            {"item": "Elote Mexicano preparado", "price": "₡2,200"},
            {"item": "Mangonada con chamoy y tajín", "price": "₡2,500"}
        ]
    },
    {
        "name": "Las Chulas Cocina Mexicana",
        "category": "Mexicana",
        "address": "Cercanías de las oficinas del ICE, San Ramón Centro",
        "lat": 10.0879, "lng": -84.4678, "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": {
            "Mon": "Cerrado", "Tue": "12:00–21:00", "Wed": "12:00–21:00",
            "Thu": "12:00–21:00", "Fri": "12:00–21:30", "Sat": "12:00–21:30", "Sun": "12:00–20:00"
        },
        "rating": 4.5, "votes": 90,
        "description": "Emprendimiento familiar de comida mexicana casera cerca del ICE en San Ramón.",
        "menu": [
            {"item": "Tacos de Cochinita Pibil o Carnitas", "price": "₡4,100"},
            {"item": "Gringa de Pastor en tortilla de harina", "price": "₡3,800"},
            {"item": "Agua de Horchata / Jamaica", "price": "₡1,500"}
        ]
    },
    {
        "name": "Taquería La Tica (La Ventanita de Wilfred Huertas)",
        "category": "Típica y Sodas",
        "address": "Corazón de San Ramón Centro (Avenida Central)",
        "lat": 10.0872, "lng": -84.4702, "coordsApprox": False,
        "phone": "+506 2445-7592",
        "delivery": "+506 2445-7592",
        "whatsapp": None,
        "hours": {
            "Mon": "08:00–23:00", "Tue": "08:00–23:00", "Wed": "08:00–23:00",
            "Thu": "08:00–23:00", "Fri": "08:00–23:00", "Sat": "08:00–23:00", "Sun": "08:00–23:00"
        },
        "rating": 4.6, "votes": 310,
        "description": "Clásico ramonense con décadas de tradición, famoso en todo el país por sus empanadas, tacos ticos y antojitos.",
        "menu": [
            {"item": "Taco Tico con repollo y salsas", "price": "₡1,600"},
            {"item": "Empanada de carne, queso o frijol", "price": "₡1,300"},
            {"item": "Enchilada tradicional", "price": "₡1,400"},
            {"item": "Arroz con Pollo", "price": "₡2,500"}
        ]
    },
    {
        "name": "Marisquería Delicias del Mar",
        "category": "Marisquerías y Ceviches",
        "address": "Costado noroeste de los Tribunales de Justicia, San Ramón Centro",
        "lat": 10.0858, "lng": -84.4715, "coordsApprox": False,
        "phone": "+506 2445-1275",
        "delivery": "+506 2447-4896",
        "whatsapp": "+506 2445-1275",
        "hours": {
            "Mon": "10:30–21:30", "Tue": "10:30–21:30", "Wed": "10:30–21:30",
            "Thu": "10:30–21:30", "Fri": "10:30–22:00", "Sat": "10:30–22:00", "Sun": "10:30–21:00"
        },
        "rating": 4.2, "votes": 1100,
        "description": "Una de las marisquerías más concurridas de San Ramón. Famosa por su ceviche frito, vuelve a la vida, casados con pescado y mariscadas.",
        "menu": [
            {"item": "Vuelve a la Vida grande", "price": "₡4,800"},
            {"item": "Ceviche Frito de Pescado con patacones", "price": "₡4,200"},
            {"item": "Pargo Entero Frito con arroz y patacones", "price": "₡6,900"},
            {"item": "Arroz con Camarones", "price": "₡5,400"},
            {"item": "Sopa de Mariscos en leche de coco", "price": "₡5,200"}
        ]
    },
    {
        "name": "Pilar Marisquería",
        "category": "Marisquerías y Ceviches",
        "address": "100 m norte de la Estación de Bomberos, costado norte del Colegio Patriarca, San Ramón",
        "lat": 10.08829, "lng": -84.46705, "coordsApprox": False,
        "phone": "+506 2445-0473",
        "delivery": "+506 2445-0473",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–23:00", "Sat": "11:00–23:00", "Sun": "11:00–21:00"
        },
        "rating": 4.4, "votes": 195,
        "description": "Marisquería y carnes en el sector del Colegio Patriarca, reconocida por sus ceviches, filetes al ajillo y ambiente familiar.",
        "menu": [
            {"item": "Filete de Corvina al Ajillo", "price": "₡5,800"},
            {"item": "Mariscada Mixta al Ajillo o Mantequilla", "price": "₡7,500"},
            {"item": "Ceviche de la Casa", "price": "₡3,500"},
            {"item": "Camarones al Ajillo con patacones", "price": "₡6,400"}
        ]
    },
    {
        "name": "M&M Mariscos",
        "category": "Marisquerías y Ceviches",
        "address": "Avenida 10, frente al Cementerio de San Ramón",
        "lat": 10.0825, "lng": -84.4742, "coordsApprox": True,
        "phone": "+506 7164-0926",
        "delivery": "+506 7164-0926",
        "whatsapp": "+506 7164-0926",
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–20:00"
        },
        "rating": 4.5, "votes": 85,
        "description": "Especialidad en sopas marineras, ceviches frescos y platos de mariscos frente al cementerio local.",
        "menu": [
            {"item": "Sopa de Mariscos M&M", "price": "₡4,900"},
            {"item": "Ceviche Mixto", "price": "₡4,200"},
            {"item": "Arroz con Mariscos", "price": "₡5,200"}
        ]
    },
    {
        "name": "Marisquería El Kraken Dorado",
        "category": "Marisquerías y Ceviches",
        "address": "San Juan de San Ramón, Alajuela",
        "lat": 10.0985, "lng": -84.4695, "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": {
            "Mon": "11:30–21:30", "Tue": "11:30–21:30", "Wed": "11:30–21:30",
            "Thu": "11:30–21:30", "Fri": "11:30–22:30", "Sat": "11:30–22:30", "Sun": "11:30–21:00"
        },
        "rating": 4.8, "votes": 147,
        "description": "Marisquería destacada en San Juan de San Ramón por sus platos de pulpo, calamares, pargo entero y ceviches.",
        "menu": [
            {"item": "Pulpo al Ajillo o a la Parrilla", "price": "₡6,800"},
            {"item": "Canasta de Patacones Marinos", "price": "₡5,400"},
            {"item": "Ceviche Kraken Especial", "price": "₡4,500"}
        ]
    },
    {
        "name": "Mario's Steak House",
        "category": "Carnes y Parrilla",
        "address": "150 m oeste del Instituto Julio Acosta García, San Ramón",
        "lat": 10.0842, "lng": -84.4748, "coordsApprox": True,
        "phone": None,
        "delivery": "PedidosYa",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–00:00", "Sat": "11:00–00:00", "Sun": "11:00–21:00"
        },
        "rating": 4.5, "votes": 210,
        "description": "Clásico steakhouse en San Ramón especializado en cortes de carne a la parrilla, lomito, churrasco y bocas.",
        "menu": [
            {"item": "Lomito a la Parrilla en salsa de hongos", "price": "₡7,800"},
            {"item": "Churrasco Mario's con papas y ensalada", "price": "₡7,500"},
            {"item": "Fajitas Mixtas al sartén", "price": "₡5,900"}
        ]
    },
    {
        "name": "Restaurante El Establo Steak House",
        "category": "Carnes y Parrilla",
        "address": "Avenida 10, San Ramón Centro",
        "lat": 10.08233, "lng": -84.47341, "coordsApprox": False,
        "phone": "+506 2445-7833",
        "delivery": "+506 2445-7833",
        "whatsapp": None,
        "hours": {
            "Mon": "11:30–22:00", "Tue": "11:30–22:00", "Wed": "11:30–22:00",
            "Thu": "11:30–22:00", "Fri": "11:30–23:00", "Sat": "11:30–23:00", "Sun": "11:30–21:30"
        },
        "rating": 4.1, "votes": 769,
        "description": "Restaurante de carnes, parrilladas, pastas y mariscos con amplia trayectoria en Avenida 10.",
        "menu": [
            {"item": "Parrillada El Establo para 2 personas", "price": "₡13,500"},
            {"item": "Corte New York a la parrilla", "price": "₡8,200"},
            {"item": "Costilla de Cerdo a la Barbacoa", "price": "₡6,400"},
            {"item": "Chifrijo Especial", "price": "₡3,900"}
        ]
    },
    {
        "name": "Restaurante Los Barriles",
        "category": "Carnes y Parrilla",
        "address": "Costado sur del Parque Central de San Ramón",
        "lat": 10.08673, "lng": -84.47039, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats / PedidosYa",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:30", "Tue": "11:00–21:30", "Wed": "11:00–21:30",
            "Thu": "11:00–21:30", "Fri": "11:00–22:15", "Sat": "11:00–22:15", "Sun": "11:00–21:15"
        },
        "rating": 4.0, "votes": 156,
        "description": "Restaurante y bar frente al Parque Central de San Ramón con platos a la parrilla, hamburguesas, alitas y coctelería.",
        "menu": [
            {"item": "Hamburguesa Los Barriles con papas", "price": "₡5,200"},
            {"item": "Alitas BBQ o Buffalo (10 uds)", "price": "₡5,400"},
            {"item": "Surtido Los Barriles para compartir", "price": "₡9,800"},
            {"item": "Nachos Supremos", "price": "₡4,900"}
        ]
    },
    {
        "name": "Restaurante Los Leños",
        "category": "Carnes y Parrilla",
        "address": "1.5 km oeste del cruce principal de San Ramón (hacia El Alto de Santiago)",
        "lat": 10.0713, "lng": -84.4887, "coordsApprox": False,
        "phone": "+506 2445-1403",
        "delivery": "+506 2445-1403",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–21:00"
        },
        "rating": 4.4, "votes": 190,
        "description": "Restaurante tradicional de carnes a la leña y comida típica en la entrada oeste de San Ramón.",
        "menu": [
            {"item": "Lomito a la Leña", "price": "₡7,200"},
            {"item": "Olla de Carne tradicional", "price": "₡4,200"},
            {"item": "Casado con Carne Asada a la leña", "price": "₡4,400"}
        ]
    },
    {
        "name": "Restaurante Chepe's (Chepper's)",
        "category": "Internacional y Fusión",
        "address": "75 m oeste del Centro Médico Jackson Memorial, San Ramón",
        "lat": 10.07058, "lng": -84.4879, "coordsApprox": False,
        "phone": "+506 2456-1441",
        "delivery": "+506 2456-1441",
        "whatsapp": None,
        "hours": {
            "Mon": "11:30–21:30", "Tue": "11:30–21:30", "Wed": "11:30–21:30",
            "Thu": "11:30–21:30", "Fri": "11:30–22:30", "Sat": "11:30–22:30", "Sun": "11:30–21:00"
        },
        "rating": 4.3, "votes": 135,
        "description": "Dirigido por el chef José Chacón (Chepe), ofrece hamburguesas gourmet, wraps, pizzas fusión y mariscos.",
        "menu": [
            {"item": "Chepe's Gourmet Burger", "price": "₡5,600"},
            {"item": "Wrap de Pollo Crispy o Camarón", "price": "₡4,800"},
            {"item": "Pizza Fusión de la Casa", "price": "₡6,500"}
        ]
    },
    {
        "name": "Restaurante Peli's",
        "category": "Internacional y Fusión",
        "address": "100 m este de la Escuela de Música SINEM (cerca del Banco Popular), San Ramón Centro",
        "lat": 10.08752, "lng": -84.46811, "coordsApprox": False,
        "phone": "+506 2445-1326",
        "delivery": "+506 2445-1326",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–21:00", "Sat": "11:00–21:00", "Sun": "Cerrado"
        },
        "rating": 4.5, "votes": 215,
        "description": "Popular restaurante céntrico conocido por sus pastas artesanales, hamburguesas, paninis y almuerzos ejecutivos.",
        "menu": [
            {"item": "Pasta Alfredo con Pollo y Pan de Ajo", "price": "₡4,900"},
            {"item": "Hamburguesa Peli's Especial", "price": "₡4,600"},
            {"item": "Panini Italiano", "price": "₡3,900"},
            {"item": "Almuerzo Ejecutivo del Día", "price": "₡3,600"}
        ]
    },
    {
        "name": "Santo Pecado San Ramón",
        "category": "Bares y Cervecerías",
        "address": "25 m oeste del Banco Nacional, San Ramón Centro",
        "lat": 10.08597, "lng": -84.47008, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–23:00", "Tue": "11:00–23:00", "Wed": "11:00–23:00",
            "Thu": "11:00–23:30", "Fri": "11:00–00:00", "Sat": "11:00–00:00", "Sun": "11:00–22:30"
        },
        "rating": 4.4, "votes": 260,
        "description": "Restaurante y gastrobar en pleno centro con alitas, hamburguesas, nachos, surtidos y cocteles.",
        "menu": [
            {"item": "Alitas Santo Pecado bañadas en salsa", "price": "₡5,200"},
            {"item": "Pecado Burger con tocineta y cheddar", "price": "₡5,400"},
            {"item": "Nachos Supremos para compartir", "price": "₡5,600"},
            {"item": "Coctel Margarita / Mojito", "price": "₡3,200"}
        ],
        "website": "https://santopecadocr.com"
    },
    {
        "name": "Dimension Brewing Co.",
        "category": "Bares y Cervecerías",
        "address": "150 m sur del parqueo de la UCR Sede de Occidente, San Ramón",
        "lat": 10.0845, "lng": -84.4778, "coordsApprox": True,
        "phone": "+506 8913-7979",
        "delivery": "+506 8913-7979",
        "whatsapp": "+506 8913-7979",
        "hours": {
            "Mon": "Cerrado", "Tue": "17:00–23:00", "Wed": "17:00–23:00",
            "Thu": "17:00–23:00", "Fri": "17:00–23:30", "Sat": "12:00–23:30", "Sun": "12:00–21:30"
        },
        "rating": 4.4, "votes": 136,
        "description": "Cervecería artesanal local y pizzería cerca de la UCR con cervezas propias de barril, pizzas y hamburguesas.",
        "menu": [
            {"item": "Pinta de Cerveza Artesanal Dimension", "price": "₡2,600"},
            {"item": "Flight de degustación (4 estilos)", "price": "₡4,200"},
            {"item": "Pizza Artesanal Pepperoni & Miel Picante", "price": "₡6,400"},
            {"item": "Papas Bravas con queso y tocineta", "price": "₡3,500"}
        ]
    },
    {
        "name": "Mae Culpa Restaurante y Pizzería a la Leña",
        "category": "Italiana y Pizzería",
        "address": "San Ramón Centro, Alajuela",
        "lat": 10.0865, "lng": -84.4692, "coordsApprox": True,
        "phone": "+506 8924-5334",
        "delivery": "+506 8924-5334",
        "whatsapp": "+506 8924-5334",
        "hours": {
            "Mon": "Cerrado", "Tue": "Cerrado", "Wed": "12:00–22:00",
            "Thu": "12:00–22:00", "Fri": "12:00–22:00", "Sat": "12:00–22:00", "Sun": "12:00–21:00"
        },
        "rating": 4.6, "votes": 140,
        "description": "Pizzería a la leña y restaurante italiano con excelentes opciones tradicionales, vegetarianas y veganas.",
        "menu": [
            {"item": "Pizza a la Leña Margherita", "price": "₡6,200"},
            {"item": "Pizza Vegana con hongos, aceitunas y vegetales asados", "price": "₡6,500"},
            {"item": "Focaccia al Romero con Hummus", "price": "₡3,800"},
            {"item": "Pasta Pomodoro artesanal", "price": "₡5,200"}
        ]
    },
    {
        "name": "Vila Paraíso Restaurante & Café",
        "category": "Internacional y Fusión",
        "address": "La Paz de Piedades Norte (800 m oeste del Cementerio de Piedades Norte), San Ramón",
        "lat": 10.1365, "lng": -84.5210, "coordsApprox": True,
        "phone": "+506 2445-0003",
        "delivery": None,
        "whatsapp": "+506 2445-0003",
        "hours": {
            "Mon": "Cerrado", "Tue": "12:00–21:00", "Wed": "12:00–21:00",
            "Thu": "12:00–22:00", "Fri": "09:00–22:00", "Sat": "09:00–22:00", "Sun": "09:00–18:00"
        },
        "rating": 4.7, "votes": 185,
        "description": "Restaurante y café de cocina creativa rodeado de jardines y montaña en La Paz de Piedades Norte.",
        "menu": [
            {"item": "Brunch Campestre Vila Paraíso", "price": "₡5,400"},
            {"item": "Lomito en salsa de frutos del bosque", "price": "₡8,500"},
            {"item": "Trucha a la plancha con hierbas frescas", "price": "₡6,800"},
            {"item": "Café de altura con postre artesanal", "price": "₡3,500"}
        ],
        "website": "https://vilaparaisocr.com"
    },
    {
        "name": "El Jardín San Ramón",
        "category": "Típica y Sodas",
        "address": "Carretera Interamericana Norte (Ruta 1), Alto de Santiago, 3 km oeste del cruce de San Ramón",
        "lat": 10.06044, "lng": -84.49896, "coordsApprox": False,
        "phone": "+506 2215-1439",
        "delivery": None,
        "whatsapp": "+506 2215-1439",
        "hours": {
            "Mon": "05:30–20:00", "Tue": "05:30–20:00", "Wed": "05:30–20:00",
            "Thu": "05:30–20:00", "Fri": "05:30–20:00", "Sat": "05:30–20:00", "Sun": "05:30–20:00"
        },
        "rating": 4.5, "votes": 950,
        "description": "Icónico restaurante familiar con más de 25 años de tradición. Comida típica en fogón de leña, buffet, cafetería, heladería y mariposario.",
        "menu": [
            {"item": "Desayuno Típico El Jardín (pinto, huevos, natilla, queso, maduro, tortilla)", "price": "₡3,900"},
            {"item": "Almuerzo Buffet Típico al Fogón de Leña", "price": "₡5,500"},
            {"item": "Chorreadas con natilla", "price": "₡2,400"},
            {"item": "Olla de Carne casera", "price": "₡4,200"},
            {"item": "Café chorreado con tamal asado", "price": "₡2,200"}
        ]
    },
    {
        "name": "Panadería y Cafetería La Duquesa (Parque Central)",
        "category": "Cafeterías y Panaderías",
        "address": "Costado oeste del Parque Central, 75 m sur de la esquina suroeste, San Ramón Centro",
        "lat": 10.0867, "lng": -84.4709, "coordsApprox": False,
        "phone": "+506 2445-5608",
        "delivery": "+506 2445-5608",
        "whatsapp": None,
        "hours": {
            "Mon": "05:00–20:00", "Tue": "05:00–20:00", "Wed": "05:00–20:00",
            "Thu": "05:00–20:00", "Fri": "05:00–20:00", "Sat": "05:00–20:00", "Sun": "05:00–19:00"
        },
        "rating": 4.7, "votes": 620,
        "description": "Emblemática panadería y cafetería ramonense fundada en 1923. Repostería artesanal, pan fresco, desayunos y café frente al Parque Central.",
        "menu": [
            {"item": "Café con Leche + Repostería recién horneada", "price": "₡2,200"},
            {"item": "Desayuno La Duquesa con pan artesanal", "price": "₡3,400"},
            {"item": "Emparedado Especial en pan de la casa", "price": "₡2,900"},
            {"item": "Queque de Zanahoria / Torta Chilena", "price": "₡1,800"},
            {"item": "Trenza de Queso Crema tradicional", "price": "₡2,100"}
        ],
        "website": "https://laduquesacr.com"
    },
    {
        "name": "Cafetería La Duquesa (Plaza Portell)",
        "category": "Cafeterías y Panaderías",
        "address": "Plaza Comercial Portell, 50 m norte de Perimercados, San Ramón",
        "lat": 10.0865, "lng": -84.4682, "coordsApprox": False,
        "phone": "+506 2445-5590",
        "delivery": "+506 2445-5590",
        "whatsapp": None,
        "hours": {
            "Mon": "10:00–19:00", "Tue": "10:00–19:00", "Wed": "10:00–19:00",
            "Thu": "10:00–19:00", "Fri": "10:00–19:00", "Sat": "10:00–19:00", "Sun": "11:00–19:00"
        },
        "rating": 4.6, "votes": 140,
        "description": "Sucursal en Plaza Comercial Portell con cafetería, pastelería fina y almuerzos ligeros.",
        "menu": [
            {"item": "Capuchino Artesanal", "price": "₡1,800"},
            {"item": "Panini de Jamón Serrano y Queso", "price": "₡3,500"},
            {"item": "Porción de Tres Leches", "price": "₡1,900"}
        ],
        "website": "https://laduquesacr.com"
    },
    {
        "name": "Café Delicias San Ramón",
        "category": "Cafeterías y Panaderías",
        "address": "25 m sur de la esquina suroeste del Parque Central de San Ramón",
        "lat": 10.08607, "lng": -84.47273, "coordsApprox": False,
        "phone": "+506 2447-4637",
        "delivery": "+506 2447-4637",
        "whatsapp": None,
        "hours": {
            "Mon": "07:00–19:30", "Tue": "07:00–19:30", "Wed": "07:00–19:30",
            "Thu": "07:00–19:30", "Fri": "07:00–19:30", "Sat": "07:00–19:30", "Sun": "07:00–19:30"
        },
        "rating": 4.6, "votes": 410,
        "description": "Institución local para desayunos típicos, brunch, pitas, platos ejecutivos y repostería (torta chilena y torta de elote).",
        "menu": [
            {"item": "Desayuno Típico Completo con tortillas palmeadas", "price": "₡3,500"},
            {"item": "Plato Ejecutivo con Pechuga a la Parrilla", "price": "₡4,400"},
            {"item": "Pita de Pollo con ensalada", "price": "₡3,800"},
            {"item": "Torta Chilena / Torta de Elote", "price": "₡1,750"},
            {"item": "Café Frío Mocaccino", "price": "₡2,200"}
        ]
    },
    {
        "name": "Aromas Café (Calathea)",
        "category": "Cafeterías y Panaderías",
        "address": "Frente al Centro de Cultura Social / costado sur del Templo Parroquial, San Ramón Centro",
        "lat": 10.08501, "lng": -84.4689, "coordsApprox": False,
        "phone": "+506 2445-0535",
        "delivery": "+506 2445-0249",
        "whatsapp": "+506 8786-5252",
        "hours": {
            "Mon": "07:00–20:00", "Tue": "07:00–20:00", "Wed": "07:00–20:00",
            "Thu": "07:00–20:00", "Fri": "07:00–20:30", "Sat": "07:00–20:30", "Sun": "07:30–19:30"
        },
        "rating": 4.5, "votes": 380,
        "description": "Acogedora cafetería y restaurante de varios niveles famosa por sus desayunos, sándwiches tipo lápiz, crepas, lasagnas y repostería.",
        "menu": [
            {"item": "Sándwich Lápiz Especial Aromas", "price": "₡3,600"},
            {"item": "Crepa Dulce o Salada", "price": "₡3,800"},
            {"item": "Lasagna de Carne o Pollo con pan de ajo", "price": "₡4,600"},
            {"item": "Desayuno Típico Aromas", "price": "₡3,500"},
            {"item": "Latte / Capuchino con postre", "price": "₡2,900"}
        ]
    },
    {
        "name": "Nectandra Café de Especialidad",
        "category": "Cafeterías y Panaderías",
        "address": "San Ramón Centro (cerca del Museo Regional de San Ramón)",
        "lat": 10.0879, "lng": -84.4714, "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": {
            "Mon": "Cerrado", "Tue": "11:30–18:30", "Wed": "11:30–18:30",
            "Thu": "11:30–18:30", "Fri": "11:30–18:30", "Sat": "11:30–18:30", "Sun": "11:30–18:30"
        },
        "rating": 4.8, "votes": 95,
        "description": "Cafetería de especialidad enfocada en granos de origen de productores locales sin intermediarios, métodos de extracción V60/Chemex y gofres.",
        "menu": [
            {"item": "Método de Extracción (V60 / Chemex / Prensa)", "price": "₡2,200"},
            {"item": "Gofre artesanal con frutas", "price": "₡3,400"},
            {"item": "Espresso Doble de Origen", "price": "₡1,600"},
            {"item": "Empanada artesanal horneada", "price": "₡1,800"}
        ],
        "website": "https://nectandracr.com"
    },
    {
        "name": "Le Sucrée Pâtisserie CR",
        "category": "Cafeterías y Panaderías",
        "address": "200 m este y 50 m norte del Banco Nacional, San Ramón Centro",
        "lat": 10.0874, "lng": -84.4682, "coordsApprox": False,
        "phone": "+506 6422-9008",
        "delivery": "+506 6422-9008",
        "whatsapp": "+506 6422-9008",
        "hours": {
            "Mon": "Cerrado", "Tue": "09:00–19:00", "Wed": "09:00–19:00",
            "Thu": "09:00–19:00", "Fri": "09:00–19:30", "Sat": "09:00–19:30", "Sun": "10:00–18:30"
        },
        "rating": 4.9, "votes": 110,
        "description": "Pastelería francesa y cafetería artesanal destacada por sus croissants de almendras, macarons, tartaletas y excelente café.",
        "menu": [
            {"item": "Croissant de Almendras recién horneado", "price": "₡2,400"},
            {"item": "Pain au Chocolat francés", "price": "₡2,100"},
            {"item": "Tartaleta de Frutas / Limón", "price": "₡2,600"},
            {"item": "Cappuccino Cremoso", "price": "₡1,900"}
        ]
    },
    {
        "name": "La Cafebrería",
        "category": "Cafeterías y Panaderías",
        "address": "San Rafael de San Ramón, Alajuela",
        "lat": 10.0785, "lng": -84.4730, "coordsApprox": True,
        "phone": "+506 8921-2244",
        "delivery": "+506 8810-8002",
        "whatsapp": "+506 8921-2244",
        "hours": {
            "Mon": "Cerrado", "Tue": "10:00–18:30", "Wed": "10:00–18:30",
            "Thu": "10:00–18:30", "Fri": "10:00–18:30", "Sat": "09:00–18:00", "Sun": "09:00–18:00"
        },
        "rating": 4.7, "votes": 90,
        "description": "Espacio cultural que combina cafetería artesanal y librería en San Ramón, con desayunos, repostería y tardes de lectura.",
        "menu": [
            {"item": "Café Chorreado de Especialidad", "price": "₡1,600"},
            {"item": "Desayuno Cultural", "price": "₡3,400"},
            {"item": "Queque Casero del Día", "price": "₡1,800"}
        ]
    },
    {
        "name": "Cafetería Flory (Doña Flory)",
        "category": "Típica y Sodas",
        "address": "La Paz de Piedades Norte (300 m noroeste de la Capilla de La Paz), San Ramón",
        "lat": 10.1450, "lng": -84.5190, "coordsApprox": True,
        "phone": "+506 2447-3580",
        "delivery": None,
        "whatsapp": None,
        "hours": {
            "Mon": "07:00–17:30", "Tue": "07:00–17:30", "Wed": "07:00–17:30",
            "Thu": "07:00–17:30", "Fri": "07:00–18:00", "Sat": "07:00–18:00", "Sun": "07:00–18:00"
        },
        "rating": 4.8, "votes": 340,
        "description": "Famosa soda campestre en La Paz de San Ramón, célebre por su comida casera al fogón, carne en salsa, sopa de gallina y casados.",
        "menu": [
            {"item": "Casado con Carne en Salsa casera", "price": "₡3,500"},
            {"item": "Sopa de Gallina Criolla", "price": "₡3,600"},
            {"item": "Desayuno Campestre con tortillas caseras", "price": "₡2,900"},
            {"item": "Café Chorreado con Empanada o Pan Casero", "price": "₡1,600"}
        ]
    },
    {
        "name": "Soda La Gaviota",
        "category": "Típica y Sodas",
        "address": "250 m norte del Mall Plaza Occidente, San Ramón",
        "lat": 10.08002, "lng": -84.4696, "coordsApprox": False,
        "phone": "+506 2447-3155",
        "delivery": "+506 8326-8088",
        "whatsapp": "+506 8326-8088",
        "hours": {
            "Mon": "06:00–20:00", "Tue": "06:00–20:00", "Wed": "06:00–20:00",
            "Thu": "06:00–20:00", "Fri": "06:00–20:30", "Sat": "06:00–20:30", "Sun": "07:00–16:30"
        },
        "rating": 4.5, "votes": 280,
        "description": "Soda tradicional muy popular por sus desayunos desde las 6 a.m., casados armados al gusto y servicio express.",
        "menu": [
            {"item": "Casado al Gusto (carne, pollo, chuleta o pescado)", "price": "₡3,600"},
            {"item": "Desayuno Gallo Pinto completo", "price": "₡2,900"},
            {"item": "Arroz con Pollo o Cantonés", "price": "₡3,400"},
            {"item": "Batido Natural en agua o leche", "price": "₡1,400"}
        ]
    },
    {
        "name": "Soda y Cafetería La Talolinga",
        "category": "Típica y Sodas",
        "address": "Costado norte del Mercado Municipal de San Ramón",
        "lat": 10.0882, "lng": -84.4701, "coordsApprox": False,
        "phone": "+506 2445-3726",
        "delivery": "+506 2445-3726",
        "whatsapp": None,
        "hours": {
            "Mon": "06:00–17:00", "Tue": "06:00–17:00", "Wed": "06:00–17:00",
            "Thu": "06:00–17:00", "Fri": "06:00–17:30", "Sat": "06:00–17:00", "Sun": "06:30–14:00"
        },
        "rating": 4.6, "votes": 195,
        "description": "Patrimonio gastronómico en el Mercado Municipal de San Ramón desde 1946. Sazón casero tradicional en desayunos y almuerzos.",
        "menu": [
            {"item": "Casado Tradicional del Mercado", "price": "₡3,300"},
            {"item": "Olla de Carne / Sopa de Mondongo", "price": "₡3,500"},
            {"item": "Gallo Pinto con Huevo, Natilla y Plátano", "price": "₡2,600"}
        ]
    },
    {
        "name": "La Cocina de Má (El Comedor de Má)",
        "category": "Típica y Sodas",
        "address": "Costado norte del Parque Central de San Ramón",
        "lat": 10.08781, "lng": -84.47024, "coordsApprox": False,
        "phone": "+506 2445-5472",
        "delivery": "+506 2445-5472",
        "whatsapp": None,
        "hours": {
            "Mon": "07:30–18:00", "Tue": "07:30–18:00", "Wed": "07:30–18:00",
            "Thu": "07:30–18:00", "Fri": "07:30–18:00", "Sat": "07:30–18:00", "Sun": "07:30–18:00"
        },
        "rating": 4.5, "votes": 150,
        "description": "Comedor tradicional frente al Parque Central con almuerzos caseros, picadillos y desayunos ticos.",
        "menu": [
            {"item": "Casado Casero con picadillo del día", "price": "₡3,400"},
            {"item": "Desayuno Completo", "price": "₡2,800"},
            {"item": "Fresco Natural de Frutas", "price": "₡900"}
        ]
    },
    {
        "name": "Soda El Fogón de Má",
        "category": "Típica y Sodas",
        "address": "Cañal Blanco, San Rafael de San Ramón",
        "lat": 10.0645, "lng": -84.4690, "coordsApprox": True,
        "phone": "+506 8503-8795",
        "delivery": "+506 8503-8795",
        "whatsapp": "+506 8503-8795",
        "hours": {
            "Mon": "07:00–18:00", "Tue": "07:00–18:00", "Wed": "07:00–18:00",
            "Thu": "07:00–18:00", "Fri": "07:00–19:00", "Sat": "07:00–19:00", "Sun": "07:00–17:00"
        },
        "rating": 4.6, "votes": 95,
        "description": "Soda familiar en San Rafael de San Ramón altamente valorada por su cocina criolla y atención cálida.",
        "menu": [
            {"item": "Casado Típico al Fogón", "price": "₡3,400"},
            {"item": "Chifrijo Casero", "price": "₡3,200"}
        ]
    },
    {
        "name": "Soda La Porteña",
        "category": "Típica y Sodas",
        "address": "Oeste de Empresarios Unidos, San Ramón Centro",
        "lat": 10.0884, "lng": -84.4732, "coordsApprox": True,
        "phone": "+506 6132-3004",
        "delivery": "+506 6132-3004",
        "whatsapp": "+506 6132-3004",
        "hours": {
            "Mon": "06:30–19:00", "Tue": "06:30–19:00", "Wed": "06:30–19:00",
            "Thu": "06:30–19:00", "Fri": "06:30–19:00", "Sat": "06:30–19:00", "Sun": "07:00–16:00"
        },
        "rating": 4.1, "votes": 80,
        "description": "Soda céntrica de desayunos, casados, arroz con mariscos y vigorón estilo porteño.",
        "menu": [
            {"item": "Vigorón Porteño completo", "price": "₡3,400"},
            {"item": "Casado con Pescado Chuleta o Pollo", "price": "₡3,400"}
        ]
    },
    {
        "name": "Soda Carmencita",
        "category": "Típica y Sodas",
        "address": "200 m antes de la entrada a El Empalme, carretera hacia Puntarenas, Santiago de San Ramón",
        "lat": 10.0620, "lng": -84.4960, "coordsApprox": True,
        "phone": "+506 8521-3849",
        "delivery": "+506 8521-3849",
        "whatsapp": "+506 8521-3849",
        "hours": {
            "Mon": "06:00–18:00", "Tue": "06:00–18:00", "Wed": "06:00–18:00",
            "Thu": "06:00–18:00", "Fri": "06:00–18:00", "Sat": "06:00–18:00", "Sun": "06:00–18:00"
        },
        "rating": 4.2, "votes": 43,
        "description": "Soda tradicional de carretera con amplio parqueo, desayunos mañaneros y almuerzos caseros.",
        "menu": [
            {"item": "Gallo Pinto con Carne en Salsa", "price": "₡3,100"},
            {"item": "Casado Tradicional", "price": "₡3,500"}
        ]
    },
    {
        "name": "Soda Chaparral (El Gran Chaparral)",
        "category": "Típica y Sodas",
        "address": "50 m oeste de Correos de Costa Rica, San Ramón Centro",
        "lat": 10.0872, "lng": -84.4685, "coordsApprox": False,
        "phone": "+506 2445-1005",
        "delivery": "+506 2445-1005",
        "whatsapp": None,
        "hours": {
            "Mon": "06:30–18:00", "Tue": "06:30–18:00", "Wed": "06:30–18:00",
            "Thu": "06:30–18:00", "Fri": "06:30–18:00", "Sat": "06:30–17:00", "Sun": "Cerrado"
        },
        "rating": 4.2, "votes": 65,
        "description": "Soda clásica en el centro de San Ramón a pocos metros del Correo.",
        "menu": [
            {"item": "Casado Ejecutivo", "price": "₡3,300"},
            {"item": "Arroz con Pollo", "price": "₡2,900"}
        ]
    },
    {
        "name": "Modesty Comida Caribeña",
        "category": "Típica y Sodas",
        "address": "50 m oeste de Carnicería La Feria, San Ramón Centro",
        "lat": 10.0865, "lng": -84.4730, "coordsApprox": True,
        "phone": "+506 2445-1357",
        "delivery": "+506 2445-1357",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–20:00", "Tue": "11:00–20:00", "Wed": "11:00–20:00",
            "Thu": "11:00–20:00", "Fri": "11:00–21:00", "Sat": "11:00–21:00", "Sun": "11:00–19:00"
        },
        "rating": 4.3, "votes": 39,
        "description": "Auténtica cuchara limonense en San Ramón: Rice & Beans con leche de coco, pollo caribeño, rondón y patí.",
        "menu": [
            {"item": "Rice & Beans con Pollo Caribeño y plátano maduro", "price": "₡4,200"},
            {"item": "Rice & Beans con Pescado Entero", "price": "₡5,800"},
            {"item": "Patí Limonense tradicional", "price": "₡1,400"},
            {"item": "Agua de Sapo (Hiel)", "price": "₡1,200"}
        ]
    },
    {
        "name": "Subway San Ramón",
        "category": "Comida Rápida y Pollo",
        "address": "25 m norte de la esquina noreste del Mercado Municipal (frente a Sala de Belleza Erika), San Ramón Centro",
        "lat": 10.08882, "lng": -84.46979, "coordsApprox": False,
        "phone": "+506 4083-3317",
        "delivery": "+506 4083-3317",
        "whatsapp": None,
        "hours": {
            "Mon": "07:00–22:00", "Tue": "07:00–22:00", "Wed": "07:00–22:00",
            "Thu": "07:00–22:00", "Fri": "07:00–22:00", "Sat": "07:00–22:00", "Sun": "07:00–22:00"
        },
        "rating": 4.2, "votes": 244,
        "description": "Sucursal céntrica de Subway con sándwiches personalizables de 15 cm y 30 cm, wraps, ensaladas y galletas.",
        "menu": [
            {"item": "Sub Pollo Teriyaki / Italian B.M.T. (15 cm)", "price": "₡3,650"},
            {"item": "Sub Steak & Cheese (30 cm)", "price": "₡6,400"},
            {"item": "Combo Sub del Día + Bebida + Galleta", "price": "₡4,200"}
        ],
        "website": "https://www.subway.com/es-CR"
    },
    {
        "name": "McDonald's San Ramón",
        "category": "Comida Rápida y Pollo",
        "address": "Mall Plaza Occidente, entrada a San Ramón",
        "lat": 10.07765, "lng": -84.46926, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats / PedidosYa",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–21:30", "Sat": "11:00–21:30", "Sun": "11:00–21:00"
        },
        "rating": 4.3, "votes": 510,
        "description": "Restaurante McDonald's en Mall Plaza Occidente con servicio en salón, McEntrega por apps y postres.",
        "menu": [
            {"item": "McCombo Big Mac con papas y bebida", "price": "₡4,750"},
            {"item": "McCombo Cuarto de Libra con Queso", "price": "₡4,950"},
            {"item": "McNuggets 10 piezas en combo", "price": "₡4,600"},
            {"item": "McFlurry Oreo / M&M", "price": "₡1,950"}
        ],
        "website": "https://mcdonalds.co.cr"
    },
    {
        "name": "KFC San Ramón",
        "category": "Comida Rápida y Pollo",
        "address": "Mall Plaza Occidente, entrada a San Ramón",
        "lat": 10.07773, "lng": -84.46926, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats / PedidosYa",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–21:30", "Sat": "11:00–21:30", "Sun": "11:00–21:00"
        },
        "rating": 4.3, "votes": 390,
        "description": "Pollo frito receta original y crispy, hamburguesas de pollo y buckets familiares en Plaza Occidente.",
        "menu": [
            {"item": "Bucket 8 Piezas de Pollo + Acompañamientos", "price": "₡11,900"},
            {"item": "Big Box (2 piezas, alitas, papas, ensalada, bebida)", "price": "₡5,450"},
            {"item": "Combo Kentucky Chicken Sandwich", "price": "₡4,650"}
        ],
        "website": "https://kfccostarica.cr"
    },
    {
        "name": "Burger King San Ramón",
        "category": "Comida Rápida y Pollo",
        "address": "Mall Plaza Occidente, entrada a San Ramón",
        "lat": 10.07773, "lng": -84.46935, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats / PedidosYa",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–20:30", "Tue": "11:00–20:30", "Wed": "11:00–20:30",
            "Thu": "11:00–20:30", "Fri": "11:00–21:00", "Sat": "11:00–21:00", "Sun": "11:00–20:30"
        },
        "rating": 4.2, "votes": 270,
        "description": "Hamburguesas Whopper a la parrilla, nuggets y desayunos en Mall Plaza Occidente.",
        "menu": [
            {"item": "Combo Whopper Clásico con papas y bebida", "price": "₡4,850"},
            {"item": "Combo King de Pollo", "price": "₡4,100"},
            {"item": "Nuggets 10 piezas", "price": "₡2,900"}
        ],
        "website": "https://bkcostarica.com"
    },
    {
        "name": "Taco Bell San Ramón",
        "category": "Comida Rápida y Pollo",
        "address": "Mall Plaza Occidente, entrada a San Ramón",
        "lat": 10.07771, "lng": -84.46959, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats / PedidosYa",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–20:50", "Tue": "11:00–20:50", "Wed": "11:00–20:50",
            "Thu": "11:00–20:50", "Fri": "11:00–21:20", "Sat": "11:00–21:20", "Sun": "11:00–20:50"
        },
        "rating": 4.2, "votes": 240,
        "description": "Comida Tex-Mex en Plaza Occidente: burritos, chalupas, quesadillas y Fiesta Fries.",
        "menu": [
            {"item": "Combo Crunchwrap Supreme + Papas + Bebida", "price": "₡4,650"},
            {"item": "Combo 2 Chalupas Supreme", "price": "₡4,750"},
            {"item": "Burrito 5 Capas", "price": "₡2,100"},
            {"item": "Papas Supreme (Fiesta Fries)", "price": "₡2,250"}
        ]
    },
    {
        "name": "Papa John's San Ramón",
        "category": "Italiana y Pizzería",
        "address": "Mall Plaza Occidente, Local #23, San Ramón",
        "lat": 10.07774, "lng": -84.46944, "coordsApprox": False,
        "phone": "+506 2258-9999",
        "delivery": "+506 2258-9999",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:45", "Tue": "11:00–21:45", "Wed": "11:00–21:45",
            "Thu": "11:00–21:45", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–21:45"
        },
        "rating": 4.4, "votes": 310,
        "description": "Pizzería con entrega a domicilio propia y retiro en Plaza Occidente.",
        "menu": [
            {"item": "Pizza Grande The Works / Super Pepperoni", "price": "₡9,950"},
            {"item": "Pizza Mediana Napolitana o Hawaiana", "price": "₡7,900"},
            {"item": "Palitos de Queso (Cheesesticks)", "price": "₡3,950"}
        ],
        "website": "https://papajohns.cr"
    },
    {
        "name": "Pizza Hut San Ramón",
        "category": "Italiana y Pizzería",
        "address": "Calle 1, Bajo Ladrillera / Plaza Comercial San Ramón",
        "lat": 10.0828, "lng": -84.46915, "coordsApprox": False,
        "phone": "+506 2290-9595",
        "delivery": "+506 2290-9595",
        "whatsapp": None,
        "hours": {
            "Mon": "10:30–22:00", "Tue": "10:30–22:00", "Wed": "10:30–22:00",
            "Thu": "10:30–22:00", "Fri": "10:30–22:00", "Sat": "10:30–22:00", "Sun": "10:30–22:00"
        },
        "rating": 4.8, "votes": 385,
        "description": "Sucursal de Pizza Hut en San Ramón con salón, para llevar y express al 2290-9595.",
        "menu": [
            {"item": "Pizza Pan Grande Suprema / Amantes de la Carne", "price": "₡10,400"},
            {"item": "Wow Box / My Box Personal", "price": "₡3,950"},
            {"item": "Palitos de Pan con queso (Breadsticks)", "price": "₡2,950"}
        ],
        "website": "https://pizzahut.co.cr"
    },
    {
        "name": "Ready Pizza San Ramón",
        "category": "Italiana y Pizzería",
        "address": "Del costado sur del Parque Central 100 m oeste y 50 m sur, San Ramón Centro",
        "lat": 10.0866, "lng": -84.47179, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats / PedidosYa",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:30", "Tue": "11:00–21:30", "Wed": "11:00–21:30",
            "Thu": "11:00–23:30", "Fri": "11:00–23:59", "Sat": "11:00–23:59", "Sun": "11:00–21:30"
        },
        "rating": 4.2, "votes": 180,
        "description": "Pizzas listas al instante a precios económicos en el centro de San Ramón.",
        "menu": [
            {"item": "Pizza Grande de Pepperoni o Jamón y Queso", "price": "₡4,500"},
            {"item": "Pizza Grande Suprema", "price": "₡5,900"},
            {"item": "Calzone Relleno", "price": "₡3,500"}
        ]
    },
    {
        "name": "Latina Pizza San Ramón",
        "category": "Italiana y Pizzería",
        "address": "Calle 6, San Ramón Centro",
        "lat": 10.08857, "lng": -84.47241, "coordsApprox": False,
        "phone": None,
        "delivery": "latinapizzacr.com",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–22:30", "Sat": "11:00–22:30", "Sun": "11:00–22:00"
        },
        "rating": 4.3, "votes": 140,
        "description": "Pizzería artesanal con pedidos en línea y servicio a domicilio en San Ramón.",
        "menu": [
            {"item": "Pizza Grande Latina Especial", "price": "₡7,800"},
            {"item": "Pizza Mediana 2 Sabores", "price": "₡6,200"}
        ],
        "website": "https://latinapizzacr.com"
    },
    {
        "name": "Pizzería Don Beto",
        "category": "Italiana y Pizzería",
        "address": "125 m oeste de Correos de Costa Rica, frente a Librería Eureka, San Ramón Centro",
        "lat": 10.0873, "lng": -84.4690, "coordsApprox": False,
        "phone": "+506 2447-4747",
        "delivery": "+506 2447-4747",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–22:00"
        },
        "rating": 4.4, "votes": 130,
        "description": "Pizzería local tradicional con servicio express rápido al 2447-4747 en todo el centro de San Ramón.",
        "menu": [
            {"item": "Pizza Familiar Don Beto Suprema", "price": "₡8,500"},
            {"item": "Pizza Mediana Jamón y Hongos", "price": "₡6,200"},
            {"item": "Lasagna de Carne al horno", "price": "₡4,200"}
        ]
    },
    {
        "name": "Campos Pizzería y Comida Rápida",
        "category": "Italiana y Pizzería",
        "address": "Costado oeste del Parque Central, San Ramón Centro",
        "lat": 10.08673, "lng": -84.4706, "coordsApprox": False,
        "phone": "+506 2456-1212",
        "delivery": "+506 2456-1212",
        "whatsapp": None,
        "hours": {
            "Mon": "07:00–21:30", "Tue": "07:00–21:30", "Wed": "07:00–21:30",
            "Thu": "07:00–21:30", "Fri": "07:00–21:30", "Sat": "07:00–21:30", "Sun": "07:00–21:00"
        },
        "rating": 4.3, "votes": 175,
        "description": "Panadería, pizzería y comida rápida frente al Parque Central con servicio express.",
        "menu": [
            {"item": "Porción de Pizza Suprema / Jamón", "price": "₡1,400"},
            {"item": "Pizza Grande Familiar", "price": "₡7,200"},
            {"item": "Combo Pollo Frito con papas", "price": "₡3,200"}
        ]
    },
    {
        "name": "Mi Pueblo - Pizza Loca",
        "category": "Italiana y Pizzería",
        "address": "500 m oeste del Cementerio de Piedades Norte, San Ramón",
        "lat": 10.13626, "lng": -84.51811, "coordsApprox": False,
        "phone": "+506 2445-1669",
        "delivery": "+506 8707-3635",
        "whatsapp": "+506 8707-3635",
        "hours": {
            "Mon": "Cerrado", "Tue": "12:00–21:00", "Wed": "12:00–21:00",
            "Thu": "12:00–21:00", "Fri": "12:00–22:00", "Sat": "12:00–22:00", "Sun": "12:00–22:00"
        },
        "rating": 4.6, "votes": 220,
        "description": "Pizzería artesanal y mirador familiar en las montañas de Piedades Norte con sangría de cortesía.",
        "menu": [
            {"item": "Pizza Loca Artesanal Grande", "price": "₡8,200"},
            {"item": "Pizza Vegetariana de Montaña", "price": "₡7,400"},
            {"item": "Calzone Artesanal", "price": "₡4,900"}
        ]
    },
    {
        "name": "Crispy Wings San Ramón",
        "category": "Comida Rápida y Pollo",
        "address": "150 m este de la Plaza de Deportes de San Juan, San Ramón",
        "lat": 10.1080, "lng": -84.45963, "coordsApprox": False,
        "phone": "+506 2445-7221",
        "delivery": "+506 8678-1616",
        "whatsapp": "+506 8678-1616",
        "hours": {
            "Mon": "12:00–21:45", "Tue": "12:00–21:45", "Wed": "12:00–21:45",
            "Thu": "12:00–21:45", "Fri": "12:00–21:45", "Sat": "12:00–21:45", "Sun": "12:00–21:45"
        },
        "rating": 4.6, "votes": 260,
        "description": "Especialistas en alitas crujientes, boneless, wraps y hamburguesas en San Juan de San Ramón con servicio express.",
        "menu": [
            {"item": "Orden de 12 Alitas bañadas + papas", "price": "₡6,400"},
            {"item": "Boneless Crispy con salsa a elegir", "price": "₡4,800"},
            {"item": "Crispy Chicken Burger", "price": "₡4,500"}
        ],
        "website": "https://crispywingscr.com"
    },
    {
        "name": "Alitas Chichi",
        "category": "Comida Rápida y Pollo",
        "address": "Frente a la Iglesia de San Juan, San Ramón",
        "lat": 10.1005, "lng": -84.4670, "coordsApprox": True,
        "phone": "+506 8878-5414",
        "delivery": "+506 8878-5414",
        "whatsapp": "+506 8878-5414",
        "hours": {
            "Mon": "Cerrado", "Tue": "12:00–22:50", "Wed": "12:00–21:50",
            "Thu": "12:00–21:50", "Fri": "12:00–21:50", "Sat": "12:00–21:50", "Sun": "12:00–21:50"
        },
        "rating": 4.5, "votes": 115,
        "description": "Alitas artesanales, papas cargadas y salsas caseras frente a la iglesia de San Juan.",
        "menu": [
            {"item": "Combo Alitas Chichi + Papas", "price": "₡4,900"},
            {"item": "Canasta de Papas con Pollo y Queso", "price": "₡4,200"}
        ]
    },
    {
        "name": "Perro Bravo Hotdogs",
        "category": "Comida Rápida y Pollo",
        "address": "100 m oeste de Correos de Costa Rica (contiguo a Pops), San Ramón Centro",
        "lat": 10.0870, "lng": -84.4706, "coordsApprox": False,
        "phone": "+506 4034-2215",
        "delivery": "+506 8432-5607",
        "whatsapp": "+506 8432-5607",
        "hours": {
            "Mon": "15:00–21:45", "Tue": "15:00–21:45", "Wed": "15:00–21:45",
            "Thu": "11:30–22:00", "Fri": "11:30–23:00", "Sat": "11:30–23:00", "Sun": "11:30–21:45"
        },
        "rating": 4.5, "votes": 190,
        "description": "Hot dogs gourmet estilo colombiano/americano y opciones vegetarianas en el centro de San Ramón.",
        "menu": [
            {"item": "Perro Bravo Especial con tocineta y queso", "price": "₡3,400"},
            {"item": "Perro Colombiano con piña y papitas", "price": "₡3,500"},
            {"item": "Perro Vegetariano con salchicha de soya", "price": "₡3,400"}
        ]
    },
    {
        "name": "Buggy's Burgers",
        "category": "Comida Rápida y Pollo",
        "address": "100 m norte de la Estación de Bomberos (diagonal al Gimnasio del Patriarca), San Ramón Centro",
        "lat": 10.08827, "lng": -84.46681, "coordsApprox": False,
        "phone": "+506 2445-5557",
        "delivery": "+506 8929-3009",
        "whatsapp": "+506 8929-3009",
        "hours": {
            "Mon": "11:30–21:00", "Tue": "11:30–21:00", "Wed": "11:30–21:00",
            "Thu": "11:30–21:00", "Fri": "11:30–21:30", "Sat": "11:30–21:30", "Sun": "11:30–21:00"
        },
        "rating": 4.5, "votes": 230,
        "description": "Clásico ramonense de hamburguesas, tacos, papas y batidos frente al Colegio Patriarca.",
        "menu": [
            {"item": "Hamburguesa Doble Buggy's con papas", "price": "₡4,200"},
            {"item": "Taco Gigante con papas", "price": "₡3,500"},
            {"item": "Chalupa Especial", "price": "₡2,900"}
        ]
    },
    {
        "name": "Hamburguesas JB",
        "category": "Comida Rápida y Pollo",
        "address": "Frente a la Bomba El Chury, San Ramón",
        "lat": 10.08266, "lng": -84.46931, "coordsApprox": False,
        "phone": "+506 2101-8484",
        "delivery": "+506 2101-8484",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:30", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–21:00"
        },
        "rating": 4.4, "votes": 165,
        "description": "Hamburguesas artesanales a la parrilla frente a Bomba Chury con servicio express directo.",
        "menu": [
            {"item": "JB Bacon Cheese Burger en combo", "price": "₡4,800"},
            {"item": "Hamburguesa Doble Smash", "price": "₡5,200"}
        ]
    },
    {
        "name": "Donde Rochi Pollo",
        "category": "Comida Rápida y Pollo",
        "address": "Costado oeste del Parque Central, contiguo a Tico Viajes, San Ramón Centro",
        "lat": 10.08727, "lng": -84.47075, "coordsApprox": False,
        "phone": "+506 2237-6942",
        "delivery": "+506 2101-7068",
        "whatsapp": "+506 2101-7068",
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–22:00"
        },
        "rating": 4.3, "votes": 110,
        "description": "Pollo frito crujiente, alitas y combos familiares al costado del Parque Central.",
        "menu": [
            {"item": "Combo 2 Piezas de Pollo + Papas + Refresco", "price": "₡3,100"},
            {"item": "Balde Familiar 8 Piezas", "price": "₡8,900"}
        ]
    },
    {
        "name": "Pollo Delicias",
        "category": "Comida Rápida y Pollo",
        "address": "Costado oeste del Mercado Municipal de San Ramón",
        "lat": 10.08811, "lng": -84.4707, "coordsApprox": False,
        "phone": "+506 2445-5733",
        "delivery": "+506 2447-3535",
        "whatsapp": None,
        "hours": {
            "Mon": "10:00–21:00", "Tue": "10:00–21:00", "Wed": "10:00–21:00",
            "Thu": "10:00–21:00", "Fri": "10:00–21:00", "Sat": "10:00–21:00", "Sun": "10:00–21:00"
        },
        "rating": 4.2, "votes": 95,
        "description": "Pollo frito y asado tradicional al costado del Mercado Municipal con express directo.",
        "menu": [
            {"item": "Pollo Entero Asado con tortillas y ensalada", "price": "₡7,800"},
            {"item": "Porción de Pollo Frito con papas", "price": "₡2,700"}
        ]
    },
    {
        "name": "Pollolandia (Centro / Empresarios Unidos)",
        "category": "Comida Rápida y Pollo",
        "address": "Frente a la parada de buses de Empresarios Unidos, San Ramón Centro",
        "lat": 10.08868, "lng": -84.47206, "coordsApprox": False,
        "phone": "+506 2447-0193",
        "delivery": "+506 2447-0193",
        "whatsapp": None,
        "hours": {
            "Mon": "09:00–21:00", "Tue": "09:00–21:00", "Wed": "09:00–21:00",
            "Thu": "09:00–21:00", "Fri": "09:00–21:00", "Sat": "09:00–21:00", "Sun": "09:00–21:00"
        },
        "rating": 4.1, "votes": 120,
        "description": "Sucursal céntrica de Pollolandia con piezas de pollo frito, alitas y combos económicos.",
        "menu": [
            {"item": "Combo 2 Piezas + Papas", "price": "₡2,650"},
            {"item": "Combo 6 Alitas + Papas", "price": "₡3,300"}
        ]
    },
    {
        "name": "Pollolandia (San Juan)",
        "category": "Comida Rápida y Pollo",
        "address": "Calle principal de San Juan de San Ramón",
        "lat": 10.09647, "lng": -84.46882, "coordsApprox": False,
        "phone": "+506 2447-3058",
        "delivery": "+506 2447-3058",
        "whatsapp": None,
        "hours": {
            "Mon": "09:00–21:00", "Tue": "09:00–21:00", "Wed": "09:00–21:00",
            "Thu": "09:00–21:00", "Fri": "09:00–21:00", "Sat": "09:00–21:00", "Sun": "09:00–21:00"
        },
        "rating": 4.1, "votes": 75,
        "description": "Sucursal de Pollolandia en San Juan con servicio para llevar y express.",
        "menu": [
            {"item": "Combo Personal Pollo Frito", "price": "₡2,650"},
            {"item": "Combo Familiar 8 piezas", "price": "₡8,400"}
        ]
    },
    {
        "name": "Heladería Pops San Ramón",
        "category": "Heladerías y Postres",
        "address": "Costado sur del Parque Central, San Ramón Centro",
        "lat": 10.08696, "lng": -84.47076, "coordsApprox": False,
        "phone": "+506 2447-6868",
        "delivery": "+506 2447-6868",
        "whatsapp": None,
        "hours": {
            "Mon": "09:00–21:00", "Tue": "09:00–21:00", "Wed": "09:00–21:00",
            "Thu": "09:00–21:00", "Fri": "09:00–21:00", "Sat": "09:00–21:00", "Sun": "09:00–21:00"
        },
        "rating": 4.6, "votes": 320,
        "description": "Heladería Pops en el corazón de San Ramón con conos, sundaes, batidos, banana split y queques helados.",
        "menu": [
            {"item": "Churchill Pops / Sundae Especial", "price": "₡2,750"},
            {"item": "Banana Split tradicional", "price": "₡3,650"},
            {"item": "Milkshake Suprema", "price": "₡2,850"},
            {"item": "Cono Doble", "price": "₡1,950"}
        ],
        "website": "https://pops.co.cr"
    },
    {
        "name": "Angelato Gelatería & Cafetería",
        "category": "Heladerías y Postres",
        "address": "Cercanías del Templo Parroquial, San Ramón Centro",
        "lat": 10.0862, "lng": -84.47007, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats",
        "whatsapp": None,
        "hours": {
            "Mon": "10:00–20:00", "Tue": "10:00–20:00", "Wed": "10:00–20:00",
            "Thu": "10:00–20:00", "Fri": "10:00–21:00", "Sat": "10:00–21:00", "Sun": "10:00–20:00"
        },
        "rating": 4.7, "votes": 115,
        "description": "Gelato artesanal italiano, malteadas de gelato, paninis de masa madre y café en el centro de San Ramón.",
        "menu": [
            {"item": "Copa de Gelato Artesanal (2 sabores)", "price": "₡2,400"},
            {"item": "Malteada de Gelato (Maracuyá, Pistacho o Chocolate)", "price": "₡2,900"},
            {"item": "Panini Caprese en pan de masa madre", "price": "₡3,800"}
        ]
    },
    {
        "name": "Panadería y Restaurante Sin Gluten Delicias Ubannia",
        "category": "Cafeterías y Panaderías",
        "address": "Barrio La Unión / San Rafael, San Ramón",
        "lat": 10.07548, "lng": -84.47893, "coordsApprox": False,
        "phone": "+506 8393-9493",
        "delivery": "+506 8393-9493",
        "whatsapp": "+506 8393-9493",
        "hours": {
            "Mon": "08:00–18:00", "Tue": "08:00–18:00", "Wed": "08:00–18:00",
            "Thu": "08:00–18:00", "Fri": "08:00–18:00", "Sat": "08:00–18:00", "Sun": "08:00–17:00"
        },
        "rating": 4.8, "votes": 85,
        "description": "Panadería y restaurante 100% libre de gluten en San Ramón con desayunos, almuerzos y repostería apta para celíacos.",
        "menu": [
            {"item": "Almuerzo Buffet 100% Libre de Gluten", "price": "₡4,500"},
            {"item": "Pan Artesanal Sin Gluten", "price": "₡2,800"},
            {"item": "Empanadas y Repostería Sin Gluten", "price": "₡1,600"}
        ]
    },
    {
        "name": "Bocaditos Bar & Restaurante",
        "category": "Bares y Cervecerías",
        "address": "300 m oeste del Hospital Carlos Luis Valverde Vega, San Ramón",
        "lat": 10.09259, "lng": -84.47235, "coordsApprox": False,
        "phone": None,
        "delivery": "Uber Eats",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–23:00", "Tue": "11:00–23:00", "Wed": "11:00–23:00",
            "Thu": "11:00–23:00", "Fri": "11:00–23:30", "Sat": "11:00–23:30", "Sun": "11:00–22:00"
        },
        "rating": 4.5, "votes": 423,
        "description": "Bar y restaurante muy popular al oeste del Hospital de San Ramón por sus bocas, chifrijo, carnes y ambiente social.",
        "menu": [
            {"item": "Chifrijo Bocaditos", "price": "₡3,600"},
            {"item": "Surtido de Carnes y Bocas", "price": "₡7,900"},
            {"item": "Fajitas de Lomito con papas", "price": "₡4,800"}
        ]
    },
    {
        "name": "Office Bar & Rest",
        "category": "Bares y Cervecerías",
        "address": "50 m oeste de la Heladería Pops, San Ramón Centro",
        "lat": 10.0869, "lng": -84.4713, "coordsApprox": False,
        "phone": "+506 4704-5737",
        "delivery": "+506 8642-5353",
        "whatsapp": "+506 8642-5353",
        "hours": {
            "Mon": "11:00–00:00", "Tue": "11:00–00:00", "Wed": "11:00–00:00",
            "Thu": "11:00–00:00", "Fri": "11:00–01:00", "Sat": "11:00–01:00", "Sun": "11:00–23:00"
        },
        "rating": 3.8, "votes": 80,
        "description": "Bar y restaurante céntrico con parrilla, alitas, bocas y transmisión de deportes.",
        "menu": [
            {"item": "Alitas BBQ / Buffalo con papas", "price": "₡4,500"},
            {"item": "Bocas de la Casa", "price": "₡2,800"}
        ]
    },
    {
        "name": "The Corner Pub",
        "category": "Bares y Cervecerías",
        "address": "200 m norte de Gollo (Calle 2), San Ramón Centro",
        "lat": 10.08621, "lng": -84.47426, "coordsApprox": False,
        "phone": "+506 2445-6902",
        "delivery": "+506 4035-6597",
        "whatsapp": None,
        "hours": {
            "Mon": "16:00–23:00", "Tue": "16:00–23:00", "Wed": "16:00–23:00",
            "Thu": "16:00–00:00", "Fri": "16:00–01:00", "Sat": "16:00–01:00", "Sun": "16:00–23:00"
        },
        "rating": 4.4, "votes": 130,
        "description": "Pub estilo inglés y bar deportivo con cervezas nacionales e importadas, hamburguesas y bocas.",
        "menu": [
            {"item": "Corner Burger con papas fritas", "price": "₡4,800"},
            {"item": "Nachos Pub", "price": "₡4,200"}
        ]
    },
    {
        "name": "Restaurante y Bar La Sala Kuarta",
        "category": "Bares y Cervecerías",
        "address": "Cercanías del Estadio Guillermo Vargas Roldán, San Ramón",
        "lat": 10.07782, "lng": -84.47219, "coordsApprox": False,
        "phone": "+506 4081-0476",
        "delivery": "+506 4081-0476",
        "whatsapp": None,
        "hours": {
            "Mon": "Cerrado", "Tue": "11:30–23:00", "Wed": "11:30–23:00",
            "Thu": "11:30–23:00", "Fri": "11:30–00:00", "Sat": "11:30–00:00", "Sun": "11:30–22:00"
        },
        "rating": 3.7, "votes": 37,
        "description": "Restaurante familiar y bar con picadas, carnes y música en vivo.",
        "menu": [
            {"item": "Surtido Sala Kuarta", "price": "₡7,500"},
            {"item": "Chifrijo Especial", "price": "₡3,500"}
        ]
    },
    {
        "name": "Tribu 506 Restaurant & Bar",
        "category": "Bares y Cervecerías",
        "address": "El Alto de Santiago, carretera hacia Puntarenas, San Ramón",
        "lat": 10.07055, "lng": -84.49025, "coordsApprox": False,
        "phone": "+506 8874-4040",
        "delivery": "+506 8874-4040",
        "whatsapp": "+506 8874-4040",
        "hours": {
            "Mon": "11:30–22:30", "Tue": "11:30–22:30", "Wed": "11:30–22:30",
            "Thu": "11:30–23:00", "Fri": "11:30–00:00", "Sat": "11:30–00:00", "Sun": "11:30–22:30"
        },
        "rating": 4.1, "votes": 777,
        "description": "Restaurante con mirador en El Alto de Santiago con parrilla, pizzas, mariscos y música en vivo.",
        "menu": [
            {"item": "Parrillada Tribu 506", "price": "₡8,900"},
            {"item": "Pizza Artesanal a la Leña", "price": "₡6,500"},
            {"item": "Ceviche y Bocas Ticas", "price": "₡3,600"}
        ]
    },
    {
        "name": "El Felipón (La Cantina de Felipón)",
        "category": "Bares y Cervecerías",
        "address": "75 m sur de la entrada a Santiago, carretera Interamericana, San Ramón",
        "lat": 10.06831, "lng": -84.49595, "coordsApprox": False,
        "phone": "+506 2445-3818",
        "delivery": "+506 2445-3818",
        "whatsapp": None,
        "hours": {
            "Mon": "09:00–17:00", "Tue": "16:00–23:00", "Wed": "16:00–23:00",
            "Thu": "16:00–23:00", "Fri": "16:00–23:00", "Sat": "11:00–23:00", "Sun": "11:00–23:00"
        },
        "rating": 4.3, "votes": 145,
        "description": "Restaurante y cantina tradicional en Santiago de San Ramón famosa por sus bocas y chifrijo.",
        "menu": [
            {"item": "Chifrijo de la Casa", "price": "₡3,400"},
            {"item": "Costilla de Cerdo frita con yuca", "price": "₡4,200"}
        ]
    },
    {
        "name": "Restaurante El Zafiro",
        "category": "Típica y Sodas",
        "address": "Volio de San Ramón, Alajuela",
        "lat": 10.12948, "lng": -84.4551, "coordsApprox": False,
        "phone": "+506 2447-2870",
        "delivery": "+506 2447-2870",
        "whatsapp": None,
        "hours": {
            "Mon": "11:00–00:00", "Tue": "11:00–00:00", "Wed": "11:00–00:00",
            "Thu": "11:00–00:00", "Fri": "11:00–00:00", "Sat": "11:00–00:00", "Sun": "11:00–00:00"
        },
        "rating": 3.9, "votes": 428,
        "description": "Tradicional bar y restaurante en el distrito de Volio de San Ramón.",
        "menu": [
            {"item": "Casado y Bocas Tradicionales", "price": "₡3,200"},
            {"item": "Pescado Entero Frito", "price": "₡5,500"}
        ]
    },
    {
        "name": "Restaurante Rancho San Rafael",
        "category": "Típica y Sodas",
        "address": "1 km sur de la Iglesia de San Rafael, San Ramón",
        "lat": 10.0580, "lng": -84.4720, "coordsApprox": True,
        "phone": "+506 8742-8806",
        "delivery": "+506 8742-8806",
        "whatsapp": "+506 8742-8806",
        "hours": {
            "Mon": "11:00–21:00", "Tue": "11:00–21:00", "Wed": "11:00–21:00",
            "Thu": "11:00–21:00", "Fri": "11:00–22:00", "Sat": "11:00–22:00", "Sun": "11:00–21:00"
        },
        "rating": 4.2, "votes": 38,
        "description": "Rancho campestre familiar en San Rafael para almuerzos típicos, tardes de café con empanadas y cenas.",
        "menu": [
            {"item": "Almuerzo Campestre en Rancho", "price": "₡3,800"},
            {"item": "Chicharrones con yuca al fogón", "price": "₡4,500"}
        ]
    },
    {
        "name": "El Bohío Cubano Bar & Restaurante",
        "category": "Internacional y Fusión",
        "address": "Ruta hacia Piedades Norte, San Ramón",
        "lat": 10.1050, "lng": -84.4820, "coordsApprox": True,
        "phone": "+506 2447-9995",
        "delivery": "+506 6282-8240",
        "whatsapp": "+506 6282-8240",
        "hours": {
            "Mon": "11:00–22:00", "Tue": "11:00–22:00", "Wed": "11:00–22:00",
            "Thu": "11:00–22:00", "Fri": "11:00–23:00", "Sat": "11:00–23:00", "Sun": "11:00–21:00"
        },
        "rating": 4.0, "votes": 48,
        "description": "Sabor cubano y caribeño en San Ramón: ropa vieja, lechón asado, moros y cristianos y mojitos.",
        "menu": [
            {"item": "Ropa Vieja con Moros y Cristianos", "price": "₡4,800"},
            {"item": "Sándwich Cubano tradicional", "price": "₡3,900"},
            {"item": "Mojito Cubano con hierbabuena", "price": "₡2,800"}
        ]
    },
    {
        "name": "Los Tajos Bar & Grill",
        "category": "Carnes y Parrilla",
        "address": "San Juan de San Ramón, Alajuela",
        "lat": 10.1030, "lng": -84.4640, "coordsApprox": True,
        "phone": "+506 8813-1104",
        "delivery": "+506 8813-1104",
        "whatsapp": "+506 8813-1104",
        "hours": {
            "Mon": "Cerrado", "Tue": "12:00–22:00", "Wed": "12:00–22:00",
            "Thu": "12:00–22:00", "Fri": "12:00–23:00", "Sat": "12:00–23:00", "Sun": "12:00–21:00"
        },
        "rating": 4.2, "votes": 45,
        "description": "Restaurante campestre y grill en San Juan rodeado de naturaleza.",
        "menu": [
            {"item": "Corte a la Parrilla Los Tajos", "price": "₡6,800"},
            {"item": "Bocas y Picadas al Carbón", "price": "₡4,200"}
        ]
    },
    {
        "name": "Ventanita Enseñas",
        "category": "Típica y Sodas",
        "address": "San Juan de San Ramón",
        "lat": 10.09871, "lng": -84.46845, "coordsApprox": False,
        "phone": "+506 8513-3808",
        "delivery": "+506 8513-3808",
        "whatsapp": "+506 8513-3808",
        "hours": {
            "Mon": "07:00–19:00", "Tue": "07:00–19:00", "Wed": "07:00–19:00",
            "Thu": "07:00–19:00", "Fri": "07:00–19:00", "Sat": "07:00–19:00", "Sun": "Cerrado"
        },
        "rating": 4.7, "votes": 55,
        "description": "Inclusiva ventanita en San Juan especializada en pupusas, empanadas, casados, gallitos y café.",
        "menu": [
            {"item": "Pupusas revueltas o de queso con curtido", "price": "₡1,500"},
            {"item": "Casado Casero", "price": "₡3,200"},
            {"item": "Empanadas de maíz", "price": "₡1,200"}
        ]
    },
    {
        "name": "Las Tardes Café & Restaurante",
        "category": "Cafeterías y Panaderías",
        "address": "Piedades Norte de San Ramón",
        "lat": 10.13656, "lng": -84.51487, "coordsApprox": False,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": {
            "Mon": "09:00–21:00", "Tue": "09:00–21:00", "Wed": "09:00–21:00",
            "Thu": "09:00–21:00", "Fri": "09:00–21:00", "Sat": "09:00–21:00", "Sun": "09:00–21:00"
        },
        "rating": 4.5, "votes": 60,
        "description": "Cafetería de montaña en Piedades Norte con café regional, sándwiches y hamburguesas.",
        "menu": [
            {"item": "Sándwich Artesanal con papas", "price": "₡3,500"},
            {"item": "Hamburguesa de la Casa", "price": "₡4,200"},
            {"item": "Café Chorreado con repostería", "price": "₡2,100"}
        ]
    },
    {
        "name": "Restaurante Cloud Forest (Villa Blanca)",
        "category": "Internacional y Fusión",
        "address": "El Silencio de Los Ángeles Norte, Ruta 702, San Ramón",
        "lat": 10.13628, "lng": -84.47552, "coordsApprox": False,
        "phone": "+506 2401-3800",
        "delivery": None,
        "whatsapp": "+506 8568-9848",
        "hours": {
            "Mon": "06:30–21:00", "Tue": "06:30–21:00", "Wed": "06:30–21:00",
            "Thu": "06:30–21:00", "Fri": "06:30–21:00", "Sat": "06:30–21:00", "Sun": "06:30–21:00"
        },
        "rating": 4.8, "votes": 210,
        "description": "Restaurante rodeado de bosque nuboso en Los Ángeles de San Ramón con ingredientes de su propia huerta orgánica.",
        "menu": [
            {"item": "Trucha del Bosque Nuboso a la plancha", "price": "₡8,900"},
            {"item": "Lomito en salsa de café ramonense", "price": "₡10,500"},
            {"item": "Sopa Crema de Ayote orgánico", "price": "₡4,200"}
        ],
        "website": "https://hotelvbcostarica.com"
    },
    {
        "name": "Loveat (Lands in Love Vegan Restaurant)",
        "category": "Internacional y Fusión",
        "address": "Ruta 702 hacia La Fortuna, San Lorenzo de San Ramón",
        "lat": 10.27071, "lng": -84.52627, "coordsApprox": False,
        "phone": "+506 2445-9333",
        "delivery": None,
        "whatsapp": None,
        "hours": {
            "Mon": "07:30–21:00", "Tue": "07:30–21:00", "Wed": "07:30–21:00",
            "Thu": "07:30–21:00", "Fri": "07:30–21:00", "Sat": "07:30–21:00", "Sun": "07:30–21:00"
        },
        "rating": 4.7, "votes": 380,
        "description": "Restaurante 100% vegetariano y vegano en medio del bosque nuboso sobre la Ruta 702 en San Lorenzo de San Ramón.",
        "menu": [
            {"item": "Plato Mediterráneo Vegano (Hummus, Falafel, Pita)", "price": "₡6,200"},
            {"item": "Pad Thai Plant-Based", "price": "₡5,800"},
            {"item": "Beyond Burger con papas rústicas", "price": "₡6,500"}
        ],
        "website": "https://landsinlove.com"
    },
    {
        "name": "La Casona Mía",
        "category": "Típica y Sodas",
        "address": "Bajo Rodríguez / San Lorenzo, Ruta 702, San Ramón",
        "lat": 10.29736, "lng": -84.52837, "coordsApprox": False,
        "phone": "+506 2475-1711",
        "delivery": "+506 2475-1711",
        "whatsapp": None,
        "hours": {
            "Mon": "06:30–21:00", "Tue": "06:30–21:00", "Wed": "06:30–21:00",
            "Thu": "06:30–21:00", "Fri": "06:30–21:00", "Sat": "06:30–21:00", "Sun": "06:30–21:00"
        },
        "rating": 4.4, "votes": 140,
        "description": "Parada tradicional en San Lorenzo de San Ramón sobre la Ruta 702 con desayunos y casados.",
        "menu": [
            {"item": "Casado Típico Casona Mía", "price": "₡3,600"},
            {"item": "Desayuno Completo de Carretera", "price": "₡2,900"}
        ]
    },
    {
        "name": "Restaurante Leonardo's",
        "category": "Carnes y Parrilla",
        "address": "Ruta 702, San Isidro de Peñas Blancas, San Ramón",
        "lat": 10.37483, "lng": -84.58985, "coordsApprox": False,
        "phone": "+506 8467-4767",
        "delivery": "+506 8341-8135",
        "whatsapp": "+506 8467-4767",
        "hours": {
            "Mon": "12:00–21:00", "Tue": "12:00–21:00", "Wed": "12:00–21:00",
            "Thu": "12:00–21:00", "Fri": "12:00–21:00", "Sat": "12:00–21:00", "Sun": "12:00–21:00"
        },
        "rating": 4.6, "votes": 165,
        "description": "Steakhouse, mariscos y comida típica sobre la Ruta 702 en Peñas Blancas de San Ramón.",
        "menu": [
            {"item": "Lomito Leonardo's a la parrilla", "price": "₡7,900"},
            {"item": "Filete de Pescado en Salsa de Mariscos", "price": "₡6,800"}
        ],
        "website": "https://leonardosrestaurante.com"
    },
    {
        "name": "La Mesa de Mamá",
        "category": "Típica y Sodas",
        "address": "Costado sureste de la Escuela de El Castillo, Peñas Blancas de San Ramón",
        "lat": 10.42727, "lng": -84.75017, "coordsApprox": False,
        "phone": "+506 2479-1954",
        "delivery": "+506 2479-1954",
        "whatsapp": None,
        "hours": {
            "Mon": "08:00–22:00", "Tue": "08:00–22:00", "Wed": "08:00–22:00",
            "Thu": "08:00–22:00", "Fri": "08:00–22:00", "Sat": "08:00–22:00", "Sun": "08:00–22:00"
        },
        "rating": 4.7, "votes": 190,
        "description": "Comida típica costarricense al fogón en El Castillo de Peñas Blancas (cantón de San Ramón).",
        "menu": [
            {"item": "Casado Típico al Fogón", "price": "₡4,200"},
            {"item": "Sopa Negra con huevo y arroz", "price": "₡3,400"}
        ]
    },
    {
        "name": "Panadería y Repostería Karen",
        "category": "Cafeterías y Panaderías",
        "address": "Costado norte del Mercado Municipal (Calle 2 / Av. 3), San Ramón Centro",
        "lat": 10.08980, "lng": -84.47127, "coordsApprox": False,
        "phone": "+506 2445-6271",
        "delivery": "+506 2445-6271",
        "whatsapp": None,
        "hours": {
            "Mon": "06:30–18:00", "Tue": "06:30–18:00", "Wed": "06:30–18:00",
            "Thu": "06:30–18:00", "Fri": "06:30–18:00", "Sat": "06:30–18:00", "Sun": "07:00–13:00"
        },
        "rating": 4.5, "votes": 42,
        "description": "Panadería, repostería y cafetería tradicional en el centro de San Ramón con pan fresco recién horneado y repostería dulce y salada.",
        "menu": [
            {"item": "Baguette / Pan Casero recién horneado", "price": "₡1,100"},
            {"item": "Arrollado de Canela / Pañuelo de Queso", "price": "₡950"},
            {"item": "Empanada de Pollo o Carne", "price": "₡1,150"},
            {"item": "Café Chorreado o Con Leche", "price": "₡1,000"}
        ]
    },
    {
        "name": "Soda y Pollería Kairós",
        "category": "Comida Rápida y Pollo",
        "address": "Frente al parqueo de la Gran Bodega de Frutas y Verduras, San Ramón",
        "lat": 10.08940, "lng": -84.47280, "coordsApprox": True,
        "phone": "+506 2445-0061",
        "delivery": "+506 2445-0061",
        "whatsapp": "+506 8568-6056",
        "hours": {
            "Mon": "10:00–21:00", "Tue": "10:00–21:00", "Wed": "10:00–21:00",
            "Thu": "10:00–21:00", "Fri": "10:00–21:30", "Sat": "10:00–21:30", "Sun": "10:00–21:00"
        },
        "rating": 4.4, "votes": 56,
        "description": "Soda y pollería local famosa por su pollo frito estilo broaster, combos con papas y comidas rápidas con servicio express.",
        "menu": [
            {"item": "Combo 2 Piezas de Pollo Frito + Papas + Refresco", "price": "₡3,600"},
            {"item": "Porción de Pollo a la Broaster con papas", "price": "₡2,750"},
            {"item": "Balde Familiar 8 Piezas de Pollo + Acompañamientos", "price": "₡10,500"}
        ]
    },
    {
        "name": "K-Harina (Soda K-Harina)",
        "category": "Típica y Sodas",
        "address": "El Salvador de Piedades Sur (junto al Salón Comunal de El Salvador, Plus Code 39PR+G3), Piedades Sur, San Ramón",
        "lat": 10.08631, "lng": -84.60981, "coordsApprox": False,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": {
            "Mon": "07:00–18:00", "Tue": "07:00–18:00", "Wed": "07:00–18:00",
            "Thu": "07:00–18:00", "Fri": "07:00–19:00", "Sat": "07:00–19:00", "Sun": "07:00–17:00"
        },
        "rating": 4.8, "votes": 19,
        "description": "Soda y mirador de montaña en El Salvador de Piedades Sur con vistas panorámicas, arte local, repostería y comida casera costarricense (K-Harina / Karina).",
        "menu": [
            {"item": "Casado Típico Casero", "price": "₡3,500"},
            {"item": "Gallo Pinto Campesino con huevos y queso", "price": "₡2,800"},
            {"item": "Empanadas / Repostería artesanal con Café Chorreado", "price": "₡1,800"}
        ],
        "website": "https://wanderboat.ai/restaurants/costa-rica/piedades-sur/k-harina/_DsdzxwXQgSJBTDRktzOeA"
    },
    {
        "name": "Maos Chicken and Wings",
        "category": "Comida Rápida y Pollo",
        "address": "La Guaria, Piedades Sur, San Ramón",
        "lat": 10.05650, "lng": -84.53900, "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": None,
        "rating": 4.5, "votes": 22,
        "description": "Especialidad en pollo frito, alitas bañadas en salsas y comida rápida en La Guaria de Piedades Sur.",
        "menu": [
            {"item": "Orden de Alitas (6 uds) con papas", "price": "₡3,800"},
            {"item": "Combo Pollo Frito + Papas", "price": "₡3,500"}
        ]
    },
    {
        "name": "Rancho-Palenque Río Piedras",
        "category": "Típica y Sodas",
        "address": "Cerca del CTP de Piedades Sur, Piedades Sur, San Ramón",
        "lat": 10.05100, "lng": -84.53650, "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": None,
        "rating": 4.6, "votes": 28,
        "description": "Restaurante rústico tipo rancho rodeado de naturaleza en Piedades Sur.",
        "menu": [
            {"item": "Casado Típico en Leña", "price": "₡3,800"},
            {"item": "Chifrijo de la Casa", "price": "₡3,400"}
        ]
    },
    {
        "name": "Finca Agroturística Veraká",
        "category": "Típica y Sodas",
        "address": "Potrerillos de Piedades Sur, San Ramón",
        "lat": 10.06800, "lng": -84.55800, "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": None,
        "rating": 4.7, "votes": 31,
        "description": "Finca agroturística y restaurante campestre en Potrerillos de Piedades Sur con gastronomía local.",
        "menu": [
            {"item": "Almuerzo Campesino Tradicional", "price": "₡4,200"},
            {"item": "Café de Altura con Tamal o Tortilla", "price": "₡2,200"}
        ]
    },
    {
        "name": "Casa Blanca Street Food",
        "category": "Comida Rápida y Pollo",
        "address": "Frente a El Lagar, Calle Tremedal, San Ramón",
        "lat": 10.08350, "lng": -84.46750, "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": None,
        "rating": 4.5, "votes": 26,
        "description": "Comida urbana, hamburguesas y street food frente a El Lagar en Tremedal de San Ramón.",
        "menu": [
            {"item": "Hamburguesa Artesanal con papas", "price": "₡4,500"}
        ]
    },
    {
        "name": "Tako's Street Food San Ramón",
        "category": "Mexicana",
        "address": "100 m este del Banco Nacional (Av. 2), San Ramón Centro",
        "lat": 10.08780, "lng": -84.46920, "coordsApprox": False,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": None,
        "rating": 4.5, "votes": 34,
        "description": "Taquería y street food céntrico a 100 m este del Banco Nacional en San Ramón.",
        "menu": [
            {"item": "Orden de Tacos Callejeros (3 uds)", "price": "₡3,600"},
            {"item": "Quesadilla / Burrito", "price": "₡3,900"}
        ]
    }
]

by_key = {}
items = []

for c in CURATED:
    k = norm_name(c["name"])
    c["district"] = get_district(c["lat"], c["lng"])
    c["source"] = "OSM + Web verificada"
    by_key[k] = c
    items.append(c)

# Add explicit aliases for OSM/RG deduplication
ALIASES = {
    "aromas": "aromas",
    "calatheaaromas": "aromas",
    "angelato": "angelatogelatoria",
    "pops": "pops",
    "buggys": "buggysburgers",
    "chepers": "chepes",
    "cheppers": "chepes",
    "nazca": "peruanonazca",
    "pizzaloca": "mipueblopizzaloca",
    "elestablo": "elestablo",
    "tribu": "tribu506",
    "olaola": "olaola",
    "rincon": "rincon",
    "cocinam": "cocinam",
    "cocinama": "cocinam",
    "felipon": "felipon",
    "cloudforest": "cloudforest",
    "loveat": "loveat",
    "kaluas": "kalhuas",
    "carmensita": "carmencita"
}

osm = json.load(open("data/osm_canton.json"))["elements"]

AMENITY_CAT = {
    "restaurant": "Típica y Sodas",
    "fast_food": "Comida Rápida y Pollo",
    "cafe": "Cafeterías y Panaderías",
    "bar": "Bares y Cervecerías",
    "pub": "Bares y Cervecerías",
    "ice_cream": "Heladerías y Postres",
    "food_court": "Comida Rápida y Pollo"
}

CUISINE_CAT = {
    "pizza": "Italiana y Pizzería",
    "italian": "Italiana y Pizzería",
    "chinese": "Asiática y Sushi",
    "japanese": "Asiática y Sushi",
    "sushi": "Asiática y Sushi",
    "seafood": "Marisquerías y Ceviches",
    "mexican": "Mexicana",
    "tex-mex": "Comida Rápida y Pollo",
    "chicken": "Comida Rápida y Pollo",
    "burger": "Comida Rápida y Pollo",
    "coffee_shop": "Cafeterías y Panaderías",
    "bubble_tea": "Heladerías y Postres",
    "juice": "Heladerías y Postres",
    "frozen_yogurt": "Heladerías y Postres",
    "mediterranean": "Internacional y Fusión"
}

def is_dup(k):
    k2 = ALIASES.get(k, k)
    if k2 in by_key:
        return by_key[k2]
    for bk, obj in by_key.items():
        if len(k2) >= 5 and len(bk) >= 5 and (k2 in bk or bk in k2):
            return obj
    return None

for e in osm:
    t = e.get("tags", {})
    name = t.get("name")
    if not name:
        continue
    lat = e.get("lat") or e.get("center", {}).get("lat")
    lng = e.get("lon") or e.get("center", {}).get("lon")
    if not lat or not lng:
        continue
    k = norm_name(name)
    if "pollolandia" in k:
        if any(abs(x["lat"]-lat)<0.002 and abs(x["lng"]-lng)<0.002 for x in items if "pollolandia" in x["name"].lower()):
            continue
        name = f"Pollolandia ({get_district(lat, lng)})"
    else:
        existing = is_dup(k)
        if existing:
            if existing.get("coordsApprox"):
                existing["lat"] = round(lat, 5)
                existing["lng"] = round(lng, 5)
                existing["coordsApprox"] = False
                existing["district"] = get_district(lat, lng)
            continue

    cuis = (t.get("cuisine") or "").lower().split(";")[0]
    cat = CUISINE_CAT.get(cuis) or AMENITY_CAT.get(t.get("amenity"), "Típica y Sodas")
    nl = name.lower()
    if "pizza" in nl or "pizzer" in nl: cat = "Italiana y Pizzería"
    elif "sushi" in nl or "chino" in nl or "china" in nl: cat = "Asiática y Sushi"
    elif "ceviche" in nl or "marisc" in nl or "marisq" in nl: cat = "Marisquerías y Ceviches"
    elif "bar" in nl or "pub" in nl or "cantina" in nl: cat = "Bares y Cervecerías"
    elif "cafe" in nl or "café" in nl or "panader" in nl: cat = "Cafeterías y Panaderías"
    elif "pollo" in nl or "wings" in nl or "burger" in nl or "hamburg" in nl: cat = "Comida Rápida y Pollo"

    dist = get_district(lat, lng)
    street = t.get("addr:street")
    addr = f"{street}, {dist}, San Ramón" if street else f"Distrito {dist}, San Ramón, Alajuela"
    phone = t.get("phone") or t.get("contact:phone") or t.get("mobile")
    oh = t.get("opening_hours")
    hours = None
    if oh:
        hours = {"Mon": oh, "Tue": oh, "Wed": oh, "Thu": oh, "Fri": oh, "Sat": oh, "Sun": oh}

    obj = {
        "name": name,
        "category": cat,
        "address": addr,
        "district": dist,
        "lat": round(lat, 5),
        "lng": round(lng, 5),
        "coordsApprox": False,
        "phone": phone,
        "delivery": phone,
        "whatsapp": t.get("contact:whatsapp"),
        "hours": hours,
        "rating": None,
        "votes": None,
        "description": f"Establecimiento registrado en OpenStreetMap en el distrito de {dist}, San Ramón.",
        "menu": [],
        "website": t.get("website"),
        "source": "OpenStreetMap"
    }
    by_key[k] = obj
    items.append(obj)

rg60 = json.load(open("data/rg_60.json"))
import random
random.seed(42)

for r in rg60:
    name = r["name"].replace("• San Ramón", "").replace("San Ramón", "").strip() or r["name"]
    k = norm_name(name)
    existing = is_dup(k)
    if existing:
        if not existing.get("rating") and r.get("rating"):
            try: existing["rating"] = float(r["rating"])
            except: pass
        if not existing.get("votes") and r.get("votes"):
            m = re.search(r"\d+", r["votes"])
            if m: existing["votes"] = int(m.group(0))
        continue

    lat = round(10.0872 + random.uniform(-0.008, 0.008), 5)
    lng = round(-84.4705 + random.uniform(-0.008, 0.008), 5)
    dist = get_district(lat, lng)
    nl = (r["name"] + " " + r["type"]).lower()
    cat = "Típica y Sodas"
    if "pizza" in nl or "pizzeria" in nl: cat = "Italiana y Pizzería"
    elif "sushi" in nl or "chinese" in nl or "asian" in nl: cat = "Asiática y Sushi"
    elif "seafood" in nl or "marisc" in nl or "marisq" in nl: cat = "Marisquerías y Ceviches"
    elif "pub" in nl or "bar" in nl: cat = "Bares y Cervecerías"
    elif "coffee" in nl or "cafe" in nl: cat = "Cafeterías y Panaderías"
    elif "fast food" in nl or "pollo" in nl or "hamburg" in nl: cat = "Comida Rápida y Pollo"
    elif "bbq" in nl or "steak" in nl or "grill" in nl: cat = "Carnes y Parrilla"

    votes_num = None
    if r.get("votes"):
        m = re.search(r"\d+", r["votes"])
        if m: votes_num = int(m.group(0))
    rating_num = None
    if r.get("rating"):
        try: rating_num = float(r["rating"])
        except: pass

    obj = {
        "name": r["name"].replace("• San Ramón", "").strip(),
        "category": cat,
        "address": f"San Ramón, Alajuela ({dist})",
        "district": dist,
        "lat": lat,
        "lng": lng,
        "coordsApprox": True,
        "phone": None,
        "delivery": None,
        "whatsapp": None,
        "hours": None,
        "rating": rating_num,
        "votes": votes_num,
        "description": f"Local gastronómico en San Ramón listado en guías locales ({r['type'] or cat}).",
        "menu": [],
        "website": r.get("url"),
        "source": "Restaurant Guru"
    }
    by_key[k] = obj
    items.append(obj)

from apply_verification import apply_google_verification
items = apply_google_verification(items, get_district)

for idx, it in enumerate(items, 1):
    it["id"] = idx
    score = 0
    if it.get("phone") or it.get("whatsapp"): score += 3
    if it.get("menu"): score += len(it["menu"])
    if it.get("hours"): score += 2
    if it.get("rating"): score += 1
    if not it.get("coordsApprox"): score += 1
    it["infoScore"] = score

items.sort(key=lambda x: (-x["infoScore"], x["name"]))
for idx, it in enumerate(items, 1):
    it["id"] = idx

with open("data/restaurants.json", "w") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

with open("data/restaurants.js", "w") as f:
    f.write("window.SAN_RAMON_RESTAURANTS = " + json.dumps(items, ensure_ascii=False) + ";\n")

print(f"Total places: {len(items)} (viveros: {sum(1 for x in items if x.get('type') == 'vivero')}, gasolineras: {sum(1 for x in items if x.get('type') == 'gasolinera')})")
print("With phone/express:", sum(1 for x in items if x.get("phone") or x.get("delivery") or x.get("whatsapp")))
print("With menu items:", sum(1 for x in items if x.get("menu")))
print("With schedule:", sum(1 for x in items if x.get("hours")))
from collections import Counter
print("By category:", Counter(x["category"] for x in items))
print("By district:", Counter(x["district"] for x in items))
