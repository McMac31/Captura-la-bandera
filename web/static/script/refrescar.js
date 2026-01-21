
let historialPuntos = {}; 

function refrescarPantalla() {
    fetch('/api/estado') 
        .then(response => response.json())
        .then(data => {
            const grid = document.querySelector('.estado-grid');

            data.jugadores.forEach(jugador => {
                // Confeti si suben los puntos
                if (historialPuntos[jugador.id] !== undefined && jugador.puntos > historialPuntos[jugador.id]) {
                    lanzarConfeti();
                }
                historialPuntos[jugador.id] = jugador.puntos;

                // Buscar tarjeta del jugador por ID
                let card = document.getElementById(`card-${jugador.id}`);

                if (!card) {
                    // Si no existe: Crea tarjeta con diseño completo
                    card = document.createElement('div');
                    card.id = `card-${jugador.id}`;
                    card.classList.add('card'); // Asegura que use el CSS .card
                    card.innerHTML = `
                        <h3 id="nombre-${jugador.id}">${jugador.nombre}</h3>
                        <p>ID: ${jugador.id}</p>
                        <div class="puntos" id="puntos-${jugador.id}">${jugador.puntos}</div>
                        <p>Posición: <span id="pos-${jugador.id}">${jugador.posicion.x}, ${jugador.posicion.y}</span></p>
                    `;
                    grid.appendChild(card);
                } else {
                    // Si existe: Actualiza todo
                    const nombreElem = document.getElementById(`nombre-${jugador.id}`);
                    const puntosElem = document.getElementById(`puntos-${jugador.id}`);
                    const posElem = document.getElementById(`pos-${jugador.id}`);

                    if (nombreElem) nombreElem.innerText = jugador.nombre; 
                    if (puntosElem) puntosElem.innerText = jugador.puntos;
                    if (posElem) posElem.innerText = `${jugador.posicion.x}, ${jugador.posicion.y}`;
                }
            });

            // Actualizar Bandera (Nombre dinámico)
            const banderaInfo = document.getElementById('bandera-info');
            if (data.bandera.portador_id) {
                const portador = data.jugadores.find(j => j.id === data.bandera.portador_id);
                const nombre = portador ? portador.nombre : `ID ${data.bandera.portador_id}`;
                banderaInfo.innerHTML = `La tiene: <strong>${nombre}</strong>`;
            } else {
                banderaInfo.innerHTML = `Estado: <strong>LIBRE EN EL CENTRO</strong>`;
            }
        })
        .catch(error => console.error('Error en AJAX:', error));
           
}

// Funcion de particulas
function lanzarConfeti() {
    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#e94560', '#00ff41', '#ffffff']
    });
}

setInterval(refrescarPantalla, 500);