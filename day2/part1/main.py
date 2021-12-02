import argparse


def parse_file(filename):
    file = open(filename, "r")
    return file.readlines()


class Submarine():
    def __init__(self):
        self.horizontal = 0
        self.depth = 0

    def forward(self, units):
        self.horizontal += units

    def up(self, units):
        self.depth -= units

    def down(self, units):
        self.depth += units

    def printLocation(self):
        print("The submarine has a horizontal position of {} and a depth of {}. These multiply to {}.".format(self.horizontal, self.depth, self.horizontal*self.depth))

    def followDirections(self, sequence):
        for instruction in sequence:
            seq_list = instruction.split(" ")
            direction = seq_list[0]
            distance = int(seq_list[1])

            if direction == "forward":
                self.forward(distance)
            elif direction == "up":
                self.up(distance)
            elif direction == "down":
                self.down(distance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    sequence = parse_file(args.filename)
    
    s = Submarine()
    s.followDirections(sequence)
    s.printLocation()