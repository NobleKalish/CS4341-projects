# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group17')
from group17character import Group17Character

# Create the game
g = Game.fromfile('../scenario2/map.txt')

# TODO Add your character
g.add_character(Group17Character("me",  # name
                                 "C",  # avatar
                                 0, 0,  # position
                                 1
                                 ))

# Run!
g.go(100)
