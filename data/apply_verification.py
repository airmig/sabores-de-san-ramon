# -*- coding: utf-8 -*-
"""Aplica la verificación de Google Maps (data/google_maps_verified.json) a la lista
construida por build_restaurants.py:

* corrige coordenadas, horarios, calificaciones y teléfonos faltantes de los lugares existentes;
* elimina los cerrados permanentemente y los duplicados;
* agrega restaurantes nuevos encontrados por distrito, los viveros (type = "vivero")
  y las gasolineras (type = "gasolinera").
"""
import json, math, os, re, unicodedata, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
STOP = set("restaurante restaurant rest soda bar pizzeria cafeteria cafe marisqueria heladeria "
           "panaderia san ramon de del la el los las y and express expres steak house alajuela the e en al".split())
GENERIC_ADDR = re.compile(r"^(San Ramón, Alajuela \(|Distrito )")


def _ascii(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def _toks(s):
    s = re.sub(r"\([^)]*\)", " ", _ascii(s)).replace("'", "")
    return [t for t in re.findall(r"[a-z0-9]+", s) if t not in STOP]


def name_level(a, b):
    """0 = distinto, 1 = parecido, 2 = muy parecido, 3 = mismo nombre."""
    if not a or not b:
        return 0
    na, nb = "".join(_toks(a)), "".join(_toks(b))
    if not na or not nb:
        ra, rb = re.sub(r"[^a-z0-9]", "", _ascii(a)), re.sub(r"[^a-z0-9]", "", _ascii(b))
        return 3 if ra == rb else 0
    if na == nb:
        return 3
    ta, tb = set(_toks(a)), set(_toks(b))
    short, long_ = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    if len(short) >= 2 and short <= long_:
        return 3
    r = difflib.SequenceMatcher(None, na, nb).ratio()
    if (len(na) >= 5 and len(nb) >= 5 and (na in nb or nb in na)) or r >= 0.85:
        return 2
    return 1 if r >= 0.75 else 0


def km(a, b):
    p = math.pi / 180
    x = (math.sin((b["lat"] - a["lat"]) * p / 2) ** 2 +
         math.cos(a["lat"] * p) * math.cos(b["lat"] * p) * math.sin((b["lng"] - a["lng"]) * p / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(x))


def _same_place(a, b):
    d = km(a, b)
    lv = name_level(a["name"], b["name"])
    return (lv == 3 and d < 0.15) or (lv == 2 and d < 0.03)


def _richness(it):
    return (len(it.get("menu") or []) * 2 + bool(it.get("phone")) + bool(it.get("hours")) +
            bool(it.get("description")) + ("Web verificada" in (it.get("source") or "")))


def _merge(keep, drop):
    for f in ("phone", "delivery", "whatsapp", "hours", "website", "rating", "votes", "status"):
        if not keep.get(f) and drop.get(f):
            keep[f] = drop[f]
    if not keep.get("menu") and drop.get("menu"):
        keep["menu"] = drop["menu"]


def _description(o, district):
    gcat = o.get("gcat")
    if o["type"] == "vivero":
        what = gcat or "Vivero"
        if district == "Fuera del cantón":
            return (f"{what} fuera del cantón de San Ramón, a unos {o.get('distanceKm', '?')} km del centro. "
                    "Datos verificados en Google Maps.")
        return f"{what} en el distrito de {district}, San Ramón. Datos verificados en Google Maps."
    if o["type"] == "gasolinera":
        return f"Gasolinera en el distrito de {district}, San Ramón. Datos verificados en Google Maps."
    return f"{gcat or 'Restaurante'} en el distrito de {district}, San Ramón. Datos verificados en Google Maps."


def apply_google_verification(items, get_district, path=None):
    data = json.load(open(path or os.path.join(HERE, "google_maps_verified.json"), encoding="utf-8"))
    updates, removes = data["updates"], data["removes"]
    src_tag = f"Google Maps ({data.get('checked', '')})".replace(" ()", "")
    stats = {"verificados": 0, "sin_verificar": 0, "eliminados": 0, "duplicados": 0,
             "nuevos_restaurantes": 0, "viveros": 0, "gasolineras": 0}

    out = []
    for it in items:
        it.setdefault("type", "restaurante")
        if it["name"] in removes:
            stats["eliminados"] += 1
            continue
        u = updates.get(it["name"])
        if u:
            it["lat"], it["lng"] = round(u["lat"], 6), round(u["lng"], 6)
            it["coordsApprox"] = False
            it["district"] = get_district(it["lat"], it["lng"])
            if u.get("hours"):
                it["hours"] = u["hours"]
            for f in ("rating", "votes"):
                if u.get(f) is not None:
                    it[f] = u[f]
            if u.get("phone") and not it.get("phone"):
                it["phone"] = u["phone"]
            if u.get("website") and not it.get("website"):
                it["website"] = u["website"]
            if u.get("address") and GENERIC_ADDR.match(it.get("address") or ""):
                it["address"] = u["address"]
            if u.get("status"):
                it["status"] = u["status"]
            it["verified"] = True
            it["googleName"] = u.get("gname")
            if src_tag not in (it.get("source") or ""):
                it["source"] = f"{it.get('source')} + {src_tag}" if it.get("source") else src_tag
            stats["verificados"] += 1
        else:
            it["verified"] = False
            stats["sin_verificar"] += 1
        out.append(it)

    # duplicates that now share the same verified location
    deduped = []
    for it in out:
        twin = next((d for d in deduped if _same_place(d, it)), None)
        if twin:
            keep, drop = (twin, it) if _richness(twin) >= _richness(it) else (it, twin)
            _merge(keep, drop)
            if keep is it:
                deduped[deduped.index(twin)] = it
            stats["duplicados"] += 1
            continue
        deduped.append(it)

    for a in data["adds"]:
        if any(_same_place(d, a) for d in deduped):
            stats["duplicados"] += 1
            continue
        district = a["district"] if a["district"] == "Fuera del cantón" else get_district(a["lat"], a["lng"])
        obj = {
            "name": a["name"],
            "type": a["type"],
            "category": a["category"],
            "address": a.get("address") or (f"{district}, San Ramón, Alajuela" if district != "Fuera del cantón" else "Alajuela"),
            "district": district,
            "lat": a["lat"],
            "lng": a["lng"],
            "coordsApprox": False,
            "phone": a.get("phone"),
            "delivery": None,
            "whatsapp": None,
            "hours": a.get("hours"),
            "rating": a.get("rating"),
            "votes": a.get("votes"),
            "description": _description(a, district),
            "menu": [],
            "website": a.get("website"),
            "source": src_tag,
            "verified": True,
        }
        if a.get("status"):
            obj["status"] = a["status"]
        if a.get("distanceKm") is not None:
            obj["distanceKm"] = a["distanceKm"]
        deduped.append(obj)
        stats[{"vivero": "viveros", "gasolinera": "gasolineras"}.get(a["type"], "nuevos_restaurantes")] += 1

    print("Verificación Google Maps:", stats)
    return deduped
