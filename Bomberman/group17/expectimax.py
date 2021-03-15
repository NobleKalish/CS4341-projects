import math
import numpy as np
import sys

from Bomberman.group17 import astar

sys.path.insert(0, '../bomberman')
from Bomberman.bomberman.events import Event
from Bomberman.bomberman.sensed_world import SensedWorld


class Expectimax:
    def __init__(self, world, depth, gamma, character):
        """
            Parameters:
                world: The game world.  Contains the world map as well as monster positions
                depth (int): The number of moves deep to simulate before scoring states with a heuristic.
                gamma (float): The discount applied to states based on how many moves away they are.
                character: The character performing expectimax
        """

        self.world = world
        self.max_depth = depth
        self.gamma = gamma
        self.character = character
        self.expecti_max = None
        self.bounds = (0, 100)
        # Defining all the possible movement directions
        self.actions = {
            (-1, -1): 0,
            (-1, 0): 1,
            (-1, 1): 2,
            (0, -1): 3,
            (0, 1): 4,
            (1, -1): 5,
            (1, 0): 6,
            (1, 1): 7,
            (0, 0): 8  # This indicates placing a bomb
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
            8: (0, 0)
        }

    def _get_neighbors(self, current) -> list[tuple[int, int]]:
        """ Find all adjacent spaces legal to move into.  Out of bounds spaces and walls are excluded.

            Parameters:
                current (tuple[int, int]): The space currently being occupied in the form [x,y]

            Returns:
                neighbors: The list of all neighboring spaces legal to move into
        """

        # TODO: Why isn't this used in the get actions helper functions?
        neighbors = list()
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x != 0 or y != 0:
                    new_x = current[0] + x
                    new_y = current[1] + y
                    if (new_y >= 0) and (new_y < self.world.height()) and (new_x >= 0) and (new_x < self.world.width()):
                        if not self.world.wall_at(new_x, new_y):
                            neighbors.append((new_x, new_y))
        return neighbors

    def _heuristic(self, goal, count_walls):
        """ Evaluate the current board state and assign a score based on distance to goal

            Parameters:
                goal (tuple[int, int]): The position of the goal in the form [x,y]
                count_walls (bool): If True, paths through walls will be considered. This allows for planned bombing
                    (default is True)

            Returns:
                The int score assigned to the board state in question
        """

        start = (self.character.x, self.character.y)
        a_star = astar.Astar(self.world)
        next_move = a_star.get_a_star(start, goal, count_walls=count_walls)
        return len(next_move) - 1

    def do_expectimax(self) -> tuple[int, int]:
        """ Perform expectimax and return the recommended move.

            Returns:
                The recommended move in the form [x,y].  [0,0] means place a bomb
        """

        world = self.world
        actions_and_worlds = self._get_player_actions(world)
        depth = 0
        self.expecti_max = np.full(9, -math.inf)
        for action_and_world in actions_and_worlds:
            self.expecti_max[self.actions.get(action_and_world[0])] =\
                self._get_expected_value(action_and_world[1], action_and_world[2], depth)
        return self.keys.get(np.argmax(self.expecti_max))

    def _get_expected_value(self, new_world, events, depth) -> float:
        """ Find the expected possible move for a monster character. Expected value step of expectimax.

            Parameters:
                new_world: The current game world.  Contains the world map as well as monster and character positions.
                events (list[Event]): The list of events occurring in that world (ex: bomb hit monster).
                depth (int): The number of moves evaluated thus far.

            Returns:
                v (float): The value of the expected move.
        """

        depth += 1
        if not new_world.me(self.character):
            return -10000
        if depth >= self.max_depth:
            return self._utility(new_world, events)
        v = 0
        actions_and_worlds = self._get_enemy_actions(new_world)
        for action_and_world in actions_and_worlds:
            p = 1/len(actions_and_worlds)
            v = v + p * self._get_max_value(action_and_world[1], action_and_world[2], depth)
        return v

    def _get_max_value(self, new_world, events, depth) -> float:
        """ Find the highest possible move for the ai character. Max value step of expectimax.

            Parameters:
                new_world: The current game world.  Contains the world map as well as monster and character positions.
                events (list[Event]): The list of events occurring in that world (ex: bomb hit monster).
                depth (int): The number of moves evaluated thus far.

            Returns:
                v (float): The value of the highest value possible move.
        """

        depth += 1
        if not new_world.me(self.character):
            return -10000
        if depth >= self.max_depth:
            return self._utility(new_world, events)
        v = -math.inf
        actions_and_worlds = self._get_player_actions(new_world)
        if actions_and_worlds is None:
            return -1000
        for action_and_world in actions_and_worlds:
            v = max(v, self._get_expected_value(action_and_world[1], action_and_world[2], depth))
        return v

    def _utility(self, world, events) -> int:
        """ Evaluate a world state to determine an overall score for expectimax comparison.

            Parameters:
                world: The current game world.  Contains the world map as well as monster and character positions.
                events (list[Event]): The list of events occurring in that world (ex: bomb hit monster)

            Returns:
                utility: The assigned score based on all evaluated factors
        """

        utility = 0
        for event in events:
            if event.tpe == Event.BOMB_HIT_MONSTER:
                utility += 50
            elif event.tpe == Event.BOMB_HIT_CHARACTER:
                return -10000
            elif event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                return -10000
            elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                return 10000
            elif event.tpe == Event.BOMB_HIT_WALL:
                utility += 5
        if world.me(self.character):
            utility += 100 - self._heuristic(world.exitcell, True)
        else:
            return -10000
        if not self.world.monsters:
            return utility
        if world.monsters:
            monsters = next(iter(world.monsters.values()))
            for m in monsters:
                utility -= 1000 - 100*(self._heuristic((m.x, m.y), False))
        return utility

    def _get_player_actions(self, world) -> list[tuple[tuple[int, int], SensedWorld, list[Event]]]:
        """ Generate a list of all possible actions that could be taken by the AI character

            Parameters:
                world: The game world.  Contains the world map as well as monster positions

            Returns:
                player_actions: A list of actions in the form [[x,y], world, events]
        """

        fake_world = SensedWorld.from_world(world)
        if fake_world.me(self.character):
            m = fake_world.me(self.character)
        else:
            return None
            # TODO: Would this ever be called?  Does it matter?
        player_actions = self._get_new_actions(m, fake_world)
        m.place_bomb()
        (new_world, events) = fake_world.next()
        player_actions.append(((0, 0), new_world, events))
        return player_actions

    def _get_enemy_actions(self, world) -> list[tuple[tuple[int, int], SensedWorld, list[Event]]]:
        """ Generate a list of all possible actions that could be taken by a Monster

            Parameters:
                world: The game world.  Contains the world map as well as monster positions

            Returns:
                actions_and_worlds: A list of actions in the form [[x,y], world, events]
        """

        fake_world = SensedWorld.from_world(world)
        actions_and_worlds = list()
        if not self.world.monsters:
            return actions_and_worlds
        monsters = next(iter(fake_world.monsters.values()))
        for m in monsters:
            actions_and_worlds.extend(self._get_new_actions(m, fake_world))
        return actions_and_worlds

    @staticmethod
    def _get_new_actions(entity, fake_world) -> list[tuple[tuple[int, int], SensedWorld, list[Event]]]:
        """ Generate a list of possible moves for the selected Entity.  Doesn't include bomb placement.

            Parameters:
                entity (entity): The character or monster whose possible moves are being looked for.
                fake_world (SensedWorld): The current world according to that entity.

            Returns:
                actions_and_worlds: A list of actions in the form [[x,y], world, events]
        """

        actions_and_worlds = list()
        for dx in [-1, 0, 1]:
            if (entity.x + dx >= 0) and (entity.x + dx < fake_world.width()):
                for dy in [-1, 0, 1]:
                    if (dx != 0) or (dy != 0):
                        if (entity.y + dy >= 0) and (entity.y + dy < fake_world.height()):
                            if not fake_world.wall_at(entity.x + dx, entity.y + dy):
                                entity.move(dx, dy)
                                (new_world, events) = fake_world.next()
                                actions_and_worlds.append(((dx, dy), new_world, events))
        return actions_and_worlds
