from Field import Field
from math import floor

class Sudoku:

    def __init__(self, filename):
        self.board: set[Field] = self.read_sudoku(filename)

    def __str__(self):
        output = "╔═══════╦═══════╦═══════╗\n"
        # iterate through rows
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"
            output += "║ "
            # iterate through columns
            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "
            output += "║\n"
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    @staticmethod
    def read_sudoku(filename):
        """
        Read in a sudoku file
        @param filename: Sudoku filename
        @return: A 9x9 grid of Fields where each field is initialized with all its neighbor fields
        """
        assert filename is not None and filename != "", "Invalid filename"
        # Setup 9x9 grid
        grid = [[Field for _ in range(9)] for _ in range(9)]

        try:
            with open(filename, "r") as file:
                for row, line in enumerate(file):
                    for col_index, char in enumerate(line):
                        if char == '\n':
                            continue
                        if int(char) == 0:
                            grid[row][col_index] = Field()
                        else:
                            grid[row][col_index] = Field(int(char))

                        grid[row][col_index].row = row
                        grid[row][col_index].col = col_index

        except FileNotFoundError:
            print("Error opening file: " + filename)

        Sudoku.add_neighbours(grid)
        return grid

    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field
        @param grid: 9x9 list of Fields
        """
        # TODO: for each field, add its neighbors
        
        for row in range(9):
            for col in range(9):
                neighbours = set()
                domain = [n for n in range(1, 10)]

                subgrid_row = floor(row / 3) * 3
                subgrid_column = floor(col / 3) * 3
                for r in range(subgrid_row, subgrid_row + 3):
                    for c in range(subgrid_column, subgrid_column + 3):
                        if (r, c) != (row, col):
                            if (grid[r][c].value == 0):
                                neighbours.add(grid[r][c])
                            
                            try:
                                domain.remove(grid[r][c].value)
                            except:
                                pass

                for neighbour_row in range(9):
                    if neighbour_row != row:
                        if (grid[r][c].value == 0):
                            neighbours.add(grid[neighbour_row][col])
                        try:
                            domain.remove(grid[neighbour_row][col].value)
                        except:
                            pass

                for neighbour_column in range(9):
                    if neighbour_column != col:
                        if (grid[r][c].value == 0):
                            neighbours.add(grid[row][neighbour_column])
                        try:
                            domain.remove(grid[row][neighbour_column].value)
                        except:
                            pass

                grid[row][col].set_neighbours(neighbours)
                grid[row][col].domain = domain

        pass

    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board