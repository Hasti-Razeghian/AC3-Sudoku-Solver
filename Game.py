from queue import PriorityQueue
from abc import ABC, abstractmethod

from Sudoku import Sudoku
from Field import Field

class AC3Heuristic(ABC):
    @abstractmethod
    def calculate_priority(self, field1, field2):
        pass

# Empty heuristic
class HeuristicDefault(AC3Heuristic):
    def calculate_priority(self, field1, field2):
        return 0
    
    def __str__(self):
        return "Empty heuristic"

# Minimum remaining values heuristic
class HeuristicMRV(AC3Heuristic):
    def calculate_priority(self, field1, field2):
        return min(len(field1.domain), len(field2.domain))
    
    def __str__(self):
        return "Minimum Remaining Value heuristic (MRV)"
    
# Finalized fields heuristic
class HeuristicFF(AC3Heuristic):
    def calculate_priority(self, field1, field2):
        return (len(field2.domain) == 1)
    
    def __str__(self):
        return "Finalized Fields heuristic (FF)"

class Game:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.heuristics = [HeuristicDefault(), HeuristicMRV(), HeuristicFF()]

        # Performance metrics
        self.queue_calls = 0
        self.arc_checks = 0

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self, heuristic_ind) -> bool:
        """
        Implement of AC-3 algorithm with MRV heuristic and arc prioritization.
        @return: True if a solution is found; False otherwise.
        """

        arc_queue = PriorityQueue()
        arc_set = set()

        self.queue_calls = 0
        self.arc_checks = 0

        heuristic = self.heuristics[heuristic_ind]

        open_fields = 0
        max_domain = 0

        print("\n--- Executing AC-3 using '{}' ---".format(heuristic))

        # Initialize queue with arcs between unassigned fields, prioritizing finalized fields first and MRV
        for row in self.sudoku.board:
            for field in row:
                if field.value == 0:
                    max_domain = max(len(field.domain), max_domain)
                    open_fields += 1

                    for neighbour in field.neighbours:
                        priority = heuristic.calculate_priority(field, neighbour)
                        arc = (field.row, field.col, neighbour.row, neighbour.col)
                        arc_queue.put((priority, arc))
                        arc_set.add(arc)


        print("Open fields: {}".format(open_fields))
        print("Initial arcs: {}".format(len(arc_set)))
        print("Max domain size: {}".format(max_domain))

        while not arc_queue.empty():
            _, arc = arc_queue.get()
            arc_set.remove(arc)  # Prevent duplicate arcs
            self.queue_calls += 1

            if self.revise(arc[0], arc[1], arc[2], arc[3]):
                field = self.sudoku.board[arc[0]][arc[1]]

                if len(field.domain) == 0:
                    return False

                # Add arcs involving updated field neighbors
                for neighbour in field.neighbours:
                    temp_arc = (neighbour.row, neighbour.col, field.row, field.col)
                    if temp_arc not in arc_set:
                        priority = heuristic.calculate_priority(neighbour, field)
                        arc_queue.put((priority, temp_arc))
                        arc_set.add(temp_arc)

        # Assign single-remaining values
        for row in self.sudoku.board:
            for field in row:
                if len(field.domain) == 1:
                    field.value = field.domain[0]

        print("Arc revisions: {}\nConstraint checks: {}".format(self.queue_calls, self.arc_checks))
        print("---------------------------------------------\n")

        return True

    def revise(self, f1_row, f1_col, f2_row, f2_col):
        """
        Process the arc between two fields, f1 and f2, removing values from f1's domain.
        @return: True if f1's domain was modified; False otherwise.
        """
        domain_changed = False
        f1 = self.sudoku.board[f1_row][f1_col]
        f2 = self.sudoku.board[f2_row][f2_col]

        for val1 in f1.domain[:]:  # iterate over a copy of the domain
            valid_option = False

            for val2 in f2.domain:
                self.arc_checks += 1
                if (val1 != val2): # If any valid option is found (such that val1 != val2), continue
                    valid_option = True
                    break

            # Remove value from domain if no valid option is found
            if (not valid_option):
                f1.domain.remove(val1)
                domain_changed = True

        return domain_changed

    def valid_solution(self, verbose=True) -> bool:
        """
        Checks the validity of a Sudoku solution.
        @return: True if the solution is valid; False otherwise.
        """
        for row in self.sudoku.board:
            for field in row:
                for n in field.neighbours:
                    if field.value == n.value and field.value != 0:
                        if verbose:
                            print(f"Duplicate number ({field.value}) at ({field.row + 1}, {field.col + 1}) and ({n.row + 1}, {n.col + 1})")
                        return False
        return True
