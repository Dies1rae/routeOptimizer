import os
import math
import re


class coordPoint:
    lat : float = 0.0
    lon : float = 0.0
    price : int = 0



    def __init__(self, lat: float, lon: float, p: int = 0):
        self.lat = lat
        self.lon = lon
        self.price = p


    @property
    def Lat(self) -> float:
        return self.lat


    @property
    def Lon(self) -> float:
        return self.lon


    @property
    def Price(self) -> int:
        return self.price


    def setPrice(self, p : int):
        self.price = p


    def setLat(self, lt : float):
        self.lat = lt


    def setLon(self, ln : float):
        self.lon = ln


    def printCoord(self):
        print(f"Latitude: {self.Lat}  Longitude: {self.Lon}")


    def printInfo(self):
        print(f"Latitude: {self.Lat}  Longitude: {self.Lon} Price: {self.Price}")


    def isZero(self) -> bool:
        return self.Lat == 0.0 or self.Lon == 0.0



class coordStorageReader:
    coordlist = list()
    sortedByDstCoordList = list ()

    startPoint : coordPoint = coordPoint(0.0, 0.0)
    currPoint : coordPoint = coordPoint(0.0, 0.0)
    nextPoint : coordPoint = coordPoint(0.0, 0.0)
    finishPoint : coordPoint = coordPoint(0.0, 0.0)
    maxDistanceFromStart : int = 715 / 2



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
            p.printInfo()


    def printSortedCoords(self):
        print(f"Start point:")
        self.getStartPoint.printCoord()
        print(f"Next points of sortedlist:")
        for p in self.sortedCoordList:
            p.printInfo()


    def readFromFile(self, coFilePath: str):
        with open(coFilePath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                coords = re.split(r'[,, ]+', line)
                try:
                    point : coordPoint
                    if(len(coords) < 3):
                        point = coordPoint(float(coords[0]), float(coords[1]))
                    else:
                        point = coordPoint(float(coords[0]), float(coords[1]), int(coords[2]))
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
                file.write(f"Latitude: {cP.Lat},  Longitude: {cP.Lon},  Price: {cP.Price}\n")


    def sortArrayByDistanceToStart(self):
        if(len(self.coordList) <= 0 or self.startPoint.isZero()):
            print("Error in storing coords, cant sort. Exiting")
            return
        
        self.setCurrPoint(self.getStartPoint)
        self.setSortedStorePoint(self.getCurrPoint)

        tmp_coord_list = self.coordList.copy()
        ptr : int  = 0
        noSortedListSize : int = len(tmp_coord_list)
        while (ptr < noSortedListSize):
            coord_dist = self.findClosestToPoint(tmp_coord_list)
            self.setNextPoint(coord_dist[0])
            print("Closest point to:")
            self.getCurrPoint.printCoord()
            print("Its this point:")
            self.getNextPoint.printCoord()
            print("With distance: " + str(coord_dist[1]))
            ptr_tmp : int = tmp_coord_list.index(self.getNextPoint)
            self.setSortedStorePoint(self.getNextPoint)
            self.setCurrPoint(self.sortedCoordList[-1]) 
            tmp_coord_list.pop(ptr_tmp)
            ptr += 1


    def findClosestToPoint(self, pointlist : list, min_dst : int = float('inf')) -> list:
        earthRad : int = 6371 #Earth radius in KM
        res_point : coordPoint
        for cP in pointlist:
                dLat : float = (cP.Lat - self.currPoint.Lat) * math.pi / 180
                dLon : float = (cP.Lon - self.currPoint.Lon) * math.pi / 180
                a : float = math.sin(dLat / 2) * math.sin((dLat / 2) + 
                        math.cos(self.currPoint.Lat * math.pi / 180) * math.cos(cP.Lat * math.pi / 180)) * math.sin(dLon / 2) * math.sin(dLon / 2)
                c : float = 2 * math.atan2(math.sqrt(abs(a)), math.sqrt(1 - abs(a)))
                dst = earthRad * c
                #dst = math.sqrt( (cP.Lat - self.currPoint.Lddat)**2 + (cP.Lon - self.currPoint.Lon)**2 )
                if dst < min_dst:
                    min_dst = dst
                    res_point = cP
        return res_point, min_dst


    def findBestPrice(self) -> int:
        max_p : coordPoint = max(self.coordList, key=lambda cP: cP.price)
        return max_p.Price

    
