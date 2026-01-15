function refrescarPantalla() {
    fetch('/api/estado') // Consulta la ruta JSON del servidor web
        .then(response => response.json())
        .then(data => {
            // 1. Actualizar datos de los jugadores
            data.jugadores.forEach(jugador => {
                // Actualizar Puntos
                const ptsElement = document.getElementById(`puntos-${jugador.id}`);
                if (ptsElement) {
                    ptsElement.innerText = jugador.puntos;
                }

                // Actualizar Posición del Jugador
                const posElement = document.getElementById(`pos-${jugador.id}`);
                if (posElement) {
                    posElement.innerText = `${jugador.posicion.x}, ${jugador.posicion.y}`;
                }
            });

            // 2. Actualizar estado de la bandera
            const banderaInfo = document.getElementById('bandera-info');
            if (data.bandera.portador_id) {
                // Buscamos el nombre del portador en la lista de jugadores recibida
                const portador = data.jugadores.find(j => j.id === data.bandera.portador_id);
                const nombre = portador ? portador.nombre : `ID ${data.bandera.portador_id}`;
                banderaInfo.innerHTML = `La tiene: <strong>${nombre}</strong>`;
            } else {
                banderaInfo.innerHTML = `Estado: <strong>LIBRE EN EL CENTRO</strong>`;
            }

            // 3. Actualizar ubicación física de la bandera
            const banderaPos = document.getElementById('bandera-pos');
            if (banderaPos) {
                banderaPos.innerText = `${data.bandera.posicion.x}, ${data.bandera.posicion.y}`;
            }
        })
        .catch(error => console.error('Error en AJAX:', error));
}


// Ejecutar la actualización cada 500ms
setInterval(refrescarPantalla, 500);