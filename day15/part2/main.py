import argparse

def parseGrid(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        grid = [[int(element) for element in line.strip()] for line in lines]
        
    return grid

def printRiskGrid(grid, lowestCostToPoint):
    for rowIdx in range(len(grid)):
        for colIdx in range(len(grid[rowIdx])):
            if (rowIdx, colIdx) in lowestCostToPoint:
                print(lowestCostToPoint[(rowIdx, colIdx)], end="")
            else:
                print(" ", end="")
        print()

def findLowestRisk(grid):
    lowestCostToPoint = {
        (0,0): 0
    }

    queue = [(0,0)]

    while len(queue) > 0:
        point = queue.pop(0)

        newPoints = [
            (point[0]-1, point[1]),
            (point[0], point[1]-1),
            (point[0]+1, point[1]),
            (point[0], point[1]+1)
        ]

        for newPoint in newPoints:
            if newPoint[0] < 0 \
                or newPoint[1] < 0 \
                or newPoint[0] >= len(grid)*5 \
                or newPoint[1] >= len(grid[0])*5:
                continue # Point out of bounds

            numXWraps = newPoint[0] // len(grid)
            numYWraps = newPoint[1] // len(grid[0])

            addFactor = numXWraps + numYWraps
            
            wrappedX = newPoint[0] % len(grid)
            wrappedY = newPoint[1] % len(grid[0])

            baseRisk = grid[wrappedX][wrappedY]
            riskAtPoint = (baseRisk + addFactor) % 10 + (baseRisk + addFactor) // 10

            newPointRisk = lowestCostToPoint[point] + riskAtPoint
            
            if newPoint not in lowestCostToPoint:
                lowestCostToPoint[newPoint] = newPointRisk
                queue.append(newPoint)
            elif newPointRisk < lowestCostToPoint[newPoint]:
                lowestCostToPoint[newPoint] = newPointRisk
                queue.append(newPoint)

    return lowestCostToPoint[(len(grid)*5-1, len(grid[0])*5-1)]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="training_input.txt")
    args = parser.parse_args()

    grid = parseGrid(args.filename)
    print(findLowestRisk(grid))