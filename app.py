from flask import Flask, render_template, request, jsonify, send_from_directory, session
import os
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

from mapa_san_marcos import construir_grafo_san_marcos, nodos_data
from calculador_ruta import dijkstra_optimizado

app = Flask(__name__)
app.secret_key = 'wa'

STATIC_FOLDER = 'static'
IMAGES_FOLDER = os.path.join(STATIC_FOLDER, 'images')
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER

if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

current_G = None
current_pos = None
current_nodos_data = None

def cargar_grafo_san_marcos():
    """
    Carga el grafo predefinido de San Marcos y lo dibuja con el estilo deseado
    sobre la imagen del mapa real.
    """
    global current_G, current_pos, current_nodos_data
    
    G, pos, nodos_info = construir_grafo_san_marcos()

    current_G = G
    current_pos = pos
    current_nodos_data = nodos_info

    mapa_real_path = os.path.join(app.config['IMAGES_FOLDER'], 'mapa_real.png')
    try:
        img = Image.open(mapa_real_path)
        img_extent = (-20, 20, -20, 20) 
    except FileNotFoundError:
        print(f"Advertencia: No se encontró la imagen del mapa real en: {mapa_real_path}")
        img = None
        img_extent = None

    plt.figure(figsize=(12, 12))
    if img is not None and img_extent is not None:
        plt.imshow(img, extent=img_extent, alpha=0.5)

    node_colors = []
    node_sizes = []
    node_labels = {}

    for node in G.nodes():
        if nodos_info[node][2]:
            node_colors.append('red')
            node_sizes.append(800)
            node_labels[node] = str(node)
        else:
            node_colors.append('lightgray')
            node_sizes.append(100)
            node_labels[node] = ''

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.7)
    nx.draw_networkx_edges(G, pos, edge_color='darkgray', width=0.5, alpha=0.5)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_color='black')

    plt.grid(False)
    plt.axis('off')

    initial_graph_path = os.path.join(app.config['IMAGES_FOLDER'], 'grafo_aleatorio.png')
    plt.savefig(initial_graph_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"Grafo inicial de San Marcos sobre mapa real guardado en: {initial_graph_path}")

    return G, pos, nodos_info

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_G, current_pos, current_nodos_data
    
    if request.method == 'POST':
        G, pos, nodos_info = cargar_grafo_san_marcos()
        selectable_nodes = sorted([node for node, data in nodos_info.items() if data[2]])
        
        return jsonify({"success": True, "nodes": selectable_nodes, "image_url": "/static/images/grafo_aleatorio.png"})
        
    else:
        if current_G is None or current_pos is None:
            cargar_grafo_san_marcos()

        if current_nodos_data:
            selectable_nodes = sorted([node for node, data in current_nodos_data.items() if data[2]])
        else:
            selectable_nodes = []

        return render_template('index.html', nodes=selectable_nodes)

@app.route('/static/images/grafo_aleatorio.png')
def serve_initial_graph():
    return send_from_directory(app.config['IMAGES_FOLDER'], 'grafo_aleatorio.png')

@app.route('/static/images/ruta.png')
def serve_route_graph():
    return send_from_directory(app.config['IMAGES_FOLDER'], 'ruta.png')

@app.route('/ruta', methods=['POST'])
def calcular_ruta_api():
    global current_G, current_pos, current_nodos_data
    if current_G is None or current_pos is None or current_nodos_data is None:
        return jsonify({"error": "No hay grafo cargado. Recargue la página."}), 400

    data = request.get_json()
    start_node_user = int(data.get('inicio'))
    end_node_user = int(data.get('fin'))

    if start_node_user not in current_G.nodes:
        return jsonify({"error": f"El nodo de inicio '{start_node_user}' no existe en el grafo."}), 400

    if end_node_user not in current_G.nodes or not current_nodos_data[end_node_user][2]:
        return jsonify({"error": f"El nodo de destino '{end_node_user}' no es un punto de destino válido."}), 400
    
    if start_node_user == end_node_user:
        full_path_distance = 0.0
        full_path_nodes = [start_node_user]
    else:
        full_path_distance, full_path_nodes = dijkstra_optimizado(current_G, start_node_user, end_node_user)

    if full_path_distance == float('inf'):
        return jsonify({"error": f"No se encontró una ruta de '{start_node_user}' a '{end_node_user}'."}), 404

    plt.figure(figsize=(12, 12))

    mapa_real_path = os.path.join(app.config['IMAGES_FOLDER'], 'mapa_real.png')
    try:
        img = Image.open(mapa_real_path)
        img_extent = (-20, 20, -20, 20) 
        plt.imshow(img, extent=img_extent, alpha=0.5)
    except FileNotFoundError:
        print(f"Advertencia: No se encontró la imagen del mapa real en: {mapa_real_path}")

    node_colors = []
    node_sizes = []
    node_labels = {}

    for node in current_G.nodes():
        if node == start_node_user:
            node_colors.append('blue')
            node_sizes.append(900)
            node_labels[node] = str(node)
        elif node == end_node_user:
            node_colors.append('green')
            node_sizes.append(900)
            node_labels[node] = str(node)
        elif current_nodos_data[node][2]:
            node_colors.append('red')
            node_sizes.append(800)
            node_labels[node] = str(node)
        else:
            node_colors.append('lightgray')
            node_sizes.append(100)
            node_labels[node] = ''

    nx.draw_networkx_nodes(current_G, current_pos, node_color=node_colors, node_size=node_sizes, alpha=0.7)
    nx.draw_networkx_edges(current_G, current_pos, edge_color='darkgray', width=0.5, alpha=0.5)
    nx.draw_networkx_labels(current_G, current_pos, labels=node_labels, font_size=10, font_color='black')

    if full_path_nodes and len(full_path_nodes) > 1:
        highlight_edges = []
        for i in range(len(full_path_nodes) - 1):
            u, v = full_path_nodes[i], full_path_nodes[i+1] 
            if current_G.has_edge(u, v):
                highlight_edges.append((u, v))
            elif current_G.has_edge(v, u):
                highlight_edges.append((v, u))
        
        nx.draw_networkx_edges(current_G, current_pos, edgelist=highlight_edges, edge_color='magenta', width=3, alpha=0.8)

    plt.title(f"Ruta de {start_node_user} a {end_node_user} sobre Mapa Real (Distancia: {round(full_path_distance, 2)})")
    plt.grid(False)
    plt.axis('off')

    route_image_path = os.path.join(app.config['IMAGES_FOLDER'], 'ruta.png')
    plt.savefig(route_image_path)
    plt.close()

    return jsonify({
        "success": True,
        "path": " -> ".join(map(str, full_path_nodes)),
        "distance": round(full_path_distance, 2),
        "image_url": "/static/images/ruta.png"
    })

with app.app_context():
    cargar_grafo_san_marcos()

if __name__ == '__main__':
    app.run(debug=True)