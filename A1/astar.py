"""
WPI CS4341 C-2017
Project 1

Arthur Lockman
Tucker Haydon
John Lomi
Jon Sawin
"""

import sys
import option as opt
from grid import Grid
from pose import Pose
from visualizer import Visualizer


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
    heuristic = int(sys.argv[2])

    grid = load_grid(filename)
    goal_pose, node_count = Astar(grid.get_start_cell(), grid.get_goal_cell(), grid, heuristic)

    path = get_path(goal_pose)
    print('Score: ', sum(i.get_g_val() for i in path))
    print('Number of actions: ', len(path))
    print('Number of nodes expanded:', node_count)
    # Estimating branching factor to be  N^(1/d)
    print('Branching factor: ', float(node_count) ** (1.0 / len(path)))
    print('\nActions and path: ')
    print('\n'.join(v.str_with_move() for v in path))


def load_grid(filename):
    """
    Load a grid from a file on disk.
    :param filename: The name of the file on disk to load.
    :return: A grid constructed from the input file.
    """
    return Grid.read_from_file(filename)


def Astar(start_cell, goal_cell, grid, heuristic):

    visualize = len(sys.argv) > 3 and sys.argv[3] == '-v'

    # Initialize queue
    start_pose = Pose(start_cell, 'NORTH', heuristic)
    start_pose.parent_move = 'Start'

    # Put start on Queue
    frontier = [start_pose]

    # Count number of nodes expanded
    node_count = 1

    # Visualizer
    if visualize == True:
        vis = Visualizer(1200, 900)

    # Find goal
    while len(frontier) > 0:
        frontier.sort(key=lambda pose: pose.get_f_val())
        lowest_cost_node = frontier.pop(0)

        if lowest_cost_node.get_gridcell() == goal_cell:
            break
        else:
            _tmp = opt.expand_node(grid, lowest_cost_node)
            node_count += len(_tmp)
            frontier.extend(_tmp)

        # if visualize == True:
        #     vis.visualize_grid(grid, frontier, goal_cell)

    if visualize == True: 
        vis.visualize_solution(grid, lowest_cost_node)

    input()

    return lowest_cost_node, node_count



def get_path(pose):
    """
    Get a path from an ending pose.
    :param pose: The pose (result of A*)
    :return: A list of poses, the path
    """
    path = []
    p = pose
    while p.get_parent() is not None:
        path.append(p)
        p = p.get_parent()
    path.append(p)
    path.reverse()
    return path

if __name__ == '__main__':
    main()
