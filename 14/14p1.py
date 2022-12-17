from collections import deque
from enum import Enum
import time

SAND_SOURCE = [500, 0]
AIR = '.'

class ElementTypes(Enum):
    ROCK = '#'
    RESTING_SAND = 'o'
    FLOWING_SAND = '~'
    FLOWING_SAND_ALT = '¬'
    MOVING_SAND = '+'

class Element:
    def __init__(self, x, y, type) -> None:
        self.x = x
        self.y = y
        self.type = type
        if type == ElementTypes.FLOWING_SAND:
            self.flipFlop = True
    
    def tostr(self) -> str:
        if self.type == ElementTypes.FLOWING_SAND:
            return self.type.value if self.flipFlop else ElementTypes.FLOWING_SAND_ALT.value
        else:
            return self.type.value

def parseRockLinesToRockPoints(pathOfStone) -> list:
    rockPoints = []

    for lineOfStone in pathOfStone:
        stonePoints = list(map(lambda nrPair: nrPair.split(','), lineOfStone.split(' -> ')))
        for i in range(len(stonePoints) - 1):
            x = int(stonePoints[i][0])
            y = int(stonePoints[i][1])
            dx = int(stonePoints[i+1][0]) - x
            dy = int(stonePoints[i+1][1]) - y
            
            startIndex = 1 if i > 0 else 0

            if dx != 0:
                negative = dx < 0
                for j in range(startIndex, abs(dx) + 1):
                    newX = x + (-j if negative else j)
                    rockPoints.append(Element(newX, y, ElementTypes.ROCK))
            else:
                negative = dy < 0
                for j in range(startIndex, abs(dy) + 1):
                    newY = y + (-j if negative else j)
                    rockPoints.append(Element(x, newY, ElementTypes.ROCK))
    
    # Remove duplicates
    indicesToRemove = []
    for i in range(len(rockPoints) - 1):
        for j in range(i + 1, len(rockPoints)):
            if rockPoints[i].x == rockPoints[j].x and rockPoints[i].y == rockPoints[j].y:
                if i not in indicesToRemove:
                    indicesToRemove.append(i)

    # Works since indicesToRemove are sorted
    for i in range(len(indicesToRemove)):
        # print(indicesToRemove[i], '\t', i)
        rockPoints.pop(indicesToRemove[i] - i)
    
    return rockPoints

def parseCaveMap(elements):
    caveMap = [[ElementTypes.MOVING_SAND.value]]
    leftX = 500
    rightX = 500

    for element in elements:
        height = len(caveMap) - 1
        x = element.x
        y = element.y

        # Update height
        if y > height:
            increaseHeightOfMap(caveMap, y - height)

        # Update width
        if x < leftX:
            increaseWidthOfMap(caveMap, x - leftX)
            leftX = x
        elif x > rightX:
            increaseWidthOfMap(caveMap, x - rightX)
            rightX = x
        
        # Insert rock
        tempX = 0 if x-leftX < 0 else x-leftX
        caveMap[y][tempX] = element.tostr()
    
    return (caveMap, leftX)
    

def getLowestRock(positionsOfElements):
    lowest = Element(0, 0, ElementTypes.ROCK) # That's alright, 0 is the roof
    for element in positionsOfElements:
        if element.type == ElementTypes.ROCK:
            if element.y < lowest.y:
                lowest = element
    
    return lowest

def increaseWidthOfMap(caveMap, value):
    for level in caveMap:
        for _ in range(abs(value)):
            if value > 0:
                level.append(AIR)
            else:
                level.insert(0, AIR)

def increaseHeightOfMap(caveMap, value):
    for _ in range(value):
        newRow = []
        for _ in range(len(caveMap[0])):
            newRow.append(AIR)
        caveMap.append(newRow)

def printCurrentMap(caveMap):
    # Print map
    for i in range(len(caveMap)):
        line = ''
        for j in range(len(caveMap[i])):
            line += caveMap[i][j]
        print(i, ':\t\t', line)

with open('input.txt') as f:
    # Format input
    l = f.read()
    pathsOfStone = l.strip().split('\n')
    positionsOfItemsInCave = parseRockLinesToRockPoints(pathsOfStone)
    caveMap, leftX = parseCaveMap(positionsOfItemsInCave)
    printCurrentMap(caveMap)

    # Sand states
    FLOWING_TO_ABYSS = 'FLOWING_TO_ABYSS'
    FALLING_DOWN = 'FALLING_DOWN'
    FALLING_DOWN_LEFT = 'FALLING_DOWN_LEFT'
    FALLING_DOWN_RIGHT = 'FALLING_DOWN_RIGHT'
    RESTING = 'RESTING'

    lowestRock = getLowestRock(positionsOfItemsInCave)
    sandFlowsToAbyss = False
    droppedUnits = 0

    while sandFlowsToAbyss == False:
        sandState = FALLING_DOWN
        sandUnit = [500, 0] # Spawn position
        sandPath = [] # For abyss backtracking

        simulatingUnit = True
        while simulatingUnit:
            x = sandUnit[0] - leftX
            y = sandUnit[1]
            if sandState == FALLING_DOWN:
                sandPath.append(Element(sandUnit[0], sandUnit[1], ElementTypes.FLOWING_SAND))
                if y + 1 == len(caveMap):
                    sandState = FLOWING_TO_ABYSS
                else:
                    # print(sandState)
                    # print('Looking at:', caveMap[y + 1][x], 'at (', x,',',y+1,')')
                    if caveMap[y + 1][x] == AIR:
                        sandUnit[1] += 1
                    else:
                        sandState = FALLING_DOWN_LEFT

            elif sandState == FALLING_DOWN_LEFT:
                sandPath.append(Element(sandUnit[0], sandUnit[1], ElementTypes.FLOWING_SAND))
                if x - 1 == -1:
                    sandState = FLOWING_TO_ABYSS
                else:
                    # print(sandState)
                    # print('Looking at:', caveMap[y + 1][x - 1], 'at (', x-1,',',y+1,')', 'Air is:', AIR)
                    if caveMap[y + 1][x - 1] == AIR:
                        sandUnit[0] += -1
                        sandUnit[1] += 1
                        sandState = FALLING_DOWN
                    else:
                        sandState = FALLING_DOWN_RIGHT

            elif sandState == FALLING_DOWN_RIGHT:
                sandPath.append(Element(sandUnit[0], sandUnit[1], ElementTypes.FLOWING_SAND))
                if x + 1 == len(caveMap[0]):
                    sandState = FLOWING_TO_ABYSS
                else:
                    # print(sandState)
                    # print('Looking at:', caveMap[y + 1][x + 1], 'at (', x+1,',',y+1,')')
                    if caveMap[y + 1][x + 1] == AIR:
                        sandUnit[0] += 1
                        sandUnit[1] += 1
                        sandState = FALLING_DOWN
                    else:
                        sandState = RESTING

            elif sandState == RESTING:
                droppedUnits += 1
                if droppedUnits % 100 == 0:
                    print('Dropped sand units:', droppedUnits)
                    printCurrentMap(caveMap)
                newRestingSandElement = Element(sandUnit[0], sandUnit[1], ElementTypes.RESTING_SAND)
                positionsOfItemsInCave.append(newRestingSandElement)
                simulatingUnit = False

            elif sandState == FLOWING_TO_ABYSS:
                for element in sandPath:
                    positionsOfItemsInCave.append(Element(element.x, element.y, ElementTypes.FLOWING_SAND))
                    simulatingUnit = False
                    sandFlowsToAbyss = True
                pass
        
            caveMap, leftX = parseCaveMap(positionsOfItemsInCave + [Element(sandUnit[0], sandUnit[1], ElementTypes.MOVING_SAND if sandState != FLOWING_TO_ABYSS else ElementTypes.FLOWING_SAND )])
            # printCurrentMap(caveMap)
            # print()
            # time.sleep(0.05)

    nrOfRestingSandUnits = 0
    for element in positionsOfItemsInCave:
        if element.type == ElementTypes.RESTING_SAND:
            nrOfRestingSandUnits += 1

    printCurrentMap(caveMap)
    print('There are', nrOfRestingSandUnits, 'resting sand units in the cave.')

    # Priority:
    #   Down
    #   Down left
    #   Down right
    #   Rest
