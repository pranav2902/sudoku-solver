import numpy as np


class SudokuBoard:
    """
    Methods dealing with sudoku board. Add more derived classes with
    constraints for other variants/sizes later.
    """

    def __init__(self, arr: np.array(int)):
        self.values_numpy = arr
        self.rows = [arr[i, :] for i in range(9)]
        self.cols = [arr[:, i] for i in range(9)]
        self.boxes = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                self.boxes.append(
                    self.values_numpy[i : i + 3, j : j + 3].reshape(1, 9).flatten()
                )
        self.pencil_marks = np.empty((9, 9), dtype=list)
        self.init_pencil_marks()
        self.update_pencil_marks()

    def init_pencil_marks(self):
        for (i, j), val in np.ndenumerate(self.values_numpy):
            self.pencil_marks[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9] if val == 0 else []

    def add_number_to_board(self, number: int, pos: list[int]) -> bool:
        i, j = pos
        self.values_numpy[i : i + 1, j : j + 1] = number
        self.update_boxes()
        self.update_pencil_marks()
        return self.is_valid_sudoku()

    def update_boxes(self):
        boxes = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                boxes.append(
                    self.values_numpy[i : i + 3, j : j + 3].reshape(1, 9).flatten()
                )
        self.boxes = boxes

    def return_box(self, pos: list[int]):
        x, y = pos
        box_index = (x // 3) * 3 + (y // 3)
        return self.get_indices_of_box(box_index), self.boxes[box_index]

    @staticmethod
    def get_indices_of_box(box_index):
        start_row = (box_index // 3) * 3
        start_col = (box_index % 3) * 3
        indices = [
            [row, col]
            for row in range(start_row, start_row + 3)
            for col in range(start_col, start_col + 3)
        ]

        return indices

    def update_pencil_marks(self):
        for (i, j), val in np.ndenumerate(self.values_numpy):
            if val != 0:
                self.pencil_marks[i][j] = []
            else:
                indices_of_box, box_vals = self.return_box([i, j])
                box_vals_wo_cell = np.delete(box_vals, indices_of_box.index([i, j]))
                row_vals_wo_cell = np.delete(self.rows[i], j)
                col_vals_wo_cell = np.delete(self.cols[j], i)

                union_vals = np.array(
                    list(
                        set(box_vals_wo_cell)
                        | set(row_vals_wo_cell)
                        | set(col_vals_wo_cell)
                    )
                )
                self.pencil_marks[i][j] = np.setdiff1d(
                    self.pencil_marks[i][j], union_vals
                )

    def remove_pos_from_board(self, pos: list[int]):
        i, j = pos
        self.values_numpy[i : i + 1, j : j + 1] = 0

    def is_valid_sudoku(self):
        if not all(
            [self._row_check(), self._col_check(), self._box_check()]
        ):  # Add box check
            return False
        return True

    def _row_check(self) -> bool:
        for row in self.values_numpy:
            non_zero_locs = np.where(row != 0)
            non_zero_vals = list(set(row[non_zero_locs]))
            # print(non_zero_vals, non_zero_locs)
            if len(non_zero_vals) != len(list(self.values_numpy[non_zero_locs])):
                return False

        return True

    def _col_check(self) -> bool:
        for row in self.values_numpy.T:
            non_zero_locs = np.where(row != 0)
            non_zero_vals = list(set(row[non_zero_locs]))
            # print(non_zero_vals, non_zero_locs)
            if len(non_zero_vals) != len(list(self.values_numpy.T[non_zero_locs])):
                return False

        return True

    def _box_check(self) -> bool:
        for box in self.boxes:
            non_zero_locs = np.where(box != 0)
            non_zero_vals = list(set(box[non_zero_locs]))
            # print(non_zero_vals, non_zero_locs)
            if len(non_zero_vals) != len(list(box[non_zero_locs])):
                return False

        return True

    def find_next_empty_cell(self):
        print("No singleton cell found, finding next empty cell\n")
        indices = np.argwhere(self.values_numpy == 0)
        return indices[0] if len(indices) else [-1, -1]

    def find_singleton_cell(self):
        indices = np.argwhere(
            [[len(lst) == 1 for lst in row] for row in self.pencil_marks]
        )
        if len(indices):
            print(f"singleton cell found at {indices[0]}\n")
        return indices[0] if len(indices) else self.find_next_empty_cell()

    def save_board_state(self):
        return SudokuBoard(np.ndarray.copy(self.values_numpy))

    @staticmethod
    def vis_board(arr: np.array(int)):
        for row in arr:
            buffer = ""
            for item in row:
                if item == 0:
                    buffer += "- "
                else:
                    buffer += f"{item} "
            print(f"{buffer}")
        print()
