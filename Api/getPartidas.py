import requests
# ------------------------------
# OBTENER PARTIDAS DEL BACKEND
# ------------------------------

url_get = "http://35.171.209.196:8080/api/partidas"

try:
    print("\nObteniendo partidas del servidor...\n")
    r = requests.get(url_get, timeout=5)

    if r.status_code == 200:
        partidas = r.json()
        print("PARTIDAS:")
        for j in partidas:
            print(f" {j['id']} - Duracion: {j['duracion']} | Jugadores: {j['jugadorIds']} | Scores: {j['scores']}")

    else:
        print("Error:", r.status_code, r.text)

except requests.exceptions.ConnectTimeout:
    print("⏱️ Timeout de conexión")

except Exception as e:
    print("Error obteniendo jugadores:", e)
