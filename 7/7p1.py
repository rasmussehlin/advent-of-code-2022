from collections import deque
import math

with open('input.txt') as f:
    l = f.read()
    # Stack od current pos. in dir-tree
    dirStack = deque()
    # Store folder names and their size (excluding subdirectories) : {<folder>: <folders[]>}
    folderSizes = dict()
    # Folders containing folders : {<folder>: <folders[]>}
    folders = dict()

    # Create input array
    l = l.strip().split('\n')

    # State variable
    cd = False
    ls = False
    # Size sum curr. folder
    folderSize = 0
    
    dirStack.append('/')

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
                dirStack.clear()
                dirStack.append('/')
            elif third == '..':
                dirStack.pop()
            else:
                dirStack.append(third)
        elif ls == False:
            # Counting folders and filesizes
            print('Dirstack: ', dirStack)
            currentFolder = dirStack[-1]
            if first == 'dir':
                print('Folders: ', folders.get(currentFolder, 'INGA VÄRDEN'))
                if folders.get(currentFolder, '---') == '---':
                    folders[currentFolder] = []
                
                folders[currentFolder].append(second)
            elif first.isnumeric():
                folderSizes[currentFolder] = int(first)
    print('Folders: ', folders)



    
