const socket = io();


const iniciar = document.getElementById('I');
const finalizar = document.getElementById('F');
const etiqueta = document.getElementById("E");
const circular = document.getElementById('C');
const color = document.getElementById("Y");
const imagen = document.getElementById("mainImage");

iniciar.onclick = () =>{
  socket.emit("Iniciar", "Init");
};

finalizar.onclick = () =>{
  socket.emit("Finalizar", "Fini");
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Ejemplo de uso: espera 2000 milisegundos (2 segundos)
async function miFuncion() {
  await sleep(5000);
}




socket.on("Etiqueta", (msg) =>{
	let labelEtiqueta;
  if (msg == "True") {
    labelEtiqueta = "Aprobado";
    etiqueta.style.backgroundColor = "green";
    etiqueta.style.color = "white";
  } else {
    labelEtiqueta = "No aprobado";
    etiqueta.style.backgroundColor = "red";
  }
  etiqueta.value = labelEtiqueta;
});

socket.on("Circular", (msg) =>{
  let labelCircular;
  if (msg == "True") {
    labelCircular = "Aprobado";
    circular.style.backgroundColor = "green";
    circular.style.color = "white";
  } else {
    labelCircular = "No aprobado";
    circular.style.backgroundColor = "red";
    circular.style.color = "white";
  }
  circular.value = labelCircular;
});



socket.on("Color", (msg) =>{
  let labelColor;
  if (msg == "True") {
    labelColor = "Aprobado";
    color.style.backgroundColor = "green";
    color.style.color = "white";
  } else {
    labelColor = "No aprobado";
    color.style.backgroundColor = "red";
    color.style.color = "white";
  }
  color.value = labelColor;
});

socket.on("cambiarImagen", (msg) =>{
  miFuncion();
  imagen.src = msg;
})
