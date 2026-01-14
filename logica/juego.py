import pygame
import sys
from config import *
from entidades.jugador import Jugador
from entidades.bandera import Bandera
from red.cliente_red import ClienteRed

# Clase principal del juego
class Juego:
    def __init__(self,nombre_jugador,email_jugador):
        # Inicializamos el juego
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.nombrelocal=nombre_jugador
        self.emaillocal=email_jugador
        self.red=ClienteRed()
        self.fuente = pygame.font.SysFont("Impact", 40)
        if self.red.conectar():
            print("Conectado al servidor de juego.")
            
        
            self.mi_id=self.red.id
        else:
            print("No se pudo conectar al servidor de juego.")

        # Cargar obstaculos desde config
        self.obstaculos = OBSTACULOS
        # Diccionario de jugadores
        self.jugadores = {}
        
        # Definimos quiénes somos (por defecto el 1/Rojo para pruebas locales)
        self.crear_objetos()

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
        #Control de red: procesar mensajes entrantes
        if self.mi_id in self.jugadores:
            jugador_local= self.jugadores[self.mi_id]

            #Guardado de posicion anterior
            pos_anterior=(jugador_local.rect.x, jugador_local.rect.y)
            jugador_local.mover(self.obstaculos) #Movimiento local

            if (jugador_local.rect.x, jugador_local.rect.y) != pos_anterior: #Si hubo cambio de posicion
                datos={
                    'id': self.mi_id,
                    'posicion':{"x": jugador_local.rect.x, "y": jugador_local.rect.y},
                    'puntos': jugador_local.puntos,
                    'nombre': jugador_local.NombreJugador,
                    'email': jugador_local.EmailJugador}
                self.red.enviar(datos) #Envio de nueva posicion al servidor
                
            #Recepcion de datos del servidor
            mensajes=self.red.obtener_mensajes()
            for mensaje in mensajes:
                if "posicion" in mensaje and "id"in mensaje: #Mensaje de posicion de otro jugador
                    id_remoto=mensaje['id']
                    if id_remoto != self.mi_id and id_remoto in self.jugadores: #Si no soy yo y conozco al jugador
                        pos= mensaje['posicion']
                        self.jugadores[id_remoto].establecer_posicion(pos['x'], pos['y']) #Actualizacion de posicion remota
                # Actualizacion de puntos si viene en el mensaje
                if "puntos" in mensaje:
                        self.jugadores[id_remoto].puntos = mensaje['puntos']
                    # Actualizacion de nombre si viene en el mensaje
                if "nombre" in mensaje:
                        self.jugadores[id_remoto].nombre = mensaje['nombre']
        
        # Lista jugadores 
        lista_jugadores = list(self.jugadores.values())

        # Actualizar Bandera
        # (Ahora usamos el nuevo método que acepta la lista de jugadores)
        self.bandera.actualizar(lista_jugadores)

        # Verificacion de robos
        for j1 in lista_jugadores:
            for j2 in lista_jugadores:
                if j1 != j2:
                    j1.robar(j2, self.bandera)

        # Verificacion de puntos
        self.verificar_puntos()

    # Verificar si algún jugador ha anotado
    def verificar_puntos(self):
        portador = self.bandera.portador
        
        if portador:
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
                print(f"¡Jugador {portador.id} ({portador.color}) anotó un punto!")
                self.resetear_ronda()

    # Funcion para resetear la ronda
    def resetear_ronda(self):
        self.bandera.reiniciar()
        # Reiniciamos a TODOS los jugadores
        for jugador in self.jugadores.values():
            jugador.reiniciar_posicion()

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
                texto_puntos = self.fuente.render(str(jugador.puntos), True, NEGRO) #
                #Centrado de texto
                rect_texto = texto_puntos.get_rect(center=rect_base.center)
                #Poner texto en pantalla
                self.pantalla.blit(texto_puntos, rect_texto)

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
        pygame.quit()
        sys.exit()