import csv
import numpy as np
from colored import fg, stylize

from typing import List, Tuple, Mapping

class Car():
    def __init__(self, game: "Structure", car: dict):
        self.name = car["car"]
        self.style_name = self.name
        self.orientation = car["orientation"]
        self.game = game

        # use the orientation to find which dimension is fixed
        # row and column values start from 1, not 0 in the file
        if self.orientation == "H":
            self.fixed = int(car["row"]) - 1
            self.current = int(car["col"]) - 1
        else:
            self.fixed = int(car["col"]) - 1
            self.current = int(car["row"]) - 1
        
        self.length = int(car["length"])
    
    def add_color(self, color: str):
        """Give this car a color in the representation.

        Args:
            color (str): The color given
        """
        self.style_name = stylize(self.name, fg(color))
    
    def occupied_spaces(self) -> List[Tuple[int]]:
        """Returns the spaces that this car currently occupies

        Returns:
            List[Tuple[int]]: The spaces occupied: (x, y).
        """
        if self.orientation == "H":
            return [(self.fixed, self.current + i) for i in range(self.length)]
        else:
            # if self.name == "I":
            #     print(self.current, self.fixed, self.length)
            return [(self.current + i, self.fixed) for i in range(self.length)]

    def possible_move(self, direction: str, steps: int):
        if not (direction == "U" or direction == "D" or direction == "L" or direction == "R"):
            raise ValueError(f"This is not a valid direction. Should be U, D, L or R")

        # the move should allign with the orientation
        if self.orientation == "H":
            if direction == "U" or direction == "D":
                raise ValueError(f"This car ({self.name}) can only move left or right.")
        else:
            if direction == "L" or direction == "R":
                raise ValueError(f"This car ({self.name}) can only move up or down.")

        move_possible = True
        self.game.remove_from_board(self)
        if direction == "D" or direction == "R":
            # check down or right
            self.current += steps

            for pos in self.occupied_spaces():
                # does it still fall on the board
                if self.game.on_board(pos):
                    # is the space already occupied
                    if self.game.board[pos]:
                        # the move is not possible
                        move_possible = False
                        break
            
            self.current -= steps
        else:
            # check up or left
            self.current -= steps

            for pos in self.occupied_spaces():
                # does it still fall on the board
                if self.game.on_board(pos):
                    # is the space already occupied
                    if self.game.board[pos]:
                        # the move is not possible
                        move_possible = False
                        break
            
            self.current += steps
        
        self.game.add_to_board(self)
        return move_possible

    def move(self, direction: str, steps: int):
        """Moves the car in the given direction
        
        Args:
            direction (str): U | D | L | R : the direction of the move
            steps (int): the number of steps moved
        """
        assert self.possible_move(direction, steps)
        
        # move the car and update the board
        self.game.remove_from_board(self)
        if direction == "D" or direction == "R":
            self.current += steps
        elif direction == "U" or direction == "L":
            self.current -= steps
        self.game.add_to_board(self)

    def give_possible_moves(self) -> List[Tuple[str]]:
        """Gives the list of moves that this car can perform
        given the current state of the board.

        Returns:
            List[Tuple[str]]: The list of moves that can be performed.
        """

        self.game.remove_from_board(self)
        # if self.name == "I":
        #     print("Board after I is removed:")
        #     print(self.game.board)
        current_pos = self.current

        possible_moves = []

        # check down or right

        move_possible = True
        num_moves = 0

        while move_possible:
            self.current += 1
            num_moves += 1

            for pos in self.occupied_spaces():
                # does it still fall on the board
                if not self.game.on_board(pos):
                    move_possible = False
                    break
                # is the space already occupied
                if self.game.board[pos]:
                    # the move is not possible
                    move_possible = False
                    break
            
            # add the move to the list
            if move_possible:
                if self.orientation == "H":
                    possible_moves.append((self.name, "R", num_moves))
                else:
                    possible_moves.append((self.name, "D", num_moves))

        # check up or left
        self.current = current_pos
        move_possible = True
        num_moves = 0

        while move_possible:
            self.current -= 1
            num_moves += 1

            for pos in self.occupied_spaces():
                # does it still fall on the board
                if not self.game.on_board(pos):
                    move_possible = False
                    break
                # is the space already occupied
                if self.game.board[pos]:
                    # the move is not possible
                    move_possible = False
                    break
            
            # add the move to the list
            if move_possible:
                if self.orientation == "H":
                    possible_moves.append((self.name, "L", num_moves))
                else:
                    possible_moves.append((self.name, "U", num_moves))
        
        # put the car back on the board
        self.current = current_pos
        self.game.add_to_board(self)
        
        return possible_moves

class Structure():
    def __init__(self, game: str, dim: int) -> None:
        self.cars: Mapping[str, Car] = {}
        self.dim = dim
        with open(game,'r') as data:
            for line in csv.DictReader(data):
                # print(line)
                name = line["car"]
                car = Car(self, line)
                self.cars[name] = car
        
        # x is always the red car
        self.red_car = self.cars["X"]
        self.red_car.add_color("red")

        # save the current_vector (for breadth first?)
        self.set_current_vector()
        self.initial_vector = self.current_vector

        self.set_board()

        # print(self.board)
    
    def set_board(self):
        # create a grid that keeps track of occupied spaces
        board = [[False] * self.dim] * self.dim
        self.board = np.array(board, dtype=bool)

        for name in self.cars:
            car = self.cars[name]
            for pos in car.occupied_spaces():
                self.board[pos] = True

    def on_board(self, position: Tuple[int]):
        """Check if a position is within the limits of the board.

        Args:
            position (Tuple[int]): The position

        Returns:
            bool: Whether this position is still on the board.
        """
        for direction in position:
            # print(direction)
            if direction < 0 or direction >= self.dim:
                # print(direction, self.dim)
                return False
        return True
    
    def remove_from_board(self, car: Car):
        # remove the car from the board
        for pos in car.occupied_spaces():
            self.board[pos] = False
    
    def add_to_board(self, car: Car):
        for pos in car.occupied_spaces():
            self.board[pos] = True
    
    def win(self) -> bool:
        """Checks if the game has been won.
        This happens when the red car reaches the other side.

        Returns:
            bool: True when the red car has reached the other side of the board
        """
        return self.red_car.current + self.red_car.length == self.dim

    def possible_moves(self):
        possible_moves = []
        # for each car:
        for name in self.cars:
            car = self.cars[name]
            possible_moves += car.give_possible_moves()

        # print(possible_moves)
        return possible_moves

    def move_car(self, move: Tuple[str]):
        name, direction, steps = move
        self.cars[name].move(direction, steps)
        self.set_current_vector()
    
    def set_current_vector(self):
        self.current_vector = "_".join([name + "." + str(self.cars[name].current) for name in self.cars])
        # print(self.current_vector)

    def __repr__(self) -> str:
        """Show the board in its current state.

        Returns:
            str: The board in a grid
        """
        row = ["."] * self.dim

        # make sure the representation is copies of the empty row
        representation = []
        for _ in range(self.dim):
            representation.append(row.copy())

        # add each car to the representation
        for name in self.cars:
            car = self.cars[name]
            if car.orientation == 'H':
                for i in range(car.length):
                    representation[car.fixed][car.current + i] = car.style_name
            else:
                for i in range(car.length):
                    representation[car.current + i][car.fixed] = car.style_name

        # create a grid in a string
        return str().join([str().join(row) + "\n" for row in representation])

if __name__ == "__main__":
    board = Structure(game, dim)
    vector = board.initial_vector
    # print(board.board)
    print(board)
    print(board.possible_moves())
    board.move_car(("J", "L"))
    # print(board.board)
    print(board)
    print(board.possible_moves())
    board.move_car(("I", "D"))
    # print(board.board)
    print(board)

    solution = []
    board.set_vector(vector, solution)
    print(board)