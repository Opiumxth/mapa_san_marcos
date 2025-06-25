let seleccionador = null;
let seleccion = false;

const btnInicial = document.getElementById("btn-inicial");
const btnCancelI = document.getElementById("btn-cancel-i");
const btnFinal = document.getElementById("btn-final");
const btnCancelF = document.getElementById("btn-cancel-f");
const btnBorrar = document.getElementById("btn-borrar");

// Botones de seleccionar
btnInicial.addEventListener('click', () => {
  activarSeleccion('inicio');
});
btnFinal.addEventListener('click', () => {
  activarSeleccion('fin');
});

// Botones de cancelar
btnCancelI.addEventListener('click', () => {
  cancelarSeleccion('inicio');
});
btnCancelF.addEventListener('click', () => {
  cancelarSeleccion('fin');
});

// Activar modo selección
function activarSeleccion(tipo) {
  seleccionador = tipo;
  seleccion = true;
  if (tipo === 'inicio') {
    btnCancelI.style.display = "inline-flex";
  } else if (tipo === 'fin') {
    btnCancelF.style.display = "inline-flex";
  }
  btnInicial.disabled = true;
  btnFinal.disabled = true;
  btnBorrar.disabled = true;
}

// Cancelar selección
function cancelarSeleccion(tipo) {
  seleccionador = null;
  seleccion = false;
  if (tipo === 'inicio') {
    btnCancelI.style.display = "none";
  } else if (tipo === 'fin') {
    btnCancelF.style.display = "none";
  }
  btnInicial.disabled = false;
  btnFinal.disabled = false;
  btnBorrar.disabled = false;
}


// Botón de borrar
btnBorrar.addEventListener('click', () => {
  if (!seleccion) {
    alert("Primero debes realizar una selección.");
  } else {
    seleccion = false;
    btnCancelI.style.display = "none";
    btnCancelF.style.display = "none";
    alert("Selecciones eliminadas.");
  }
});