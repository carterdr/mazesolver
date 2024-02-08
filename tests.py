import unittest
from window import Maze, Point
from window import Window
from window import Cell
class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 4
        num_rows = 4
        m1 = Maze(20, 20, num_rows, num_cols, 50, 50, Window(800, 800))
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )
    def test_maze_entr_exit(self):
        cell = Cell(Window(400, 40), Point(10, 10), Point(100, 100))
        cell.delete_walls()
        self.assertFalse(cell.has_bottom_wall or cell.has_left_wall or cell.has_top_wall or cell.has_right_wall)
    def test_reset_cells(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(20, 20, num_rows, num_cols, 50, 50, Window(400, 400))
        m1._reset_cells_visited()
        for row in m1._cells:
            for cell in row:
                self.assertFalse(cell.visited)
if __name__ == "__main__":
    unittest.main()