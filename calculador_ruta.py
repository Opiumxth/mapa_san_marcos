import networkx as nx
import os
import heapq
import matplotlib.pyplot as plt
from generador_grafos import generar_grafo_aleatorio, norma 

def sonIguales(p1, p2, tolerancia=1e-6):
    return abs(p1[0] - p2[0]) <= tolerancia and abs(p1[1] - p2[1]) <= tolerancia

def distanciaCamino(P, A, B):
    x0, y0 = P
    x1, y1 = A
    x2, y2 = B

    productoEscalar = (x2 - x1)*(x0 - x1) + (y2 - y1)*(y0 - y1)

    if norma(A,B)**2 == 0:
        return A, norma(A,P)

    escalar = max(0, min(1, productoEscalar/norma(A,B)**2))
    proyX = x1 + escalar*(x2 - x1)
    proyY = y1 + escalar*(y2 - y1)
    puntoProy = (proyX, proyY)
    return puntoProy, norma(P, puntoProy)

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

def visualizar_y_guardar_grafo(grafo, posiciones, nombre_archivo="grafo_aleatorio.png", ruta_guardado="grafos_generados"):
    """Visualiza y guarda un grafo en un archivo PNG."""
    if not os.path.exists(ruta_guardado):
        os.makedirs(ruta_guardado)
    filepath = os.path.join(ruta_guardado, nombre_archivo)

    plt.figure(figsize=(12, 10))
    nx.draw(grafo, posiciones, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', font_size=10, width=1)
    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    edge_labels_rounded = {k: round(v, 2) for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(grafo, posiciones, edge_labels=edge_labels_rounded, font_size=8, label_pos=0.3)
    plt.title("Grafo Aleatorio Generado")
    plt.grid(True)
    plt.savefig(filepath)
    plt.show()
    print(f"Grafo guardado en: {filepath}")

if __name__ == "__main__":
    num_nodos = 10
    prob_conexion = 0.4
    rango_coord_x = (-15, 15)
    rango_coord_y = (-15, 15)
    G, pos = generar_grafo_aleatorio(num_nodos, prob_conexion, rango_coord_x, rango_coord_y)
    print(f"Grafo aleatorio cargado con {len(G.nodes())} nodos y {len(G.edges())} aristas.")

    visualizar_y_guardar_grafo(G, pos)

    try:
        x = float(input("Coordenada X del punto P: "))
        y = float(input("Coordenada Y del punto P: "))
    except ValueError:
        print("Entrada inválida. Por favor, ingrese números para las coordenadas.")
        exit()

    G.add_node("P")
    pos["P"] = (x, y)

    minDist = float("inf")
    puntoCercano = None
    nodoA = nodoB = None

    for u, v in G.edges():
        puntoProj, d = distanciaCamino(pos["P"], pos[u], pos[v])
        if d < minDist:
            minDist = d
            puntoCercano = puntoProj
            nodoA = u
            nodoB = v

    start_node_for_dijkstra = "P"

    if nodoA is None and G.nodes():
        primer_nodo = next(iter(G.nodes()))
        G.add_edge("P", primer_nodo, weight=norma(pos["P"], pos[primer_nodo]))
        start_node_for_dijkstra = primer_nodo
        print("Grafo sin aristas, conectando P al primer nodo disponible.")
    elif nodoA is not None:
        if sonIguales(puntoCercano, pos[nodoA]): 
            G.add_edge("P", nodoA, weight=minDist)
            start_node_for_dijkstra = nodoA
        elif sonIguales(puntoCercano, pos[nodoB]): 
            G.add_edge("P", nodoB, weight=minDist)
            start_node_for_dijkstra = nodoB
        else:
            G.remove_edge(nodoA, nodoB)
            G.add_node("Q")
            pos["Q"] = puntoCercano

            G.add_edge("Q", nodoA, weight=norma(pos["Q"], pos[nodoA]))
            G.add_edge("Q", nodoB, weight=norma(pos["Q"], pos[nodoB]))
            G.add_edge("P", "Q", weight=minDist)
            start_node_for_dijkstra = "Q"
    elif not G.nodes():
        print("El grafo generado está vacío. No se puede calcular la ruta.")
        exit()

    print("Nodos disponibles:", sorted(list(G.nodes())))
    inicio_usuario = input("Elige el nodo de inicio para la ruta: ").upper()
    if inicio_usuario not in G.nodes:
        print(f"Error: El nodo '{inicio_usuario}' no existe en el grafo.")
        exit()
    start_node_for_dijkstra = inicio_usuario

    fin = input("¿A dónde quieres llegar (nombre del nodo)?: ").upper()

    if fin not in G.nodes:
        print(f"Error: El nodo '{fin}' no existe en el grafo. Nodos disponibles: {sorted(list(G.nodes()))}")
    elif start_node_for_dijkstra == fin:
        print(f"Ya estás en el destino '{fin}'. Distancia: 0.0")
        D = (0.0, [fin])
    else:
        D = dijkstra_optimizado(G, start_node_for_dijkstra, fin)

        if D is not None and D != (float('inf'), []):
            print("La ruta es {} y tiene una distancia de {}".format(D[-1], round(D[-2], 2))) 
            ruta = D[-1]
            path_edges = []
            for i in range(len(ruta) - 1):
                path_edges.append((ruta [i], ruta [i+1]))

            plt.figure(figsize=(12, 10))
            nx.draw(G, pos, with_labels=True, node_color=['blue' if n == start_node_for_dijkstra else 'green' if n == fin else 'skyblue' for n in G.nodes()], node_size=800, edge_color=['red' if e in path_edges or (e[::-1]) in path_edges else 'gray' for e in G.edges()], font_size=10, width=2)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            edge_labels_rounded = {k: round(v, 2) for k, v in edge_labels.items()}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_rounded, font_size=8, label_pos=0.3)
            plt.title(f"Ruta de {start_node_for_dijkstra} a {fin}")
            plt.grid(True)
            nombre_archivo_ruta = f"ruta_{start_node_for_dijkstra}_a_{fin}.png"
            ruta_guardado_ruta = "rutas_encontradas"
            if not os.path.exists(ruta_guardado_ruta):
                os.makedirs(ruta_guardado_ruta)
            filepath_ruta = os.path.join(ruta_guardado_ruta, nombre_archivo_ruta)
            plt.savefig(filepath_ruta)
            plt.show()
            print(f"Ruta guardada en: {filepath_ruta}")
        else:
            print(f"No se encontró una ruta de '{start_node_for_dijkstra}' a '{fin}'.")