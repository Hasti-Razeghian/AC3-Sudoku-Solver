import os
from Game import Game
from Sudoku import Sudoku

sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")

class App:


    @staticmethod
    def solve_sudoku(sudoku_file):
        game = Game(Sudoku(sudoku_file))
        game.show_sudoku()

        try:
            # Convert the input to an integer
            heuristic_ind = int(input("0 = Default\n"
                        "1 = MRV\n"
                        "2 = FF\n"
                        "Enter heuristic: "))
            
            # Check if the number is within the range
            if not 0 <= heuristic_ind <= 2:
                print("Input is not between 0 and 2.")
                return
            
        except ValueError:
            print("Invalid input!")
            return

        if (game.solve(int(heuristic_ind)) and game.valid_solution()):
            print("Arc consistent solution found! Updated fields:")
            game.show_sudoku()
        else:
            print("Could not solve this sudoku :'(")

    @staticmethod
    def start():
        while True:
            file_num = input("Enter Sudoku file (1-5): ")
            print("\n")

            file = None
            for filename in os.listdir(sudoku_folder):
                if file_num in filename:
                    file = filename
            if file is not None:
                App.solve_sudoku(os.path.join(sudoku_folder, file))
            else:
                print("Invalid choice")

            continue_input = input("Continue? (yes/no): ")
            if continue_input.lower() != 'yes':
                break


if __name__ == "__main__":
    App.start()

