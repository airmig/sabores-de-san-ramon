# Sabores de San Ramón

Mapa interactivo de restaurantes, sodas, cafeterías, bares y viveros de San Ramón, Alajuela, Costa Rica.

**Ver el mapa:** https://airmig.github.io/sabores-de-san-ramon/

- Filtro por tipo: Todos, Restaurantes o Viveros.
- Filtros por categoría, distrito, abierto ahora, con teléfono y con menú.
- Ficha de cada lugar con dirección, teléfono, horario, calificación y enlaces a Waze y Google Maps.

## Datos

Los datos combinan OpenStreetMap, investigación web pública y una verificación en Google Maps (octubre 2026).
Verifique horarios y precios antes de visitar.

Para regenerar `data/restaurants.json` y `data/restaurants.js`:

```bash
python3 data/build_restaurants.py
```

El script aplica las correcciones de `data/google_maps_verified.json` mediante `data/apply_verification.py`.

## Ejecutar localmente

Es un sitio estático. Sirva la carpeta con cualquier servidor web:

```bash
python3 -m http.server 8000
```
