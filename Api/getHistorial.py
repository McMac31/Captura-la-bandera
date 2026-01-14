import requests
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