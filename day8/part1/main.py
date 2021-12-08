import argparse

def parse_file(filename):
    file = open(filename, "r")
    displays = file.readlines()
    for idx in range(len(displays)):
        displays[idx] = [in_out.split() for in_out in displays[idx].split(" | ")]

    return displays


def countSimples(displays):
    count = 0

    for display in displays:
        for outputDigit in display[1]:
            l = len(outputDigit)
            
            if l == 2 or l == 3 or l == 4 or l == 7:
                count += 1

    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    displays = parse_file(args.filename)
    print(countSimples(displays))