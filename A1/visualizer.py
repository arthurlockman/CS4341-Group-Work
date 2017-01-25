from tkinter import *
from grid import Grid

class Visualizer:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.master = Tk()

        self.canvas = Canvas(self.master, width=width, height=height)
        self.canvas.pack()

    def visualize_grid(self, grid, frontier, goal_cell):

        num_rows = len(grid.get_grid())
        num_cols = len(grid.get_grid()[0])

        square_width = self.width / num_cols
        square_height = self.height / num_rows

        self.canvas.delete(ALL)

        for row in range(num_rows):
            for col in range(num_cols):

                upper_left_x = 0 + col * square_width
                upper_left_y = 0 + row * square_height

                if grid.get_cell(row, col).is_explored('NORTH') or grid.get_cell(row, col).is_explored('SOUTH') or grid.get_cell(row, col).is_explored('EAST') or grid.get_cell(row, col).is_explored('WEST'):
                    self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="black")
                else:
                    self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="white")
                    self.canvas.create_text(upper_left_x, upper_left_y, anchor=NW, text=grid.get_grid()[row][col].write_to_string())

        for pose in frontier:
            cell = pose.get_gridcell()
            upper_left_x = cell.get_col() * square_width
            upper_left_y = cell.get_row() * square_height
            self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="yellow")

        upper_left_x = goal_cell.get_col() * square_width
        upper_left_y = goal_cell.get_row() * square_height
        self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="green")
                


        self.master.update_idletasks()
        self.master.update()
