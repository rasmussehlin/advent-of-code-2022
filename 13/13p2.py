# Haven't finished any nice output to the terminal.. too tired :)
from functools import cmp_to_key
from collections import deque

PRINT_VERBOSE = True
STEP_MANUALLY = False

def log(text):
    if (PRINT_VERBOSE):
        print(text)

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

def parsePackets(packets):
    newPackets = []
    for packet in packets:
        newPackets.append(parseLineIntoList(packet))
    
    return newPackets

# The recursice compare function
def isInCorrectOrder(left, right):
    if type(left) is int and type(right) is int:
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0
    elif type(left) is list and type(right) is list:
        result = 0
        for i in range(min(len(left), len(right))):
            result = isInCorrectOrder(left[i], right[i])
            if result != None:
                return 1 if result else -1
        
        if result == None:    
            if len(right) < len(left):
                return 1
            elif len(left) < len(right):
                return -1
            else:
                return 0
    else:
        if type(left) is int:
            left = [left]
        elif type(right) is int:
            right = [right]
        
        return isInCorrectOrder(left, right)

with open('example.txt') as f:
    # Format input
    l = f.read()
    pairsText = l.strip().replace('\n\n', '\n').split('\n')
    pairsText.append('[[2]]')
    pairsText.append('[[6]]')
    
    # Parse input
    log(pairsText)
    packets = parsePackets(pairsText)
    log(packets)

    # It was difficult to get a .sort(comparator) function
    # Where the comparator returns -1, 0, 1. Thanks to https://stackoverflow.com/questions/5213033/sort-a-list-of-lists-with-a-custom-compare-function
    # for giving the beneath two lines of code:
    # sorted(packets, key=cmp_to_key(isInCorrectOrder))
    packets.sort(key=cmp_to_key(isInCorrectOrder))

    # # Main loop (comparison)
    # indexToPrint = None
    # correctOrderIndices = []
    # index = 0
    # while index < len(packets) - 1:
    #     print('index:', '.'*index)
    #     first = packets[index]
    #     second = packets[index + 1]
    #     input()

    #     if isInCorrectOrder(first, second, 0) == False:
    #         print('Not ordered, changing places and setting index to 0.')
    #         tempFirst = first
    #         packets[index] = second
    #         packets[index + 1] = tempFirst
    #         index = 0
    #         continue
        

    #     index += 1
    
    # It's in order now! Let's find the divider packets
    firstIndex = -1
    secondIndex = -1
    for i in range(len(packets)):
        if str(packets[i]) == '[[6]]':
            firstIndex = i
        
        if str(packets[i]) == '[[2]]':
            secondIndex = i

        if firstIndex != -1 and secondIndex != -1:
            break
    
    print('\nThe decoder key is', firstIndex, '*', secondIndex, ':', firstIndex * secondIndex)
