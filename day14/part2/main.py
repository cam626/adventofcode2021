import argparse
import copy
from tqdm import tqdm

def parseInput(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        
        template = lines[0].strip()

        pairTree = {}
        frequencyMap = {
            template[0]: 1
        }

        for idx in range(len(template)-1):
            letter1 = template[idx]
            letter2 = template[idx+1]
            if letter1 not in pairTree:
                pairTree[letter1] = {}

            if letter2 not in pairTree[letter1]:
                pairTree[letter1][letter2] = 0

            pairTree[letter1][letter2] += 1

            if letter2 not in frequencyMap:
                frequencyMap[letter2] = 0

            frequencyMap[letter2] += 1

        rules = {}
        for i in range(2, len(lines)):
            l = lines[i].strip().split(" -> ")
            rules[l[0]] = l[1]

    return pairTree, rules, frequencyMap


def applyRule(pairTree, newPairTree, frequencyMap, rule, insertionLetter):
    letter1 = rule[0]
    letter2 = rule[1]

    # Check if the rule matches, if not nothing changes
    if letter1 not in pairTree:
        return

    if letter2 not in pairTree[letter1]:
        return

    # Figure out how many times we find this rule
    numPairs = pairTree[letter1][letter2]

    # Keep track of the count of each letter. No letters 
    # are deleted, we only insert the new letter once per 
    # pair that the rule matched
    if insertionLetter not in frequencyMap:
        frequencyMap[insertionLetter] = 0
    frequencyMap[insertionLetter] += numPairs

    # The pairs that were matched no longer exist
    if letter1 in newPairTree and letter2 in newPairTree[letter1]:
        newPairTree[letter1][letter2] -= numPairs
        if newPairTree[letter1][letter2] == 0:
            newPairTree[letter1].pop(letter2)

            if len(newPairTree[letter1]) == 0:
                newPairTree.pop(letter1)

    # Add pairs corresponding to L1-Insert
    if letter1 not in newPairTree:
        newPairTree[letter1] = {}

    if insertionLetter not in newPairTree[letter1]:
        newPairTree[letter1][insertionLetter] = 0
        
    newPairTree[letter1][insertionLetter] += numPairs
    
    # Add pairs corresponding to Insert-L2
    if insertionLetter not in newPairTree:
        newPairTree[insertionLetter] = {}

    if letter2 not in newPairTree[insertionLetter]:
        newPairTree[insertionLetter][letter2] = 0

    newPairTree[insertionLetter][letter2] += numPairs


def takeStep(pairTree, rules, frequencyMap):
    newPairTree = copy.deepcopy(pairTree)
    for rule, insertionLetter in rules.items():
        applyRule(pairTree, newPairTree, frequencyMap, rule, insertionLetter)
    
    return newPairTree


def getScore(frequencyMap):
    highestCount = 0
    lowestCount = float("inf")
    for _, count in frequencyMap.items():
        if count > highestCount:
            highestCount = count
        if count < lowestCount:
            lowestCount = count
    
    return highestCount - lowestCount


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="training_input.txt")
    parser.add_argument("-n", "--numSteps", default=10, type=int)
    args = parser.parse_args()

    pairTree, rules, frequencyMap = parseInput(args.filename)
    for _ in range(args.numSteps):
        pairTree = takeStep(pairTree, rules, frequencyMap)
    
    print(getScore(frequencyMap))
