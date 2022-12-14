# Haven't finished any nice output to the terminal.. too tired :)

from collections import deque

PRINT_VERBOSE = False
STEP_MANUALLY = False

def log(text):
    if (PRINT_VERBOSE):
        print(text)
        # input()

def waitOnStep():
    if STEP_MANUALLY:
        input()

def parseLineIntoList(line):
    # States
    WAITING_FOR_CHARACTER = 'WAITING_FOR_CHARACTER'
    BUILDING_NUMBER = 'BUILDING_NUMBER__'
    CREATING_NEW_LIST = 'CREATING_NEW_LIST'
    MOVING_ONE_LEVEL_UP = 'MOVING_ONE_LEVEL_UP'

    mainList = []
    currentList = mainList
    listStack = deque()
    listStack.append(currentList)

    number = ''
    state = WAITING_FOR_CHARACTER
    currentIndex = 0
    while currentIndex < len(line):
        character = line[currentIndex]
        # log(state +  '\t' + character +  '\t' + str(currentIndex) +  '\t' + str(mainList))
        # waitOnStep()

        if state == WAITING_FOR_CHARACTER:
            if character == '[':
                state = CREATING_NEW_LIST
            elif character.isnumeric():
                state = BUILDING_NUMBER
                number = ''
            elif character == ',':
                state = WAITING_FOR_CHARACTER
                currentIndex += 1
            elif character == ']':
                state = MOVING_ONE_LEVEL_UP

        elif state == BUILDING_NUMBER:
            if character.isnumeric():
                number = number + character
                currentIndex += 1
            else:
                currentList.append(int(number))
                
                if character == ',':
                    state = WAITING_FOR_CHARACTER
                    currentIndex += 1
                elif character == ']':
                    state = MOVING_ONE_LEVEL_UP

        elif state == CREATING_NEW_LIST:
            newList = []
            currentList.append(newList)
            listStack.append(currentList)
            currentList = newList
            state = WAITING_FOR_CHARACTER
            currentIndex += 1

        elif state == MOVING_ONE_LEVEL_UP:
            currentList = listStack.pop()
            state = WAITING_FOR_CHARACTER
            currentIndex += 1
    
    return mainList[0]

def parsePairStringsToListsAndNumbers(pairStrings):
    pairs = []
    for pairString in pairStrings:
        pairList = []
        for pair in pairString:
            pairList.append(parseLineIntoList(pair))

        pairs.append(pairList)
    
    return pairs

# The recursice compare function
def isInCorrectOrder(left, right, level):
    if type(left) is int and type(right) is int:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    elif type(left) is list and type(right) is list:
        result = None
        for i in range(min(len(left), len(right))):
            result = isInCorrectOrder(left[i], right[i], level + 1)
            if result != None:
                return result
        
        if result == None:    
            if len(right) < len(left):
                return False
            elif len(left) < len(right):
                return True
            else:
                return None
    else:
        if type(left) is int:
            left = [left]
        elif type(right) is int:
            right = [right]
        
        return isInCorrectOrder(left, right, level + 1)

with open('input.txt') as f:
    # Format input
    l = f.read()
    pairsText = l.strip().split('\n\n')
    pairs = []
    for pairText in pairsText:
        pairs.append(pairText.split('\n'))
    
    # Parse input
    pairs = parsePairStringsToListsAndNumbers(pairs)

    # Main loop (comparison)
    indexToPrint = None
    correctOrderIndices = []
    for i in range(len(pairs)):
        indexToPrint = i + 1
        left = pairs[i][0]
        right = pairs[i][1]

        isCorrectOrder = isInCorrectOrder(left, right, 0)

        if isCorrectOrder:
            log(indexToPrint)
            correctOrderIndices.append(indexToPrint)
            
    # Print result
    result = 0
    for index in correctOrderIndices:
        result += index
    
    print('\nThe sum of all indices is:', result)
