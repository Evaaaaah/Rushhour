
from structure import Structure

import numpy as np
import os

class Random(Structure):
    def __init__(self, game: str, dim: int) -> None:
        super().__init__(game, dim)

    def run(self):
        self.current_solution = []

        while not self.win():
            # print(self.board)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self)

            # possible moves
            moves = self.possible_moves()
            print(moves)

            # pick random
            index = np.random.randint(len(moves))
            to_move = moves[index]
            print(to_move)

            # update board
            self.move_car(to_move)

            self.current_solution.append(to_move)

        return self.current_solution

if __name__ == "__main__":
    algorithm = Random(game, dim)
    solution = algorithm.run()
    print(len(solution))