import urllib2, json
url = "https://services1.arcgis.com/LsoiDXzijohT7g97/arcgis/rest/services/COVID19ChileAcciones/FeatureServer/1/query?where=1%3D1&outFields=CuarentenaID,Nombre,Estado,Alcance,FInicio,FTermino,Cut_Com,Detalle,Shape__Area,Shape__Length&outSR=4326&f=pgeojson"
response = urllib2.urlopen(url)
data = json.loads(response.read())
fixedata =json.dumps(data,sort_keys=True, indent=4,separators=(',', ':'))
file = open("../output/Cuarentenas-Test.geojson", "w")
file.write(fixedata)
file.close()
