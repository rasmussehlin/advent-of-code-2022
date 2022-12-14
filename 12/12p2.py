from collections import deque

PATH_CHARACTER = '+'
STOMPED_GROUND_CHARACTER = '.'

# Prints the map to stdout
def printHeightMap(heightMap):
    for y in range(len(heightMap)):
        for x in range(len(heightMap[0])):
            print(chr(heightMap[y][x]), end='')
        print()
    print()

# A class that performs a breadth first search
class PathFinder:
    def __init__(self, heightMap, startPosition) -> None:
        # Create a deep copy of heightMap
        self.heightMap = [[ord('?')]*len(lines[0]) for i in range(len(lines))]
        for y in range(len(heightMap)):
            for x in range(len(heightMap[0])):
                self.heightMap[y][x] = heightMap[y][x]
        self.startPosition = startPosition
        
        # Contains the next step to do
        self.stepsQue = deque()
        # x-coordinate  y-coordinate    parentPositionTuple
        self.currentPosition = (startPosition[0], startPosition[1], None)
        self.visitedPositions = []
        self.visitedPositions.append(self.startPosition)
    
    def checkAndAddStep(self, x, y):
        if x < 0:
            return
        if y < 0:
            return
        if x >= len(self.heightMap[0]):
            return
        if y >= len(self.heightMap):
            return
        # Thanks https://stackoverflow.com/questions/9542738/python-find-in-list
        alreadyVisited = next((pos for pos in self.visitedPositions if pos[0] == x and pos[1] == y), False)
        if alreadyVisited:
            return
        
        # Get current height
        currentY = self.currentPosition[1]
        currentX = self.currentPosition[0]
        currentHeight = self.heightMap[currentY][currentX]
        if chr(currentHeight) == 'S':
            currentHeight = ord('a')
        if chr(currentHeight) == 'E':
            currentHeight = ord('z')
        proposedPositionHeight = self.heightMap[y][x]

        # Compare heights
        canDescend = proposedPositionHeight == currentHeight - 1 or proposedPositionHeight >= currentHeight

        if canDescend:
            alreadyAddedToStepQue = next((pos for pos in self.stepsQue if pos[0] == x and pos[1] == y), False)
            if not alreadyAddedToStepQue:
                self.stepsQue.append((x, y, self.currentPosition))
    
    def findPossibleSteps(self):
        x = self.currentPosition[0]
        y = self.currentPosition[1]

        self.checkAndAddStep(x - 1, y) # Left
        self.checkAndAddStep(x, y + 1) # Down
        self.checkAndAddStep(x + 1, y) # Right
        self.checkAndAddStep(x, y - 1) # Up

    def takeNextStep(self):
        self.currentPosition = self.stepsQue.popleft()
        self.visitedPositions.append(self.currentPosition)

def parseHeightMap():
    heightMap = [[0]*len(lines[0]) for i in range(len(lines))]
    startPosition = (0, 0)
    endPosition = (0, 0)
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            heightMap[y][x] = ord(lines[y][x])
            if lines[y][x] == 'E':
                endPosition = (x, y)
            elif lines[y][x] == 'S':
                startPosition = (x, y)
    return heightMap, startPosition, endPosition

def updateHeightMapWithTrail(heightMap, pathFinderDescending):
    descendingX = pathFinderDescending.currentPosition[0]
    descendingY = pathFinderDescending.currentPosition[1]

    heightMap[descendingY][descendingX] = ord(STOMPED_GROUND_CHARACTER)

def getShortestPath(descender):
    path = []

    def addToPath(positionObject):
        hasParent = True
        while hasParent:
            path.append((positionObject[0], positionObject[1]))
            if positionObject[2] != None:
                positionObject = positionObject[2]
            else:
                hasParent = False

    # From descender
    positionObject = next((pos for pos in descender.visitedPositions if pos[0] == descender.currentPosition[0] and pos[1] == descender.currentPosition[1]))
    addToPath(positionObject)

    return path


with open('input.txt') as f:
    # Format input
    l = f.read()
    lines = l.strip().split('\n')
    heightMap = [[ord('?')]*len(lines[0]) for i in range(len(lines))]
    startPosition = (0, 0)
    endPosition = (0, 0)
    rounds = 0

    heightMap, startPosition, endPosition = parseHeightMap()

    # Initialize PathFinders
    fromEnd = PathFinder(heightMap, startPosition=endPosition)

    # Path finding loop
    intersectionPoint = None
    while True:
        fromEnd.findPossibleSteps()
        fromEnd.takeNextStep()
        updateHeightMapWithTrail(heightMap, fromEnd)

        # # Print progress
        # if rounds % 5 == 0:
        #     print(rounds)
        #     printHeightMap(heightMap)

        x = fromEnd.currentPosition[0]
        y = fromEnd.currentPosition[1]
        if fromEnd.heightMap[y][x] == ord('a'):
            break

        rounds += 1
    
    # Get result and print it
    shortestPath = getShortestPath(fromEnd)

    # Create Path Map with heights
    pathMap = [[ord(' ')]*len(lines[0]) for i in range(len(lines))]
    for coordinate in shortestPath:
        pathMap[coordinate[1]][coordinate[0]] = fromEnd.heightMap[coordinate[1]][coordinate[0]]
    
    # Create Path Map with upperCase
    upperCasePathMap = [[ord(' ')]*len(lines[0]) for i in range(len(lines))]
    for y in range(len(heightMap)):
        for x in range(len(heightMap[0])):
            upperCasePathMap[y][x] = fromEnd.heightMap[y][x]
    for coordinate in shortestPath:
        upperCasePathMap[coordinate[1]][coordinate[0]] = ord(chr(fromEnd.heightMap[coordinate[1]][coordinate[0]]).upper())

    # Create Path Map with arrows
    arrowMap = [[ord(' ')]*len(lines[0]) for i in range(len(lines))]
    prevCoordinate = shortestPath[0]
    for coordinate in shortestPath:
        x = prevCoordinate[0]
        y = prevCoordinate[1]
        if prevCoordinate != None:
            nextX = coordinate[0]
            nextY = coordinate[1]
            if nextX == x - 1:
                arrowMap[y][x] = ord('<')
            elif nextX == x + 1:
                arrowMap[y][x] = ord('>')
            elif nextY == y - 1:
                arrowMap[y][x] = ord('^')
            elif nextY == y + 1:
                arrowMap[y][x] = ord('v')
        prevCoordinate = coordinate

    
    print('== heightMap ==')
    printHeightMap(heightMap)
    print('== pathMap ==')
    printHeightMap(pathMap)
    print('== upperCasePathMap ==')
    printHeightMap(upperCasePathMap)
    print('== arrowMap ==')
    printHeightMap(arrowMap)

    # -1 because starting 'a' included in `shortestPath`
    print('The shortest path was', len(shortestPath) - 1, 'steps long.')
