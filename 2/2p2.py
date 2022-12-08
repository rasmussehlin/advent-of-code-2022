def oversatt(a):
    match a:
        case 'A':
            return 1
        case 'B':
            return 2
        case 'C':
            return 3

with open('input.txt') as f:
    l = f.read()
    l = l.strip().split("\n")
    summ = 0

    l = list(map(lambda line: line.split(), l))
    # for line in l:
    #     line[0] = oversatt(line[0])
    
    for line in l:
        motis = line[0]
        match line[1]:
            case 'X':
                match motis:
                    case 'A':
                        summ += 3
                    case 'B':
                        summ += 1
                    case 'C':
                        summ += 2                
            case 'Y':
                summ += oversatt(motis)
                summ += 3
            case 'Z':
                match motis:
                    case 'A':
                        summ += 2
                    case 'B':
                        summ += 3
                    case 'C':
                        summ += 1               
                summ += 6

    print(summ)