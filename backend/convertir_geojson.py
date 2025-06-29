import json
import math

def norma(p1, p2):
    """Calcula la distancia entre dos puntos"""
    return round(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2), 2)

def convertir_geojson(geojson_path, nodos_out, aristas_out):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodos = []
    aristas = []
    coords_map = {}  # Mapea IDs a coordenadas para calcular pesos

    for feature in data['features']:
        tipo = feature['geometry']['type']
        props = feature['properties']

        if tipo == "Point":
            id_nodo = props.get("id")
            x, y = feature['geometry']['coordinates']
            nodos.append({
                "id": id_nodo,
                "x": x,
                "y": y
            })
            coords_map[id_nodo] = (x, y)

        elif tipo == "LineString":
            origen = props.get("origen")
            destino = props.get("destino")

            if origen in coords_map and destino in coords_map:
                peso = norma(coords_map[origen], coords_map[destino])
                aristas.append({
                    "origen": origen,
                    "destino": destino,
                    "peso": peso
                })
            else:
                print(f"Advertencia: origen o destino no encontrados en nodos ({origen}, {destino})")

    with open(nodos_out, 'w', encoding='utf-8') as f:
        json.dump(nodos, f, indent=4)

    with open(aristas_out, 'w', encoding='utf-8') as f:
        json.dump(aristas, f, indent=4)

    print(f"Archivos generados: {nodos_out} y {aristas_out}")

if __name__ == "__main__":
    convertir_geojson(
        geojson_path="backend/mapa.geojson",     # Ruta a tu archivo .geojson
        nodos_out="backend/nodos.json",          # Salida para nodos
        aristas_out="backend/aristas.json"       # Salida para aristas
    )