import sys
import os
import geopandas as gpd
import matplotlib.pyplot as plt

from coord import coordPoint, coordStorageReader

mapOfRu = "/home/sensenet/Apps/PROJ/py/coord_parser/maps/ru.shp"


def showMap(mapfile: str):
    Map = gpd.read_file(mapfile)
    print(Map.shape)
    Map.plot()
    plt.show()


def main() -> int:
    coordstorage = coordStorageReader()
    
    coordstorage.readFromFile("/home/sensenet/Apps/PROJ/py/coord_parser/champ_coords")
    coordstorage.printCoords()
    ptr : int  = 0
    noSortedListSize : int = len(coordstorage.coordList)
    while ptr < noSortedListSize:
        coordstorage.findClosestPoint()   
        ptr += 1
    
    coordstorage.printSortedCoords()
    coordstorage.writeSortedToFile("/home/sensenet/Apps/PROJ/py/coord_parser/champ_coords_sorted")
    #showMap(mapOfRu)
    return 0


if __name__ == '__main__':
    main()
