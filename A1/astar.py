"""
WPI CS4341 C-2017
Project 1

Arthur Lockman
Tucker Haydon
John Lomi
John Sawin
"""
import sys


def main():
    """
    The main project function.
    :return: none
    """
    # If we don't have all of the params, exit and print help.
    if len(sys.argv) < 3:
        print('Usage: astar.py [filename] [heurstic value (1-6)]')
        print('       filename: should be the name or path to a map file to load')
        print('       heurstic: can be one of the following:')
        print('           1: 0 heuristic')
        print('           2: Min(vertical, horizontal)')
        print('           3: Max(vertical, horizontal)')
        print('           4: Vertical + horizontal')
        print('           5: Better admissable heuristic')
        print('           6: Non-admissible heuristic')
        # TODO: fix this documentation once we have the right heuristics
        exit()

    astar_map = load_map(sys.argv[1])
    print(astar_map)


def load_map(filename):
    """
    Load a map from a file on disk.
    :param filename: The name of the file on disk to load.
    :return: A map constructed from the input file.
    """
    return Map.read_from_file(filename)


if __name__ == '__main__':
    main()
