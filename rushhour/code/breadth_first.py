from structure import Structure

class Breadth(Structure):
    def __init__(self, game: str, dim: int) -> None:
        super().__init__(game, dim)

        # the queue will consist of (vector, solution pairs)
        self.queue = [(self.initial_vector, [])]
        self.visited_states = {self.initial_vector}
        self.current_solution = []
    
    def run(self):
        # possible_moves = self.possible_moves()
        # print(possible_moves)
        solution = []

        while not self.win():
        # while len(solution) < 10:
            # load next from queue
            # print(self.queue)
            vector, solution = self.queue.pop(0)
            self.set_vector(vector, solution)
            # print(self)
            # print(self.board)
            # print(solution)
            # if solution == [("A", "L"), ("A", "R")]:
            #     print(vector)
            #     print(self.initial_vector)

            # perform all possible moves
            possible_moves = self.possible_moves()
            # print(possible_moves)
            for move in possible_moves:
                # reset board
                self.set_vector(vector, solution)

                # perform the move
                self.move_car(move)
                self.current_solution.append(move)

                # check win
                if self.win():
                    return self.current_solution
                
                # if a vector already exists, don't add it to queue
                if not self.current_vector in self.visited_states:
                    # else, add the new solution to the queue and the vector to the visited states
                    self.visited_states.add(self.current_vector)
                    self.queue.append((self.current_vector, self.current_solution.copy()))
            

    def set_vector(self, vector, solution):
        car_positions = vector.split("_")

        assert len(car_positions) == len(self.cars)

        for car_position in car_positions:
            name, cur_pos = car_position.split(".")
            car = self.cars[name]
            car.current = int(cur_pos)

        self.current_solution = solution.copy()

        self.set_board()
        # print(self.board)

    def play_solution(self, solution):
        pass