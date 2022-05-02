import sys
import pydoc
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
seedCharacters = 9
currentSeed = None
inputSeed = None

globalObjectPool = ['$', '$', '$', '%', '%', '%', '^', '^', '*', '*', 'A', 'H', '&']

def GenerateSeed(charAmt=9):
    seed = ""
    for i in range(0, charAmt):
        seed += str(random.randint(0, 9))

    return int(seed)

def ChangeSeed(seed):
    random.seed(seed)
    return seed

def SaveSeed(seed):
    try:
        seedFile = open("Seeds.txt", "a")
        seedFile.write(" " + str(seed) + " ")
        seedFile.close()
    except:
        print("Saving failed.")

def ViewSeeds():
    try:
        seedFile = open("Seeds.txt", "r")
        print(seedFile.read())
        seedFile.close()
    except:
        print("Cannot open seed file.")

def InitGen(seedCharacters):
    currentSeed = GenerateSeed(seedCharacters)
    random.seed(currentSeed)
    return currentSeed

def InitMap(mapSizeX, mapSizeY, gameMap, currentSeed):
    '''Creates a virtual map with an area of mapSizeX * mapSizeY and initializes the random number generator.'''
    for x in range(mapSizeX):
        gameMap.append([y for y in range(mapSizeY)])

    ClearMap()

def CreateRooms(minRooms, maxRooms):
    '''Creates rooms randomly by creating intersecting walls'''
    for i in range(random.randint(minRooms, maxRooms)):
        startX = random.randint(1, mapSizeX - 1) # starting point along X axis
        startY = random.randint(1, mapSizeY - 1) # starting point along Y axis

        if ((not gameMap[0][startY] == emptyCharacter) or (not gameMap[startX][0] == emptyCharacter)):
            continue

        tileList = []

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
    '''Places objects from the object pool randomly around the map'''
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
    '''Clears the map of all objects (and walls)'''
    for x in range(mapSizeX):
        for y in range(mapSizeY):
            gameMap[x][y] = emptyCharacter

def DrawMap():
    '''Draws the map to the console'''
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

def Main(): # Unused function
    return

#Initialize
currentSeed = InitGen(seedCharacters)
InitMap(mapSizeX, mapSizeY, gameMap, currentSeed) #put clear map function before if used again in the program.

while (playing):
    print('Current seed:' + str(currentSeed))
    playerInput = pyip.inputMenu(['Generate New Map', 'Generate New Seed', 'Input Seed', 'Save Current Seed', 'View Saved Seeds', 'Exit'], numbered=True)
    if (playerInput == 'Generate New Map'):
        ClearMap()
        CreateRooms(minRooms, maxRooms)
        PopulateMap(minTries, maxTries, populationChance, globalObjectPool)
        DrawMap()
    elif (playerInput == 'Generate New Seed'):
        currentSeed = InitGen(seedCharacters)
    elif (playerInput == 'Input Seed'):
        seedInput = pyip.inputInt("\n")
        currentSeed = ChangeSeed(seedInput)
    elif (playerInput == 'Save Current Seed'):
        SaveSeed(currentSeed)
    elif (playerInput == 'View Saved Seeds'):
        ViewSeeds()
    else:
        playing = False
