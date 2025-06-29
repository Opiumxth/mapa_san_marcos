const btnRuta = document.getElementById("btn-ruta");
const btnBorrar = document.getElementById("btn-borrar");

const inputInicio = document.getElementById("nodo-inicio");
const inputFin = document.getElementById("nodo-fin");

const imgRuta = document.getElementById("img-ruta");

btnRuta.addEventListener("click", async () => {
  const inicio = inputInicio.value.trim().toUpperCase();
  const fin = inputFin.value.trim().toUpperCase();

  if (!inicio || !fin) {
    alert("Por favor, ingresa ambos nodos");
    return;
  }

  if (inicio === fin) {
    alert("El nodo de inicio y fin no pueden ser iguales");
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/ruta", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ inicio, fin })
    });

    const data = await response.json();

    if (response.ok) {
      imgRuta.src = "http://localhost:5000/static/ruta.png";
    } else {
      alert(data.error || "Error al calcular la ruta.");
    }
  } catch (error) {
    alert("Error al conectarse con el servidor.");
    console.error(error);
  }
});

btnBorrar.addEventListener("click", () => {
  inputInicio.value = "";
  inputFin.value = "";
  imgRuta.src = "http://localhost:5000/ruta-imagen";  // Grafo sin ruta
});