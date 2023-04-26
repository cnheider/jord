from qgis.core import *  # attach main QGIS library
from qgis.utils import *  # attach main python library


def single_vector_layer():
    # Attach libraries

    import os  # attach operating system library

    # Set the working directory
    wd = "C:/test"  # Set work directory
    os.chdir(wd)  # Change the directory

    # Set a variable for the current project instance
    Prj = QgsProject().instance()  # Object for current project

    # Save the project to this file name
    pnm = "Test.qgs"  # Project file name
    pnm = wd + "/" + pnm  # Concat. with path
    Prj.write(pnm)  # Save the project

    # Create an array [] object with the polygon vertices
    vrtcs = []
    vrtcs.append(QgsPointXY(396100, 8969000))
    vrtcs.append(QgsPointXY(396100, 8973900))
    vrtcs.append(QgsPointXY(397900, 8973900))
    vrtcs.append(QgsPointXY(397900, 8969000))

    # Create a polygon from the vertices
    ply_01 = QgsGeometry.fromPolygonXY([vrtcs])

    # Create a feature object then append the polygon into
    ftr = QgsFeature()
    ftr.setGeometry(ply_01)
    print(ftr.geometry())

    # Create a layer for the feature and add to the project
    lyr = QgsVectorLayer("Polygon?crs=epsg:29194", "Test", "memory")
    Prj.addMapLayers([lyr])

    # Make the layer editable, add the feature and save
    lyr.startEditing()
    lyr.addFeature(ftr)
    lyr.commitChanges()

    # Save as a shapefile
    Fl_ou = "Test.shp"
    Fl_ou = wd + "/" + Fl_ou

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"

    QgsVectorFileWriter.writeAsVectorFormatV2(
        lyr, Fl_ou, QgsCoordinateTransformContext(), options
    )


def multiple_raster_layers():
    myDir = r"C:\temp"
    layers = layers = iface.mapCanvas().layers()
    pipe = QgsRasterPipe()
    for layer in layers:
        extent = layer.extent()
    width, height = layer.width(), layer.height()
    renderer = layer.renderer()
    provider = layer.dataProvider()
    crs = layer.crs().toWkt()
    pipe.set(provider.clone())
    pipe.set(renderer.clone())
    file_writer = QgsRasterFileWriter("%s\\%s.tif" % (myDir, layer.name()))
    file_writer.writeRaster(pipe, width, height, extent, layer.crs())
    print
    "%s\\%s.tif" % (myDir, layer.name())
