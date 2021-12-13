import argparse

def parseInput(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

        pointLocations = []
        foldInstructions = []
        for line in lines:
            if not line.startswith("fold") and "," in line:
                pointLocations.append([int(item) for item in line.strip().split(",")])
            elif line.startswith("fold"):
                direction = line[11]
                location = int(line.strip().split("=")[1])
                foldInstructions.append((direction, location))

    return pointLocations, foldInstructions

def foldX(pointLocations, foldLocation):
    for point in pointLocations:
        if point[0] > foldLocation:
            distance = point[0] - foldLocation
            point[0] = foldLocation - distance

def foldY(pointLocations, foldLocation):
    for point in pointLocations:
        if point[1] > foldLocation:
            distance = point[1] - foldLocation
            point[1] = foldLocation - distance

def makeFold(pointLocations, instruction):
    if instruction[0] == "x":
        foldX(pointLocations, instruction[1])
    elif instruction[0] == "y":
        foldY(pointLocations, instruction[1])

def numVisiblePoints(pointLocations):
    locs = set()
    for point in pointLocations:
        locs.add((point[0], point[1]))
    return len(locs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="training_input.txt")
    args = parser.parse_args()

    pointLocations, foldInstructions = parseInput(args.filename)

    makeFold(pointLocations, foldInstructions[0])
    print(numVisiblePoints(pointLocations))