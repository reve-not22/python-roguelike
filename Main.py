import sys
import pydoc
import math
import random
import pyinputplus as pyip
import copy
import keyboard
from time import sleep

playing = True
gameMap = []
mapSizeX = 10
mapSizeY = 10
populationChance = 50
emptyCharacter = " "
maxTries = int(mapSizeX * mapSizeY)
minTries = int(maxTries / 2)
minRooms = 1
maxRooms = 4
seedCharacters = 9
currentSeed = None
inputSeed = None

initObjectPool = []
mapObjectPool = []

### CLASSES ###

class Object:
    '''Basic object class'''
    character = " "

    def __init__(self, character=' ', isSolidObject=True, startPos = (None, None)):
        self.character = character
        self.isSolidObject = isSolidObject
        self.x, self.y = startPos
        if not(self.x == None or self.y == None):
            self.setPos(self.x, self.y)

    def interact():
        print("You could not comprehend the object.")

    def remove(self):
        gameMap[self.x][self.y] == emptyCharacter
        mapObjectPool.remove(self)

    def setPos(self, x, y):
        try:
            if gameMap[x][y] == emptyCharacter:
                if not(self.x == None or self.y == None): #check if the object is on the map
                    if gameMap[self.x][self.y] == self.character: # set the map to empty if you were at that point before
                        gameMap[self.x][self.y] = emptyCharacter
                self.x = x
                self.y = y# set internal position
                gameMap[self.x][self.y] = self.character # set map character
            else:
                print("Space is already occupied.")
        except:
            print("Space is out of bounds")

class Door(Object):
    '''Openable and closable door object'''
    character = "{"

    def __init__(self, coords):
        super().__init__("{", startPos=coords)

class Wall(Object):
    '''Immovable/unbreakable wall object'''
    character = "#"

    def __init__(self, coords):
        super().__init__("#", startPos=coords)

class Consumable(Object):
    '''Consumable class, can use to give the player stats or health'''

    def __init__(self, character='&', healPoints=0, speedIncrease=0, dmgIncrease=0, healthIncrease=0, xpIncrease=0):
        super().__init__(character)
        self.healPoints = healPoints
        self.speedIncrease = speedIncrease
        self.dmgIncrease = dmgIncrease
        self.xpIncrease = xpIncrease

    def consume(player):
        player.hp += self.healPoints
        player.speed += self.speedIncrease
        player.damage += self.dmgIncrease
        player.xp += self.xpIncrease

class Enemy(Object):
    '''Enemy class, attacks player'''

    def __init__(self):
        super().__init__(self)

class Player(Object):
    '''Player class that controls position, stats, and inventory'''
    character = "@"
    maxHP = 100

    def __init__(self, startCoords, hp=maxHP, attack=1, defense=1, speed=1, startingItems = []):
        super().__init__(self.character, startCoords)
        self.hp = hp
        self.xp = 0
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.inventory = startingItems
        if startCoords:
            x, y = startCoords
            self.setPos(x, y)

    def move(self, moveCoords, numMoves):
        moveX, moveY = moveCoords
        for x in range(0, numMoves):
            self.setPos(self.x + moveX, self.y + moveY)

### OBJECT FUNCTIONS ###

def findObjectByCoords(objectPool, coords):
    cordX, cordY = coords
    for item in objectPool:
        if item.x == cordX and item.y == cordY:
            return item

### PLAYER FUNCTIONS ###


### NUMBER GENERATOR FUNCTIONS ###

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

### MAP FUNCTIONS ###

def PopulateObjectPool(pool, maxConsumables, maxEnemies):
    for x in range(0, random.randint(maxConsumables / 2, maxConsumables)):
        for z in range(0, 2):
            chance = random.randint(0, 3)
            hp = 0
            sI = 0
            dI = 0
            hI = 0
            if chance == 0:
                hp += random.randint(Player.maxHP / 2, Player.maxHP)
            elif chance == 1:
                sI += 1
            elif chance == 2:
                dI += 1
            else:
                hI += 1

        pool.append(Consumable('&', hp, sI, dI, hI))
    #for y in range(0, random.randint(maxEnemies / 2, maxEnemies)):
        #add enemy to object pool


def InitMap(mapSizeX, mapSizeY, gameMap, currentSeed):
    '''Creates a virtual map with an area of mapSizeX * mapSizeY and initializes the random number generator.'''
    for x in range(mapSizeX):
        gameMap.append([y for y in range(mapSizeY)])

    ClearMap()

def CreateRooms(minRooms, maxRooms):
    '''Creates rooms randomly by creating intersecting walls'''
    for i in range(random.randint(minRooms, maxRooms)):
        topCorner_l = (random.randint(0, mapSizeX - 5), random.randint(2, mapSizeY - 2))
        bottomCorner_r = (random.randint(topCorner_l[0] + 2, mapSizeX - 1), random.randint(0, topCorner_l[1] - 2))
        topCorner_r = (bottomCorner_r[0], topCorner_l[1])
        bottomCorner_l = (topCorner_l[0], bottomCorner_r[1])

        if gameMap[topCorner_l[0]][topCorner_l[1]] == Wall.character: continue

        if gameMap[topCorner_r[0]][topCorner_r[1]] == Wall.character: continue

        if gameMap[bottomCorner_l[0]][bottomCorner_l[1]] == Wall.character: continue

        if gameMap[bottomCorner_r[0]][topCorner_r[1]] == Wall.character: continue

        for x in range(topCorner_l[0], topCorner_r[0]):
            mapObjectPool.append(Wall((x, topCorner_l[1])))

        for x1 in range(bottomCorner_l[0], bottomCorner_r[0]):
            mapObjectPool.append(Wall((x1, bottomCorner_l[1])))

        for y in range(bottomCorner_l[1], topCorner_l[1]):
            mapObjectPool.append(Wall((bottomCorner_l[0], y)))

        for y1 in range(bottomCorner_r[1], topCorner_r[1]):
            mapObjectPool.append(Wall((bottomCorner_r[0], y1)))

        mapObjectPool.append(Wall(topCorner_r))

def PopulateMap(minTries, maxTries, populationChance, objectPool):
    '''Places objects from the object pool randomly around the map'''
    localObjectPool = copy.deepcopy(objectPool)

    curPoint = (random.randint(0, mapSizeX - 1), random.randint(0, mapSizeY - 1))

    for i in range(random.randint(minTries, maxTries)):
        if ((random.randint(0, 100) > (populationChance - 1) and len(localObjectPool) > 0)):
            if (gameMap[curPoint[0]][curPoint[1]] == emptyCharacter):
                itemToAdd = localObjectPool[random.randrange(0, len(localObjectPool))]
                mapObjectPool.append(itemToAdd)
                itemToAdd.setPos(curPoint[0], curPoint[1])
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

#Initialize
#currentSeed = InitGen(seedCharacters)
InitMap(mapSizeX, mapSizeY, gameMap, currentSeed) #put clear map function before if used again in the program.
PopulateObjectPool(initObjectPool, 4, 10)
currentSeed = ChangeSeed(GenerateSeed())
ClearMap()
PlayerObj = Player((0, 0))
mapObjectPool.append(PlayerObj)
CreateRooms(minRooms, maxRooms)
PopulateMap(minTries, maxTries, populationChance, initObjectPool)
DrawMap()

while (playing):
    nextTurn = False
    while (not nextTurn):
        usrInput = keyboard.read_key()
        if (usrInput == "w"):
            nextTurn = True
            move = (0, 1)
        if (usrInput == "s"):
            nextTurn = True
            move = (0, -1)
        if (usrInput == "a"):
            nextTurn = True
            move = (-1, 0)
        if (usrInput == "d"):
            nextTurn = True
            move = (1, 0)

        PlayerObj.move(move, 1)

    DrawMap()
    print('Current seed:' + str(currentSeed))
    sleep(0.1)

