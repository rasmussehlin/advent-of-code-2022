import time

NOT_VISITED = '_'
VISITED = '#'

def increaseArray(x, y, visitedPositions):
    if x > 0:
        for row in visitedPositions:
            row.append(NOT_VISITED)
    elif x < 0:
        for row in visitedPositions:
            row.insert(0, NOT_VISITED)
    if y > 0:
        visitedPositions.append([NOT_VISITED] * len(visitedPositions[0]))
    if y < 0:
        visitedPositions.insert(0, [NOT_VISITED] * len(visitedPositions[0]))


def moveHead(stepCharacter, headPosition, tailPosition, visitedPositions):
    match stepCharacter:
        case 'L':
            if headPosition[0] == 0:
                increaseArray(-1, 0, visitedPositions)
                tailPosition[0] += 1
            else:
                headPosition[0] -= 1
        case 'U':
            # Increase array size
            if headPosition[1] == len(visitedPositions) - 1:
                increaseArray(0, 1, visitedPositions)
            
            # Update head position
            headPosition[1] += 1
        case 'R':
            # Increase array size
            if headPosition[0] == len(visitedPositions[0]) - 1:
                increaseArray(1, 0, visitedPositions)

            # Update head position
            headPosition[0] += 1
        case 'D':
            if headPosition[1] == 0:
                increaseArray(0, -1, visitedPositions)
                tailPosition[1] += 1
            else:
                headPosition[1] -= 1

def updateTail(headPosition, tailPosition, visitedPositions):
    # 1 2 3 4 5
    # 6 _ 3 _ 7
    # 8 8 T 9 9
    # A _ E _ B
    # C D E F G

    hx = headPosition[0]
    hy = headPosition[1]
    tx = tailPosition[0]
    ty = tailPosition[1]

    dy = ty - hy
    dx = tx - hx

    if abs(dy) <= 1 and abs(dx) <= 1:
        return
    
    if dy == 0:
        tailPosition[0] -= int(dx / abs(dx))
    elif dx == 0:
        tailPosition[1] -= int(dy / abs(dy))
    elif abs(dy) == 1:
        if abs(dx) == 2:
            tailPosition[0] -= int(dx / abs(dx))
            tailPosition[1] -= int(dy / abs(dy))
    elif abs(dx) == 1:
        if abs(dy) == 2:
            tailPosition[0] -= int(dx / abs(dx))
            tailPosition[1] -= int(dy / abs(dy))
    
    visitedPositions[tailPosition[1]][tailPosition[0]] = VISITED

def printMap(visitedPositions, headPosition, tailPosition):
    for row in range(len(visitedPositions)):
        for col in range(len(visitedPositions[0])):
            if tailPosition[0] == col and tailPosition[1] == row:
                print('T', end='')
            elif headPosition[0] == col and headPosition[1] == row:
                print('H', end='')
            else:
                print(visitedPositions[row][col], end='')
        print(end='\n')



with open('input.txt') as f:
    l = f.read()
    steps = l.strip().split('\n')
    steps = list(map(lambda step: step.split(' '), steps))

    headPosition = [0, 0]
    tailPosition = [0, 0]
    visitedPositions = [[VISITED]]
    visitedPositions[tailPosition[1]][tailPosition[0]] = VISITED

    SLEEP_TIME = 0.01

    for step in steps:
        for i in range(int(step[1])):
            # print('Taking step:', step[0], '\tHead:', headPosition, '\tTail:', tailPosition)
            # print()
            moveHead(step[0], headPosition, tailPosition, visitedPositions)
            # printMap(visitedPositions, headPosition, tailPosition)
            # time.sleep(SLEEP_TIME)
            updateTail(headPosition, tailPosition, visitedPositions)
            # printMap(visitedPositions, headPosition, tailPosition)
            # time.sleep(SLEEP_TIME)
    
    visitations = 0
    for row in visitedPositions:
        for col in row:
            if col == VISITED:
                visitations += 1


    print(visitations)



