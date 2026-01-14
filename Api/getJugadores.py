import requests

# ------------------------------
# OBTENER JUGADORES DEL BACKEND
# ------------------------------

url_get = "http://35.171.209.196:8080/api/jugadores"

try:
    print("\nObteniendo jugadores del servidor...\n")
    r = requests.get(url_get, timeout=5)

    if r.status_code == 200:
        jugadores = r.json()
        print("Jugadores recibidos:")
        for j in jugadores:
            print(f"ID: {j['id']} - Nombre: {j['nombre']} | Email: {j['email']}")
    else:
        print("Error:", r.status_code, r.text)

except requests.exceptions.ConnectTimeout:
    print("⏱️ Timeout de conexión")

except Exception as e:
    print("Error obteniendo jugadores:", e)