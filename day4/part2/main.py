import argparse
from board import Board


def parse_file(filename):
    file = open(filename, "r")
    lines = file.readlines()

    chosenNumbers = lines[0].split(",")
    numBoards = (len(lines) - 1) // 6

    boards = []
    for boardNum in range(numBoards):
        data = lines[2+boardNum*6:2+(boardNum+1)*6-1]
        newBoard = Board(data)
        boards.append(newBoard)

    return chosenNumbers, boards


def findWinner(chosenNumbers, boards):
    numWinners = 0
    for number in chosenNumbers:
        for boardIdx, board in enumerate(boards):
            if board.drawNumber(int(number)):
                numWinners += 1
                if numWinners == len(boards):
                    return boardIdx


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    chosenNumbers, boards = parse_file(args.filename)

    winningBoard = boards[findWinner(chosenNumbers, boards)]
    
    print("The last winning score is:", winningBoard.getScore())
    winningBoard.print()