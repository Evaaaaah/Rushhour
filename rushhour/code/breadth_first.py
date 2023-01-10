from structure import Structure
from typing import List, Tuple

class Breadth(Structure):
    def __init__(self, game: str, dim: int) -> None:
        super().__init__(game, dim)

        # the queue will consist of (vector, solution pairs)
        self.queue = [(self.initial_vector, [])]
        self.visited_states = {self.initial_vector}
        self.current_solution = []
    
    def run(self) -> List[Tuple[str]]:
        """Run the breadth first algorithm.
        It will keep running untill a solution is found.

        Returns:
            List[Tuple[str]]: The solution to the puzzle.
        """
        solution = []

        while not self.win():
            # load next from queue
            vector, solution = self.queue.pop(0)
            self.set_vector(vector, solution)

            # perform all possible moves
            possible_moves = self.possible_moves()

            for move in possible_moves:
                # reset board
                self.set_vector(vector, solution)

                # perform the move
                self.move_car(move)
                self.current_solution.append(move)

                # check win
                if self.win():
                    return self.current_solution
                
                # if a vector does not already exists, 
                # add the new solution to the queue and the vector to the visited states
                if not self.current_vector in self.visited_states:
                    self.visited_states.add(self.current_vector)
                    self.queue.append((self.current_vector, self.current_solution.copy()))
        
        return self.current_solution

    def set_vector(self, vector: str, solution: List[Tuple[str]]):
        """Set the state of the board with a vector and a solution to this vector.
        Note: it is not checked whether this solution leads to this state of the board.

        Args:
            vector (str): The state of the board. Should be formatted as:
                {car1_name}.{car1_position}_{car2_name}.{car2_position}
            solution (List[Tuple[str]]): The solution up to this point.
        """
        car_positions = vector.split("_")

        assert len(car_positions) == len(self.cars)

        for car_position in car_positions:
            name, cur_pos = car_position.split(".")
            car = self.cars[name]
            car.current = int(cur_pos)

        self.current_solution = solution.copy()

        self.set_board()
