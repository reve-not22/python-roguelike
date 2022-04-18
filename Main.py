import math
import random
import pyinputplus as pyip
import copy

playing = True
gameMap = []
mapSizeX = 10
mapSizeY = 10
populationChance = 50
emptyCharacter = " "
wallCharacter = "#"
doorCharacter = "{"
maxTries = int(mapSizeX * mapSizeY)
minTries = int(maxTries / 2)
minRooms = 1
maxRooms = 4

globalObjectPool = ['$', '$', '$', '%', '%', '%', '^', '^', '*', '*', 'A', 'H', '&']

def Init(mapSizeX, mapSizeY, gameMap):    
    # create the virtual map
    for x in range(mapSizeX):
        gameMap.append([y for y in range(mapSizeY)])

    ClearMap()
    
def CreateRooms(minRooms, maxRooms):
    for i in range(random.randint(minRooms, maxRooms)):
        startX = random.randint(1, mapSizeX - 1) # starting point along X axis
        startY = random.randint(1, mapSizeY - 1) # starting point along Y axis

        if ((not gameMap[0][startY] == emptyCharacter) or (not gameMap[startX][0] == emptyCharacter)):
            continue
        
        tileList = []

        print(str(startX) + ' ' + str(startY))
        
        wallLocX = 0 # used for creating the wall
        for x in range(startX):
            gameMap[wallLocX][startY] = wallCharacter
            tileList.append((wallLocX, startY))
            wallLocX += 1

        wallLocY = 0 
        for y in range(startY):
            gameMap[startX][wallLocY] = wallCharacter
            tileList.append((startX, wallLocY))
            wallLocY += 1

        chosenTileCoords = tileList[random.randint(0, len(tileList) - 1)]
        gameMap[chosenTileCoords[0]][chosenTileCoords[1]] = doorCharacter # turn a random tile in the wall into a door

def PopulateMap(minTries, maxTries, populationChance, objectPool):
    
    localObjectPool = copy.deepcopy(objectPool)
    
    curPoint = (random.randint(0, mapSizeX - 1), random.randint(0, mapSizeY - 1))
    print(gameMap[curPoint[0]][curPoint[1]])
    
    for i in range(random.randint(minTries, maxTries)):
        if ((random.randint(0, 100) > (populationChance - 1) and len(localObjectPool) > 0)):
            if (gameMap[curPoint[0]][curPoint[1]] == emptyCharacter):
                itemToAdd = localObjectPool[random.randrange(0, len(localObjectPool))]
                gameMap[curPoint[0]][curPoint[1]] = itemToAdd
                localObjectPool.remove(itemToAdd)

        try:
            curPoint = (math.abs(curPoint[0] + random.randint(-1, 1)), math.abs(curPoint[1] + random.randint(-1, 1))) # set the next object spawn to somewhere around the current one.
        except:
            curPoint = (random.randint(0, mapSizeX - 1), random.randint(0, mapSizeY - 1)) #set the next object to a random in-bounds spot if it is out of bounds.
            continue

def ClearMap():
    for x in range(mapSizeX):
        for y in range(mapSizeY):
            gameMap[x][y] = emptyCharacter

def DrawMap():
    columns = []
    yValues = []
    
    for x in gameMap:
        columns.append(x)
        for y in x:
            yValues.append(y)

    for i in reversed(range(0, mapSizeY)):
        rowToPrint = ""
        for z in range(0, len(columns)):
             rowToPrint += f" {gameMap[z][i]} "

        print(rowToPrint + '\n')

def Main(): # WIP, will be used in final version
    return

Init(mapSizeX, mapSizeY, gameMap) #make sure this comes first!
CreateRooms(minRooms, maxRooms)
PopulateMap(minTries, maxTries, populationChance, globalObjectPool)
DrawMap()
while (playing):
    playerInput = pyip.inputMenu(['Generate New Map', 'Exit'], numbered=True)
    if (playerInput == 'Generate New Map'):
        ClearMap()
        CreateRooms(minRooms, maxRooms)
        PopulateMap(minTries, maxTries, populationChance, globalObjectPool)
        DrawMap()
    else:
        playing = False
