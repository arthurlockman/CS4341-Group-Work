
import sys


class InputParser:

    def __init__(self):
        pass

    @classmethod
    def parse_input(cls, filename):
        # Remove the filename and cast all characters to ints
        with open(filename, 'r') as f:
            file_contents = f.readlines()
            return list(map(int, file_contents[0].split()))

