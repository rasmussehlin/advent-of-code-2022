from collections import deque
import functools
import math


# Thanks Wikipedia..!
def chineeseRemainderTheorem(item, divisors):
        # Create array with rests
        rests = []
        for divisor in divisors:
            rests.append(item % divisor)
        
        # print('rests',rests)
        
        # The product of all divisors
        N = functools.reduce(lambda a, b: a*b, divisors)
        # print('N',N)

        # Euler's totient function
        def phi(x):
            numbers = 0
            for i in range(1, x + 1):
                if math.gcd(i, x) == 1:
                    numbers += 1
            # print('phi(', x, ') = ', numbers, sep='')
            return numbers

        # Solutions to the congruends (N/ni)^(phi(ni)-1) (mod ni)
        solutions = []
        for i in range(len(divisors)):
            base = int(N / divisors[i])
            base = base % divisors[i]
            exponent = phi(divisors[i]) - 1

            power = base
            # print(0, 'power:', power)
            for j in range(exponent - 1):
                power = power * base
                power = power % divisors[i]
                # print(j, 'power:', power)
            
            # print('power:', power)
            # print('base:', base)
            # print('exponent:', exponent)
            # print('int(math.pow(base, exponent)):', int(math.pow(base, exponent)))
            # print('divisors[i]:', divisors[i])

            solutions.append(power % divisors[i])
        
        # print('Solutions bi:', solutions)

        # Calculating the smallest number for the rests
        x = 0
        for i in range(len(divisors)):
            x += rests[i] * solutions[i] * int(N / divisors[i])
        
        # print(x)
        
        return x

class Monkey:
    items = deque()
    operationFunc = ''
    divisor = 0
    trueThrowTo = -1
    falseThrowTo = -1
    nrOfInspections = 0
    indexForPrinting = -1

    def __init__(self, items, operationFunc, divisor, ifTrue, ifFalse) -> None:
        self.items = items
        self.operationFunc = operationFunc
        self.divisor = divisor
        self.trueThrowTo = ifTrue
        self.falseThrowTo = ifFalse
        self.nrOfInspections = 0

    def operation(self, old) -> int:
        return eval('old' + self.operationFunc)

    def getReceivingMonkey(self, worryLevel) -> bool:
        if worryLevel % self.divisor == 0:
            return self.trueThrowTo
        else:
            return self.falseThrowTo
    
    def throwAllItems(self, otherMonkeys, divisors):
        for i in range(len(self.items)):
            item = self.items.popleft()
            item = self.operation(item)
            # item = int(item / 3) # Part 2

            # So, I do believe I'm supposed to solve 
            # this using the "Chineese remainder theorem"?
            
            # print('== Rests for', item,'==')
            # for divisor in divisors:
            #     print(item % divisor, end=', ')
            # print()
            # print()

            item = chineeseRemainderTheorem(item, divisors)

            # print('== Rests for new item', item,'==')
            # for divisor in divisors:
            #     print(item % divisor, end=', ')
            # print()

            # input()

            receivingMonkey = self.getReceivingMonkey(item)
            otherMonkeys[receivingMonkey].items.append(item)
            self.nrOfInspections += 1

def parseNewMonkey(monkeyText):
    rows = monkeyText.strip().split('\n')
    # items
    itemsText = list(map(lambda string: string.replace(',', ''), rows[1].strip().split(' ')))
    items = deque()
    for i in range(2, len(itemsText)):
        items.append(int(itemsText[i]))
    
    # operation
    operationText = rows[2].strip()
    operation = operationText[21:len(operationText)]

    # test
    test = rows[3].strip().split(' ')
    divisor = int(test[3])

    # throws
    ifTrue = int(rows[4].strip().split(' ')[5])
    ifFalse = int(rows[5].strip().split(' ')[5])

    return Monkey(items, operation, divisor, ifTrue, ifFalse)

def printAllMonkeys(monkeys):
    for i in range(len(monkeys)):
        print(str(i) + ':', monkeys[i].items)

def onlyRelativePrimes(divisors):
    toRemove = []
    skipIndexes = []
    for i in range(len(divisors) - 1):
        if skipIndexes.count(i) != 0:
            continue

        for j in range(i + 1, len(divisors)):
            if divisors[i] % divisors[j] == 0:
                toRemove.append(divisors[j])
                skipIndexes.append(j)
            elif divisors[j] % divisors[i] == 0:
                toRemove.append(divisors[i])
                break
    
    for divisor in toRemove:
        divisors.remove(divisor)

with open('input.txt') as f:
    # Format input
    l = f.read()
    monkeyInput = l.strip().split('\n\n')
    monkeys = []
    NR_OF_ROUNDS = 10000

    # Add monkeys
    for monkeyText in monkeyInput:
        monkeys.append(parseNewMonkey(monkeyText))

    # Get all divisors and remove them
    # who aren't realtive prime
    divisors = []
    for monkey in monkeys:
        divisors.append(monkey.divisor)

    onlyRelativePrimes(divisors)
    # print(divisors, end='\n\n\n')
    
    # Throw stuff!
    for i in range(NR_OF_ROUNDS):
        for j in range(len(monkeys)):
            monkeys[j].indexForPrinting = j # For printing results, aestethics
            monkeys[j].throwAllItems(monkeys, divisors)
    #     printAllMonkeys(monkeys)
    #     # input()
    
    print('== Final item distribution ==')
    printAllMonkeys(monkeys)
    print()

    
    monkeys.sort(key=lambda monkey: monkey.nrOfInspections, reverse=True)
    print('== Monkeys sorted by number of inspections ==')
    for i in range(len(monkeys)):
        print(str(monkeys[i].indexForPrinting) + ':', monkeys[i].nrOfInspections)

    levelOfMonkeyBusiness = monkeys[0].nrOfInspections * monkeys[1].nrOfInspections
    print('Level of monkey business:', levelOfMonkeyBusiness)
