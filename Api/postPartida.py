import requests

# ------------------------------
# ENVÍA RESULTADO AL BACKEND
# ------------------------------

url = "http://35.171.209.196:8080/api/partidas"  # Cambia si usas EC2
partida = {
                "duracion": 88,
                "id": 4,
                "jugadorIds": [4, 2, 3],
                "scores": [95, 80, 110]
        }
try:
    print("\nEnviando patida al servidor...\n")
    r = requests.post(url, json=partida, timeout=5)
    print("Respuesta del servidor:", r.text)

except requests.exceptions.ConnectTimeout:
    print("⏱️ Timeout de conexión: no se pudo conectar con el servidor")

except Exception as e:
    print("Error enviando datos:", e)