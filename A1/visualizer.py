from tkinter import *
from grid import Grid

class Visualizer:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.master = Tk()

        self.canvas = Canvas(self.master, width=width, height=height)
        self.canvas.pack()

    def visualize_solution(self, grid, final_pose):

        num_rows = len(grid.get_grid())
        num_cols = len(grid.get_grid()[0])

        square_width = self.width / num_cols
        square_height = self.height / num_rows

        # Clear canvas
        self.canvas.delete(ALL)
        
        # Draw grid
        for row in range(num_rows):
            for col in range(num_cols):
                upper_left_x = 0 + col * square_width
                upper_left_y = 0 + row * square_height
                self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="white")
                self.canvas.create_text(upper_left_x, upper_left_y, anchor=NW, text=grid.get_grid()[row][col].write_to_string())

        self.draw_path_square(grid, final_pose, square_width, square_height)

    def draw_path_square(self, grid, pose, square_width, square_height):
        if pose is None:
            return
        else:
            row = pose.get_gridcell().get_row()
            col = pose.get_gridcell().get_col()

            upper_left_x = 0 + col * square_width
            upper_left_y = 0 + row * square_height

            self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="green")
            self.canvas.create_text(upper_left_x, upper_left_y, anchor=NW, text=grid.get_grid()[row][col].write_to_string())

            self.draw_path_square(grid, pose.get_parent(), square_width, square_height)


    def visualize_grid(self, grid, frontier, goal_cell):

        num_rows = len(grid.get_grid())
        num_cols = len(grid.get_grid()[0])

        square_width = self.width / num_cols
        square_height = self.height / num_rows

        self.canvas.delete(ALL)

        # Draw expanded nodes
        for row in range(num_rows):
            for col in range(num_cols):
                upper_left_x = 0 + col * square_width
                upper_left_y = 0 + row * square_height

                if grid.get_cell(row, col).is_explored('NORTH') or grid.get_cell(row, col).is_explored('SOUTH') or grid.get_cell(row, col).is_explored('EAST') or grid.get_cell(row, col).is_explored('WEST'):
                    self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="red")
                else:
                    self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="white")

                self.canvas.create_text(upper_left_x, upper_left_y, anchor=NW, text=grid.get_grid()[row][col].write_to_string())

         # Draw frontier
        for pose in frontier:
            cell = pose.get_gridcell()
            row = cell.get_row()
            col = cell.get_col()
            upper_left_x = cell.get_col() * square_width
            upper_left_y = cell.get_row() * square_height
            if not (cell.is_explored('NORTH') or cell.is_explored('SOUTH') or cell.is_explored('EAST') or cell.is_explored('WEST')):
                self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="yellow")
                self.canvas.create_text(upper_left_x, upper_left_y, anchor=NW, text=grid.get_grid()[row][col].write_to_string())



        # Drag goal
        upper_left_x = goal_cell.get_col() * square_width
        upper_left_y = goal_cell.get_row() * square_height
        self.canvas.create_rectangle(upper_left_x, upper_left_y, upper_left_x + square_width, upper_left_y + square_height, fill="green")
                


        self.master.update_idletasks()
        self.master.update()
