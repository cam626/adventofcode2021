import argparse


def parse_file(filename):
    file = open(filename, "r")
    return file.readlines()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    args = parser.parse_args()

    sequence = parse_file(args.filename)

    count = 0
    for idx in range(len(sequence)-3):
        sum1 =  int(sequence[idx]) + int(sequence[idx+1]) + int(sequence[idx+2])
        sum2 =  int(sequence[idx+1]) + int(sequence[idx+2]) + int(sequence[idx+3])
        if idx != 0 and sum2 > sum1:
            count = count + 1

    print("The count is:", count)