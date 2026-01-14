import requests
url_get = "http://35.171.209.196:8080/api/ranking"
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