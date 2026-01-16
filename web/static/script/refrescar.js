
// Variable global para comparar los puntos anteriores y detectar cambios
let historialPuntos = {}; 

function refrescarPantalla() {
    fetch('/api/estado') // Consulta la ruta JSON del servidor central
        .then(response => response.json())
        .then(data => {
            const grid = document.querySelector('.estado-grid');

            data.jugadores.forEach(jugador => {
                // --- LÓGICA DE CONFETI ---
                // Si ya teníamos registro de este jugador y sus puntos actuales son mayores
                if (historialPuntos[jugador.id] !== undefined && jugador.puntos > historialPuntos[jugador.id]) {
                    lanzarConfeti();
                }
                // Actualizamos el historial con el valor nuevo
                historialPuntos[jugador.id] = jugador.puntos;

                // --- ACTUALIZACIÓN DE TARJETAS (Dinámica) ---
                let card = document.getElementById(`card-${jugador.id}`);
                if (!card) {
                    card = document.createElement('div');
                    card.id = `card-${jugador.id}`;
                    card.className = 'card';
                    card.innerHTML = `
                        <h3>${jugador.nombre}</h3>
                        <div class="puntos" id="puntos-${jugador.id}">${jugador.puntos}</div>
                        <p>Posición: <span id="pos-${jugador.id}">${jugador.posicion.x}, ${jugador.posicion.y}</span></p>
                    `;
                    grid.appendChild(card);
                } else {
                    document.getElementById(`puntos-${jugador.id}`).innerText = jugador.puntos;
                    document.getElementById(`pos-${jugador.id}`).innerText = `${jugador.posicion.x}, ${jugador.posicion.y}`;
                }
            });

            // Actualizar estado de la bandera
            const banderaInfo = document.getElementById('bandera-info');
            if (data.bandera.portador_id) {
                // Buscamos el nombre del portador en los datos frescos de la API
                const portador = data.jugadores.find(j => j.id === data.bandera.portador_id);
                const nombre = portador ? portador.nombre : `Jugador ${data.bandera.portador_id}`;
                banderaInfo.innerHTML = `La tiene: <strong>${nombre}</strong>`;
            } else {
                banderaInfo.innerHTML = `Estado: <strong>LIBRE EN EL CENTRO</strong>`;
            }

            // ACTUALIZAR POSICIÓN FÍSICA (Ahora será dinámica)
            const banderaPos = document.getElementById('bandera-pos');
            if (banderaPos) {
                banderaPos.innerText = `${data.bandera.posicion.x}, ${data.bandera.posicion.y}`;
            }
        })
        .catch(error => console.error('Error en AJAX:', error));
           
}

// Función para disparar la animación de confeti
function lanzarConfeti() {
    confetti({
        particleCount: 200,
        spread: 100,
        origin: { y: 0.6 },
        colors: ['#e15a70', '#00ff40', '#ffffff'] // Color confeti personalizado
    });
}

// Ejecutar la actualización cada 500ms
setInterval(refrescarPantalla, 500);