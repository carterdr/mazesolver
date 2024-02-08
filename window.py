import random
import time
from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Tikle"
        self.__canvas = Canvas(self.__root, width = width, height = height)
        self.__canvas.pack()
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    def wait_for_close(self):
        self.__window_running = True
        while (self.__window_running):
            self.redraw()
    def close(self):
        self.__window_running = False
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Line:
    def __init__(self, p1, p2):
        self.x1 = p1.x
        self.y1 = p1.y
        self.x2 = p2.x
        self.y2 = p2.y
    def draw(self, canvas, fill_color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill = fill_color, width = 2)
        canvas.pack()
class Cell:
    def __init__(self, window, p1, p2, lw = True, rw = True, tw = True, bw = True):
        self.has_left_wall = lw
        self.has_right_wall = rw
        self.has_top_wall = tw
        self.has_bottom_wall = bw
        self._x1 = p1.x
        self._x2 = p2.x
        self._y1 = p1.y
        self._y2 = p2.y 
        self._win = window
        self.visited = False
    def draw(self):
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "#ffffff")
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "#ffffff")
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "#ffffff")
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "#ffffff")
    def delete_walls(self):
        self.has_left_wall = False
        self.has_right_wall = False
        self.has_bottom_wall = False
        self.has_top_wall = False
    def draw_move(self, to_cell, undo = False):
        center1 = self.getCenter()
        center2 = to_cell.getCenter()
        self._win.draw_line(Line(center1, center2), "gray" if undo else "red")
    def getCenter(self):
        return Point((self._x2 - self._x1)/2 + self._x1, (self._y2 - self._y1)/2 + self._y1)
class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win, seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        self._cells = [[None for j in range(self.num_cols)] for i in range(self.num_rows)]  
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell = Cell(self.win, Point(self.x1 + j * self.cell_size_x, self.y1 + i * self.cell_size_y), Point(self.x1 + (j + 1) * self.cell_size_x, self.y1 + (i + 1) * self.cell_size_y))
                self._cells[i][j] = cell
                cell.draw()
                self._animate()
    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)
    def _break_entrance_and_exit(self):
        self._cells[0][0].delete_walls()
        self._cells[0][0].draw()
        self._cells[-1][-1].delete_walls()
        self._cells[-1][-1].draw()
    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            neighbors = []
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:
                neighbors.append(((1, 0), self._cells[i + 1][j]))
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:
                neighbors.append(((0, 1), self._cells[i][j + 1]))
            if j >= 1 and not self._cells[i][j - 1].visited:
                neighbors.append(((0, -1), self._cells[i][j - 1]))
            if i >= 1 and not self._cells[i - 1][j].visited:
                neighbors.append(((-1, 0), self._cells[i - 1][j]))
            if len(neighbors) == 0:
                current_cell.draw()
                return
            else:
                direction = random.randint(0, len(neighbors)-1)
                nextCell = neighbors[direction][1]
                eraseDirection = neighbors[direction][0]
                if eraseDirection == (0, 1):
                    nextCell.has_left_wall = False
                    current_cell.has_right_wall = False
                elif eraseDirection == (-1, 0):
                    nextCell.has_bottom_wall = False
                    current_cell.has_top_wall = False
                elif eraseDirection == (1, 0):
                    nextCell.has_top_wall = False
                    current_cell.has_bottom_wall = False
                else:
                    nextCell.has_right_wall = False
                    current_cell.has_left_wall = False
                current_cell.draw()
                nextCell.draw()
                self._break_walls_r(i + eraseDirection[0], j + eraseDirection[1])
    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
    def solve(self):
        self._solve_r(0, 0)
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if current_cell == self._cells[-1][-1]:
            return True
        for direction in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            newI = i + direction[0]
            newJ = j + direction[1]
            if 0 <= newI < self.num_rows and 0 <= newJ < self.num_cols:
                nextCell = self._cells[newI][newJ]
                if nextCell.visited:
                    continue
                if direction == (0, 1):
                    if nextCell.has_left_wall or current_cell.has_right_wall:
                        continue
                elif direction == (-1, 0):
                    if nextCell.has_bottom_wall or current_cell.has_top_wall:
                        continue
                elif direction == (1, 0):
                    if nextCell.has_top_wall or current_cell.has_bottom_wall:
                        continue
                else:
                    if nextCell.has_right_wall or  current_cell.has_left_wall:
                        continue
                current_cell.draw_move(nextCell)
                if self._solve_r(newI, newJ):
                    return True
                current_cell.draw_move(nextCell, True)
                
        return False
                    
