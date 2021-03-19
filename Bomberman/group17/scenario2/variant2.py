# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../group17')
from group17character import Group17Character

# Create the game
# random.seed(123)  # TODO Change this if you want different random choices
g = Game.fromfile('../scenario2/map2.txt')
g.add_monster(StupidMonster("stupid",  # name
                            "S",  # avatar
                            3, 9  # position
                            ))

# TODO Add your character
g.add_character(Group17Character("me",  # name
                                 "C",  # avatar
                                 0, 0,  # position
                                 2
                                 ))

# Run!
g.go(200)
