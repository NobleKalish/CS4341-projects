# This is necessary to find the main code
import sys
import math
from operator import itemgetter
import q_learning

from Bomberman.bomberman.events import Event
from Bomberman.group17 import expectimax

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from Bomberman.bomberman.entity import CharacterEntity
from colorama import Fore, Back


class Group17Character(CharacterEntity):
    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, avatar, x, y, variant):
        super().__init__(name, avatar, x, y)
        # Max search depth
        self.variant = variant
        self.world = None
        self.max_depth = 5
        self.gamma = 0.9
        self.variant_solutions = {
            1: self.variant1,
            2: self.variant2,
            3: self.variant3,
            4: self.variant4,
            5: self.variant5
        }

    def do(self, wrld):
        self.world = wrld
        func = self.variant_solutions.get(self.variant)
        func()

    def variant1(self):
        # pass
        q = q_learning.QLearning(self.world.height(), self.world.width())
        q.create_rewards(self.world)
        q.print_grid()
        q.train()
        shortest_path = q.get_shortest_path(self.x, self.y)


    def variant2(self):
        ex_max = expectimax.Expectimax(self.world, self.max_depth, self.gamma, self)
        move = ex_max.do_expectimax()
        self.move(move[1], move[0])

    def variant3(self):
        ex_max = expectimax.Expectimax(self.world, self.max_depth, self.gamma, self)
        move = ex_max.do_expectimax()
        self.move(move[1], move[0])

    def variant4(self):
        pass

    def variant5(self):
        pass
