from collections import deque

class Monkey:
    items = deque()
    operationFunc = ''
    dividingFactor = 0
    trueThrowTo = -1
    falseThrowTo = -1
    nrOfInspections = 0
    indexForPrinting = -1

    def __init__(self, items, operationFunc, dividingFactor, ifTrue, ifFalse) -> None:
        self.items = items
        self.operationFunc = operationFunc
        self.dividingFactor = dividingFactor
        self.trueThrowTo = ifTrue
        self.falseThrowTo = ifFalse
        self.nrOfInspections = 0

    def operation(self, old) -> int:
        return eval('old' + self.operationFunc)

    def getReceivingMonkey(self, worryLevel) -> bool:
        if worryLevel % self.dividingFactor == 0:
            return self.trueThrowTo
        else:
            return self.falseThrowTo
    
    def throwAllItems(self, otherMonkeys):
        for i in range(len(self.items)):
            item = self.items.popleft()
            item = self.operation(item)
            item = int(item / 3)
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
    dividingFactor = int(test[3])

    # throws
    ifTrue = int(rows[4].strip().split(' ')[5])
    ifFalse = int(rows[5].strip().split(' ')[5])

    return Monkey(items, operation, dividingFactor, ifTrue, ifFalse)

def printAllMonkeys(monkeys):
    for i in range(len(monkeys)):
        print(str(i) + ':', monkeys[i].items)

with open('input.txt') as f:
    # Format input
    l = f.read()
    monkeyInput = l.strip().split('\n\n')
    monkeys = []
    NR_OF_ROUNDS = 20

    # Add monkeys
    for monkeyText in monkeyInput:
        monkeys.append(parseNewMonkey(monkeyText))
    
    # Throw stuff!
    for i in range(NR_OF_ROUNDS):
        for j in range(len(monkeys)):
            monkeys[j].indexForPrinting = j # For printing results, aestethics
            monkeys[j].throwAllItems(monkeys)
    
    print('== Final item distribution ==')
    printAllMonkeys(monkeys)
    print()

    
    monkeys.sort(key=lambda monkey: monkey.nrOfInspections, reverse=True)
    print('== Monkeys sorted by number of inspections ==')
    for i in range(len(monkeys)):
        print(str(monkeys[i].indexForPrinting) + ':', monkeys[i].nrOfInspections)

    levelOfMonkeyBusiness = monkeys[0].nrOfInspections * monkeys[1].nrOfInspections
    print('Level of monkey business:', levelOfMonkeyBusiness)
