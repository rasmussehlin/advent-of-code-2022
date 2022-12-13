from collections import deque

def printHeightMap(heightMap):
    for y in range(len(heightMap)):
        for x in range(len(heightMap[0])):
            print(chr(heightMap[y][x]), end='')
        print()
    print()

with open('input.txt') as f:
    # Format input
    l = f.read()
    lines = l.strip().split('\n')
    heightMap = [[0]*len(lines[0]) for i in range(len(lines))]
    startPosition = (0, 0)
    endPosition = (0, 0)

    printHeightMap(heightMap)

    for y in range(len(lines)):
        for x in range(len(lines[0])):
            heightMap[y][x] = ord(lines[y][x])
            if lines[y][x] == 'E':
                endPosition = (x, y)
            elif lines[y][x] == 'S':
                startPosition = (x, y)

    printHeightMap(heightMap)