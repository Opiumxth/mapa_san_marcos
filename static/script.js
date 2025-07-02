const btnRuta = document.getElementById("btn-ruta");
const btnBorrar = document.getElementById("btn-borrar");
const btnGenerarNuevo = document.getElementById("btn-generar-nuevo");

const selectInicio = document.getElementById("nodo-inicio");
const selectFin = document.getElementById("nodo-fin");

const imgRuta = document.getElementById("img-ruta");
const caminoResultado = document.getElementById("camino-resultado");
const distanciaResultado = document.getElementById("distancia-resultado");

async function updateNodeSelects() {
    try {

        const response = await fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        });
        const data = await response.json();

        if (response.ok && data.success) {
            const nodes = data.nodes;

            selectInicio.innerHTML = '';
            selectFin.innerHTML = '';

            nodes.forEach(node => {
                const optionStart = document.createElement('option');
                optionStart.value = node;
                optionStart.textContent = node;
                selectInicio.appendChild(optionStart);

                const optionEnd = document.createElement('option');
                optionEnd.value = node;
                optionEnd.textContent = node;
                selectFin.appendChild(optionEnd);
            });
            
            imgRuta.src = "/static/images/grafo_aleatorio.png" + '?' + new Date().getTime();
            caminoResultado.textContent = "N/A";
            distanciaResultado.textContent = "N/A";

        } else {
            console.error("Error al obtener los nodos del grafo:", data.error || "Desconocido");
            alert("No se pudo cargar la lista de nodos. Por favor, recargue la página.");
        }
    } catch (error) {
        console.error("Error al conectarse con el servidor para obtener nodos:", error);
        alert("Error al conectarse con el servidor. Por favor, intente de nuevo.");
    }
}

btnRuta.addEventListener("click", async () => {
    const inicio = selectInicio.value;
    const fin = selectFin.value;

    if (!inicio || !fin) {
        alert("Por favor, selecciona ambos nodos.");
        return;
    }

    if (inicio === fin) {
        alert("El nodo de inicio y fin no pueden ser iguales.");
        return;
    }

    try {
        const response = await fetch("/ruta", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ inicio: parseInt(inicio), fin: parseInt(fin) })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            imgRuta.src = data.image_url + '?' + new Date().getTime();
            caminoResultado.textContent = data.path;
            distanciaResultado.textContent = data.distance;
        } else {
            alert(data.error || "Error al calcular la ruta.");
        }
    } catch (error) {
        alert("Error al conectarse con el servidor.");
        console.error(error);
    }
});

btnBorrar.addEventListener("click", () => {
    if (selectInicio.options.length > 0) {
        selectInicio.selectedIndex = 0;
    }
    if (selectFin.options.length > 0) {
        selectFin.selectedIndex = 0;
    }
    imgRuta.src = "/static/images/grafo_aleatorio.png" + '?' + new Date().getTime();
    caminoResultado.textContent = "N/A";
    distanciaResultado.textContent = "N/A";
});

btnGenerarNuevo.addEventListener("click", updateNodeSelects);

document.addEventListener("DOMContentLoaded", () => {
    updateNodeSelects();
});