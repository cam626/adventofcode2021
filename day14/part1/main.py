import argparse

class Node():
    def __init__(self, letter):
        self.letter = letter
        self.prev = None
        self.next = None

def parseInput(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        
        head = None
        prev = None
        for letter in lines[0].strip():
            node = Node(letter)

            if not head:
                head = node

            if not prev:
                prev = node
            else:
                prev.next = node
                node.prev = prev
                prev = node

        rules = {}
        for i in range(2, len(lines)):
            l = lines[i].strip().split(" -> ")
            rules[l[0]] = l[1]

    return head, rules

def printSequence(head):
    itr = head
    while itr is not None:
        print(itr.letter, end="")
        itr = itr.next
    print()

def insertLetter(a, b, letter):
    newNode = Node(letter)
    a.next = newNode
    newNode.next = b
    newNode.prev = a
    b.prev = newNode

def takeStep(head, rules):
    itr = head.next
    prev = head

    while itr is not None:
        pair = prev.letter + itr.letter
        if pair in rules:
            insertLetter(prev, itr, rules[pair])

        prev = itr
        itr = itr.next

def scoreSequence(head):
    itr = head
    counts = {}
    while itr is not None:
        if itr.letter not in counts:
            counts[itr.letter] = 1
        else:
            counts[itr.letter] += 1
        itr = itr.next

    highestFrequency = 0
    lowestFequency = float("inf")
    for _, val in counts.items():
        if val > highestFrequency:
            highestFrequency = val
        if val < lowestFequency:
            lowestFequency = val

    return highestFrequency - lowestFequency

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="training_input.txt")
    parser.add_argument("-n", "--numSteps", default=10, type=int)
    args = parser.parse_args()

    head, rules = parseInput(args.filename)
    
    for step in range(args.numSteps):
        takeStep(head, rules)
        printSequence(head)

    print(scoreSequence(head))