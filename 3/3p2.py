def translate(v):
    if ord(v) < 97:
        return 27 + ord(v) - 65
    else:
        return ord(v) - 96

def findSame(group):
    for r1 in group[0]:
        for r2 in group[1]:
            if r1 == r2:
                for r3 in group[2]:
                    if r1 == r3:
                        return translate(r1)


with open('input.txt') as f:
    l = f.read()
    l = l.strip().split("\n")
    summ = 0
    for i in range(int(len(l) / 3)):
        group = l[i*3:i*3 + 3]
        summ += findSame(group)
    print(summ)