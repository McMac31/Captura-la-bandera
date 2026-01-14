import requests
# ------------------------------
#Borrar Jugador
# ------------------------------

url = "http://35.171.209.196:8080/api/jugadores/1"

try:
    r = requests.delete(url, timeout=5)

    if r.status_code in (200, 204):
        print("✅ Jugador eliminado correctamente")
    else:
        print("❌ Error:", r.status_code, r.text)

except Exception as e:
    print("Error eliminando jugador:", e)
