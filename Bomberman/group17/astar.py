from queue import PriorityQueue

""" A class for performing A* search between two points.  Options for considering paths through walls and for 
spaces near monsters being more costly"""


class Astar:
    def __init__(self, world):
        """
            Parameters:
                world: The game world.  Contains the world map as well as monster positions
        """
        self.world = world

    def get_next_move(self, start, goal, count_walls=True, scary_monsters=True):
        """ Perform A* path planning from start to goal and return the path taken.

            Parameters:
                start (tuple[int, int]): The position to start the path from in the form (x,y).
                    Usually the character's location
                goal (tuple[int, int]): The position of the goal in the form (x,y)
                count_walls (bool): If True, paths through walls will be considered. This allows for planned bombing
                    (default is True)
                scary_monsters (bool): If True, spaces within 3 of the monster will cost extra,
                    incentivizing other routes.
                    (default is True)

            Returns:
                path (list[tuple[int, int]]): The list of every step on the optimal path from start to goal.
        """

        came_from = self._get_a_star(start, goal, count_walls, scary_monsters)
        path = [goal]
        while path[0] != start:
            path.insert(0, came_from.get(path[0]))
        return path

    def _get_a_star(self, start, goal, count_walls, scary_monsters):
        """ Perform A* path planning from start to goal and return

            Parameters:
                start (tuple[int, int]): The position to start the path from in the form (x,y).
                    Usually the character's location
                goal (tuple[int, int]): The position of the goal in the form (x,y)
                count_walls (bool): If True: Paths through walls will be considered
                scary_monsters (bool): If True, spaces within 3 of the monster will cost extra,
                    incentivizing other routes.

            Returns:
                came_from (dict[Union[tuple[int, int], tuple[int, int]]):
        """
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()[1]  # extract just the location

            if current == goal:
                break

            if count_walls:
                next_neighbors = self._get_neighbors(current)
            else:
                next_neighbors = self._get_neighbors_without_walls(current)
            for next_neighbor in next_neighbors:
                if next_neighbor[1] == 1:  # If the neighbor is a wall
                    new_cost = cost_so_far[current] + 3
                else:
                    new_cost = cost_so_far[current] + 1
                if scary_monsters:  # Increase costs near monsters
                    for monster in next(iter(self.world.monsters.values())):
                        if self._heuristic((monster.x, monster.y), next_neighbor[0]) <= 3:
                            new_cost += 2
                if next_neighbor[0] not in cost_so_far or new_cost < cost_so_far[next_neighbor[0]]:
                    cost_so_far[next_neighbor[0]] = new_cost
                    priority = new_cost + self._heuristic(goal, next_neighbor[0])
                    frontier.put((priority, next_neighbor[0]))
                    came_from[next_neighbor[0]] = current
        return came_from

    def _get_neighbors(self, current):
        """ Find all neighboring positions including walls

            Parameters:
                current (tuple[int, int]): current position in the form (x,y)

            Returns:
                neighbors (list[tuple[tuple[int, int], int]]): List of tuples.  Each neighbor takes the form
                    [[x, y], isWall?]. If the neighbor is a wall, isWall? will be 1.  Otherwise isWall? will be 0.
        """
        neighbors = list()
        for dx in [-1, 0, 1]:
            if (current[0] + dx >= 0) and (current[0] + dx < self.world.width()):
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        if (current[1] + dy >= 0) and (current[1] + dy < self.world.height()):
                            if not self.world.wall_at(current[0] + dx, current[1] + dy):
                                neighbors.append(((current[0] + dx, current[1] + dy), 0))
                            else:
                                neighbors.append(((current[0] + dx, current[1] + dy), 1))
        return neighbors

    def _get_neighbors_without_walls(self, current):
        """ Find all neighboring positions that aren't walls

            Parameters:
                current (tuple[int, int]): current position in the form (x,y)

            Returns:
                neighbors (list[tuple[tuple[int, int], int]]): List of tuples.  Each neighbor takes the form
                    [[x, y], isWall?].  For this function isWall? is always 0, but it's there to maintain compatibility
                    with _get_neighbors.
        """

        neighbors = list()
        for dx in [-1, 0, 1]:
            if (current[0] + dx >= 0) and (current[0] + dx < self.world.width()):
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        if (current[1] + dy >= 0) and (current[1] + dy < self.world.height()):
                            if not self.world.wall_at(current[0] + dx, current[1] + dy):
                                neighbors.append(((current[0] + dx, current[1] + dy), 0))
        return neighbors

    @staticmethod
    def _heuristic(goal, neighbor) -> int:
        """ Returns the euclidean distance between the goal and a point neighbor

            Parameters:
                goal (tuple[int, int]): goal position in the form (x,y)
                neighbor (tuple[int, int]): neighbor position in the form (x,y)

            Returns:
                distance (int): the euclidean distance
        """
        x_distance = goal[0] - neighbor[0]
        y_distance = goal[1] - neighbor[1]
        return x_distance + y_distance
