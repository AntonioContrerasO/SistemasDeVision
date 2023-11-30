var express = require("express");
var app = express();
var server = require("http").Server(app);
var io = require("socket.io")(server);

app.use(express.static("public"));


io.on('connection', (socket) => {
  console.log('a user connected');
  
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });


  // Comunicacion con pagina

  socket.on('Iniciar', (msg) => {
  	io.emit("pythonIniciar","1");
  })

  socket.on('Finalizar', (msg) => {
  	io.emit("pythonFinalizar","2");
  })

  socket.on('NuevaImagenCount', (msg) =>{
    io.emit("NuevaImagen",msg)
  })




  socket.on('CambiarImagenPagina', (msg) =>{
    io.emit("cambiarImagen",msg)
  })

   socket.on('AprobadoCirculo', (msg) =>{
    io.emit("Circular",msg)
  })

  socket.on('AprobadoEtiqueta', (msg) =>{
    io.emit("Etiqueta",msg)
  })

  socket.on('AprobadoColor', (msg) =>{
    io.emit("Color",msg)
  })





});


server.listen(5000, function () {
  console.log("Servidor corriendo en http://localhost:5000");
});

