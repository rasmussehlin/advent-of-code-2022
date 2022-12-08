def vinnare(a, b):
    if a == 'A' and b == 'Y' or a == 'B' and b == 'Z' or a == 'C' and b == 'X':
        return 6
    elif a == 'A' and b == 'X' or a == 'B' and b == 'Y' or a == 'C' and b == 'Z':
        return 3
    else:
        return 0

with open('input.txt') as f:
    l = f.read()
    l = l.strip().split("\n")
    summ = 0
    for line in l:
        v = line.split()
        jag = v[1]
        if jag == 'X':
            summ += 1
        elif jag == 'Y':
            summ += 2
        else:
            summ += 3
        
        summ += vinnare(v[0], v[1])

    print(summ)