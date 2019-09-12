import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\OSGeo4W64\apps\Qt5\plugins'
os.environ['QGIS_PREFIX_PATH'] = r'C:\OSGeo4W64\apps\qgis'
os.environ['PATH'] += r';C:\OSGeo4W64\apps\qgis\bin;C:\OSGeo4W64\apps\Qt5\bin;C:\OSGeo4W64\apps\qgis\python\plugins'

import sys
from qgis.core import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

def buffering(outLayer, distance, layer, segments):
    features = layer.getFeatures()

    for inFeat in features:
        outFeat = QgsFeature()
        inGeom = QgsGeometry()
        outGeom = QgsGeometry()
        
        attrs = inFeat.attributes()
        print(attrs)
        inGeom = QgsGeometry(inFeat.geometry())
        outGeom = inGeom.buffer(float(distance), segments)
        #wkt = outGeom.asWkt()
        #print(wkt)

        outFeat.setGeometry(outGeom)
        outFeat.setAttributes(attrs)
   
        outLayer.addFeature(outFeat)
        del outFeat, inGeom, outGeom

QgsApplication.setPrefixPath("C:\\OSGeo4W\\apps\\qgis\\", True)
qgs = QgsApplication([], True)
qgs.initQgis()

sys.path.append(r'C:\OSGeo4W64\apps\qgis\python\plugins')
import processing
from processing.core.Processing import Processing
Processing.initialize()

#inLayer = QgsProject.instance().mapLayersByName('befolkning')[0]
inLayer = QgsVectorLayer("C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/befolkning.shp", "befolkning", "ogr")


print(inLayer.isValid())
provider = inLayer.dataProvider()
fields = provider.fields()

#for feature in inLayer.getFeatures():
#    print("Feature ID: ", feature.id())

for rad in range(2000,11000,1000):
    outPath = f'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/circles_{rad}.shp'
    #writer = QgsVectorFileWriter(f'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/Test{rad}.shp', 'CP1250', fields, 100, provider.sourceCrs(), "ESRI Shapefile")
    if os.path.isfile(outPath):
        os.remove(outPath)
    outLayer = QgsVectorLayer('Polygon?crs=EPSG:3006', "buffers", "memory")
    pr = outLayer.dataProvider() 
    pr.addAttributes(fields)
    outLayer.updateFields()
    outLayer.startEditing()
    buffering(outLayer, rad, inLayer, 4)
    outLayer.commitChanges()
    print(outLayer.featureCount())
    QgsVectorFileWriter.writeAsVectorFormat(outLayer, outPath, 'CP1250', provider.sourceCrs(), 'ESRI Shapefile')
    
    newLayer = QgsVectorLayer(outPath,"Circles","ogr")
    newLayer.dataProvider().createSpatialIndex()
    print(newLayer.featureCount())


    joinPath = 'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/befolkning.shp'
    outPathJoin = f'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/befolkning_circle{rad}.shp'
    processing.run("qgis:joinattributesbylocation",{
                            "INPUT":newLayer, 
                            "JOIN":joinPath,
                            "PREDICATE":0,
                            "METHOD":0,
                            "DISCARD_NONMATCHING":0,
                            "PREFIX":f"m{rad}_",
                            "OUTPUT":outPathJoin})


    outLayer = QgsVectorLayer(f'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/befolkning_circle{rad}.shp',"Circles","ogr")
    csvOut = f'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/befolkning_circle_{rad}.csv'
    QgsVectorFileWriter.writeAsVectorFormat(outLayer, csvOut, "utf-8", outLayer.crs(),"CSV",layerOptions =['GEOMETRY=NULL'])
    del outLayer
    if os.path.isfile(outPathJoin):
        os.remove(outPathJoin)
        os.remove(f'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/befolkning_circle{rad}.dbf')