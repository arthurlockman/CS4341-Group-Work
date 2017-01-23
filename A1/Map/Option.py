import math
import Map

class Option():

	def __init__(self, _map, start_position):
		self.map = _map
		self.start_position = start_position

	def get_cost(self):
		return self.cost

	def get_start_position(self):
		return self.start_position

	def get_end_position(self):
		return self.end_position

	def get_end_direction(self):
		return self.end_direction

	def within_map_bounds(self, row, col):
		num_rows = len(self.map)
		num_cols = len(self.map[0])

		return row >= 0 and col >= 0 and row < num_rows and col < num_cols


class Forward(Option):

	def __init__(self, _map, start_position, start_direction):
		super().__init__(_map, start_position)

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

		if self.within_map_bounds(new_row, new_col):
			self.cost = self.map[new_row][new_col]
		else:
			self.cost = math.inf

class ClockwiseTurn(Option):

	def __init__(self, _map, start_position, start_direction):
		super().__init__(_map, start_position)

		# Does not move anywhere
		self.end_position = start_position

		# Cost is equal to one third of the position cost
		self.cost = math.ceil(self.map[start_position[0]][start_position[1]] / 3.0)

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

	def __init__(self, _map, start_position, start_direction):
		super().__init__(_map, start_position)

		# Does not move anywhere
		self.end_position = start_position

		# Cost is equal to one third of the position cost
		self.cost = math.ceil(self.map[start_position[0]][start_position[1]] / 3.0)

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

	def __init__(self, _map, start_position, start_direction):
		super().__init__(_map, start_position)

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

		if self.within_map_bounds(new_row, new_col):
			# Constant cost
			self.cost = 20
		else:
			self.cost = math.inf

# m = Map.Map.read_from_file('map.txt').get_map()
# f = Forward(Map.Map.read_from_file('map.txt').get_map(), (0, 0), 'SOUTH')
		