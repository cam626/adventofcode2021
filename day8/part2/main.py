import argparse
from digit import Digit

class Display():
    def __init__(self, inputDigitStrings, outputDigitStrings):
        # inputDigits contains one of each digit ("Each entry consists of ten unique signal patterns")
        self.inputDigits = [Digit(digitString) for digitString in inputDigitStrings]
        self.outputDigits = [Digit(digitString) for digitString in outputDigitStrings]

        # We should know at least 1, 4, 7, and 8 at the start
        self.discoveredDigits = {}
        for inputDigit in self.inputDigits:
            if inputDigit.digit != None:
                self.discoveredDigits[inputDigit.digit] = inputDigit

        # The segments are arranged as they were in the original diagrams:
        #  aaaa 
        # b    c
        # b    c
        #  dddd 
        # e    f
        # e    f
        #  gggg
        #
        # So e mapped to g means that wire e in this display is equivalent to 
        # segment g. When this is fully filled in we can decode any digit
        self.wireToSegmentMap = {}
        self.segmentToWireMap = {}

        # 2, 3, 5
        self.fiveSegmentDigits = []

        # 0, 6, 9
        self.sixSegmentDigits = []

        for digit in self.inputDigits:
            if digit.numSegmentsOn == 5:
                self.fiveSegmentDigits.append(digit)
            elif digit.numSegmentsOn == 6:
                self.sixSegmentDigits.append(digit)

        self.discoverSegmentA()
        self.discoverDigit6()
        self.discoverSegmentC()
        self.discoverSegmentF()
        self.discoverDigit3()
        self.discoverSegmentG()
        self.discoverSegmentD()
        self.discoverDigit9and0()
        self.discoverSegmentB()
        self.discoverSegmentE()
        self.discoverDigit2and5()


    def discoverSegmentA(self):
        # Depends on 1 and 7
        wireForSegmentASet = self.discoveredDigits[7].onWires - self.discoveredDigits[1].onWires
        wireForSegmentA = wireForSegmentASet.pop()
        self.wireToSegmentMap[wireForSegmentA] = "a"
        self.segmentToWireMap["a"] = wireForSegmentA


    def discoverDigit6(self):
        # Depends on 1
        for digit in self.sixSegmentDigits:
            if len(digit.onWires - self.discoveredDigits[1].onWires) == 5:
                self.discoveredDigits[6] = digit
                digit.digit = 6
                break


    def discoverSegmentC(self):
        # Depends on 1 and 6
        wireForSegmentCSet = self.discoveredDigits[1].onWires - self.discoveredDigits[6].onWires
        wireForSegmentC = wireForSegmentCSet.pop()
        self.wireToSegmentMap[wireForSegmentC] = "c"
        self.segmentToWireMap["c"] = wireForSegmentC


    def discoverSegmentF(self):
        # Depends on 1 and c
        wireForSegmentFSet = self.discoveredDigits[1].onWires - set(self.segmentToWireMap["c"])
        wireForSegmentF = wireForSegmentFSet.pop()
        self.wireToSegmentMap[wireForSegmentF] = "f"
        self.segmentToWireMap["f"] = wireForSegmentF


    def discoverDigit3(self):
        # Depends on 1
        for digit in self.fiveSegmentDigits:
            if len(digit.onWires - self.discoveredDigits[1].onWires) == 3:
                self.discoveredDigits[3] = digit
                digit.digit = 3
                break

    
    def discoverSegmentG(self):
        # Depends on 3, 4 and a
        wireForSegmentGSet = self.discoveredDigits[3].onWires - self.discoveredDigits[4].onWires - set(self.segmentToWireMap["a"])
        wireForSegmentG = wireForSegmentGSet.pop()
        self.wireToSegmentMap[wireForSegmentG] = "g"
        self.segmentToWireMap["g"] = wireForSegmentG


    def discoverSegmentD(self):
        # Depends on 3, a, c, f and g
        wireForSegmentDSet = self.discoveredDigits[3].onWires - set([self.segmentToWireMap["a"], self.segmentToWireMap["c"], self.segmentToWireMap["f"], self.segmentToWireMap["g"]])
        wireForSegmentD = wireForSegmentDSet.pop()
        self.wireToSegmentMap[wireForSegmentD] = "d"
        self.segmentToWireMap["d"] = wireForSegmentD


    def discoverDigit9and0(self):
        # Depends on 6 and d
        for digit in self.sixSegmentDigits:
            if digit.digit == 6:
                continue

            if len(digit.onWires - set(self.segmentToWireMap["d"])) == 5:
                self.discoveredDigits[9] = digit
                self.discoveredDigits[9].digit = 9
            else:
                self.discoveredDigits[0] = digit
                self.discoveredDigits[0].digit = 0


    def discoverSegmentB(self):
        # Depends on 9, a, c, d, f and g
        wireForSegmentBSet = self.discoveredDigits[9].onWires - set([self.segmentToWireMap["a"], self.segmentToWireMap["c"], self.segmentToWireMap["d"], self.segmentToWireMap["f"], self.segmentToWireMap["g"]])
        wireForSegmentB = wireForSegmentBSet.pop()
        self.wireToSegmentMap[wireForSegmentB] = "b"
        self.segmentToWireMap["b"] = wireForSegmentB


    def discoverSegmentE(self):
        wireForSegmentESet = self.discoveredDigits[0].onWires - self.discoveredDigits[3].onWires - set(self.segmentToWireMap["b"])
        wireForSegmentE = wireForSegmentESet.pop()
        self.wireToSegmentMap[wireForSegmentE] = "e"
        self.segmentToWireMap["e"] = wireForSegmentE


    def discoverDigit2and5(self):
        for digit in self.fiveSegmentDigits:
            if digit.digit == 3:
                continue

            if len(digit.onWires - set(self.segmentToWireMap["c"])) == 4:
                self.discoveredDigits[2] = digit
                self.discoveredDigits[2].digit = 2
            else:
                self.discoveredDigits[5] = digit
                self.discoveredDigits[5].digit = 5


    def decodeDigit(self, digitStr):
        for num in self.discoveredDigits:
            if num == None: continue
            digit = self.discoveredDigits[num]
            if digit.onWires == set(digitStr):
                return num
        
        return -1


    def getValue(self):
        total = 0
        position = 1000
        for digit in self.outputDigits:
            digit.digit = self.decodeDigit(digit.onWires)
            total += position * digit.digit
            position /= 10

        return total


def parse_file(filename):
    file = open(filename, "r")
    displays = file.readlines()
    for idx in range(len(displays)):
        displays[idx] = [in_out.split() for in_out in displays[idx].split(" | ")]
        display = Display(displays[idx][0], displays[idx][1])
        displays[idx] = display

    return displays


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    displays = parse_file(args.filename)

    total = 0
    for display in displays:
        val = display.getValue()
        total += val
    print(total)