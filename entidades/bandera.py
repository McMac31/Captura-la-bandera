import pygame
from config import *

#Clase Bandera
class Bandera:
    def __init__(self):
        # Inicializamos la bandera
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.portador = None
        self.capturada = False

    #Funcion para que la bandera vuelva a la posicion inicial
    def reiniciar(self):
        self.portador = None
        self.capturada = False
        self.rect.center = (ANCHO // 2, ALTO // 2)

    def actualizar(self, lista_jugadores=None): # Mantenemos el argumento por compatibilidad, aunque no se use
        # La bandera SOLO se mueve si tiene portador asignado por el servidor
        if self.portador:
            self.rect.center = self.portador.rect.center
            self.capturada = True

    #Funcion para dibujar la bandera
    def dibujar(self, pantalla):
        # Usamos VERDE_BANDERA si existe, si no el verde normal
        color = VERDE_BANDERA if 'VERDE_BANDERA' in globals() else VERDE
        pygame.draw.rect(pantalla, color, self.rect) #La bandera es verde
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2) #Borde de la bandera