function refrescarPantalla() {
    fetch('/api/estado')
        .then(response => response.json())
        .then(data => {
            // Actualizar puntos de jugadores
            data.jugadores.forEach(jugador => {
                // Buscamos el elemento por el ID que asignaremos en el HTML
                const ptsElement = document.getElementById(`puntos-${jugador.id}`);
                if (ptsElement) {
                    ptsElement.innerText = jugador.puntos;
                }
            });

            // Actualizar estado de la bandera
            const banderaInfo = document.getElementById('bandera-info');
            if (data.bandera.portador_id) {
                banderaInfo.innerHTML = `La tiene: <strong>Jugador ${data.bandera.portador_id}</strong>`;
            } else {
                banderaInfo.innerHTML = `Estado: <strong>LIBRE EN EL CENTRO</strong>`;
            }
        })
        .catch(error => console.error('Error en AJAX:', error));
}

// Ejecutar la actualización cada 500ms
setInterval(actualizarMonitor, 500);