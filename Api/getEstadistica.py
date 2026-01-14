import requests
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
