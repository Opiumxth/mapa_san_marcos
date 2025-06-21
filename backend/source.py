import folium

latitude = -12.056948933839282
longitude = -77.08453591307409
m = folium.Map(location=[latitude, longitude], zoom_start=15)
puntos = []

def agregar_punto(lon, lat):
    puntos.append((lat, lon))
    print(f"Punto agregado: ({lat}, {lon})")

from folium.plugins import Draw

draw = Draw(
    export=True,
    draw_options={
        'polyline': False,
        'polygon': False,
        'rectangle': False,
        'circle': False,
        'marker': True
    }
)

draw.add_to(m)
m