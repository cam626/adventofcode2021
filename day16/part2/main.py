import argparse
import sys

class Packet():
    def __init__(self, binStr):
        self.versionBits = binStr[0:3]
        self.idBits = binStr[3:6]
        self.packetContent = binStr[6:]

        self.bitsConsumed = 6

        self.version = convertBinaryToDecimal(self.versionBits)
        self.id = convertBinaryToDecimal(self.idBits)

        self.literal = None
        self.subPackets = []

        self.parsePacket()


    def parsePacket(self):
        if self.id == 4:
            self.parseLiteral()
        else:
            self.parseOperator()
        

    def parseLiteral(self):
        idx = 0
        binStr = ""
        while self.packetContent[idx] == "1":
            binStr += self.packetContent[idx+1:idx+5]
            idx += 5

        # Once we encounter a 0 at the start of the group, we need to read one
        # more group
        binStr += self.packetContent[idx+1:idx+5]
        self.literal = convertBinaryToDecimal(binStr)
        self.bitsConsumed += idx+5


    def parseOperator(self):
        self.mode = self.packetContent[0]
        self.bitsConsumed += 1

        if self.mode == "0":
            self.subPacketBitLength = convertBinaryToDecimal(self.packetContent[1:16])
            self.subPacketBits = self.packetContent[16:]
            self.bitsConsumed += 15
            self.parseSubPacketsForNumBits()
        elif self.mode == "1":
            self.numSubPackets = convertBinaryToDecimal(self.packetContent[1:12])
            self.subPacketBits = self.packetContent[12:]
            self.bitsConsumed += 11
            self.parseSubPackets()


    def parseSubPacketsForNumBits(self):
        bitsForSubPackets = 0
        subPacketStart = 0

        while bitsForSubPackets < self.subPacketBitLength:
            newSubPacket = Packet(self.subPacketBits[subPacketStart:])
            self.subPackets.append(newSubPacket)
            bitsForSubPackets += newSubPacket.bitsConsumed
            subPacketStart += newSubPacket.bitsConsumed

        self.bitsConsumed += bitsForSubPackets      

    
    def parseSubPackets(self):
        bitsForSubPackets = 0
        subPacketStart = 0

        while len(self.subPackets) < self.numSubPackets:
            newSubPacket = Packet(self.subPacketBits[subPacketStart:])
            self.subPackets.append(newSubPacket)
            bitsForSubPackets += newSubPacket.bitsConsumed
            subPacketStart += newSubPacket.bitsConsumed

        self.bitsConsumed += bitsForSubPackets


def convertBinaryToDecimal(binStr):
    decimal = 0
    for idx in range(len(binStr)):
        if binStr[-1 - idx] == "1":
            decimal += 2 ** (idx)

    return decimal


def convertHexToBinary(hexStr):
    hexToBin = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"
    }

    binStr = ""
    for character in hexStr:
        binStr += hexToBin[character]

    return binStr


def sumPacketVersions(packet):
    if len(packet.subPackets) == 0:
        return packet.version

    s = packet.version
    for subPacket in packet.subPackets:
        s += sumPacketVersions(subPacket)

    return s


def evaluate(packet):
    if packet.id == 4:
        return packet.literal

    elif packet.id == 0:
        tot = 0
        for subPacket in packet.subPackets:
            tot += evaluate(subPacket)
        return tot

    elif packet.id == 1:
        tot = evaluate(packet.subPackets[0])
        for idx in range(1, len(packet.subPackets)):
            tot *= evaluate(packet.subPackets[idx])
        return tot

    elif packet.id == 2:
        m = float("inf")
        for subPacket in packet.subPackets:
            val = evaluate(subPacket)
            if val < m:
                m = val
        return m

    elif packet.id == 3:
        m = 0
        for subPacket in packet.subPackets:
            val = evaluate(subPacket)
            if val > m:
                m = val
        return m

    elif packet.id == 5:
        return evaluate(packet.subPackets[0]) > evaluate(packet.subPackets[1])
        
    elif packet.id == 6:
        return evaluate(packet.subPackets[0]) < evaluate(packet.subPackets[1])
        
    elif packet.id == 7:
        return evaluate(packet.subPackets[0]) == evaluate(packet.subPackets[1])


if __name__ == "__main__":
    sys.setrecursionlimit(10**6)

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="training_input.txt")
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        hexStr = f.read().strip()

    binStr = convertHexToBinary(hexStr)
    
    packet = Packet(binStr)
    print(evaluate(packet))