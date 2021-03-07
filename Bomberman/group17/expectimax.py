import math
import numpy as np
from operator import itemgetter
from bomberman.events import Event
from bomberman.sensed_world import SensedWorld


class Expectimax:
    def __init__(self, world, depth, gamma, character):
        self.world = world
        self.max_depth = depth
        self.gamma = gamma
        self.character = character
        self.expecti_max = None
        self.actions = {
            (-1, -1): 0,
            (-1, 0): 1,
            (-1, 1): 2,
            (0, -1): 3,
            (0, 1): 4,
            (1, -1): 5,
            (1, 0): 6,
            (1, 1): 7,
            (0, 0): 8
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

    def _get_neighbors(self, current):
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

    def _heuristic(self, goal, neighbor):
        x_distance = goal[0] - neighbor[0]
        y_distance = goal[1] - neighbor[1]
        return x_distance + y_distance

    def do_expectimax(self):
        world = self.world
        actions_and_worlds = self._get_player_actions(world)
        depth = 0
        self.expecti_max = np.full(8, -math.inf)
        for action_and_world in actions_and_worlds:
            self.expecti_max[self.actions.get(action_and_world[0])] = self._get_expected_value(action_and_world[1], action_and_world[2], depth)
        return self.keys.get(np.argmax(self.expecti_max))

    def _get_expected_value(self, new_world, events, depth):
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

    def _get_max_value(self, new_world, events, depth):
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

    def _utility(self, world, events):
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
            utility += 100 - self._heuristic(world.exitcell, (world.me(self.character).x, world.me(self.character).y))
        else:
            return -10000
        monsters = next(iter(world.monsters.values()))
        for m in monsters:
            utility -= 1000 - (self._heuristic((m.x, m.y), (world.me(self.character).x, world.me(self.character).y)))
        return utility

    def _get_player_actions(self, world):
        fake_world = SensedWorld.from_world(world)
        if fake_world.me(self.character):
            m = fake_world.me(self.character)
        else:
            return None
        return self._get_new_actions(m, fake_world)

    def _get_enemy_actions(self, world):
        fake_world = SensedWorld.from_world(world)
        actions_and_worlds = list()
        monsters = next(iter(fake_world.monsters.values()))
        for m in monsters:
            actions_and_worlds.extend(self._get_new_actions(m, fake_world))
        return actions_and_worlds

    def _get_new_actions(self, entity, fake_world):
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
