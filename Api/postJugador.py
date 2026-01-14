import requests
# ------------------------------
# ENVÍA RESULTADO AL BACKEND
# ------------------------------
nombre = input("Introduce tu nombre: ")
email = input("Introduce tu email: ")

url = "http://35.171.209.196:8080/api/jugadores"  # Cambia si usas EC2
jugador ={
        "nombre": nombre,
        "email": email
    }

try:
    print("\nEnviando datos al servidor...\n")
    r = requests.post(url, json=jugador, timeout=5)
    print("Respuesta del servidor:", r.text)

except requests.exceptions.ConnectTimeout:
    print("⏱️ Timeout de conexión: no se pudo conectar con el servidor")

except Exception as e:
    print("Error enviando datos:", e)