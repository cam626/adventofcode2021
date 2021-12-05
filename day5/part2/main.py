import argparse


class IntersectionCounter():
    def __init__(self):
        self.visitedOne = set()
        self.visitedTwoPlus = set()


    def flipForPositiveIteration(self, a, b):
        if b < a:
            return b, a
        return a, b


    def visitPoint(self, point):
        if point not in self.visitedOne and point not in self.visitedTwoPlus:
            self.visitedOne.add(point)
        elif point in self.visitedOne:
            self.visitedTwoPlus.add(point)
            self.visitedOne.remove(point)


    def processHorizontalLine(self, startX, endX, y):
        startX, endX = self.flipForPositiveIteration(startX, endX)

        for x in range(startX, endX+1):
            point = (x,y)
            self.visitPoint(point)


    def processVerticalLine(self, x, startY, endY):
        startY, endY = self.flipForPositiveIteration(startY, endY)
            
        for y in range(startY, endY+1):
            point = (x,y)
            self.visitPoint(point)


    def processDiagonalLine(self, startX, endX, startY, endY):
        xIterDirection = int((endX - startX) / abs((endX - startX)))
        yIterDirection = int((endY - startY) / abs((endY - startY)))

        distance = abs(endX - startX) + 1

        for iter in range(distance):
            point = (startX + iter * xIterDirection, startY + iter * yIterDirection)
            self.visitPoint(point)


    def countDoubleIntersections(self, lines):
        for line in lines:
            startX = int(line[0][0])
            startY = int(line[0][1])
            endX = int(line[1][0])
            endY = int(line[1][1])

            if startX == endX:
                self.processVerticalLine(startX, startY, endY)
            elif startY == endY:
                self.processHorizontalLine(startX, endX, startY)
            else:
                self.processDiagonalLine(startX, endX, startY, endY)


    def getNumDoubleIntersected(self):
        return len(self.visitedTwoPlus)


def parse_file(filename):
    file = open(filename, "r")
    rawLines = file.readlines()

    lines = []
    for rawLine in rawLines:
        newLine = rawLine.strip("\n").split(" -> ")

        start = newLine[0].split(",")
        end = newLine[1].split(",")

        lines.append([start, end])

    return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    lines = parse_file(args.filename)
    counter = IntersectionCounter()
    counter.countDoubleIntersections(lines)
    print("There were {} points that were intersected 2 or more times".format(counter.getNumDoubleIntersected()))