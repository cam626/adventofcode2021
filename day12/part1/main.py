import argparse

def parseInput(filename):
    adjList = {}
    with open(filename, "r") as f:
        edges = f.readlines()
        for edgeStr in edges:
            edge = edgeStr.strip().split("-")
            start = edge[0]
            end = edge[1]

            # Edges go both ways
            if start not in adjList:
                adjList[start] = []
            adjList[start].append(end)

            if end not in adjList:
                adjList[end] = []
            adjList[end].append(start)

    return adjList


def bfs(node, adjList, visited):
    if node == "end":
        return 1

    if node in visited:
        return 0

    newVisited = visited.copy()
    if not node.isupper():
        newVisited.add(node)

    numPaths = 0
    for childNode in adjList[node]:
        numPaths += bfs(childNode, adjList, newVisited)

    return numPaths

def bfsDriver(adjList):
    visited = set()

    return bfs("start", adjList, visited)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="training_input.txt")
    args = parser.parse_args()

    adjList = parseInput(args.filename)
    numPaths = bfsDriver(adjList)
    print(numPaths)