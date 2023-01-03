from qgis.core import QgsMapLayerRegistry, QgsRasterLayer

from jord.qgis_utilities import read_project_setting

read_project_setting("WMS_SERVER_PATH")

# TODO ADD A WAY TO ADD A LAYER TO THE MAP

# wms_url="http://localhost/MapServer/mapserv.exe?map=c:/inetpub/wwwroot/data//Mapfile.map&request=GetMap&service=WMS&version=1.3.0&layers=Region_Map&width=480.000&height=480.000&format=image/png&bbox=8.473957,77.262417,8.519412,77.307871&crs=EPSG:4326&styles="
wms_url = "url=http://localhost/MapServer/mapserv.exe?map=Mapfile.map&layers=layers&styles=&format=image/png&crs=EPSG:4326"
# wms_url = wms_url + "&styles="
print(wms_url)
# setting prefix path of qgis
# TODO: get this path dynamically
# qgis_prefix = "C:\\OSGeo4W64\\apps\\qgis-ltr"
# QgsApplication.setPrefixPath(qgis_prefix, True)
# QgsApplication.initQgis()

# adding the WMS Layer
rlayer = QgsRasterLayer(wms_url, "default map", "wms", True)
print(rlayer.isValid())
if rlayer.isValid:
    QgsMapLayerRegistry.instance().addMapLayer(rlayer)
else:
    print(rlayer.error().message())
