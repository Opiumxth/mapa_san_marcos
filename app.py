from flask import Flask, send_from_directory, request, jsonify
from backend.calculador_ruta import calcular_y_guardar_ruta

app = Flask(__name__, static_folder="frontend", static_url_path="/")

@app.route('/')
def index():
    return send_from_directory("frontend", "index.html")

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory("frontend", path)

@app.route("/ruta", methods=["POST"])
def ruta():
    data = request.json
    inicio = data.get("inicio")
    fin = data.get("fin")
    
    ruta_img = calcular_y_guardar_ruta(inicio, fin)
    
    if ruta_img:
        return jsonify({"ruta": f"/{ruta_img}"})
    else:
        return jsonify({"error": "Ruta no encontrada"}), 400

if __name__ == '__main__':
    app.run(debug=True)