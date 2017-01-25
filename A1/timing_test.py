import time
import astar as astar
from grid import Grid
from pose import Pose

current_milli_time = lambda: int(round(time.time() * 1000))

num_trials = 5

sizes = [10, 15, 20, 25, 30, 35, 40, 45, 50]


for size in sizes:

    total_time = 0.0
    grid = Grid.create_new_grid(size, size)

    for i in range(num_trials):

        start_time = current_milli_time()

        goal_pose = astar.Astar(grid.get_start_cell(), grid.get_goal_cell(), grid, 5)

        end_time = current_milli_time()

        total_time += end_time - start_time

    average_time = float(total_time) / float(num_trials)

    print(str(size) + 'x' + str(size) + ' grid: ' + str(average_time))
