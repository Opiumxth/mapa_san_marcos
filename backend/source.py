import networkx as nx
import matplotlib.pyplot as plt

def norma(p1, p2):
    return round((((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5),2)

def sonIguales(p1, p2, tolerancia=1e-6):
    return abs(p1[0] - p2[0]) <= tolerancia and abs(p1[1] - p2[1]) <= tolerancia

def distanciaCamino(P, A, B):
    x0, y0 = P
    x1, y1 = A
    x2, y2 = B

    productoEscalar = (x2 - x1)*(x0 - x1) + (y2 - y1)*(y0 - y1)

    if norma(A, B)**2 == 0:
        return A, norma(A, P)

    escalar = max(0, min(1, productoEscalar/norma(A, B)**2))
    proyX = x1 + escalar*(x2 - x1)
    proyY = y1 + escalar*(y2 - y1)
    puntoProy = (proyX, proyY)
    return puntoProy, norma(P, puntoProy)


def dijkstra(G, inicio, fin):
    infinito = float('inf')
    vertices = list(G.nodes)
    distancias = {nodo: infinito for nodo in vertices}
    fijos = {nodo: False for nodo in vertices}
    padres = {nodo: None for nodo in vertices}

    distancias[inicio] = 0
    fijos[inicio] = True
    nuevoFijo = inicio

    while not all(fijos.values()):
        for vecino in G.neighbors(nuevoFijo):
            if not fijos[vecino]:
                nuevaDist = distancias[nuevoFijo] + G[nuevoFijo][vecino]['weight']
                if distancias[vecino] > nuevaDist:
                    distancias[vecino] = nuevaDist
                    padres[vecino] = nuevoFijo

        menorDist = infinito
        for nodo in vertices:
            if not fijos[nodo] and distancias[nodo] < menorDist:
                menorDist = distancias[nodo]
                candidato = nodo

        nuevoFijo = candidato
        fijos[nuevoFijo] = True

        if nuevoFijo == fin:
            camino = [fin]
            while camino[0] != inicio:
                camino.insert(0, padres[camino[0]])
            return distancias[fin], camino

G = nx.Graph()

pos = {
    "A": (0,0),
    "B": (-4.9,0),
    "C": (-0.9,10),
    "D": (-4,-3),
    "E": (0.4,4),
    "F": (-8,3),
    "G": (-8,9)
}

G.add_edge("A", "B", weight=norma(pos["A"], pos["B"]))
G.add_edge("B", "C", weight=norma(pos["B"], pos["C"]))
G.add_edge("C", "D", weight=norma(pos["C"], pos["D"]))
G.add_edge("C", "E", weight=norma(pos["C"], pos["E"]))
G.add_edge("E", "F", weight=norma(pos["E"], pos["F"]))
G.add_edge("F", "G", weight=norma(pos["F"], pos["G"]))
G.add_edge("G", "A", weight=norma(pos["G"], pos["A"]))
G.add_edge("C", "G", weight=norma(pos["C"], pos["G"]))

x = float(input("Punto X: "))
y = float(input("Punto Y: "))

G.add_node("P")
pos["P"] = (x, y)

minDist = float("inf")
puntoCercano = None
conexion1 = conexion2 = None
nodoA = nodoB = None

for u, v in G.edges():
    puntoProj, d = distanciaCamino(pos["P"], pos[u], pos[v])
    if d < minDist:
        minDist = d
        puntoCercano = puntoProj
        nodoA = u
        nodoB = v

if sonIguales(puntoCercano, pos[nodoA]):
    G = nx.relabel_nodes(G, {nodoA: "Q"})
    pos["Q"] = pos.pop(nodoA)
    G.add_edge("P", "Q", weight=minDist)

elif sonIguales(puntoCercano, pos[nodoB]):
    G = nx.relabel_nodes(G, {nodoB: "Q"})
    pos["Q"] = pos.pop(nodoB)
    G.add_edge("P", "Q", weight=minDist)

else:
    G.remove_edge(nodoA, nodoB)
    G.add_node("Q")
    pos["Q"] = puntoCercano

    G.add_edge("Q", nodoA, weight=norma(pos["Q"], pos[nodoA]))
    G.add_edge("Q", nodoB, weight=norma(pos["Q"], pos[nodoB]))
    G.add_edge("P", "Q", weight=minDist)

fin = str(input("¿A dónde quieres llegar?: "))
D=dijkstra(G,"Q",fin.upper())
print("El camino más corto es {} y la distancia es de {}".format(D[1],D[0]))

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray', font_size=10)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()

"""import folium

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
m"""
