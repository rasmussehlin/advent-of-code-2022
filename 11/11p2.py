from collections import deque
import functools
import math


# Thanks Wikipedia..!
def chineeseRemainderTheorem(item, divisors):
    # I'm kind of pleased with this solution :)
    def getRestFromPower(base, exponent, divisor):
        power = base
        for _ in range(exponent - 1):
            power = power * base
            power = power % divisor
        return power

    # Create array containing rests for divisors
    rests = []
    for divisor in divisors:
        rests.append(item % divisor)
    
    # The product of all divisors
    N = functools.reduce(lambda a, b: a*b, divisors)

    # Euler's totient function
    def phi(x):
        numbers = 0
        for i in range(1, x + 1):
            if math.gcd(i, x) == 1:
                numbers += 1
        return numbers

    # Solutions to the congruends (N/ni)^(phi(ni)-1) (mod ni)
    solutions = []
    for i in range(len(divisors)):
        base = int(N / divisors[i])
        base = base % divisors[i]
        exponent = phi(divisors[i]) - 1
        solutions.append(getRestFromPower(base, exponent, divisors[i]))
    
    # Calculating the smallest number for given rests
    x = 0
    for i in range(len(divisors)):
        x += rests[i] * solutions[i] * int(N / divisors[i])
    
    return x

# The blueprint for a monkey
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

    def calculateNewWorryLevel(self, old) -> int:
        return eval('old' + self.operationFunc)

    def getReceivingMonkeyIndex(self, worryLevel) -> bool:
        if worryLevel % self.divisor == 0:
            return self.trueThrowTo
        else:
            return self.falseThrowTo
    
    def throwAllItems(self, otherMonkeys, divisors):
        for i in range(len(self.items)):
            item = self.items.popleft()
            item = self.calculateNewWorryLevel(item)

            # Using the "Chineese remainder theorem" to solve
            # the smallest number which lives up to all the 
            # rests given for item % [all the divisors]
            item = chineeseRemainderTheorem(item, divisors)

            receivingMonkey = self.getReceivingMonkeyIndex(item)
            otherMonkeys[receivingMonkey].items.append(item)
            self.nrOfInspections += 1

# Create monkey object from text input
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

# Helper function to print all monkeys and their items
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
    
    # Throw stuff!
    for i in range(NR_OF_ROUNDS):
        if i % 1000 == 0:
            print('Currently on round', i)
            printAllMonkeys(monkeys)
            print()

        for j in range(len(monkeys)):
            monkeys[j].indexForPrinting = j # For printing results, aestethics
            monkeys[j].throwAllItems(monkeys, divisors)
    
    # Print result
    print('== Final item distribution ==')
    printAllMonkeys(monkeys)
    print()
    
    # Sort monkeys by nr of inspections
    monkeys.sort(key=lambda monkey: monkey.nrOfInspections, reverse=True)
    print('== Monkeys sorted by number of inspections ==')
    for i in range(len(monkeys)):
        print(str(monkeys[i].indexForPrinting) + ':', monkeys[i].nrOfInspections)

    levelOfMonkeyBusiness = monkeys[0].nrOfInspections * monkeys[1].nrOfInspections
    print('Level of monkey business:', levelOfMonkeyBusiness)
