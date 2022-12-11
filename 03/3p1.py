def translate(v):
    if ord(v) < 97:
        return 27 + ord(v) - 65
    else:
        return ord(v) - 96

def findSame(a, b):
    for c1 in a:
        for c2 in b:
            if ord(c1) == ord(c2):
                return translate(c1)

with open('input.txt') as f:
    l = f.read()
    l = l.strip().split("\n")
    summ = 0
    for line in l:
        a = line[:int(len(line)/2)]
        b = line[int(len(line)/2):]
        summ += findSame(a, b)
    print(summ)