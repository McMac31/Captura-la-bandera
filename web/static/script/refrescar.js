
<<<<<<< HEAD
// Variable global para comparar los puntos anteriores y detectar cambios
let historialPuntos = {}; 

function refrescarPantalla() {
    fetch('/api/estado') // Consulta la ruta JSON del servidor central
=======
let historialPuntos = {}; 

function refrescarPantalla() {
    fetch('/api/estado') 
>>>>>>> desarrollo
        .then(response => response.json())
        .then(data => {
            const grid = document.querySelector('.estado-grid');

            data.jugadores.forEach(jugador => {
<<<<<<< HEAD
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
=======
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
>>>>>>> desarrollo
                        <div class="puntos" id="puntos-${jugador.id}">${jugador.puntos}</div>
                        <p>Posición: <span id="pos-${jugador.id}">${jugador.posicion.x}, ${jugador.posicion.y}</span></p>
                    `;
                    grid.appendChild(card);
                } else {
<<<<<<< HEAD
                    document.getElementById(`puntos-${jugador.id}`).innerText = jugador.puntos;
                    document.getElementById(`pos-${jugador.id}`).innerText = `${jugador.posicion.x}, ${jugador.posicion.y}`;
=======
                    // Si existe: Actualiza todo
                    const nombreElem = document.getElementById(`nombre-${jugador.id}`);
                    const puntosElem = document.getElementById(`puntos-${jugador.id}`);
                    const posElem = document.getElementById(`pos-${jugador.id}`);

                    if (nombreElem) nombreElem.innerText = jugador.nombre; 
                    if (puntosElem) puntosElem.innerText = jugador.puntos;
                    if (posElem) posElem.innerText = `${jugador.posicion.x}, ${jugador.posicion.y}`;
>>>>>>> desarrollo
                }
            });

            // Actualizar Bandera (Nombre dinámico)
            const banderaInfo = document.getElementById('bandera-info');
            if (data.bandera.portador_id) {
<<<<<<< HEAD
                // Buscamos el nombre del portador en los datos frescos de la API
                const portador = data.jugadores.find(j => j.id === data.bandera.portador_id);
                const nombre = portador ? portador.nombre : `Jugador ${data.bandera.portador_id}`;
=======
                const portador = data.jugadores.find(j => j.id === data.bandera.portador_id);
                const nombre = portador ? portador.nombre : `ID ${data.bandera.portador_id}`;
>>>>>>> desarrollo
                banderaInfo.innerHTML = `La tiene: <strong>${nombre}</strong>`;
            } else {
                banderaInfo.innerHTML = `Estado: <strong>LIBRE EN EL CENTRO</strong>`;
            }
<<<<<<< HEAD

            // ACTUALIZAR POSICIÓN FÍSICA (Ahora será dinámica)
            const banderaPos = document.getElementById('bandera-pos');
            if (banderaPos) {
                banderaPos.innerText = `${data.bandera.posicion.x}, ${data.bandera.posicion.y}`;
            }
=======
>>>>>>> desarrollo
        })
        .catch(error => console.error('Error en AJAX:', error));
           
}

<<<<<<< HEAD
// Función para disparar la animación de confeti
function lanzarConfeti() {
    confetti({
        particleCount: 200,
        spread: 100,
        origin: { y: 0.6 },
        colors: ['#e15a70', '#00ff40', '#ffffff'] // Color confeti personalizado
=======
// Funcion de particulas
function lanzarConfeti() {
    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#e94560', '#00ff41', '#ffffff']
>>>>>>> desarrollo
    });
}

setInterval(refrescarPantalla, 500);