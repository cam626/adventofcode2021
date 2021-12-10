import argparse

scoreTable = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    lines = parse_file(args.filename)
    corruptedLines, corruptedCharacters = findCorruptedLines(lines)

    totalScore = 0
    for corruptedCharacter in corruptedCharacters:
        totalScore += scoreTable[corruptedCharacter]

    print(totalScore)