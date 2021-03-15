# This is necessary to find the main code
import sys
import math

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from bomberman.entity import CharacterEntity
from group17 import astar, expectimax, q_learning, minimax
from colorama import Fore, Back


class Group17Character(CharacterEntity):
    def __init__(self, name, avatar, x, y, variant):
        """
            Parameters:
                name (str): the name of this player
                avatar (str): The character used to denote the player on the map.  Usually "C"
                x (int): The starting x position of the player
                y (int): The starting y position of the player
                variant (int): Which variant of the AI is requested.  Current choices are 1-5
        """

        super().__init__(name, avatar, x, y)
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
        # This section defines the possible moves from the current location
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
        """ Run the specified AI variant
            Parameters:
                wrld: The game world.  Contains the world map as well as monster positions
        """

        self.world = wrld
        func = self.variant_solutions.get(self.variant)
        func()

    def variant1(self):
        """ Run AI Variant 1"""

        if self.state == 0:
            self.perform_a_star(False)
        elif self.state == 1:
            self.perform_expectimax(5, 0)
        elif self.state == 2:
            self.bomb_state()

    def variant2(self):
        """ Run AI Variant 2"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(2):
            self.state = 1
        if self.state == 0:
            self.perform_a_star(True)
        elif self.state == 1:
            self.perform_expectimax(3, 2)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def variant3(self):
        """ Run AI Variant 3"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(2):
            self.state = 1
        if self.state == 0:
            self.perform_a_star(True)
        elif self.state == 1:
            self.perform_expectimax(5, 2)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def variant4(self):
        """ Run AI Variant 4"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(3):
            self.state = 1
        if self.state == 0:
            self.perform_a_star(True)
        elif self.state == 1:
            self.perform_expectimax(5, 3)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def variant5(self):
        """ Run AI Variant 5"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(3):
            self.state = 1
        if self.state == 0:
            self.perform_a_star(True)
        elif self.state == 1:
            self.perform_mini_max(5, 3)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def _check_for_monster(self, limit) -> bool:
        """ Check for a monster within <limit> spaces

            Parameters:
                limit (int): The radius around the character to check for monsters.

            Returns:
                True if a monster is present within limit spaces
        """

        if not self.world.monsters:
            return False
        monsters = next(iter(self.world.monsters.values()))
        for m in monsters:
            if abs(m.x - self.x) <= limit and abs(m.y - self.y) <= limit:
                return True
        return False

    def perform_a_star(self, scary_monsters, count_walls=True):
        """ Use A* search to perform one move

            Parameters:
                scary_monsters (bool): When True the search adds cost to spaces near monsters.
                count_walls (bool): When True include walls into possible path
        """

        a_star = astar.Astar(self.world)
        current_location = (self.x, self.y)
        goal = self.world.exitcell
        next_move = a_star.get_a_star(current_location, goal, count_walls=count_walls, scary_monsters=scary_monsters)[1]
        if self.world.wall_at(next_move[0], next_move[1]):
            self.bomb_at = (self.x, self.y)
            self.place_bomb()
            self.bomb_state()
            self.state = 2
        else:
            new_x = next_move[0] - self.x
            new_y = next_move[1] - self.y
            self.move(new_x, new_y)

    def perform_expectimax(self, depth, limit):
        """ Use Expectimax to perform one move

            Parameters:
                depth (int): The depth to perform expectimax to.
                limit (int): The radius to check for monsters when determining the next state.
        """

        ex_max = expectimax.Expectimax(self.world, depth, 0.9, self)
        ex_max.do_expectimax()
        ex_max_result = ex_max.do_expectimax()
        new_x = ex_max_result[0]
        new_y = ex_max_result[1]
        if new_x == 0 and new_y == 0:
            self.place_bomb()
            self.bomb_at = (self.x, self.y)
            self.bomb_state()
            self.state = 2
        else:
            self.move(new_x, new_y)
        if not self._check_for_monster(limit):
            if self.bomb_move == 1:
                self.state = 2
            else:
                self.state = 0

    def perform_mini_max(self, depth, limit):
        """ Use Minimax to perform one move

            Parameters:
                depth (int): The depth to perform minimax to.
                limit (int): The radius to check for monsters when determining the next state.
        """

        monster = None
        if self.world.monsters:
            monsters = next(iter(self.world.monsters.values()))
            for m in monsters:
                if m.name == "aggressive":
                    monster = m
        Minimax = minimax.Minimax(self, depth, monster)
        move = Minimax.alpha_beta_search(self.world)
        if move[0] != 0 or move[1] != 0:
            self.move(move[0], move[1])
        else:
            self.state = 2
            self.bomb_at = (self.x, self.y)
            self.place_bomb()
            self.bomb_state()
        if not self._check_for_monster(limit):
            if self.bomb_move == 1:
                self.state = 2
            else:
                self.state = 0

    def bomb_state(self):
        """ Identify the best move given a bomb is on the map
        """

        start_x = self.x
        start_y = self.y
        if self.bomb_move == 0:
            for dx in [-1, 1]:
                if (start_x + dx >= 0) and (start_x + dx < self.world.width()):
                    for dy in [-1, 1]:
                        if (start_y + dy >= 0) and (start_y + dy < self.world.height()):
                            if not self.world.wall_at(start_x + dx, start_y + dy):
                                self.bomb_move = 1
                                self.move(dx, dy)
        else:
            if not self.world.bomb_at(self.bomb_at[0], self.bomb_at[1]):
                if not self.world.explosion_at(self.bomb_at[0], self.bomb_at[1] + 1):
                    self.state = 0
                    self.bomb_move = 0
            self.move(0, 0)

    def check_for_direct_route(self):
        if self.world.monsters:
            monsters = next(iter(self.world.monsters.values()))
            for m in monsters:
                if m.y >= self.y:
                    return False
        a_star = astar.Astar(self.world)
        current_location = (self.x, self.y)
        goal = self.world.exitcell
        next_move = a_star.get_a_star(current_location, goal, count_walls=False, scary_monsters=False)
        if len(next_move) == 0:
            return False
        return True

