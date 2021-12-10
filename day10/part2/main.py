import argparse

scoreTable = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

reverseMap = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}

def parse_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    for row in lines:
        row = row.strip()

    return lines

# Lol
def reverseCharacter(character):
    return reverseMap[character]

def isLineCorrupted(line):
    openChunks = []
    for character in line:
        if character in ["(", "{", "[", "<"]:
            openChunks.append(character)
        elif character in [")", "}", "]", ">"]:
            if reverseCharacter(character) != openChunks[-1]:
                return (True, character)
            openChunks.pop()

    return (False, None)

def findCorruptedLines(lines):
    corruptedLines = []
    corruptedCharacters = []
    for lineIdx, line in enumerate(lines):
        corruptedFlag, corruptedChar = isLineCorrupted(line)
        if corruptedFlag:
            corruptedLines.append(lineIdx)
            corruptedCharacters.append(corruptedChar)

    return corruptedLines, corruptedCharacters

def removeLines(lines, indices):
    newLines = []
    for lineIdx in range(len(lines)):
        if lineIdx in indices:
            continue
        newLines.append(lines[lineIdx])

    return newLines

def completeLine(line):
    openChunks = []
    for character in line:
        if character in ["(", "{", "[", "<"]:
            openChunks.append(character)
        elif character in [")", "}", "]", ">"]:
            # Not corrupted so we can assume it closes the right thing
            openChunks.pop()

    # Now just close them in order:
    closingChunks = ""
    for i in range(len(openChunks)-1, -1, -1):
        closingChunks += reverseCharacter(openChunks[i])

    return closingChunks

def completeLines(lines):
    completionStrings = []
    for line in lines:
        completionString = completeLine(line)
        completionStrings.append(completionString)

    return completionStrings

def getScore(completionString):
    score = 0
    for character in completionString:
        score *= 5
        score += scoreTable[character]

    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    lines = parse_file(args.filename)
    corruptedLines, corruptedCharacters = findCorruptedLines(lines)

    lines = removeLines(lines, corruptedLines)
    completionStrings = completeLines(lines)

    scores = []
    for completionString in completionStrings:
        score = getScore(completionString)
        scores.append(score)

    scores.sort()
    if len(scores) % 2 == 0:
        print("Even number of scores :(")
        exit(1)

    middleScoreIdx = len(scores) // 2
    print(scores[middleScoreIdx])