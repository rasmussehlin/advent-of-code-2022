def updateVisibleTrees(visibleTreesMatrix, treeRows):
    highestInEachColumn = [-1] * len(treeRows[0])

    rowIndex = 0
    for treeRow in treeRows:
        highestInRow = -1
        colIndex = 0
        for tree in treeRow:
            alreadyAdded = False
            treeHeight = int(tree)
            
            if treeHeight > highestInRow:
                visibleTreesMatrix[rowIndex][colIndex] = 1
                highestInRow = treeHeight
                alreadyAdded = True
            
            if treeHeight > highestInEachColumn[colIndex]:
                highestInEachColumn[colIndex] = treeHeight
                
                if alreadyAdded == False:
                    visibleTreesMatrix[rowIndex][colIndex] = 1
                    alreadyAdded = True

            colIndex += 1
        rowIndex += 1

with open('input.txt') as f:
    l = f.read()
    treeRows = l.strip().split('\n')
    
    visibleTreesMatrix = [[0]*len(treeRows[0]) for i in range(len(treeRows))]

    updateVisibleTrees(visibleTreesMatrix, treeRows)

    # Reverse input
    for index in range(0, len(treeRows)):
        treeRows[index] = treeRows[index][::-1]
    treeRows.reverse()

    # Reverse visible trees matrix
    for index in range(0, len(visibleTreesMatrix)):
        visibleTreesMatrix[index].reverse()
    visibleTreesMatrix.reverse()

    updateVisibleTrees(visibleTreesMatrix, treeRows)
    
    f = open("output8p1.txt", "w")
    visibleTrees = 0
    for row in visibleTreesMatrix:
        f.write(''.join(map(str, row)))
        f.write('\n')
        for col in row:
            visibleTrees += int(col)
    f.close()

    print(visibleTrees)
