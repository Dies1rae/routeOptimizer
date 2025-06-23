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
    coordstorage.sortArrayByDistanceToStart()
    
    coordstorage.printSortedCoords()
    coordstorage.writeSortedToFile("/home/sensenet/Apps/PROJ/py/coord_parser/champ_coords_sorted")
    print(coordstorage.findBestPrice())
    #showMap(mapOfRu)
    return 0


if __name__ == '__main__':
    main()
