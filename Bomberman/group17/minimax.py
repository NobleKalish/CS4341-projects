import math
import minimax_node
import sys

sys.path.insert(0, '../bomberman')
from sensed_world import SensedWorld


class Minimax:
    def __init__(self, character, depth, monster):
        self.character = character
        self.depth = depth
        self.monster = monster

    # The first level of an Alpha-Beta search that kicks off the rest.
    # Separated because the moves need to be tracked at the first level
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [int]: the column of the move evaluated to be best
    def alpha_beta_search(self, world):
        # Array of possible moves
        possible_moves = []
        successors = self.get_successors(world, self.character)
        successors.extend(self.addBombAction(world))
        alpha = -math.inf
        beta = math.inf
        # For each possible move
        for successor in successors:
            new_world = successor[1]
            move = successor[0]
            # create new node, evaluation created by alpha-beta searching all possible children to max_depth
            new_node = minimax_node.MinimaxNode(new_world, move, self.min_value(new_world, self.depth - 1, alpha, beta))
            # check if the move wins and if so return immediately
            if new_node.evaluation == math.inf:
                return new_node.move
            elif new_node.evaluation > alpha:
                alpha = new_node.evaluation
            # Add to the array
            possible_moves.append(new_node)
        # Assign Starting Vals to find the best move
        highest_move_val = -math.inf
        next_move = (0, 0)
        # Find the column associated with the best move
        for move in possible_moves:
            if move.evaluation >= highest_move_val:
                next_move = move.move
                highest_move_val = move.evaluation
        return next_move

    # find the maximum assured score from a given board
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int] depth: levels of depth to explore
    # PARAM [float] min_bound:
    # PARAM [float] max_bound:
    # RETURN [float] maximum assured score
    def max_value(self, world, depth, min_bound, max_bound):
        value = -math.inf
        # If node is terminal, than we have lost
        if not world.me(self.character):
            return -math.inf
        # If depth = 0, than we need to use the heuristic
        if depth == 0:
            return self.get_evaluation(world)
        # Now we evaluate each possible next move
        successors = self.get_successors(world, self.character)
        successors.extend(self.addBombAction(world))
        for successor in successors:
            world = successor[1]
            value = max(value, self.min_value(world, depth - 1, min_bound, max_bound))
            min_bound = max(value, min_bound)
            if min_bound >= max_bound:
                return value
        return value

    # find the minimum assured score from a given board
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int] depth: levels of depth to explore
    # PARAM [float] min_bound:
    # PARAM [float] max_bound:
    # RETURN [float] minimum assured score
    def min_value(self, world, depth, min_bound, max_bound):
        value = math.inf
        if not world.monsters:
            return math.inf
        # If depth = 0, than we need to use the heuristic
        if depth == 0:
            return self.monster_get_evaluation(world)
        # Now we evaluate each possible next move
        successors = self.get_successors(world, self.monster)
        for successor in successors:
            new_world = successor[1]
            value = min(value, self.max_value(new_world, depth - 1, min_bound, max_bound))
            max_bound = min(value, max_bound)
            if max_bound <= min_bound:
                return value
        return value

    def get_successors(self, world, entity):
        fake_world = SensedWorld.from_world(world)
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

    def get_evaluation(self, world):
        exit_cell = world.exitcell
        utility = 0
        utility -= 100 - self.ecludian_distance((self.character.x, self.character.y), (self.monster.x, self.monster.y))
        utility += 100 - self.ecludian_distance((self.character.x, self.character.y), (exit_cell.x, exit_cell.y))
        return utility

    def addBombAction(self, world):
        action_and_world = list()
        fake_world = SensedWorld.from_world(world)
        entity = fake_world.me(self.character)
        entity.place_bomb()
        (new_world, events) = fake_world.next()
        action_and_world.append(((0, 0), new_world, events))
        return action_and_world

    def ecludian_distance(self, start, goal):
        x = start[0] - goal[0]
        y = start[1] - goal[1]
        return (x**2 + y**2)**0.5

    def monster_get_evaluation(self, world):
        utility = 0
        utility -= 10 - self.ecludian_distance((self.character.x, self.character.y), (self.monster.x, self.monster.y))
        return utility
