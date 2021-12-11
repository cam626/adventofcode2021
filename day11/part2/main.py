import argparse

def printGrid(grid):
    for row in grid:
        for element in row:
            print(element, end=" ")
        print()


def parse_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    for idx in range(len(lines)):
        row = lines[idx].strip()
        newRow = [int(element) for element in row]
        lines[idx] = newRow

    return lines


def increaseEnergyLevels(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col] += 1

# Increases the energy level of all surrounding octopi by 1
# Does not change the energy level at the current position
def flash(grid, row, col):
    if row != 0:
        grid[row-1][col] += 1

        if col != 0:
            grid[row-1][col-1] += 1
        if col != len(grid[row-1])-1:
            grid[row-1][col+1] += 1

    if row != len(grid)-1:
        grid[row+1][col] += 1

        if col != 0:
            grid[row+1][col-1] += 1
        if col != len(grid[row+1])-1:
            grid[row+1][col+1] += 1
        
    if col != 0:
        grid[row][col-1] += 1
    if col != len(grid[row])-1:
        grid[row][col+1] += 1


def flashGrid(grid):
    flashed = [[0]*len(grid[0]) for _ in range(len(grid))]
    flashCount = 0

    newFlashCount = float("inf")
    while newFlashCount != 0:
        newFlashCount = 0
        for rowIdx, row in enumerate(grid):
            for colIdx, element in enumerate(row):
                if element > 9 and not flashed[rowIdx][colIdx]:
                    flash(grid, rowIdx, colIdx)
                    newFlashCount += 1
                    flashed[rowIdx][colIdx] = 1

        flashCount += newFlashCount
        
    return flashCount, flashed


def resetFlashed(grid, flashed):
    for rowIdx in range(len(flashed)):
        for colIdx in range(len(flashed[rowIdx])):
            if flashed[rowIdx][colIdx] == 1:
                grid[rowIdx][colIdx] = 0


def simulate(grid, numDays):
    flashCount = 0
    for day in range(numDays):
        increaseEnergyLevels(grid)
        newFlashCount, flashed = flashGrid(grid)
        if newFlashCount == 100:
            print(day+1)
        flashCount += newFlashCount
        resetFlashed(grid, flashed)
    
    return flashCount


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    parser.add_argument("-n", "--numDays", type=int, default=100)
    args = parser.parse_args()

    grid = parse_file(args.filename)
    flashCount = simulate(grid, args.numDays)
    print(flashCount)
    