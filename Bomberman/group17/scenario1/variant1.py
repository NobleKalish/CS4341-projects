# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from Bomberman.bomberman.game import Game

# TODO This is your code!
sys.path.insert(1, '../group17')

# Uncomment this if you want the empty test character
from Bomberman.group17.group17character import Group17Character

# Uncomment this if you want the interactive character
# from interactivecharacter import InteractiveCharacter

# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character

# Uncomment this if you want the test character
g.add_character(Group17Character("me", # name
                              "C",  # avatar
                              0, 0,  # position
                                 1 # variant solution
))

# Uncomment this if you want the interactive character
# g.add_character(InteractiveCharacter("me", # name
#                                      "C",  # avatar
#                                      0, 0  # position
# ))

# Run!

# Use this if you want to press ENTER to continue at each step
# g.go(0)

# Use this if you want to proceed automatically
g.go(1)
