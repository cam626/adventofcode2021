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


def getBasinSize(grid, lowPoint):
    inBasin = set()

    visited = set()

    queue = list()
    queue.append(lowPoint)
    while len(queue) != 0:
        point = queue.pop(0)
        row, col = point
        
        if point in visited:
            continue

        visited.add(point)
        if grid[row][col] == 9:
            continue
        
        inBasin.add(point)

        left = grid[row-1][col] if row > 0 else None
        up = grid[row][col - 1] if col > 0 else None
        right = grid[row+1][col] if row < len(grid) - 1 else None
        down = grid[row][col+1] if col < len(grid[0]) - 1 else None

        if left != None and left not in visited:
            queue.append((row-1, col))
        if up != None and up not in visited:
            queue.append((row, col-1))
        if right != None and right not in visited:
            queue.append((row+1, col))
        if down != None and down not in visited:
            queue.append((row, col+1))

    return len(inBasin)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    grid = parse_file(args.filename)
    lowPoints = findLowPoints(grid)
    totalRisk = 0
    basinSizes = []
    for point in lowPoints:
        basinSizes.append(getBasinSize(grid, point))

    basinSizes.sort(reverse=True)
    print(basinSizes[0] * basinSizes[1] * basinSizes[2])