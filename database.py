import sys
import os.path
from tkinter import *
from tkinter import font

# Import all the different types of items.
from capital import *

"""
The idea is to load the item specs from the config files into the overall template database.

Not finished implementing all item types.

"""

class CapitalDatabase():
    """
    Tests:


    >>> Data = CapitalDatabase()
    >>> a = Data.GetTower(0)
    >>> a.name
    'Titan T200'
    >>> not Data.Towers == None
    True
    >>> not Data.Radios == None
    True

    """

    def __init__(self):
        # Set the file path to point in the directory.
        file_path = os.path.dirname(__file__)
        if file_path != "":
            os.chdir(file_path)

        # Load in the database dictionaries from files.
        # These dictionaries contain the possible items you can buy for the game.
        try:
            # Load equipment configurations
            self.Towers = self.loadDict("gameconfig/towers.csv")
            self.Radios = self.loadDict("gameconfig/radios.csv")
            self.Wired = self.loadDict("gameconfig/wired.csv")
            self.Routers = self.loadDict("gameconfig/routers.csv")
            self.Buildings = self.loadDict("gameconfig/buildings.csv")
        except:
            print("Failed to initialize capital database.")
            quit()

    # Load in the contents of a configuration file in order to 
    # build the database of capital.
    def loadDict(self,filename):
        inFile = open(filename,'r')
        returnDict = { }
        id = 0

        for line in inFile:
            line = line.rstrip()
            fields = line.split(",")

            # Allow comments in config file.
            if '#' in fields[0]: continue

            tempList = []
            for field in fields:
                tempList.append(field)

            returnDict[id] = tempList
            id = id + 1
                
        return returnDict

    def GetTower(self,id):
        return Tower(self.Towers[id])

    def GetRadio(self,id):
        return Radio(self.Radios[id])

    def GetWired(self,id):
        return Wired(self.Wired[id])

    def GetRouter(self,id):
        return Router(self.Routers[id])

    def GetBuilding(self,id):
        return Building(self.Buildings[id])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
