import argparse


def parse_file(filename):
    file = open(filename, "r")
    return file.readlines()


class SlidingWindowAlgorithm():
    def listComprehension(sequence):
        # List comprehension version
        triple_sum = lambda idx : int(sequence[idx]) + int(sequence[idx+1]) + int(sequence[idx+2])
        count = sum([1 for idx in range(len(sequence)-3) if triple_sum(idx) < triple_sum(idx+1)])
        
        print("The count with list comprehension is:", count)


    def iterativeMethod(sequence):
        # Iterative version
        count = 0
        for idx in range(len(sequence)-3):
            sum1 =  int(sequence[idx]) + int(sequence[idx+1]) + int(sequence[idx+2])
            sum2 =  int(sequence[idx+1]) + int(sequence[idx+2]) + int(sequence[idx+3])
            if sum2 > sum1:
                count = count + 1

        print("The count with for-loop iteration is:", count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, default="training_input.txt")
    parser.add_argument("-a", "--alg", type=str, default="list_comp", choices=["list_comp", "iterative"])
    args = parser.parse_args()

    sequence = parse_file(args.filename)
    
    if args.alg == "list_comp":
        SlidingWindowAlgorithm.listComprehension(sequence)
    elif args.alg == "iterative":
        SlidingWindowAlgorithm.iterativeMethod(sequence)