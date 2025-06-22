import os
import math


class coordPoint:
    lat : float = 0.0
    lon : float = 0.0

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    @property
    def Lat(self) -> float:
        return self.lat

    @property
    def Lon(self) -> float:
        return self.lon

    def printCoord(self):
        print(f"Latitude: {self.Lat}  Longitude: {self.Lon}")
    
    def isZero(self) -> bool:
        return self.Lat == 0.0 and self.Lon == 0.0


class coordStorageReader:
    coordlist = list()
    sortedByDstCoordList = list ()

    startPoint : coordPoint = coordPoint(0.0, 0.0)
    currPoint : coordPoint = coordPoint(0.0, 0.0)
    nextPoint : coordPoint = coordPoint(0.0, 0.0)

    def __init__(self):
        pass

    @property
    def coordList(self) -> list:
        return self.coordlist

    @property
    def sortedCoordList(self) -> list:
        return self.sortedByDstCoordList

    @property
    def getStartPoint(self) -> coordPoint:
        return self.startPoint

    @property
    def getNextPoint(self) -> coordPoint:
        return self.nextPoint

    @property
    def getCurrPoint(self) -> coordPoint:
        return self.currPoint

    def setStorePoint(self, coPoint: coordPoint):
        self.coordlist.append(coPoint)

    def setSortedStorePoint(self, coPoint: coordPoint):
        self.sortedByDstCoordList.append(coPoint)

    def setStartPoint(self, stPoint: coordPoint):
        self.startPoint = stPoint

    def setNextPoint(self, point: coordPoint):
        self.nextPoint = point

    def setCurrPoint(self, point: coordPoint):
        self.currPoint = point

    def printCoords(self):
        print(f"Start point:")
        self.getStartPoint.printCoord()
        print(f"Next point of given list:")
        for p in self.coordList:
            p.printCoord()

    def printSortedCoords(self):
        print(f"Start point:")
        self.getStartPoint.printCoord()
        print(f"Next points of sortedlist:")
        for p in self.sortedCoordList:
            p.printCoord()

    def readFromFile(self, coFilePath: str):
        with open(coFilePath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                coords = line.strip().split(',')
                try:
                    point = coordPoint(float(coords[0]), float(coords[1]))
                    if(point.isZero()):
                        print("No storing to zero point. Pass...")
                        continue
                    self.setStorePoint(point)
                except ValueError:
                    pass
                    #print("ERROR WITH: {coords}")
        if(len(self.coordlist) > 0):
            self.setStartPoint(self.coordlist.pop(0))
    
    def writeSortedToFile(self, coFilePath: str):
        with open(coFilePath, 'w') as file:
            for cP in self.sortedCoordList:
                file.write(f"Latitude: {cP.Lat}  Longitude: {cP.Lon}\n")

    def findClosestPoint(self):
        if(len(self.coordlist) <= 0 or self.startPoint.isZero()):
            print("Error in storing coords, cant sort. Exiting")
            return
        if(len(self.sortedCoordList) == 0):
            self.setCurrPoint(self.getStartPoint)
            self.setSortedStorePoint(self.getCurrPoint)
        else:
            self.setCurrPoint(self.sortedCoordList[-1])
        min_dst = float('inf')
        earthRad : int = 6371 #Earth radius in KM
        for cP in self.coordlist:
            dLat : float = (cP.Lat - self.currPoint.Lat) * math.pi / 180
            dLon : float = (cP.Lon - self.currPoint.Lon) * math.pi / 180
            a : float = math.sin(dLat / 2) * math.sin((dLat / 2) + 
                        math.cos(self.currPoint.Lat * math.pi / 180) * math.cos(cP.Lat * math.pi / 180)) * math.sin(dLon / 2) * math.sin(dLon / 2)
            c : float = 2 * math.atan2(math.sqrt(abs(a)), math.sqrt(1 - abs(a)))
            dst = earthRad * c
            #dst = math.sqrt( (cP.Lat - self.currPoint.Lddat)**2 + (cP.Lon - self.currPoint.Lon)**2 )
            if dst < min_dst:
                min_dst = dst
                self.setNextPoint(cP)

        print("Closest point to:")
        self.getCurrPoint.printCoord()
        print("Its this point:")
        self.getNextPoint.printCoord()
        print("With distance: " + str(min_dst))
        ptr_tmp : int = self.coordlist.index(self.getNextPoint)
        self.setSortedStorePoint(self.getNextPoint)
        self.coordList.pop(ptr_tmp)
                

    
    
