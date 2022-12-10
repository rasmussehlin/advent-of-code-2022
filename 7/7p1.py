from collections import deque
import math

class Folder:
    children = []
    totalSize = 0
    def __init__(self, name, parent) -> None:
        self.name = name
        self.parent = parent
        self.children = []
        self.totalSize = 0
    def getParentString(self) -> str:
        if self.parent != None:
            return self.parent.getParentString() + '/' +  self.name
        else:
            return '$ '
        

with open('input.txt') as f:
    l = f.read()
    # Stack od current pos. in dir-tree
    dirStack = deque()
    dirStack.append('/')

    rootFolder = Folder('/', None)

    # Create input array
    l = l.strip().split('\n')

    # State variable
    cd = False
    ls = False
    # Size sum curr. folder
    folderSize = 0

    currentFolderObject = rootFolder

    totalSize = 0

    for line in l:
        line = line.split(' ')
        first = line[0]
        second = line[1]
        if len(line) > 2:
            third = line[2]

        # Check line type (state)
        cd = False
        ls = False
        if first == '$':
            folderSize = 0
            if second == 'cd':
                cd = True
            elif second == 'ls':
                ls = True
        
        # Perform state action
        if cd:
            if third == '/':
                currentFolderObject = rootFolder
            elif third == '..':
                currentFolderObject = currentFolderObject.parent
            else:
                # Store dir structure
                newFolder = Folder(third, parent=currentFolderObject)
                currentFolderObject.children.append(newFolder)
                currentFolderObject = newFolder
        elif ls == False:
            # Counting folders and filesizes
            if first == 'dir':
                pass
            elif first.isnumeric():
                currentFolderObject.totalSize += int(first)
                totalSize += int(first)

    # Count sizes
    currentFolderObject = rootFolder
    dirStack.clear()
    dirStack.append((currentFolderObject, 0))
    treeHasBeenTraversed = False
    totalSizeOfDirectories = 0

    while treeHasBeenTraversed == False:
        currentFolderObject = dirStack[-1][0]
        currentChildIndex = dirStack[-1][1]

        # All children traversed?
        hasZeroChildren = len(currentFolderObject.children) == 0
        allChildrenTraversed = len(currentFolderObject.children) == currentChildIndex

        if hasZeroChildren or allChildrenTraversed:
            if currentFolderObject.parent != None:
                currentFolderObject.parent.totalSize += currentFolderObject.totalSize
            else:
                # We're at the root
                treeHasBeenTraversed = True

            if currentFolderObject.totalSize <= 100000:
                totalSizeOfDirectories += currentFolderObject.totalSize
            
            # Remove this folderObject
            dirStack.pop()

            continue

        # Traversing children
        dirStack[-1] = (dirStack[-1][0], dirStack[-1][1] + 1) # Increase child index
        # Add child to stack
        dirStack.append((currentFolderObject.children[currentChildIndex], 0))

    print(totalSizeOfDirectories)