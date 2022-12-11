from collections import deque

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

    while len(instructions) > 0:
        if instructionCycles == 0:
            # Read instruction
            resultTuple = readInstruction(instructions)
            currentInstruction = resultTuple[0]
            instructionCycles = resultTuple[1]
        

        # print(str(currentCycle) + ':\t', xRegister, '\t', 'addx(' + str(currentInstruction[1]) + ')\t' if currentInstruction[0] == 'addx' else 'noop\t', instructionCycles, '\t')
        # input(end='')
        
        if currentCycle == 20 or (currentCycle - 20) % 40 == 0:
            # print(str(currentCycle) + ':\t', 'Signalstrength =\t', currentCycle, '\t*\t', xRegister, '\t=\t', currentCycle * xRegister)
            # input()
            totalSignalStrength += currentCycle * xRegister


        if instructionCycles > 0:
            # Do work
            if currentInstruction[0] == 'addx':
                instructionCycles -= 1
                if instructionCycles == 0:
                    xRegister += int(currentInstruction[1])
            elif currentInstruction[0] == 'noop':
                instructionCycles -= 1
        
        currentCycle += 1
    
    # print()
    print('totalSignalStrength', totalSignalStrength)

        