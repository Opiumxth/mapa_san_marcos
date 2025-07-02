import networkx as nx
import random
import math

def norma(p1, p2):
    return round((((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5),2)

def generar_grafo_aleatorio(num_nodos, prob_conexion, rango_coord_x=(-10, 10), rango_coord_y=(-10, 10)):
    """
    Genera un grafo aleatorio con nodos y aristas.

    Args:
        num_nodos (int): Número de nodos en el grafo.
        prob_conexion (float): Probabilidad de que dos nodos estén conectados (entre 0 y 1).
        rango_coord_x (tuple): Rango (min, max) para las coordenadas X de los nodos.
        rango_coord_y (tuple): Rango (min, max) para las coordenadas Y de los nodos.

    Returns:
        tuple: Un grafo de NetworkX y un diccionario de posiciones para los nodos.
    """
    G = nx.Graph()
    pos = {}

    for i in range(num_nodos):
        node_name = chr(65 + i)
        G.add_node(node_name)
        pos[node_name] = (round(random.uniform(rango_coord_x[0], rango_coord_x[1]), 2),
                          round(random.uniform(rango_coord_y[0], rango_coord_y[1]), 2))

    nodos = list(G.nodes())
    for i in range(num_nodos):
        for j in range(i + 1, num_nodos):
            if random.random() < prob_conexion:
                node1 = nodos[i]
                node2 = nodos[j]
                weight = norma(pos[node1], pos[node2])
                G.add_edge(node1, node2, weight=weight)

    return G, pos

if __name__ == "__main__":
    grafo_prueba, posiciones_prueba = generar_grafo_aleatorio(num_nodos=7, prob_conexion=0.5)
    print("Grafo generado:", grafo_prueba.nodes())
    print("Posiciones:", posiciones_prueba)
    print("Aristas:", grafo_prueba.edges(data=True))