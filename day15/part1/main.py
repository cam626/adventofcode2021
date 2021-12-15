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
                or newPoint[0] >= len(grid) \
                or newPoint[1] >= len(grid[0]):
                continue # Point out of bounds

            newPointRisk = lowestCostToPoint[point] + grid[newPoint[0]][newPoint[1]]
            
            if newPoint not in lowestCostToPoint:
                lowestCostToPoint[newPoint] = newPointRisk
                queue.append(newPoint)
            elif newPointRisk < lowestCostToPoint[newPoint]:
                lowestCostToPoint[newPoint] = newPointRisk
                queue.append(newPoint)

    return lowestCostToPoint[(len(grid)-1, len(grid[0])-1)]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="training_input.txt")
    args = parser.parse_args()

    grid = parseGrid(args.filename)
    print(findLowestRisk(grid))