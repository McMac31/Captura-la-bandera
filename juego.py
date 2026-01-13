import pygame
import sys
from config import *
from jugador import Jugador
from bandera import Bandera

#Clase principal del juego
class Juego:
    def __init__(self):
        #Inicializamos el juego
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.ejecutando = True
        self.crear_objetos()

    #Creamos los objetos del juego
    def crear_objetos(self):
        self.j_rojo = Jugador(20, ALTO//2 - 20, ROJO, TECLAS_ROJO)
        self.j_azul = Jugador(ANCHO - 60, ALTO//2 - 20, AZUL, TECLAS_AZUL)
        self.bandera = Bandera()

    #Manjeamos los eventos del juego de salida
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False

    #Actualizamos el estado del juego
    def actualizar(self):
        self.j_rojo.mover()
        self.j_azul.mover()
        self.bandera.actualizar(self.j_rojo, self.j_azul)
        self.j_rojo.intentar_robar(self.j_azul, self.bandera)
        self.j_azul.intentar_robar(self.j_rojo, self.bandera)
        self.verificar_puntos()

    #Verificar si algún jugador ha anotado
    def verificar_puntos(self):
        if self.bandera.portador == self.j_rojo and self.j_rojo.rect.colliderect(BASE_ROJA_RECT):
            self.j_rojo.puntos += 1
            self.resetear_ronda()
        elif self.bandera.portador == self.j_azul and self.j_azul.rect.colliderect(BASE_AZUL_RECT):
            self.j_azul.puntos += 1
            self.resetear_ronda()

    #Funcion para resetear la ronda
    def resetear_ronda(self):
        self.bandera.reiniciar()
        self.j_rojo.reiniciar_posicion()
        self.j_azul.reiniciar_posicion()

    #Dibujamos todos los elementos en la pantalla
    def dibujar(self):
        self.pantalla.fill(BLANCO)
        pygame.draw.rect(self.pantalla, COLOR_BASEROJA, BASE_ROJA_RECT)
        pygame.draw.rect(self.pantalla, COLOR_BASEAZUL, BASE_AZUL_RECT)
        pygame.draw.line(self.pantalla, (220, 220, 220), (ANCHO//2, 0), (ANCHO//2, ALTO), 2)

        #Dibujamos jugadores y bandera
        self.j_rojo.dibujar(self.pantalla)
        self.j_azul.dibujar(self.pantalla)
        self.bandera.dibujar(self.pantalla)

        # Actualizamos la pantalla
        pygame.display.flip()

    #Funcion que arranca el juego
    def correr(self):
        while self.ejecutando:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)
        # Salimos del juego
        pygame.quit()
        sys.exit()