def calculateScoreForView(treeHeight, trees):
    visibleTrees = 0
    for tree in trees:
        if tree < treeHeight:
            visibleTrees += 1
        elif tree >= treeHeight:
            visibleTrees += 1
            break

    return visibleTrees

def calculateScenicScore(treeRows, rowIndex, colIndex):
    if colIndex == 0 or colIndex == len(treeRows[0]) - 1 or rowIndex == 0 or rowIndex == len(treeRows) - 1:
        return 0

    # Left
    leftTrees = treeRows[rowIndex][:colIndex]
    leftTrees = leftTrees[::-1]

    # Right
    rightTrees = treeRows[rowIndex][colIndex + 1:]

    #Top
    topTrees = ''
    for i in range(rowIndex):
        topTrees += treeRows[i][colIndex]
    topTrees = topTrees[::-1]

    # Bottom
    bottomTrees = ''
    for i in range(rowIndex + 1, len(treeRows)):
        bottomTrees += treeRows[i][colIndex]

    # Calculate
    treeHeight = treeRows[rowIndex][colIndex]
    scenicScore = 1
    scenicScore = scenicScore * calculateScoreForView(treeHeight, leftTrees)
    scenicScore = scenicScore * calculateScoreForView(treeHeight, rightTrees)
    scenicScore = scenicScore * calculateScoreForView(treeHeight, topTrees)
    scenicScore = scenicScore * calculateScoreForView(treeHeight, bottomTrees)

    return scenicScore

with open('input.txt') as f:
    l = f.read()
    treeRows = l.strip().split('\n')
    
    scenicScoreMatrix = [[0]*len(treeRows[0]) for i in range(len(treeRows))]

    f = open("output8p2.txt", "w")
    highestScore = 0
    for rowIndex in range(len(scenicScoreMatrix)):
        for colIndex in range(len(scenicScoreMatrix[0])):
            scenicScoreMatrix[rowIndex][colIndex] = calculateScenicScore(treeRows, rowIndex, colIndex)
            if scenicScoreMatrix[rowIndex][colIndex] > highestScore:
                highestScore = scenicScoreMatrix[rowIndex][colIndex]
        
        f.write('\t'.join(map(str, scenicScoreMatrix[rowIndex])))
        f.write('\n')
    
    f.close()
    
    print(highestScore)
