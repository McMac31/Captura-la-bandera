from logica.juego import Juego
# Punto de entrada del juego
if __name__ == "__main__":
    nombre_jugador=input("Ingrese su nombre: ")
    email_jugador=input("Ingrese su email: ")
    CapturaBandera=Juego(nombre_jugador,email_jugador)
    CapturaBandera.correr()