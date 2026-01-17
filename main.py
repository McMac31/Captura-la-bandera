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

    # Registramos una sola vez y obtenemos el ID real de la base de datos
    id_db = api.registrar_jugador(nombre_jugador, email_jugador)
    if id_db:      
        # Enviar parametros de partida
        CapturaBandera = Juego(nombre_jugador, email_jugador, id_db)
        
        #Arrancar el juego SOLO si se registró correctamente
        CapturaBandera.correr()
    else:
        print("No se pudo conectar con AWS para registrar al jugador.")