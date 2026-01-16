from logica.juego import Juego
from email_validator import validate_email, EmailNotValidError
from API.api_servicio import APIService
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

    id_db = api.registrar_jugador(nombre_jugador, email_jugador)
    if id_db: # Si recibimos un ID válido 
        # Pasamos los datos al juego
        CapturaBandera = Juego(nombre_jugador, email_jugador, id_db) 
        # olo corremos el juego si el objeto se creó correctamente
        CapturaBandera.correr()
    else:
        print("Error: No se pudo registrar al jugador en AWS. Verifica tu conexión.")