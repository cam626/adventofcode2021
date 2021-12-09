import argparse


def parse_file(filename):
    file = open(filename, "r")
    rows = file.readlines()
    for idx in range(len(rows)):
        row = [int(col) for col in rows[idx].strip()]
        rows[idx] = row

    return rows


def isLowPoint(grid, row, col):
    currentItem = grid[row][col]
    if row > 0 and grid[row-1][col] <= currentItem:
        return False
    if col > 0 and grid[row][col - 1] <= currentItem:
        return False
    if row < len(grid) - 1 and grid[row+1][col] <= currentItem:
        return False
    if col < len(grid[0]) - 1 and grid[row][col+1] <= currentItem:
        return False
    return True


def findLowPoints(grid):
    lowPoints = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if isLowPoint(grid, row, col):
                lowPoints.append((row, col))

    return lowPoints


def riskLevel(grid, row, col):
    return grid[row][col] + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    grid = parse_file(args.filename)
    lowPoints = findLowPoints(grid)
    totalRisk = 0
    for point in lowPoints:
        totalRisk += riskLevel(grid, point[0], point[1])

    print(totalRisk)