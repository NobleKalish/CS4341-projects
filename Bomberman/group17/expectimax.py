import math
import numpy as np
import sys

import astar
from Bomberman.bomberman.monsters.selfpreserving_monster import SelfPreservingMonster

sys.path.insert(0, '../bomberman')
from events import Event
from sensed_world import SensedWorld


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

    def _heuristic(self, goal, world, count_walls):
        """ Evaluate the current board state and assign a score based on distance to goal

            Parameters:
                goal (tuple[int, int]): The position of the goal in the form [x,y]
                count_walls (bool): If True, paths through walls will be considered. This allows for planned bombing
                    (default is True)

            Returns:
                The int score assigned to the board state in question
        """
        me = world.me(self.character)
        start = (me.x, me.y)
        # a_star = astar.Astar(self.world)
        # next_move = a_star.get_a_star(start, goal, count_walls=count_walls, scary_monsters=False)
        # return len(next_move) - 1
        ############ UNCOMMENT BELOW TO MAKE THINGS FASTER #####################
        x = goal[0] - start[0]
        y = goal[1] - start[1]
        return (x**2 + y**2)**0.5

    def do_expectimax(self) -> tuple[int, int]:
        """ Perform expectimax and return the recommended move.

            Returns:
                The recommended move in the form [xs,y].  [0,0] means place a bomb
        """

        world = SensedWorld.from_world(self.world)
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
        check_events = self._check_events(events)
        if check_events == math.inf or check_events == -math.inf:
            return check_events
        if not new_world.me(self.character):
            return -math.inf
        if depth >= self.max_depth:
            return self._utility(new_world, events)
        v = 0
        actions_and_worlds = self._get_enemy_actions(new_world)
        for action_and_world in actions_and_worlds:
            new_events = action_and_world[2]
            new_events.extend(events)
            p = 0
            for value in self.world.monsters.values():
                for m in value:
                    p = 1 - (1/((self._heuristic((m.x, m.y), new_world, False))+2))**2
            v = v + p * self._get_max_value(action_and_world[1], new_events, depth)
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
        check_events = self._check_events(events)
        if check_events == math.inf or check_events == -math.inf:
            return check_events
        if not new_world.me(self.character):
            return -math.inf
        if depth >= self.max_depth:
            return self._utility(new_world, events)
        v = -math.inf
        actions_and_worlds = self._get_player_actions(new_world)
        for action_and_world in actions_and_worlds:
            new_events = action_and_world[2]
            new_events.extend(events)
            v = max(v, self._get_expected_value(action_and_world[1], new_events, depth))
        return v

    def _utility(self, world, events) -> int:
        """ Evaluate a world state to determine an overall score for expectimax comparison.

            Parameters:
                world: The current game world.  Contains the world map as well as monster and character positions.
                events (list[Event]): The list of events occurring in that world (ex: bomb hit monster)

            Returns:
                utility: The assigned score based on all evaluated factors
        """

        utility = self._check_events(events)
        utility -= 50*self._heuristic(world.exitcell, world, True)
        if not world.monsters:
            return utility
        if world.monsters:
            for value in world.monsters.values():
                for m in value:
                    utility += 100*(self._heuristic((m.x, m.y), world, False))
        return utility

    def _get_player_actions(self, world) -> list[tuple[tuple[int, int], SensedWorld, list[Event]]]:
        """ Generate a list of all possible actions that could be taken by the AI character

            Parameters:
                world: The game world.  Contains the world map as well as monster positions

            Returns:
                player_actions: A list of actions in the form [[x,y], world, events]
        """

        fake_world = SensedWorld.from_world(world)
        m = fake_world.me(self.character)
        player_actions = self._get_new_actions(m, fake_world, True)
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
        if not fake_world.monsters:
            return actions_and_worlds
        else:
            for value in fake_world.monsters.values():
                for m in value:
                    is_monster_smart = False
                    if m.name != "stupid":
                        is_monster_smart = True
                    actions_and_worlds.extend(self._get_new_actions(m, fake_world, False, is_monster_smart))
            return actions_and_worlds

    @staticmethod
    def _get_new_actions(entity, fake_world, avoid_bombs, is_monster_smart=False) -> list[tuple[tuple[int, int], SensedWorld, list[Event]]]:
        """ Generate a list of possible moves for the selected Entity.  Doesn't include bomb placement.

            Parameters:
                entity (entity): The character or monster whose possible moves are being looked for.
                fake_world (SensedWorld): The current world according to that entity.
                avoid_bombs (bool): Should the entity avoid killing themselves by eliminating potential explosion
                                    squares as movement options?

            Returns:
                actions_and_worlds: A list of actions in the form [[x,y], world, events]
        """

        actions_and_worlds = list()
        if is_monster_smart:
            if entity.name == "aggressive":
                rnge = 2
            else:
                rnge = 1
            entity = SelfPreservingMonster(entity.name, "A", entity.x, entity.y, rnge)
            (found, dx, dy) = entity.look_for_character(fake_world)
            if found:
                entity.move(dx, dy)
                (new_world, events) = fake_world.next()
                actions_and_worlds.append(((0, 0), new_world, events))
                return actions_and_worlds
        for dx in [-1, 0, 1]:
            if (entity.x + dx >= 0) and (entity.x + dx < fake_world.width()):
                for dy in [-1, 0, 1]:
                    if (dx != 0) or (dy != 0):
                        if (entity.y + dy >= 0) and (entity.y + dy < fake_world.height()):
                            if not fake_world.wall_at(entity.x + dx, entity.y + dy):
                                if avoid_bombs:  # This means that stupid monsters won't ignore explosions
                                    if not fake_world.explosion_at(entity.x + dx, entity.y + dy):
                                        entity.move(dx, dy)
                                        (new_world, events) = fake_world.next()
                                        actions_and_worlds.append(((dx, dy), new_world, events))
                                else:
                                    entity.move(dx, dy)
                                    (new_world, events) = fake_world.next()
                                    actions_and_worlds.append(((dx, dy), new_world, events))
        return actions_and_worlds

    def _check_events(self, events):
        utility = 0
        for event in events:
            if event.tpe == Event.BOMB_HIT_MONSTER:
                utility += 5000
            elif event.tpe == Event.BOMB_HIT_CHARACTER:
                return -math.inf
            elif event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                return -math.inf
            elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                return math.inf
            elif event.tpe == Event.BOMB_HIT_WALL:
                utility += 5
        return utility