from main import SudokuBoard
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class Solver():

    def __init__(self, arr: np.array):
        self.board = SudokuBoard(arr)

    def solve(self):
        self.board.vis_board(arr=self.board.values_numpy)
        pos = self.board.find_next_empty_cell()
        print(pos)
        x,y = pos
        if x == -1 and y == -1:
            print("Solved board below: ")
            self.board.vis_board(arr=self.board.values_numpy)
        else:
            self.board = self.board.save_board_state()
            for i in range(1, 10):
                if not self.board.add_number_to_board(i, pos):
                    self.board.remove_pos_from_board(pos)
                    continue
                else:
                    self.solve()



if __name__ == "__main__":
    arr_med = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])

    arr_easy = np.array([
    [5, 3, 4, 6, 7, 0, 9, 0, 2],
    [0, 7, 0, 1, 9, 5, 3, 4, 0],
    [1, 9, 0, 3, 4, 2, 5, 0, 7],
    [8, 5, 9, 0, 0, 1, 4, 2, 3],
    [4, 2, 0, 8, 5, 0, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 0, 1, 5, 3, 7, 2, 0, 4],
    [0, 8, 7, 4, 1, 9, 6, 3, 0],
    [3, 0, 5, 2, 0, 0, 1, 7, 9]
])

    so = Solver(arr=arr_easy)
    so.solve()

