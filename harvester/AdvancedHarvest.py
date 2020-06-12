import requests
import json
import pandas as pand
from arcgis.gis import GIS
from arcgis.features import Table,GeoAccessor, GeoSeriesAccessor
from IPython.display import display
gis = GIS()
#Medidas Sanitarias:0b944d9bf1954c71a7fae96bdddee464
Medidas=gis.content.get('0b944d9bf1954c71a7fae96bdddee464')
Capas=Medidas.layers
Cuarentenas=Capas[1]
CuarTotal=Cuarentenas.query(out_fields='CuarentenaID,Nombre,Estado,Alcance,FInicio,FTermino,Cut_Com,Detalle,Shape__Area,Shape__Length',return_geometry=False).sdf
CuarTotal.set_index("OBJECTID", inplace=True)
CuarActivas=CuarTotal[(CuarTotal['Estado'] == 1)|(CuarTotal['Estado'] == 3)]
CuarHistoricas=CuarTotal[(CuarTotal['Estado'] == 2)]
Productos=[CuarTotal,CuarActivas,CuarHistoricas]
for producto in Productos:
    producto.loc[(producto.Estado == 1),'Estado']='Activa'
    producto.loc[(producto.Estado == 2),'Estado']='Histórica'
    producto.loc[(producto.Estado == 3),'Estado']='Futura'
    producto.loc[(producto.Alcance == 1),'Alcance']='Comuna completa'
    producto.loc[(producto.Alcance == 2),'Alcance']='Área Urbana Completa'
    producto.loc[(producto.Alcance == 3),'Alcance']='Área Rural Completa'
    producto.loc[(producto.Alcance == 4),'Alcance']='Sector Específico'
    producto.rename(columns={'CuarentenaID': 'ID', 'FInicio': 'Fecha de Inicio','FTermino': 'Fecha de Término','Cut_Com': 'Código CUT Comuna','Shape__Area': 'Superficie en m2','Shape__Length': 'Perímetro en m'},inplace=True)
CuarTotal.to_csv(path_or_buf="../output/Cuarentenas-Totales.csv",index=False)
CuarActivas.to_csv(path_or_buf="../output/Cuarentenas-Activas.csv",index=False)
CuarHistoricas.to_csv(path_or_buf="../output/Cuarentenas-Historicas.csv",index=False)
url = "https://services1.arcgis.com/LsoiDXzijohT7g97/arcgis/rest/services/COVID19ChileAcciones/FeatureServer/1/query?where=1%3D1&outFields=Nombre,Estado,Alcance,FInicio,FTermino,Cut_Com,Detalle,Shape__Area,Shape__Length,CuarentenaID&outSR=4326&orderByFields=CuarentenaID+ASC&f=pgeojson"
payload = {}
headers= {}
response = requests.request("GET", url, headers=headers, data = payload)
data=response.json()
with open('../output/data.geojson', 'w', encoding="cp1252") as f:
    json.dump(data,f,indent=2)