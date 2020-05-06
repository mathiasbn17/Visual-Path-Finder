from nodes import Nodes
from math import inf
import time

# Should have universal display measures.
display_width = 800
display_height = 600


def dijkstra(nodes):

    def lowest_tentative(grid, height, width):
        smallest = inf
        xy_coord = ()
        for y in range(height):
            for x in range(width):
                if grid[y][x].f < smallest and grid[y][x].is_Open and not grid[y][x].is_Wall:
                    smallest = grid[y][x].f
                    xy_coord = (x, y)
        return xy_coord

    maze = []
    maze_width = Nodes.width
    maze_height = Nodes.height
    for i in range(maze_height): maze.append([node for node in Nodes.nodeList[i * maze_width: (i + 1) * maze_width]])
    for node in nodes:
        if node.is_endNode:
            while node.is_Open:
                xy = lowest_tentative(maze, maze_height, maze_width)
                if xy == ():
                    return False
                x = xy[0]
                y = xy[1]
                maze[y][x].visit()

                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dx, dy in directions:
                    if x + dx < maze_width and not x + dx < 0 and y + dy < maze_height and not y + dy < 0:
                        if maze[y][x].f + 1 < maze[y + dy][x + dx].f and maze[y + dy][x + dx].is_Open:
                            maze[y + dy][x + dx].f = maze[y][x].f + 1
                            maze[y + dy][x + dx].prev = maze[y][x]
                time.sleep(0.00001)

            connect(node.prev)
            Nodes.connected.reverse()
            for path_node in Nodes.connected:
                path_node.path_Up = True
                while path_node.path_Up:
                    path_node.make_path()
                time.sleep(0.02)


def a_star(nodes):
    def lowest_f(grid, height, width, goal_pos):
        smallest = inf
        xy_coord = ()
        for y in range(height):
            for x in range(width):
                h = manhattan_distance((x, y), goal_pos)
                if grid[y][x].f + h < smallest and grid[y][x].is_Open and not grid[y][x].is_Wall:
                    smallest = grid[y][x].f + h
                    xy_coord = (x, y)
        return xy_coord

    def manhattan_distance(node, goal_pos):
        return abs(node[0] - goal_pos[0]) + abs(node[1] - goal_pos[1])

    maze = []
    maze_width = Nodes.width
    maze_height = Nodes.height
    for i in range(maze_height): maze.append([node for node in Nodes.nodeList[i * maze_width: (i + 1) * maze_width]])
    for node in nodes:
        if node.is_endNode:
            while node.is_Open:
                xy = lowest_f(maze, maze_height, maze_width, (int(node.X / display_width * maze_width), int((node.Y - 60) / (display_height - 60) * maze_height)))
                if xy == ():
                    return False
                x = xy[0]
                y = xy[1]
                maze[y][x].visit()
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dx, dy in directions:
                    if x + dx < maze_width and not x + dx < 0 and y + dy < maze_height and not y + dy < 0:
                        if maze[y][x].f + 1 < maze[y + dy][x + dx].f and maze[y + dy][x + dx].is_Open:
                            maze[y + dy][x + dx].f = maze[y][x].f + 1
                            maze[y + dy][x + dx].prev = maze[y][x]
                time.sleep(0.00001)

            connect(node.prev)
            Nodes.connected.reverse()
            for path_node in Nodes.connected:
                path_node.path_Up = True
                while path_node.path_Up:
                    path_node.make_path()
                time.sleep(0.02)


def breadth_first(nodes):
    maze = []
    maze_width = Nodes.width
    maze_height = Nodes.height
    for i in range(maze_height): maze.append([node for node in Nodes.nodeList[i * maze_width: (i + 1) * maze_width]])
    for node in nodes:
        if node.is_endNode:
            for rows in maze:
                for cell in rows:
                    if cell.is_startNode:
                        y = maze.index(rows)
                        x = rows.index(cell)
            queue = [(x, y)]
            while node.is_Open:
                xy_coord = queue[0]
                x, y = xy_coord[0], xy_coord[1]
                maze[y][x].visit()
                del queue[0]
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dx, dy in directions:
                    if -1 < x + dx < maze_width and -1 < y + dy < maze_height:
                        if maze[y][x].f + 1 < maze[y + dy][x + dx].f and maze[y + dy][x + dx].is_Open and not maze[y + dy][x + dx].is_Wall:
                            queue.append((x + dx, y + dy))
                            maze[y + dy][x + dx].f = maze[y][x].f + 1
                            maze[y + dy][x + dx].prev = maze[y][x]
            connect(node.prev)
            Nodes.connected.reverse()
            for path_node in Nodes.connected:
                path_node.path_Up = True
                while path_node.path_Up:
                    path_node.make_path()
                time.sleep(0.02)


def connect(point):
    if point.prev is None:
        return point.f
    else:
        Nodes.connected.append(point)
        connect(point.prev)



method_dict = {
    "dijkstra": dijkstra,
    "A*": a_star,
    "Breadth  first": breadth_first
}

# Add Depth first
# Swarming?
# Greedy Best first search
