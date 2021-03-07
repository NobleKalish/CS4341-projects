# This is necessary to find the main code
import sys
import math

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from group17 import astar, expectimax
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
        self.bomb_move = 0
        self.bomb_at = None
        self.world = None
        self.variant_solutions = {
            1: self.variant1,
            2: self.variant2,
            3: self.variant3,
            4: self.variant4,
            5: self.variant5
        }
        self.keys = {
            0: (-1, -1),
            1: (-1, 0),
            2: (-1, 1),
            3: (0, -1),
            4: (0, 1),
            5: (1, -1),
            6: (1, 0),
            7: (1, 1),
        }
        self.state = 0

    def do(self, wrld):
        self.world = wrld
        func = self.variant_solutions.get(self.variant)
        func()

    def variant1(self):
        if self.state == 0:
            self.perform_a_star()
        elif self.state == 2:
            dx, dy = self.bomb_state()
            if dx and dy:
                self.move(dx, dy)

    def variant2(self):
        if self._check_for_monster(2):
            self.state = 1
        elif self.state == 2:
            dx, dy = self.bomb_state()
            if dx and dy:
                self.move(dx, dy)
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
        if self.world.wall_at(next_move[0], next_move[1]):
            self.state = 2
            self.bomb_at = (self.x, self.y)
            self.place_bomb()
        else:
            new_x = next_move[0] - self.x
            new_y = next_move[1] - self.y
            self.move(new_x, new_y)

    def perform_expectimax(self):
        ex_max = expectimax.Expectimax(self.world, 5, 0.9, self)
        ex_max.do_expectimax()
        ex_max_result = ex_max.do_expectimax()
        new_x = ex_max_result[0] - self.x
        new_y = ex_max_result[1] - self.y
        self.move(new_x, new_y)

    def bomb_state(self):
        start_x = self.x
        start_y = self.y
        if self.bomb_move == 0:
            for dx in [-1, 1]:
                if (start_x + dx >= 0) and (start_x + dx < self.world.width()):
                    for dy in [-1, 1]:
                        if (start_y + dy >= 0) and (start_y + dy < self.world.height()):
                            if not self.world.wall_at(start_x + dx, start_y + dy):
                                self.bomb_move = 1
                                return dx, dy
        else:
            if not self.world.bomb_at(self.bomb_at[0], self.bomb_at[1]):
                if not self.world.explosion_at(self.bomb_at[0], self.bomb_at[1]+1):
                    self.state = 0
                    self.bomb_move = 0
            return 0, 0
