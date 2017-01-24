import math
from .grid import Grid
from .pose import Pose

def expand_node(grid, pose):
	options = get_options(grid, pose)
	child_poses = []

	for opt in options:
		child_poses.append(Pose(grid.get_cell(*opt.get_end_position()), opt.get_end_direction(), pose.get_heuristic()))

	return child_poses



def get_options(grid, pose):

	position = pose.get_position()
	direction = pose.get_direction()

	return [
		Forward(grid, position, direction),
		ClockwiseTurn(grid, position, direction),
		CounterclockwiseTurn(grid, position, direction),
		Leap(grid, position, direction)
	]


class Option():

	def __init__(self, grid, start_position):
		self.grid = grid
		self.start_position = start_position

	def get_cost(self):
		return self.cost

	def get_start_position(self):
		return self.start_position

	def get_end_position(self):
		return self.end_position

	def get_end_direction(self):
		return self.end_direction

	def within_grid_bounds(self, row, col):
		num_rows = len(self.grid.get_grid())
		num_cols = len(self.grid.get_grid()[0])

		return row >= 0 and col >= 0 and row < num_rows and col < num_cols


class Forward(Option):

	def __init__(self, grid, start_position, start_direction):
		super().__init__(grid, start_position)

		# Still facing same direction
		self.end_direction = start_direction

		current_row = start_position[0]
		current_col = start_position[1]

		if start_direction == 'NORTH':
			new_row = current_row - 1
			new_col = current_col
		elif start_direction == 'EAST':
			new_row = current_row
			new_col = current_col + 1
		elif start_direction == 'WEST':
			new_row = current_row
			new_col = current_col - 1
		elif start_direction == 'SOUTH':
			new_row = current_row + 1
			new_col = current_col
		else:
			print('ERROR: Direction unacceptable: ' + start_direction)

		self.end_position = (new_row, new_col)

		if self.within_grid_bounds(new_row, new_col):
			self.cost = self.grid.get_cell(new_row, new_col).get_cell_cost()
		else:
			self.cost = math.inf

class ClockwiseTurn(Option):

	def __init__(self, grid, start_position, start_direction):
		super().__init__(grid, start_position)

		# Does not move anywhere
		self.end_position = start_position

		# Cost is equal to one third of the position cost
		self.cost = math.ceil(self.grid.get_cell(start_position[0], start_position[1]).get_cell_cost() / 3.0)

		if start_direction == 'NORTH':
			self.end_direction = 'EAST'
		elif start_direction == 'EAST':
			self.end_direction = 'SOUTH'
		elif start_direction == 'WEST':
			self.end_direction = 'NORTH'
		elif start_direction == 'SOUTH':
			self.end_direction = 'WEST'
		else:
			print('ERROR: Direction unacceptable: ' + start_direction)

class CounterclockwiseTurn(Option):

	def __init__(self, grid, start_position, start_direction):
		super().__init__(grid, start_position)

		# Does not move anywhere
		self.end_position = start_position

		# Cost is equal to one third of the position cost
		self.cost = math.ceil(self.grid.get_cell(start_position[0], start_position[1]).get_cell_cost() / 3.0)

		if start_direction == 'NORTH':
			self.end_direction = 'WEST'
		elif start_direction == 'EAST':
			self.end_direction = 'NORTH'
		elif start_direction == 'WEST':
			self.end_direction = 'SOUTH'
		elif start_direction == 'SOUTH':
			self.end_direction = 'EAST'
		else:
			print('ERROR: Direction unacceptable: ' + start_direction)

class Leap(Option):

	def __init__(self, grid, start_position, start_direction):
		super().__init__(grid, start_position)

		# Still facing same direction
		self.end_direction = start_direction

		current_row = start_position[0]
		current_col = start_position[1]

		if start_direction == 'NORTH':
			new_row = current_row - 3
			new_col = current_col
		elif start_direction == 'EAST':
			new_row = current_row
			new_col = current_col + 3
		elif start_direction == 'WEST':
			new_row = current_row
			new_col = current_col - 3
		elif start_direction == 'SOUTH':
			new_row = current_row + 3
			new_col = current_col
		else:
			print('ERROR: Direction unacceptable: ' + start_direction)

		self.end_position = (new_row, new_col)

		if self.within_grid_bounds(new_row, new_col):
			# Constant cost
			self.cost = 20
		else:
			self.cost = math.inf



# UNIT TESTS
g = Grid.read_from_file('./grid/test_grid.txt')
start_cell = g.get_start_cell()
goal_cell = g.get_goal_cell()

# Test basic forward
f = Forward(g, (0, 0), 'SOUTH')
assert (f.end_direction == 'SOUTH')
assert (f.end_position == (1, 0))
assert (f.cost == 3)

# Test forward off map. Infinite cost
f = Forward(g, (0, 0), 'NORTH')
assert (f.end_direction == 'NORTH')
assert (f.end_position == (-1, 0))
assert (f.cost == math.inf)

# Test clockwise turn
t = ClockwiseTurn(g, (0, 0), 'NORTH')
assert (t.end_direction == 'EAST')
assert (t.end_position == (0, 0))
assert (t.cost == 1.0)

# Test counterclockwise turn
t = CounterclockwiseTurn(g, (0, 0), 'NORTH')
assert (t.end_direction == 'WEST')
assert (t.end_position == (0, 0))
assert (t.cost == 1.0)

# Test leap right
l = Leap(g, (0, 0), 'EAST')
assert (l.end_direction == 'EAST')
assert (l.end_position == (0, 3))
assert (l.cost == 20)

# Test leap down
l = Leap(g, (0, 0), 'SOUTH')
assert (l.end_direction == 'SOUTH')
assert (l.end_position == (3, 0))
assert (l.cost == 20)

# Test leap unacceptable
l = Leap(g, (0, 0), 'NORTH')
assert (l.end_direction == 'NORTH')
assert (l.end_position == (-3, 0))
assert (l.cost == math.inf)

# Test get options
options = get_options(g, Pose(start_cell, 'NORTH', 1))
assert (len(options) == 4)
assert (options[0].get_cost() == 3)
assert (options[1].get_cost() == 1)
assert (options[2].get_cost() == 1)
assert (options[3].get_cost() == 20)

# Test expand_node
child_poses = expand_node(g, Pose(start_cell, 'EAST', 1))
assert (len(child_poses) == 4)
assert (child_poses[0].get_position() == (9, 5))
assert (child_poses[0].get_direction() == 'EAST')

assert (child_poses[1].get_position() == (9, 4))
assert (child_poses[1].get_direction() == 'SOUTH')

assert (child_poses[2].get_position() == (9, 4))
assert (child_poses[2].get_direction() == 'NORTH')

assert (child_poses[3].get_position() == (9, 7))
assert (child_poses[3].get_direction() == 'EAST')




