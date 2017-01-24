"""
WPI CS4341 C-2017
Project 1

Arthur Lockman
Tucker Haydon
John Lomi
Jon Sawin
"""
import sys
from grid import Grid
from pose import Pose
import option


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
    print(astar_map.get_map())
    goalPose = Astar(astar_map.start_pos, astar_map.goal_pos, astar_map, sys.argv[2])
    path = getPath(goalPose)
    printPath(path)


def load_map(filename):
    """
    Load a map from a file on disk.
    :param filename: The name of the file on disk to load.
    :return: A map constructed from the input file.
    """
    return Grid.read_from_file(filename)


def Astar(start, goal, map , heuristic):
    #initialize queue
    startPose = Pose(start, 'N', heuristic)

    #put start on Queue
    poseList = [startPose]

    #find goal
    while poseList.len() > 0:
        sorted(poseList, key=lambda Pose: Pose.get_f_val())
        elt = poseList.pop()

        if elt[0] == goal:
            return elt
        else:
            poseList.append(option.expand_node(map, elt))


if __name__ == '__main__':
    main()
