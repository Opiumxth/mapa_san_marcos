import networkx as nx
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

def generar_imagen_base():
    G, pos = cargar_grafo_desde_json("backend/nodos.json", "backend/aristas.json")

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray',
            node_size=800, font_size=10, width=2)

    labels = nx.get_edge_attributes(G, 'weight')
    labels = {k: round(v, 2) for k, v in labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    plt.title("Mapa de San Marcos (sin ruta)")
    plt.grid(True)

    plt.savefig("frontend/static/ruta.png")
    plt.close()

if __name__ == "__main__":
    generar_imagen_base()
    print("Imagen base generada en frontend/static/ruta.png")