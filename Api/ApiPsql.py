from asyncio import timeout
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
# ------------------------------
# ENTRADA DE DATOS DEL JUGADOR
# ------------------------------
nombre = input("Introduce tu nombre: ")
email = input("Introduce tu email: ")
score = 0
# ------------------------------
# ENVÍA RESULTADO AL BACKEND
# ------------------------------

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
# ------------------------------
# OBTENER PARTIDAS DEL BACKEND
# ------------------------------

url_get = "http://35.171.209.196:8080/api/partidas"

try:
    print("\nObteniendo jugadores del servidor...\n")
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

# ------------------------------
# OBTENER HISTORIAL DEL BACKEND
# ------------------------------

url_get = "http://35.171.209.196:8080/api/jugadores/2/estadisticas"
try:
    print("\nObteniendo Historial del servidor...\n")
    r = requests.get(url_get, timeout=5)

    if r.status_code == 200:
        historial = r.json()
        j= r.json()
        print("HISTORIAL:")
        #for j in historial:
        print(f" {historial['jugadorId']} - Duracion Total: {historial['duracionTotal']} | Partidas jugadas: {historial['totalPartidas']} | Scores: {historial['scoreTotal']}")
        print(f"Jugador: {j['jugadorId']} - duracionTotal {j['duracionTotal']} - Score min: {j['scoreMinimo']} - Score max: {j['scoreMaximo']}")
        # "duracionPromedio", "duracionTotal", "jugadorId","scoreMaximo","scoreMinimo", "scorePromedio"."scoreTotal","totalPartidas"
    else:
        print("Error:", r.status_code, r.text)
except requests.exceptions.ConnectTimeout:
    print("⏱️ Timeout de conexión")
except Exception as e:
    print("Error obteniendo historial:", e)
# ------------------------------
# OBTENER RANKING DEL BACKEND
# ------------------------------

url_get = "http://35.171.209.196:8080/api/jugadores/ranking"
try:
    print("\nObteniendo Ranking del servidor...\n")
    r = requests.get(url_get,timeout=5)

    if r.status_code==200:
        ranking= r.json()
        print("RANKING:")
        for j in ranking:
            print(f"Nombre: {j['nombre']} - Partidas: {j['totalPartidas']} - Score: {j['scoreTotal']} - Duracion: {j['duracionTotal']}")
    else:
        print("Error:",r.status_code,r.text)
except requests.exceptions.ConnectTimeout:
    print("Timeout de conexión")
except Exception as e:
    print("Error obteniendo ranking",e)
# ------------------------------
# OBTENER ESTADÍSTICA DEL BACKEND
# ------------------------------
url_get = "http://35.171.209.196:8080/api/estadisticas"
try:
    print("\nEstadisticas del servidor")
    r=requests.get(url_get, timeout=5)

    if r.status_code==200:
        j=r.json()
        print("ESTADÍSTICA")
        #for j in estadistica:

        print(f"Promedio Jugadores por Partida: {j['promedioJugadoresPorPartida']} - Promedio Score PorPartida:  {j['promedioScorePorPartida']} - Total Jugadores: {j['totalJugadores']} - Total Partidas: {j['totalPartidas']} - Promedio Duracion Por Partida: {j['promedioDuracionPorPartida']}")
    else:
        print("Error", r.status_code,r.text)
except requests.exceptions.ConnectTimeout:
    print("Timeout de conexión")
except Exception as e:
    print("error obteniendo estadística",e)















