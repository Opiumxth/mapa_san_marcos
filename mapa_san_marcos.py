import networkx as nx
import math
import matplotlib.pyplot as plt

nodos_data = {
    1: (-4.5, 18.5, False),
    2: (-3.5, 14.5, False),
    3: (-6.5, 14, False),
    4: (-7.5, 14, False),
    5: (-12.5, 17, False),
    6: (-12.6, 15, False),
    7: (-11, 15, True), # Nodo Objetivo
    8: (-12.8, 12.5, True), # Nodo Objetivo
    9: (-13, 11.5, False),
    10: (-10, 11.2, True), # Nodo Objetivo
    11: (-9, 11.1, False),
    12: (-8, 11, False),
    13: (-9.5, 9, False),
    14: (-8, 12, True), # Nodo Objetivo
    15: (-6.2, 11.5, True), # Nodo Objetivo
    16: (-6, 10.2, False),
    17: (-13, 9.5, False),
    18: (-8, 9.5, False),
    19: (-8.2, 8, True), # Nodo Objetivo
    20: (-8.5, 6.2, False),
    21: (-3.5, 5.5, False),
    22: (-2.5, 7, True), # Nodo Objetivo
    23: (-1.5, 9, False),
    24: (-3.5, 10, False),
    25: (1.5, 7, False),
    26: (-1.2, 2.2, False),
    27: (-2, 2.7, False),
    28: (-2, 4, False),
    29: (-6, 6, False),
    30: (-6.5, 3.5, True), # Nodo Objetivo
    31: (-6.5, 1.8, False),
    32: (-9.5, 2, False),
    33: (-9, 5, True), # Nodo Objetivo
    34: (-9.8, 1, True), # Nodo Objetivo
    35: (-10, -1.5, True), # Nodo Objetivo
    36: (-10.1, -4.6, False),
    37: (-14.5, -4, False),
    38: (-5.5, -6.2, False),
    39: (-1.5, -9, False),
    40: (0.8, -9.5, False),
    41: (2, -11, False),
    42: (-0.5, -14, False),
    43: (-0.1, -15.5, True), # Nodo Objetivo
    44: (2.5, -13.5, True), # Nodo Objetivo
    45: (0.2, -17.2, False),
    46: (5.5, -16.5, False),
    47: (4.5, -13, False),
    48: (6, -12.8, False),
    49: (7, -16.2, False),
    50: (9, -16, True), # Nodo Objetivo
    51: (11, -15.5, False),
    52: (10.2, -13, True), # Nodo Objetivo
    53: (10, -12, False),
    54: (9.7, -11, True), # Nodo Objetivo
    55: (9.5, -10, False),
    56: (12, -9.5, False),
    57: (12.5, -11.5, False),
    58: (13.2, -11.3, False),
    59: (13.5, -13, False),
    60: (15, -11, True), # Nodo Objetivo
    61: (16.5, -10.5, False),
    62: (16.5, -14, False),
    63: (16, -8.5, False),
    64: (15.8, -7, True), # Nodo Objetivo
    65: (11.5, -7, True), # Nodo Objetivo
    66: (14, -4.5, True), # Nodo Objetivo
    67: (15.2, -4.6, False),
    68: (11, -5.6, False),
    69: (11, -5, False),
    70: (10.8, -4, False),
    71: (13.5, -3.4, False),
    72: (15, -3, False),
    73: (9.6, -4.2, False),
    74: (8, -4, False),
    75: (9.2, -3, True), # Nodo Objetivo
    76: (8.8, -1.5, False),
    77: (12, -0.5, False),
    78: (11.5, 0.2, True), # Nodo Objetivo
    79: (11.5, 1, False),
    80: (7, 4, False),
    81: (6, 2, False),
    82: (7, 1.5, False),
    83: (7, 0, False),
    84: (14, 0.5, False),
    85: (4, 3.5, False)
}

conexiones_data = [
    (1, 2), (1, 5),
    (2, 3), (2, 1),
    (3, 1), (3, 15), (3, 4),
    (4, 14),
    (5, 6), (5, 1),
    (6, 7), (6, 8),
    (7, 6),
    (8, 9),
    (9, 10), (9, 17),
    (10, 11),
    (11, 12), (11, 13),
    (12, 14), (12, 18),
    (13, 17), (13, 18),
    (14, 4),
    (15, 16),
    (16, 24),
    (17, 37),
    (18, 19),
    (19, 20),
    (20, 29), (20, 33),
    (21, 22), (21, 24), (21, 28), (21, 29),
    (22, 23),
    (23, 24), (23, 25),
    (24, 16),
    (25, 26), (25, 85),
    (26, 27),
    (27, 28), (27, 38),
    (28, 21),
    (29, 30),
    (30, 31),
    (31, 32),
    (32, 33), (32, 34),
    (33, 20),
    (34, 35),
    (35, 36),
    (36, 37), (36, 38),
    (37, 17),
    (38, 39),
    (39, 40), (39, 42),
    (40, 41),
    (41, 55),
    (42, 44), (42, 45),
    (43, 45),
    (44, 47),
    (45, 46),
    (46, 47), (46, 49),
    (47, 48),
    (48, 49), (48, 53),
    (49, 50),
    (50, 51),
    (51, 52), (51, 62),
    (52, 53),
    (53, 54), (53, 57),
    (54, 55),
    (55, 56),
    (56, 63), (56, 65),
    (57, 58),
    (58, 59), (58, 60),
    (60, 61),
    (61, 62), (61, 63),
    (62, 51),
    (63, 64),
    (64, 67),
    (65, 68),
    (66, 67), (66, 68),
    (67, 72),
    (68, 69),
    (69, 70),
    (70, 71), (70, 73),
    (71, 72), (71, 77),
    (72, 84),
    (73, 74), (73, 75),
    (74, 83),
    (75, 76),
    (76, 77),
    (77, 78),
    (78, 79),
    (79, 80),
    (80, 81), (80, 85),
    (81, 82),
    (82, 83),
    (84, 79),
    (85, 25)
]

def norma(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos 2D."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def construir_grafo_san_marcos():
    """
    Construye el grafo de San Marcos con los nodos y conexiones predefinidos.
    Asigna las coordenadas como atributo 'pos' y los pesos (distancias euclidianas)
    a las aristas.
    """
    G = nx.Graph()

    for nodo_id, (x, y, es_destino) in nodos_data.items():
        G.add_node(nodo_id, pos=(x, y), es_destino=es_destino)

    for u, v in conexiones_data:
        if u in G.nodes and v in G.nodes:
            pos_u = G.nodes[u]['pos']
            pos_v = G.nodes[v]['pos']
            weight = norma(pos_u, pos_v)
            G.add_edge(u, v, weight=weight)
        else:
            print(f"Advertencia: Nodos {u} o {v} no encontrados para la conexión.")

    pos = nx.get_node_attributes(G, 'pos')
    
    return G, pos, nodos_data

def dibujar_grafo_base(G, pos, nodos_info, file_path):
    plt.figure(figsize=(16, 16))

    node_colors = []
    node_sizes = []
    node_labels = {}

    for node in G.nodes():
        if nodos_info[node][2]:
            node_colors.append('red')
            node_sizes.append(800)
            node_labels[node] = node
        else:
            node_colors.append('lightgray')
            node_sizes.append(100)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)

    nx.draw_networkx_edges(G, pos, edge_color='darkgray', width=0.5, alpha=0.6)

    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_color='black')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels_rounded = {k: round(v, 2) for k, v in edge_labels.items()}

    plt.title("Mapa de Nodos de San Marcos (Destinos Resaltados)")
    plt.grid(False)
    plt.axis('off')
    
    plt.savefig(file_path)
    plt.close()