from collections import deque

with open('input.txt') as f:
    l = f.read()
    instructions = l.strip().split('\n')
    instructions = list(map(lambda instr: instr.split(' '), instructions))
    instructions = deque(instructions)
    
    