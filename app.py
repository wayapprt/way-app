from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

from geopy.distance import geodesic

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

class Position(BaseModel):
    lat: float
    lon: float 

def calcular_distancia_coordenadas(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

def calcular_ruta_optima(punto_partida, puntos_destino):
    ruta_optima = []
    ruta_optima.append(punto_partida[0])
    puntos_no_visitados = puntos_destino.copy()

    while puntos_no_visitados:
        punto_mas_cercano = min(puntos_no_visitados, key=lambda punto: calcular_distancia_coordenadas(ruta_optima[-1], punto))
        ruta_optima.append(punto_mas_cercano)
        puntos_no_visitados.remove(punto_mas_cercano)

    return ruta_optima

@app.get('/')
def read_root():
    return {"welcome":"Welcome to my REST API!",
            "message":"Initial route"}

@app.post('/definir_ruta', response_model = Position)
def definir_ruta(punto_partida: Position, puntos_destino: List[Position]):

    ppartida = [(punto_partida.lat,punto_partida.lon)]

    puntosXrecorrer = []

    for punto in puntos_destino:
        puntosXrecorrer.append((punto.lat,punto.lon))

    # Tenemos el ppartida = punto de partida y puntosXrecorrer: puntos por recorrer

    # llamamos a la funcion que contiene el algoritmo con la nueva posicion y el conjunto de posociones
    ruta_optima = calcular_ruta_optima(ppartida, puntosXrecorrer)

    # ruta_optima = calcular_ruta_optima(punto_partida,puntos_destino)
    url = "https://www.google.com/maps/dir/"
    for point in ruta_optima:
        latitud, longitud = point
        url += f"{latitud},{longitud}/"
  
    response = {
        "ruta_op" :  ruta_optima,
        "url" : url
    }
    
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

