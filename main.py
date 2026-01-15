from logica.juego import Juego
from email_validator import validate_email, EmailNotValidError
# Punto de entrada del juego
if __name__ == "__main__":
    nombre_jugador=input("Ingrese su nombre: ")

    while True:
        try:
            email_jugador=input("Ingrese su email: ")
            validate_email(email_jugador)
            break
        except EmailNotValidError:
            print("Email inválido ingrese un formato correcto.")
    CapturaBandera=Juego(nombre_jugador,email_jugador)
    CapturaBandera.correr()