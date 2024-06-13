import pandas as pd
from fastapi import FastAPI

metro = pd.read_excel('xlsx/metro.xlsx')
normal_estandar = pd.read_excel('xlsx/normal_estandar.xlsx')
alto_estandar = pd.read_excel('xlsx/alto_estandar.xlsx')
puntos_bip = pd.read_excel('xlsx/puntos_bip.xlsx')
retail = pd.read_excel('xlsx/retail.xlsx')

columns = {
    'metro': ['CODIGO', 'ENTIDAD', 'ESTACION', 'DIRECCION', 'COMUNA', 'HORARIO', 'ESTE', 'NORTE', 'LONGITUD', 'LATITUD'],
    'estandar': ['CODIGO', 'ENTIDAD', 'DIRECCION', 'COMUNA', 'HORARIO', 'ESTE', 'NORTE', 'LONGITUD', 'LATITUD'],
    'estandar_with_name': ['CODIGO', 'ENTIDAD', 'NOMBRE', 'DIRECCION', 'COMUNA', 'HORARIO', 'ESTE', 'NORTE', 'LONGITUD', 'LATITUD']
}

metro.columns = pd.Index(columns['metro'])
normal_estandar.columns = pd.Index(columns['estandar'])
alto_estandar.columns = pd.Index(columns['estandar'])
puntos_bip.columns = pd.Index(columns['estandar_with_name'])
retail.columns = pd.Index(columns['estandar_with_name'])

cond = 'COMUNA'

metro = metro.dropna(subset = cond).reset_index(drop = True).drop(index = 0).reset_index(drop = True).drop(['NORTE', 'ESTE'], axis = 1)
normal_estandar = normal_estandar.dropna(subset = cond).reset_index(drop = True).drop(index = 0).reset_index(drop = True).drop(['NORTE', 'ESTE'], axis = 1)
alto_estandar = alto_estandar.dropna(subset = cond).reset_index(drop = True).drop(index = 0).reset_index(drop = True).drop(['NORTE', 'ESTE'], axis = 1)
puntos_bip = puntos_bip.dropna(subset = cond).reset_index(drop = True).drop(index = 0).reset_index(drop = True).drop(['NORTE', 'ESTE'], axis = 1)
retail = retail.dropna(subset = cond).reset_index(drop = True).drop(index = 0).reset_index(drop = True).drop(['NORTE', 'ESTE'], axis = 1)

metro = metro.assign(CATEGORIA='Metro').assign(FUNCIONES='Venta de tarjeta, Carga de tarjeta, Consulta de saldo, Activacion de carga remota')
normal_estandar = normal_estandar.assign(CATEGORIA='Centro Bip!').assign(FUNCIONES='Venta de tarjeta, Carga de tarjeta, Consulta de saldo, Activacion de carga remota')
alto_estandar = alto_estandar.assign(CATEGORIA='Centro Bip! Full').assign(FUNCIONES='Venta de tarjeta, Carga de tarjeta, Consulta de saldo, Activacion de carga remota, Reemplazo de tarjeta, Recuperacion de saldo de tarjetas corrompidas')
puntos_bip = puntos_bip.assign(CATEGORIA='Punto Bip!').assign(FUNCIONES='Carga de tarjeta, Consulta de saldo, Activacion de carga remota')
retail = retail.assign(CATEGORIA='Supermercados').assign(FUNCIONES='Carga de tarjeta')

retail = retail.drop('ENTIDAD', axis=1).rename(columns={'NOMBRE': 'ENTIDAD'})
puntos_bip = puntos_bip.drop('ENTIDAD', axis=1).rename(columns={'NOMBRE': 'ENTIDAD'})
metro['ENTIDAD'] = metro['ENTIDAD'].apply(lambda x: x + ' ').values + metro['ESTACION'].values
metro.drop('ESTACION', axis=1, inplace=True)

df = pd.concat([metro, normal_estandar, alto_estandar, puntos_bip, retail], axis=0).reset_index()

json = df.to_json()

app = FastAPI()

@app.get("/api/v1/resource")
def read_resource():
    global json
    return {'result': json}

