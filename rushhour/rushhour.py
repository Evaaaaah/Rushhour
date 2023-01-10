import sys
sys.path.insert(0, "code")
from structure import Structure
from random_algorithm import Random
from breadth_first import Breadth

games_6 = ["gameboards/Rushhour6x6_1.csv", "gameboards/Rushhour6x6_2.csv", "gameboards/Rushhour6x6_3.csv"]
games_9 = ["gameboards/Rushhour9x9_4.csv", "gameboards/Rushhour9x9_5.csv", "gameboards/Rushhour9x9_6.csv"]
game_12 = "gameboards/Rushhour12x12_7.csv"

print("Games of 6 by 6:")
for game in games_6:
    algorithm = Breadth(game, 6)
    solution = algorithm.run()
    print(solution)

print()
print("First game of 9 by 9:")
game = games_9[0]
algorithm = Breadth(game, 9)
solution = algorithm.run()
print(solution)