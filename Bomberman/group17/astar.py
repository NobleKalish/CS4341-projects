from queue import PriorityQueue


class Astar:
    def __init__(self, world, character):
        self.world = world
        self.character = character

    def get_next_move(self, goal, count_walls=True):
        came_from = self._get_a_star(goal, count_walls)
        x_start = self.character.x
        y_start = self.character.y
        start = (x_start, y_start)
        path = [goal]
        while path[0] != start:
            path.insert(0, came_from.get(path[0]))
        return path

    def _get_a_star(self, goal, count_walls):
        frontier = PriorityQueue()
        x_start = self.character.x
        y_start = self.character.y
        start = (x_start, y_start)
        frontier.put((0, start))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current[1] == goal:
                break

            if count_walls:
                next_neighbors = self._get_neighbors(current[1])
            else:
                next_neighbors = self._get_neighbors_without_walls(current[1])
            for next_neighbor in next_neighbors:
                if next_neighbor[1] == 1:
                    new_cost = cost_so_far[current[1]] + 3
                else:
                    new_cost = cost_so_far[current[1]] + 1
                if next_neighbor[0] not in cost_so_far or new_cost < cost_so_far[next_neighbor[0]]:
                    cost_so_far[next_neighbor[0]] = new_cost
                    priority = new_cost + self._heuristic(goal, next_neighbor[0])
                    frontier.put((priority, next_neighbor[0]))
                    came_from[next_neighbor[0]] = current[1]
        return came_from

    def _get_neighbors(self, current):
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
        neighbors = list()
        for dx in [-1, 0, 1]:
            if (current[0] + dx >= 0) and (current[0] + dx < self.world.width()):
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        if (current[1] + dy >= 0) and (current[1] + dy < self.world.height()):
                            if not self.world.wall_at(current[0] + dx, current[1] + dy):
                                neighbors.append(((current[0] + dx, current[1] + dy), 0))
        return neighbors

    def _heuristic(self, goal, neighbor):
        x_distance = goal[0] - neighbor[0]
        y_distance = goal[1] - neighbor[1]
        return x_distance + y_distance
