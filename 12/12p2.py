from collections import deque

PATH_CHARACTER = '+'
STOMPED_GROUND_CHARACTER = '.'

def printHeightMap(heightMap):
    for y in range(len(heightMap)):
        for x in range(len(heightMap[0])):
            print(chr(heightMap[y][x]), end='')
        print()
    print()

# A class that performs a bread first search
class PathFinder:
    def __init__(self, heightMap, startPosition, endPosition, climbing) -> None:
        self.heightMap = [[ord('?')]*len(lines[0]) for i in range(len(lines))]
        for y in range(len(heightMap)):
            for x in range(len(heightMap[0])):
                self.heightMap[y][x] = heightMap[y][x]
        # self.heightMap = heightMap[:]
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.climbing = climbing
        
        # Contains the next step to do
        self.stepsQue = deque()
        # x-coordinate  y-coordinate    parentPositionTuple
        self.currentPosition = (startPosition[0], startPosition[1], None)
        self.visitedPositions = []
        self.visitedPositions.append(self.startPosition)
    
    def checkAndAddStep(self, x, y):
        if x < 0:
            # print('Coordinate out of bounds.')
            return
        if y < 0:
            # print('Coordinate out of bounds.')
            return
        if x >= len(self.heightMap[0]):
            # print('Coordinate out of bounds.')
            return
        if y >= len(self.heightMap):
            # print('Coordinate out of bounds.')
            return
        # Thanks https://stackoverflow.com/questions/9542738/python-find-in-list
        # print(next((pos for pos in self.visitedPositions if pos[0] == x and pos[1] == y), False))
        alreadyVisited = next((pos for pos in self.visitedPositions if pos[0] == x and pos[1] == y), False)
        if alreadyVisited:
            # print('Already visited!!')
            return
        
        currentHeight = self.heightMap[self.currentPosition[1]][self.currentPosition[0]]
        if chr(currentHeight) == 'S':
            currentHeight = ord('a')
        if chr(currentHeight) == 'E':
            currentHeight = ord('z')
        proposedPositionHeight = self.heightMap[y][x]

        # print('CurrentPos:\t', self.currentPosition)
        # print('Climbing:\t',self.climbing)
        # print('Comparison:\t', proposedPositionHeight, chr(proposedPositionHeight), '==', currentHeight, chr(currentHeight))
        climbingCheck = self.climbing and (proposedPositionHeight == currentHeight + 1 or proposedPositionHeight <= currentHeight)
        descendingCheck = not self.climbing and (proposedPositionHeight == currentHeight - 1 or proposedPositionHeight >= currentHeight)

        if climbingCheck or descendingCheck:
            # print('Added step(', x, ',', y, ')')
            alreadyAdded = next((pos for pos in self.stepsQue if pos[0] == x and pos[1] == y), False)
            if not alreadyAdded:
                self.stepsQue.append((x, y, self.currentPosition))
    
    def findPossibleSteps(self):
        x = self.currentPosition[0]
        y = self.currentPosition[1]

        self.checkAndAddStep(x - 1, y) # Left
        self.checkAndAddStep(x, y + 1) # Up
        self.checkAndAddStep(x + 1, y) # Right
        self.checkAndAddStep(x, y - 1) # Down

    def takeNextStep(self):
        self.currentPosition = self.stepsQue.popleft()
        self.visitedPositions.append(self.currentPosition)

    def intersectsWith(self, otherPathFinder):
        for position in self.visitedPositions:
            visitedByBoth = next((pos for pos in otherPathFinder.visitedPositions if pos[0] == position[0] and pos[1] == position[1]), False)
            if visitedByBoth:
                return visitedByBoth
        
        return None


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

def updateHeightMapWithTrail(heightMap, pathFinderClimbing, pathFinderDescending):
    climbingX = pathFinderClimbing.currentPosition[0]
    climbingY = pathFinderClimbing.currentPosition[1]
    descendingX = pathFinderDescending.currentPosition[0]
    descendingY = pathFinderDescending.currentPosition[1]

    heightMap[climbingY][climbingX] = ord(STOMPED_GROUND_CHARACTER)
    heightMap[descendingY][descendingX] = ord(STOMPED_GROUND_CHARACTER)

def getShortestPath(descender):
    path = []

    def addToPath(self, positionObject):
        hasParent = True
        while hasParent:
            path.append((positionObject[0], positionObject[1]))
            if positionObject[2] != None:
                positionObject = positionObject[2]
            else:
                hasParent = False

    # From climber
    # positionObject = next((pos for pos in climber.visitedPositions if pos[0] == intersectionPoint[0] and pos[1] == intersectionPoint[1]))
    # addToPath(path, positionObject)
    # path.reverse() # Climbers positions gets added backwards

    # From descender
    positionObject = next((pos for pos in descender.visitedPositions if pos[0] == descender.currentPosition[0] and pos[1] == descender.currentPosition[1]))
    addToPath(path, positionObject)

    return path

with open('input.txt') as f:
    # Format input
    l = f.read()
    lines = l.strip().split('\n')
    heightMap = [[ord('?')]*len(lines[0]) for i in range(len(lines))]
    startPosition = (0, 0)
    endPosition = (0, 0)
    rounds = 0

    # printHeightMap(heightMap)
    heightMap, startPosition, endPosition = parseHeightMap()
    printHeightMap(heightMap)

    # Initialize PathFinders
    fromStart = PathFinder(heightMap, startPosition, endPosition, climbing=True)
    fromEnd = PathFinder(heightMap, startPosition=endPosition, endPosition=startPosition, climbing=False)

    # Path finding loop
    intersectionPoint = None
    while True:
        # fromStart.findPossibleSteps()
        fromEnd.findPossibleSteps()

        # fromStart.takeNextStep()
        fromEnd.takeNextStep()

        updateHeightMapWithTrail(heightMap, fromStart, fromEnd)

        if rounds < 1000 and rounds % 250 == 0 or rounds > 1000 and rounds % 25 == 0:
            print(rounds)
            printHeightMap(heightMap)
            # input()

        # intersectionPoint = fromStart.intersectsWith(fromEnd)
        # if intersectionPoint != None:
            # break
        x = fromEnd.currentPosition[0]
        y = fromEnd.currentPosition[1]
        if fromEnd.heightMap[y][x] == ord('a'):
            break

        rounds += 1
    
    # Get result and print it
    shortestPath = getShortestPath(fromEnd)

    # Create Path Map with heights
    pathMap = [[ord(' ')]*len(lines[0]) for i in range(len(lines))]
    count = 0
    for coordinate in shortestPath:
        pathMap[coordinate[1]][coordinate[0]] = fromEnd.heightMap[coordinate[1]][coordinate[0]]
        count += 1
        # print(count)
        # printHeightMap(pathMap)
        # input()
    
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

    
    printHeightMap(heightMap)
    printHeightMap(fromStart.heightMap)
    printHeightMap(fromEnd.heightMap)
    printHeightMap(pathMap)
    printHeightMap(upperCasePathMap)
    printHeightMap(arrowMap)

    print('The shortest path was', len(shortestPath) - 1, 'steps long.')
        






