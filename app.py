from geopy.distance import geodesic
import simplekml
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import models

app = FastAPI()

class Addresses(BaseModel): # Serializar
    id: int
    codigo_postal: int
    lat: float
    lon: float
    nombre_comuna: str
    nombre_calle: str
    numero_municipal: int

    class Config:
        orm_true: True

db = SessionLocal()

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

def crear_kml(ruta_optima):
    kml = simplekml.Kml()
    ruta = kml.newlinestring(name="Ruta Óptima")

    for punto in ruta_optima:
        latitud, longitud = punto
        ruta.coords.addcoordinates([(longitud, latitud)])

    return ruta
    # ruta_archivo_kml = "ruta_optima.kml"
    # kml.save(ruta_archivo_kml)
    # print("Archivo KML generado y guardado con éxito.")

@app.get('/')
def read_root():
    return {"welcome":"Welcome to my REST API!",
            "message":"Initial route"}


@app.get('/obtener_direcciones')
def leer_direcciones():
    return {"message":"conjunto de direcciones"}
    

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
  
    rop = crear_kml(ruta_optima)
    print(rop)
    response = {
        "ruta_op" :  ruta_optima,
        "kml_rop" :  str(rop),
        "url" : url
    }
    
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

@app.get('/addresses', response_model = List[Addresses], status_code = 200)
async def get_all_addresses():
    # addresses = db.query(models.Addresses).all()
    response = db.query(models.Addresses).all()
    
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

# @app.get('/addresses/{nombre_comuna}', response_model = List[Addresses], status_code = 200)
@app.get('/addresses/{nombre_comuna}' )
async def get_common_addresses(nombre_comuna: str):

    try:
        filtro = nombre_comuna
        result = db.query(models.Addresses).filter(models.Addresses.nombre_comuna == filtro.upper()).all()
        json_compatible_item_data = jsonable_encoder(result)
        return JSONResponse(content=json_compatible_item_data)
    except:
        print("An exception occurred")
    

    
