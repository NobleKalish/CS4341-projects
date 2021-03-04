# This is necessary to find the main code
import sys
import math
from operator import itemgetter
import q_learning

from Bomberman.bomberman.events import Event
from Bomberman.group17 import expectimax, astar

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
        self.variant_solutions = {
            1: self.variant1,
            2: self.variant2,
            3: self.variant3,
            4: self.variant4,
            5: self.variant5
        }
        self.state = 0

    def do(self, wrld):
        self.world = wrld
        func = self.variant_solutions.get(self.variant)
        func()

    def variant1(self):
        a_star = astar.Astar(self.world, self)
        if self.state == 0:
            next_move = a_star.get_next_move()[1]
            self.move(next_move[1], next_move[0])

    def variant2(self):
        a_star = astar.Astar(self.world, self)
        ex_max = expectimax.Expectimax(self.world, 5, 0.9, self)
        # if self._check_for_monster(1):
        #     self.state = 1
        # else:
        #     self.state = 0
        if self.state == 0:
            next_move = a_star.get_next_move()[1]
            new_x = next_move[0] - self.x
            new_y = next_move[1] - self.y
            self.move(new_x, new_y)
        elif self.state == 1:
            ex_max.do_expectimax()

    def variant3(self):
        a_star = astar.Astar(self.world, self)
        ex_max = expectimax.Expectimax(self.world, 5, 0.9, self)
        # if self._check_for_monster(1):
        #     self.state = 1
        # else:
        #     self.state = 0
        if self.state == 0:
            next_move = a_star.get_next_move()[1]
            new_x = next_move[0] - self.x
            new_y = next_move[1] - self.y
            self.move(new_x, new_y)
        elif self.state == 1:
            ex_max.do_expectimax()
    def variant4(self):
        pass

    def variant5(self):
        pass

    def _check_for_monster(self, limit):
        monsters = next(iter(self.world.monsters.values()))
        for m in monsters:
            if abs(m.x - self.x) <= limit or abs(m.y - self.y) <= limit:
                return True
        return False
