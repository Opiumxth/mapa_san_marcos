import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

def cargar_grafo_desde_json(nodos_file, aristas_file):
    G = nx.Graph()
    pos = {}

    with open(nodos_file, "r") as f:
        nodos = json.load(f)

    with open(aristas_file, "r") as f:
        aristas = json.load(f)

    for nodo in nodos:
        G.add_node(nodo["id"])
        pos[nodo["id"]] = (nodo["x"], nodo["y"])

    for arista in aristas:
        G.add_edge(arista["origen"], arista["destino"], weight=arista["peso"])

    return G, pos


def dijkstra_optimizado(G, inicio, fin):
    import heapq
    infinito = float('inf')
    distancias = {nodo: infinito for nodo in G.nodes}
    padres = {nodo: None for nodo in G.nodes}
    priority_queue = [(0, inicio)]

    distancias[inicio] = 0

    while priority_queue:
        dist_actual, nodo_actual = heapq.heappop(priority_queue)

        if dist_actual > distancias[nodo_actual]:
            continue

        if nodo_actual == fin:
            camino = [fin]
            while camino[0] != inicio:
                camino.insert(0, padres[camino[0]])
            return distancias[fin], camino

        for vecino in G.neighbors(nodo_actual):
            weight = G[nodo_actual][vecino]['weight']
            nuevaDist = distancias[nodo_actual] + weight

            if nuevaDist < distancias[vecino]:
                distancias[vecino] = nuevaDist
                padres[vecino] = nodo_actual
                heapq.heappush(priority_queue, (nuevaDist, vecino))
    return infinito, []


def calcular_y_guardar_ruta(inicio, fin):
    G, pos = cargar_grafo_desde_json("backend/nodos.json", "backend/aristas.json")

    if inicio not in G.nodes() or fin not in G.nodes():
        return None

    if inicio == fin:
        return None

    distancia, camino = dijkstra_optimizado(G, inicio, fin)
    if distancia == float("inf"):
        return None

    plt.figure(figsize=(10, 8))

    color_nodos = []
    for n in G.nodes():
        if n == inicio:
            color_nodos.append('blue')
        elif n == fin:
            color_nodos.append('green')
        else:
            color_nodos.append('skyblue')

    aristas_ruta = [(camino[i], camino[i+1]) for i in range(len(camino) - 1)]
    color_aristas = ['red' if (e in aristas_ruta or (e[1], e[0]) in aristas_ruta) else 'gray' for e in G.edges()]

    nx.draw(G, pos, with_labels=True, node_color=color_nodos, edge_color=color_aristas,
            node_size=800, font_size=10, width=2)

    labels = nx.get_edge_attributes(G, 'weight')
    labels = {k: round(v, 2) for k, v in labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    plt.title("Ruta más corta")
    plt.grid(True)

    ruta_img = "static/ruta.png"
    plt.savefig(f"frontend/{ruta_img}")
    plt.close()

    return ruta_img


# #Aqui se cargan ambos archivos de aristas y vertices inicialmente extraidos de un .geojson
# def cargar_grafo_desde_json(nodos_file, aristas_file):
#     G = nx.Graph()
#     pos = {}

#     with open(nodos_file, "r") as f:
#         nodos = json.load(f)

#     with open(aristas_file, "r") as f:
#         aristas = json.load(f)

#     for nodo in nodos:
#         G.add_node(nodo["id"])
#         pos[nodo["id"]] = (nodo["x"], nodo["y"])

#     for arista in aristas:
#         G.add_edge(arista["origen"], arista["destino"], weight = arista["peso"])

#     return G, pos

# #Algoritmo de recorrido minimo
# def dijkstra_optimizado(G, inicio, fin):
#     import heapq
#     infinito = float('inf')
#     distancias = {nodo: infinito for nodo in G.nodes}
#     padres = {nodo: None for nodo in G.nodes}
#     priority_queue = [(0, inicio)]

#     distancias[inicio] = 0

#     while priority_queue:
#         dist_actual, nodo_actual = heapq.heappop(priority_queue)

#         if dist_actual > distancias[nodo_actual]:
#             continue

#         if nodo_actual == fin:
#             camino = [fin]
#             while camino[0] != inicio:
#                 camino.insert(0, padres[camino[0]])
#             return distancias[fin], camino

#         for vecino in G.neighbors(nodo_actual):
#             weight = G[nodo_actual][vecino]['weight']
#             nuevaDist = distancias[nodo_actual] + weight

#             if nuevaDist < distancias[vecino]:
#                 distancias[vecino] = nuevaDist
#                 padres[vecino] = nodo_actual
#                 heapq.heappush(priority_queue, (nuevaDist, vecino))
#     return infinito, []


# #Aqui se genera un grafo aleatorio, pero para SM tiene que ser uno fijo
# #Aqui habia una funcion crear grafo aleatorio pero ya no se usa

# #Para crear el grafo fijo, con un archivo json, lo ideal es que exista un json de vertices y otro de aristas, update: ya se creo esa funcion que carga ambos .json
# def visualizar_grafo(G, pos, camino = None, inicio = None, fin = None):
#     plt.figure(figsize = (10,8))

#     color_nodos = []
#     for n in G.nodes():
#         if n == inicio:
#             color_nodos.append('blue')
#         elif n == fin:
#             color_nodos.append('green')
#         else:
#             color_nodos.append('skyblue')

#     aristas_ruta = []

#     if camino:
#         aristas_ruta = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
#     color_aristas = ['red' if (e in aristas_ruta or (e[1], e[0]) in aristas_ruta) else 'gray' for e in G.edges()]

#     nx.draw(G, pos, with_labels = True, node_color = color_nodos, edge_color = color_aristas,
#             node_size = 800, font_size = 10, width = 2)

#     labels = nx.get_edge_attributes(G, 'weight')
#     labels = {k: round(v, 2) for k, v in labels.items()}
#     nx.draw_networkx_edge_labels(G, pos, edge_labels = labels, font_size = 8)

#     plt.title("Grafo y Ruta mas corta (Usando algoritmo Dijkstra)")
#     plt.grid(True)
#     plt.show()
# #Final de funcion para visualizar el grafo


# def calcular_y_guardar_ruta(inicio, fin):
#     G, pos = cargar_grafo_desde_json("backend/nodos.json", "backend/aristas.json")

#     if inicio not in G.nodes() or fin not in G.nodes():
#         return None

#     if inicio == fin:
#         return None

#     distancia, camino = dijkstra_optimizado(G, inicio, fin)
#     if distancia == float("inf"):
#         return None

#     plt.figure(figsize=(10, 8))

#     color_nodos = []
#     for n in G.nodes():
#         if n == inicio:
#             color_nodos.append('blue')
#         elif n == fin:
#             color_nodos.append('green')
#         else:
#             color_nodos.append('skyblue')

#     aristas_ruta = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
#     color_aristas = ['red' if (e in aristas_ruta or (e[1], e[0]) in aristas_ruta) else 'gray' for e in G.edges()]

#     nx.draw(G, pos, with_labels=True, node_color=color_nodos, edge_color=color_aristas,
#             node_size=800, font_size=10, width=2)

#     labels = nx.get_edge_attributes(G, 'weight')
#     labels = {k: round(v, 2) for k, v in labels.items()}
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

#     plt.title("Ruta mas corta")
#     plt.grid(True)

#     ruta_img = "frontend/ruta.png"
#     plt.savefig(ruta_img)
#     plt.close()

#     return ruta_img



#Ejecucion del main()


#Nota para el futuro
    #Al tener el archivo geojson copiar el script de gtp para hacer que genere los dos aristas.json y nodos.json, y estos moverlos adentro del backend, porque al momento de llamarlos estan o tienen como nombre backend/nodos.json y backend/aristas.json, eso creo que es todo, ahora falta ver que se muestren las imagenes