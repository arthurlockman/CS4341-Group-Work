"""
WPI CS4341 C-2017
Project 1

Arthur Lockman
Tucker Haydon
John Lomi
Jon Sawin
"""
import sys
from grid.grid import Grid
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

    filename = sys.argv[1]
    heuristic = sys.argv[2]

    grid = load_grid(filename)
    goal_pose = Astar(grid.get_start_cell(), grid.get_goal_position(), grid, heuristic)

    # path = get_path(goal_pose)
    # print_path(path)


def load_grid(filename):
    """
    Load a grid from a file on disk.
    :param filename: The name of the file on disk to load.
    :return: A grid constructed from the input file.
    """
    return Grid.read_from_file(filename)


def Astar(start_cell, goal_cell, grid, heuristic):
    #initialize queue
    start_pose = Pose(start_cell, 'NORTH', heuristic)

    #put start on Queue
    pose_list = [start_pose]

    #find goal
    while pose_list.len() > 0:
        sorted(pose_list, key=lambda Pose: Pose.get_f_val())
        elt = pose_list.pop()

        if elt[0] == goal_cell:
            return elt
        else:
            pose_list.append(option.expand_node(grid, elt))


if __name__ == '__main__':
    main()
