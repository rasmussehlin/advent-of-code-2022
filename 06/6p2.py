from collections import deque
import math

with open('input.txt') as f:
    l = f.read()
    que = deque()
    index = 0
    done = False
    skip = 0
    for i in range(0, len(l), 1):
        different = True
        for c in range(i, i+14):
            for d in range(i, i+14):
                if c == d:
                    continue
                elif l[c] == l[d]:
                    different = False
        
        if different:
            index = i + 14
            break
        
    
    print(len(l[0:index]))
