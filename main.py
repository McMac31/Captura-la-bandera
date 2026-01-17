from logica.juego import Juego
from email_validator import validate_email, EmailNotValidError
from Api.api_servicio import APIService
# Punto de entrada del juego
if __name__ == "__main__":
    api=APIService()
    
    #Validacion de nombre y email
    while True:
        nombre_jugador = input("Ingrese su nombre: ").strip() # Usamos strip para quitar espacios extras
        if nombre_jugador: # Si la cadena no está vacía
            break
        else:
            print("El nombre no puede estar vacío. Por favor, ingrese un nombre.")

    while True:
        try:
            email_jugador=input("Ingrese su email: ")
            validate_email(email_jugador)
            break
        except EmailNotValidError:
            print("Email inválido ingrese un formato correcto.")
    CapturaBandera=Juego(nombre_jugador,email_jugador)
    api.registrar_jugador(nombre_jugador,email_jugador)
    CapturaBandera.correr()