from collections import deque
import time

with open('input.txt') as f:
    l = f.read()
    instructions = l.strip().split('\n')
    instructions = list(map(lambda instr: instr.split(' '), instructions))
    instructions.reverse()
    instructions = deque(instructions)
    
    currentCycle = 1
    xRegister = 1
    instructionCycles = 0
    currentInstruction = None

    totalSignalStrength = 0

    def readInstruction(instructions):
        instruction = instructions.pop()

        if instruction[0] == 'noop':
            return (instruction, 1)
        
        if instruction[0] == 'addx':
            return (instruction, 2)
        
        raise ValueError('Instruction "' + instruction[0] + '" not known')

    # For fixing the first printed symbol
    # What did I do wrong? The currentCycle starts at 1
    print('.', end='')

    while len(instructions) > 0:
        # 1. Read instruction
        if instructionCycles == 0:
            resultTuple = readInstruction(instructions)
            currentInstruction = resultTuple[0]
            instructionCycles = resultTuple[1]
        
        # 2. Check current value
        if currentCycle == 20 or (currentCycle - 20) % 40 == 0:
            totalSignalStrength += currentCycle * xRegister
        
        # 3. Print pixel
        horizontalPosition = (currentCycle - 1) % 40 # 0 - 39

        # horizontalPosition = (currentCycle - int(currentCycle / 40) * 40) - 1
        # if horizontalPosition < 0:
        #     horizontalPosition = 0
        if currentCycle % 40 == 0:
            print('\n', end='')
            # time.sleep(0.1)
        
        if abs(horizontalPosition - xRegister) <= 1:
            print('#', end='')
        else:
            print('.', end='')
        
        # input()

        # 4. Do work according to instruction
        if instructionCycles > 0:
            if currentInstruction[0] == 'addx':
                instructionCycles -= 1
                if instructionCycles == 0:
                    xRegister += int(currentInstruction[1])
            elif currentInstruction[0] == 'noop':
                instructionCycles -= 1
        
        currentCycle += 1
    
    # print()
    # print('totalSignalStrength', totalSignalStrength)

        