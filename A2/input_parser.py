
import sys


class InputParser:

    def __init__(self):
        pass

    @classmethod
    def parse_input(cls):
        # Remove the filename and cast all characters to ints
        return list(map(int, sys.argv[1:]))