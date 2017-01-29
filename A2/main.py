from input_parser import InputParser
import sys


def main():
    filename = sys.argv[1]
    run_time = sys.argv[2]
    print(InputParser.parse_input(filename))


if __name__ == '__main__':
    main()
