

class Board():
    def __init__(self, data):
        self.matrix = []
        for row in data:
            newRow = []
            splitRow = row.strip("\n").split()
            for element in splitRow:
                newRow.append(int(element))

            self.matrix.append(newRow)

        # The number of marked elements in each row and column respectively
        self.rowMarkedCount = [0] * len(self.matrix)
        self.columnMarkedCount = [0] * len(self.matrix[0])
        self.lastMarked = None


    def drawNumber(self, number):
        for rowIdx in range(len(self.matrix)):
            for colIdx in range(len(self.matrix[rowIdx])):
                if self.matrix[rowIdx][colIdx] == number:
                    self.matrix[rowIdx][colIdx] = -1
                    self.rowMarkedCount[rowIdx] += 1
                    self.columnMarkedCount[colIdx] += 1
                    self.lastMarked = number

                    if self.rowMarkedCount[rowIdx] == len(self.matrix[rowIdx]) or self.columnMarkedCount[colIdx] == len(self.matrix):
                        return True
                    else:
                        return False # This assumes a number can only appear once

        return False

    
    def unmarkedSum(self):
        total = 0
        for row in self.matrix:
            for element in row:
                if element != -1:
                    total += element
        
        return total


    def getScore(self):
        return self.unmarkedSum() * self.lastMarked

    
    def print(self):
        for row in self.matrix:
            for element in row:
                print(element, end=" ")
            print()