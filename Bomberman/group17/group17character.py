# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
import astar, expectimax
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
        if self.check_for_direct_route():
            self.state = 3
        if self.state == 0:
            self.perform_a_star(False, True)
        elif self.state == 1:
            self.perform_expectimax(5, 0)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def variant2(self):
        """ Run AI Variant 2"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(3):
            self.state = 1
        if self.state == 0:
            if self.world.bombs != {}:
                self.perform_expectimax(4, 2)
            else:
                self.perform_a_star(True, True)
        elif self.state == 1:
            self.perform_expectimax(4, 2)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def variant3(self):
        """ Run AI Variant 3"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(4):
            self.state = 1
        if self.state == 0:
            if self.world.bombs != {}:
                self.perform_expectimax(5, 3)
            else:
                self.perform_a_star(True, True)
        elif self.state == 1:
            self.perform_expectimax(5, 3)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def variant4(self):
        """ Run AI Variant 4"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(4):
            self.state = 1
        if self.state == 0:
            if self.world.bombs != {}:
                self.perform_expectimax(5, 4)
            else:
                self.perform_a_star(True, True)
        elif self.state == 1:
            self.perform_expectimax(5, 4)
        elif self.state == 2:
            self.bomb_state()
        elif self.state == 3:
            self.perform_a_star(False, False)

    def variant5(self):
        """ Run AI Variant 4"""
        if self.check_for_direct_route():
            self.state = 3
        elif self._check_for_monster(4):
            self.state = 1
        if self.state == 0:
            if self.world.bombs != {}:
                self.perform_expectimax(5, 4)
            else:
                self.perform_a_star(True, True)
        elif self.state == 1:
            self.perform_expectimax(5, 4)
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

        start = (self.x, self.y)
        if not self.world.monsters:
            return False
        for value in self.world.monsters.values():
            for m in value:
                a_star = astar.Astar(self.world)
                next_move = a_star.get_a_star(start, (m.x, m.y), False, False)
                if len(next_move) == 0:
                    return False
                elif len(next_move)-1 <= limit:
                    return True
        return False

    def perform_a_star(self, scary_monsters, count_walls):
        """ Use A* search to perform one move

            Parameters:
                scary_monsters (bool): When True the search adds cost to spaces near monsters.
                count_walls (bool): When True include walls into possible path
        """

        a_star = astar.Astar(self.world)
        current_location = (self.x, self.y)
        goal = self.world.exitcell
        next_moves = a_star.get_a_star(current_location, goal, count_walls, scary_monsters)
        if len(next_moves) == 0:
            self.move(0, 0)
            return
        next_move = next_moves[1]
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
                                if not self.world.bomb_at(start_x + dx, start_y + dy) \
                                        and not self.world.explosion_at(start_x + dx, start_y + dy):
                                    self.bomb_move = 1
                                    self.move(dx, dy)
        else:
            if not self.world.bomb_at(self.bomb_at[0], self.bomb_at[1]):
                if not self.world.explosion_at(self.bomb_at[0], self.bomb_at[1] + 1):
                    self.state = 0
                    self.bomb_move = 0
            self.move(0, 0)

    def check_for_direct_route(self) -> bool:
        """ Check if the charater is closer to the goal than any monster and there's a clear path to said goal.

            Returns: True if the character can safely run straight to the goal.  Requires a path two shorter than
                     the closest monster
        """

        a_star = astar.Astar(self.world)
        current_location = (self.x, self.y)
        goal = self.world.exitcell
        ai_next_moves = a_star.get_a_star(current_location, goal, count_walls=False, scary_monsters=False)
        if len(ai_next_moves) == 0:
            return False
        ai_fast_path = len(ai_next_moves)
        monster_fast_path = 1000
        if self.world.monsters:
            for value in self.world.monsters.values():
                for m in value:
                    m_current_location = (m.x, m.y)
                    if m_current_location == goal:
                        return False
                    m_next_moves = a_star.get_a_star(m_current_location, goal, count_walls=False, scary_monsters=False)
                    if len(m_next_moves) != 0:
                        if len(m_next_moves) < monster_fast_path:
                            monster_fast_path = len(m_next_moves)
        return ai_fast_path < monster_fast_path - 1

    def get_closest_monster(self) -> str:
        """ Find the closest monster and return it's name as a string"""

        closest_monster = None
        closest_range = 100
        for value in self.world.monsters.values():
            for m in value:
                distance = ((m.x - self.x) ** 2 + (m.y - self.y) ** 2) ** 0.5
                if distance < closest_range:
                    closest_monster = m.name
                    closest_range = distance
        return closest_monster

