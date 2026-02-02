import pygame
from config import *
import math
#Clase Bandera
class Bandera:
    def __init__(self):
        # Inicializamos la bandera
        self.rect = pygame.Rect(0, 0, 30, 45)
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.portador = None
        self.capturada = False
        self.oscilacion = 0

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
        # 1. Dibujamos el Mástil (una línea gris oscura)
        pygame.draw.line(pantalla, (100, 100, 100), 
                         (self.rect.left, self.rect.bottom), 
                         (self.rect.left, self.rect.top), 3)
        
        # 2. Calculamos el movimiento de la tela con una onda seno
        offset = math.sin(self.oscilacion) * 5
        
        # 3. Dibujamos la Tela (un polígono triangular que vibra)
        puntos_tela = [
            (self.rect.left, self.rect.top),
            (self.rect.right + offset, self.rect.top + 12),
            (self.rect.left, self.rect.top + 25)
        ]
        
        # Usamos el color configurado o el verde por defecto
        color = VERDE_BANDERA if 'VERDE_BANDERA' in globals() else (50, 200, 50)
        
        pygame.draw.polygon(pantalla, color, puntos_tela)
        # Un pequeño borde negro para que resalte
        pygame.draw.polygon(pantalla, NEGRO, puntos_tela, 2)
        
       