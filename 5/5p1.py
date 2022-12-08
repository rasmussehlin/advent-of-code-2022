from collections import deque
import math

with open('input.txt') as f:
    l = f.read()
    l = l.rstrip().split("\n")
    startPositions = l[0:8]
    print(startPositions)
    
    # Build deques
    deques = []
    for i in range(9):
        deques.append(deque())

    # Fill deques
    lastC = ' '
    index = 0
    for i in range(0, 8):
        print('On position: ' + str(7-i))
        index = 0
        for c in startPositions[7-i]:
            if lastC == '[':
                print("Floor: " + str(math.floor(index / 4)))
                deques[math.floor(index / 4)].append(c)
            index += 1
            lastC = c
    
    print('\n\n')
    print('Deques constructed:')
    print(deques)
    print('\n\n')

    # Make the moves
    moves = l[10:]
    nrOfMoves = 0
    for move in moves:
        nrOfMoves += 1
        move = move.split(' ')
        print(move)
        print('Popping ', int(move[1]), ' from ', int(move[3]) - 1, '(', len(deques[int(move[3]) - 1]), ')', ' to ', int(move[5]) - 1, '(', len(deques[int(move[5]) - 1]), ')')
        for i in range(0, int(move[1])):
            print('pop!')
            deques[int(move[5]) - 1].append(deques[int(move[3]) - 1].pop())
    
    # Moves made
    print('Moves made. (', nrOfMoves, ')')
    print(deques)

    # Print top most cargo
    for d in deques:
        print(d.pop(), end='')