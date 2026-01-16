function refrescarPantalla() {
    fetch('/api/estado') // Consulta la ruta JSON del servidor web
        .then(response => response.json())
        .then(data => {
            // Por cada jugador en la respuesta
            data.jugadores.forEach(jugador => {
                // Actualizar Puntos
                const ptsJugador = document.getElementById(`puntos-${jugador.id}`); //Variable puntos del jugador
                if (ptsJugador) {
                    ptsJugador.innerText = jugador.puntos;
                }

                // Actualizar Posición del Jugador
                const posJugador = document.getElementById(`pos-${jugador.id}`);
                if (posJugador) {
                    posJugador.innerText = `${jugador.posicion.x}, ${jugador.posicion.y}`;
                }
            });

            // Actualizar estado de la bandera
            const banderaInfo = document.getElementById('bandera-info');
            if (data.bandera.portador_id) {
                // Buscamos el nombre del portador en la lista de jugadores recibida
                const portador = data.jugadores.find(j => j.id === data.bandera.portador_id); // Funcion lambda para encontrar el portador
                const nombre = portador ? portador.nombre : `ID ${data.bandera.portador_id}`; // Si no se encuentra, mostrar ID
                banderaInfo.innerHTML = `La tiene: <strong>${nombre}</strong>`;
            } else {
                banderaInfo.innerHTML = `Estado: <strong>LIBRE EN EL CENTRO</strong>`;
            }

            // Actualizar ubicación física de la bandera
            const banderaPos = document.getElementById('bandera-pos');
            if (banderaPos) {
                banderaPos.innerText = `${data.bandera.posicion.x}, ${data.bandera.posicion.y}`;
            }
        })
        .catch(error => console.error('Error en AJAX:', error));
}


// Ejecutar la actualización cada 500ms
setInterval(refrescarPantalla, 500);