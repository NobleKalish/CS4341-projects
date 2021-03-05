# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from bomberman.game import Game
from bomberman.monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../group17')
from group17.group17character import Group17Character

# Create the game
# random.seed(123)  # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("selfpreserving",  # name
                                    "S",  # avatar
                                    3, 9,  # position
                                    1  # detection range
                                    ))

# TODO Add your character
g.add_character(Group17Character("me",  # name
                                 "C",  # avatar
                                 0, 0,  # position
                                 3  # variant
                                 ))

# Run!
g.go(1000)