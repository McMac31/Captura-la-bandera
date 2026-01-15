import pygame
import sys
from config import *
from entidades.jugador import Jugador
from entidades.bandera import Bandera
from red.cliente_red import ClienteRed
from web.servidor_web import ServerFlask

# Clase principal del juego
class Juego:
    def __init__(self,nombre_jugador,email_jugador):
        # Inicializamos el juego
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        
        # Control de LAG
        self.ultimo_envio = 0
        self.intervalo_envio = 50 #50ms

        self.nombrelocal=nombre_jugador
        self.emaillocal=email_jugador
        self.red=ClienteRed()
        self.fuenteptos = pygame.font.SysFont("Impact", 40)
        self.fuentenombre = pygame.font.SysFont("Verdana", 15)
        
        # Cargar obstaculos desde config (por defecto los locales)
        self.obstaculos = OBSTACULOS

        if self.red.conectar():
            print("Conectado al servidor de juego.")
            self.mi_id=self.red.id
            
            # Si recibimos un mapa del servidor, usamos ese y machacamos el local
            if self.red.mapa_recibido is not None and len(self.red.mapa_recibido) > 0:
                self.obstaculos = []
                for (x, y, w, h) in self.red.mapa_recibido:
                    self.obstaculos.append(pygame.Rect(x, y, w, h))
                print("Mapa sincronizado con el servidor.")
            else:
                 print("Usando mapa local (No se recibió mapa del servidor).")

        else:
            print("No se pudo conectar al servidor de juego.")
            self.mi_id = 1 # ID por defecto si falla

        # Diccionario de jugadores
        self.jugadores = {}
        
        # Definimos quiénes somos (por defecto el 1/Rojo para pruebas locales)
        self.crear_objetos()
        self.servidor_web = ServerFlask(self)
        self.servidor_web.start()  # Iniciamos el servidor web en un hilo
        

   # Creamos los objetos del juego
    def crear_objetos(self):
        self.bandera = Bandera()
        # Configuracion multijugador
        # Lista con datos: (ID, Posición X, Posición Y, Color,nombre,email)
        # Usamos ANCHO-80 y ALTO-80 para que no nazcan pegados al borde exacto
        datos_jugadores = [
            (1, 40, 40, ROJO),             # J1: Rojo (Esquina. Superior. Izquieda)
            (2, ANCHO-80, 40, AZUL),       # J2: Azul (Esquina. Superior. Derecha)
            (3, 40, ALTO-80, AMARILLO),    # J3: Amarillo (Esquina. Inferior. Izquieda)
            (4, ANCHO-80, ALTO-80, VERDE)  # J4: Verde (Esquina. Inferior. Derecha)
        ]

        for pid, x, y, color in datos_jugadores:
            # Determinamos si este jugador es el usuario local
            es_local = (pid == self.mi_id)

            if es_local:
                nombreFinal = self.nombrelocal
                emailFinal = self.emaillocal
            else:
                nombreFinal = f"Jugador {pid}"
                emailFinal = ""
            # Creamos el jugador
            jugador = Jugador(x, y, color, pid, nombreFinal, emailFinal, es_local)
            
            # Solo asignamos controles si es el jugador local
            if es_local:
                jugador.controles = TECLAS_LOCAL 
            # Lo guardamos en el diccionario
            self.jugadores[pid] = jugador

    # Manejamos los eventos del juego de salida
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False

   # Actualizamos el estado del juego
    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()

        #Control de red y movimiento local
        if self.mi_id in self.jugadores:
            jugador_local= self.jugadores[self.mi_id]

            #Guardado de posicion anterior
            pos_anterior=(jugador_local.rect.x, jugador_local.rect.y)
            puntos_anteriores = jugador_local.puntos
            
            jugador_local.mover(self.obstaculos) #Movimiento local

            # Si toco la bandera y nadie la tiene, la PIDO. No la cojo directamente.
            if self.bandera.portador is None and self.bandera.rect.colliderect(jugador_local.rect):
                self.red.enviar({'evento': 'PETICION', 'id': self.mi_id})

            # Control de LAG: Solo enviamos cada 50s
            if tiempo_actual - self.ultimo_envio > self.intervalo_envio:
                if (jugador_local.rect.x, jugador_local.rect.y) != pos_anterior or jugador_local.puntos != puntos_anteriores: #Si hubo cambio de posicion o puntos
                    datos={ #Datos a enviar
                        'id': self.mi_id,
                        'posicion':{"x": jugador_local.rect.x, "y": jugador_local.rect.y},
                        'puntos': jugador_local.puntos,
                        'nombre': jugador_local.NombreJugador,
                        'email': jugador_local.EmailJugador}
                    self.red.enviar(datos) #Envio de nueva posicion al servidor
                    self.ultimo_envio = tiempo_actual
                
        #Recepcion de datos del servidor
        mensajes = self.red.obtener_mensajes()
        
        #Eventos para saber que hacer
        hubo_reset = False
        for mensaje in mensajes:
            # Si recibimos evento
            if "evento" in mensaje:
                evento = mensaje["evento"]
                
                # Si el evento es COGER
                if evento == "COGER" and "id" in mensaje:
                    id_ganador = mensaje["id"]
                    if id_ganador in self.jugadores:
                        print(f"La bandera es de {self.jugadores[id_ganador].NombreJugador} ID: {id_ganador}") 
                        self.bandera.portador = self.jugadores[id_ganador] #le damos la bandera al jugador correspondiente
                
                # Evento RESET 
                elif evento == "RESET":
                    #  Actualizamos los puntos del jugador que anotó 
                    if "id" in mensaje and "puntos" in mensaje:
                        id_anotador = mensaje["id"]
                        if id_anotador in self.jugadores:
                            self.jugadores[id_anotador].puntos = mensaje["puntos"]
                    # Reiniciamos la ronda
                    self.resetear_ronda()
                    hubo_reset = True
                    continue 

                #JUGADOR DESCONECTADO 
                elif evento == "SALIDA":
                    if "id" in mensaje:
                        id_salida = mensaje["id"]
                        # Si alguien se fue, borramos su muñeco y liberamos memoria en cliente
                        if id_salida in self.jugadores and id_salida != self.mi_id:
                            print(f"Jugador {self.nombrelocal} {id_salida} desconectado. Eliminando sprite.")
                            del self.jugadores[id_salida]
                    continue

            # Actualizacion de posiciones y puntos de jugadores
            if not hubo_reset and "id" in mensaje: 
                id_remoto = mensaje['id']
                #Solo aceptamos datos de OTROS
                if id_remoto != self.mi_id: 
                    
                    # --- NUEVO: SI EL JUGADOR NO EXISTE (ej: reingreso), LO RE-CREAMOS ---
                    if id_remoto not in self.jugadores:
                         # Mapa rapido de datos originales para reconstruir al jugador
                         datos_base = {
                            1: (40, 40, ROJO),
                            2: (ANCHO-80, 40, AZUL),
                            3: (40, ALTO-80, AMARILLO),
                            4: (ANCHO-80, ALTO-80, VERDE)
                         }
                         if id_remoto in datos_base:
                             x_ini, y_ini, color_ini = datos_base[id_remoto]
                             nuevo_j = Jugador(x_ini, y_ini, color_ini, id_remoto, f"Jugador {id_remoto}", "", False)
                             self.jugadores[id_remoto] = nuevo_j

                    # Si ya existe (o lo acabamos de crear), actualizamos
                    if id_remoto in self.jugadores:
                        jugador_remoto = self.jugadores[id_remoto]
                        
                        if "posicion" in mensaje:  # Actualizacion de posicion
                            pos = mensaje['posicion']
                            jugador_remoto.establecer_posicion(pos['x'], pos['y']) 
                        
                        # Actualizacion de puntos 
                        if "puntos" in mensaje:
                                jugador_remoto.puntos = mensaje['puntos']
                        # Actualizacion de nombre 
                        if "nombre" in mensaje:
                                jugador_remoto.NombreJugador = mensaje['nombre']

        # Lista jugadores 
        lista_jugadores = list(self.jugadores.values())
        # Actualizar Bandera (ya no calcula colisiones sola)
        self.bandera.actualizar()

        # Verificacion de robos
        for j1 in lista_jugadores:
            if j1.es_local:
                # Solo intento robar si NO tengo la bandera
                if self.bandera.portador != j1:
                    for j2 in lista_jugadores:
                        if j1 != j2:
                            # Si robo a alguien, aviso de un RESET
                            if j1.robar(j2, self.bandera):
                                self.red.enviar({'id': self.mi_id, 'evento': 'RESET'})
                                self.resetear_ronda() # Me reseteo yo tambien visualmente al instante

                # Controlamos el suicidio con la bandera
                else: 
                    # Comprobamos si choco con algun enemigo
                    for enemigo in lista_jugadores:
                        if j1 != enemigo and j1.rect.colliderect(enemigo.rect):
                            self.red.enviar({'id': self.mi_id, 'evento': 'RESET'})
                            self.resetear_ronda() # Me reseteo al instante
                            break

        # Verificacion de puntos
        self.verificar_puntos()

    # Verificar si algún jugador ha anotado
    def verificar_puntos(self):
        portador = self.bandera.portador
        
        # Solo verificamos si nosotros llevamos la bandera (Autoridad)
        if portador and portador.es_local:
            anoto_punto = False
            
            # Verificamos colisión con la base correspondiente según el ID
            if portador.id == 1 and portador.rect.colliderect(BASE_ROJA):
                anoto_punto = True
            elif portador.id == 2 and portador.rect.colliderect(BASE_AZUL):
                anoto_punto = True
            elif portador.id == 3 and portador.rect.colliderect(BASE_AMARILLA):
                anoto_punto = True
            elif portador.id == 4 and portador.rect.colliderect(BASE_VERDE):
                anoto_punto = True
            # Si anotó, incrementamos puntos y reseteamos ronda
            if anoto_punto:
                portador.puntos += 1
                print(f"{portador.NombreJugador} con ID: {portador.id} anotó un punto!")
                self.resetear_ronda()
                datos_puntuar = {
                    'id': self.mi_id,
                    'evento': 'RESET',         # Indicamos que es un reset de ronda
                    'puntos': portador.puntos   # Enviamos el dato actualizado
                }
                self.red.enviar(datos_puntuar)
            

    # Funcion para resetear la ronda
    def resetear_ronda(self):
        self.bandera.reiniciar()
        # Reiniciamos a TODOS los jugadores
        for jugador in self.jugadores.values():
            if hasattr(jugador, 'reiniciar_posicion'): # Si el metodo existe
                jugador.reiniciar_posicion()
            else:
                 # Backup por si no existe el metodo en jugador
                jugador.rect.x = jugador.inicio_x
                jugador.rect.y = jugador.inicio_y

    # Dibujamos todos los elementos en la pantalla
    def dibujar(self):
        self.pantalla.fill(BLANCO)
        
        # Dibujar Obstáculos
        for muro in self.obstaculos:
            pygame.draw.rect(self.pantalla, GRIS, muro)

        # Dibujo las 4 Bases 
        pygame.draw.rect(self.pantalla, COLOR_BASE_ROJA, BASE_ROJA)
        pygame.draw.rect(self.pantalla, COLOR_BASE_AZUL, BASE_AZUL)
        pygame.draw.rect(self.pantalla, COLOR_BASE_AMARILLA, BASE_AMARILLA)
        pygame.draw.rect(self.pantalla, COLOR_BASE_VERDE, BASE_VERDE)
        # Dibujar puntos de cada jugador en su base
        mapa_bases = {
            1: BASE_ROJA,
            2: BASE_AZUL,
            3: BASE_AMARILLA,
            4: BASE_VERDE
        }
        for jugador in self.jugadores.values():
            # Buscamos la base que le toca a este jugador
            rect_base = mapa_bases.get(jugador.id) # Obtener el rectángulo de la base
            if rect_base:
                texto_nombre = self.fuentenombre.render(str(jugador.NombreJugador), True, NEGRO)
                texto_puntos = self.fuenteptos.render(str(jugador.puntos), True, NEGRO) 
                #Centrado de texto
                rect_texto = texto_puntos.get_rect(center=rect_base.center)
                rect_nombre = texto_nombre.get_rect(midbottom=(rect_base.centerx, rect_texto.top))
                #Poner texto en pantalla
                self.pantalla.blit(texto_puntos, rect_texto)
                self.pantalla.blit(texto_nombre, rect_nombre)

        # Dibujar jugadores
        for jugador in self.jugadores.values():
            jugador.dibujar(self.pantalla)
            
        self.bandera.dibujar(self.pantalla)

        # Actualizamos la pantalla
        pygame.display.flip()

    # Funcion que arranca el juego
    def correr(self):
        while self.ejecutando:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)
        # Salimos del juego
        if self.red.cliente:
            self.red.cliente.close()
        pygame.quit()
        sys.exit()