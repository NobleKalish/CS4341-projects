# This is necessary to find the main code
import sys
import math

from group17 import astar, expectimax

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from bomberman.entity import CharacterEntity
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
        self.perform_a_star()

    def variant2(self):
        if self._check_for_monster(2):
            self.state = 1
        else:
            self.state = 0
        if self.state == 0:
            self.perform_a_star()
        elif self.state == 1:
            self.perform_expectimax()

    def variant3(self):
        if self._check_for_monster(2):
            self.state = 1
        else:
            self.state = 0
        if self.state == 0:
            self.perform_a_star()
        elif self.state == 1:
            self.perform_expectimax()

    def variant4(self):
        if self._check_for_monster(3):
            self.state = 1
        else:
            self.state = 0
        if self.state == 0:
            self.perform_a_star()
        elif self.state == 1:
            self.perform_expectimax()

    def variant5(self):
        pass

    def _check_for_monster(self, limit):
        monsters = next(iter(self.world.monsters.values()))
        for m in monsters:
            if abs(m.x - self.x) <= limit and abs(m.y - self.y) <= limit:
                return True
        return False

    def perform_a_star(self):
        a_star = astar.Astar(self.world, self)
        next_move = a_star.get_next_move()[1]
        new_x = next_move[0] - self.x
        new_y = next_move[1] - self.y
        self.move(new_x, new_y)

    def perform_expectimax(self):
        ex_max = expectimax.Expectimax(self.world, 5, 0.9, self)
        ex_max.do_expectimax()
