from nodes import Nodes
import random
import time

black = (40, 40, 40)

#def create_maze():


"""Prim's randomized algorithm is a maze generating algorithm. It starts from a random coordinate in a grid full of 
walls and works its way out, extending the maze in a random direction for each iteration as long as it does not 
reconnect with another part of the maze."""


def randomized_prims_algorithm(nodes):
    # Creates a 2D array so it's easier to handle as a grid.
    maze = []
    maze_width = Nodes.width
    maze_height = Nodes.height
    for i in range(maze_height): maze.append([node for node in Nodes.nodeList[i * maze_width: (i + 1) * maze_width]])

    # Makes all nodes to walls so we can connect a path through. The alternative is to first run the algorithm below
    # and then backtrack it and build the walls. Because there won't be a very distinct pattern with Prim's
    # randomized algorithm I think it'll look nicer this way.
    Nodes.reset()
    for node in nodes:
        node.is_Wall = True
        node.color = black

    # Chooses a random coordinate in the grid, the node which the path will originate from.
    y = random.randrange(0, maze_height)
    x = random.randrange(0, maze_width)

    # List to keep track of which walls have been erased (made non-walls). Later this list will also carry the
    # coordinates of nodes which should not be erased, i.e. nodes, which if erased, would connect two different
    # parts of the maze. For obvious reasons this is not wanted.
    erased = []
    maze[y][x].erase()
    erased.append((x, y))

    # Creates a list of connected walls (meaning that, if we were to erase them, they'd connect to another non-wall).
    connected_walls = []

    # Creates a list of neighbor-coordinates (or rather the difference between neighbors
    # and the first randomized node, that being (x, y)).
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # In this program a path cannot be diagonal.

    # Iterates over every direction
    for dx, dy in directions:
        # Makes sure that neighbor-coordinate is within the grid.
        if -1 < x + dx < maze_width and -1 < y + dy < maze_height:
            connected_walls.append((x + dx, y + dy))

    # This is where the magic happens.
    while len(connected_walls) > 0:

        # Chooses a random index within the length of connected_walls list.
        index = random.randrange(0, len(connected_walls))

        # Picks out the coordinate (made random by index, which is randomly selected).
        xy_coord = connected_walls[index]

        # Removes the chosen coordinate from the list, it can only be picked once.
        # Alternative: connected_walls.pop(index); though the return is not needed.
        del connected_walls[index]

        # Splits coordinate into x and y.
        x, y = xy_coord[0], xy_coord[1]

        # Erases (makes non-wall) the node at the given coordinate, and adds it to the erased list.
        maze[y][x].erase()
        erased.append((x, y))

        # Again, creates a list of possible ways to travel and iterates over the list.
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            if -1 < x + dx < maze_width and -1 < y + dy < maze_height:

                # If the neighbor-coordinate has not been erased and is not already in connected_walls list,
                # then it should be added.
                if (x + dx, y + dy) not in erased and not (x + dx, y + dy) in connected_walls:
                    connected_walls.append((x + dx, y + dy))

                # If it already is in the connected_walls list, this means that it should never be erased, since
                # that would connect two different parts of the maze. Therefore, if that is the case, it is removed
                # and added to the erased list, so that if it is encountered again it gives False for the above if-
                # - statement, making sure that it will never again be added to the connected_walls list.
                elif (x + dx, y + dy) in connected_walls:
                    connected_walls.remove((x + dx, y + dy))
                    erased.append((x + dx, y + dy))

        # Pauses the algorithm so that the interface is cleaner.
        time.sleep(0.01)


def recursive_division(nodes):
    Nodes.clear_grid()
    maze = []
    maze_width = Nodes.width
    maze_height = Nodes.height
    for i in range(maze_height):
        maze.append([node for node in Nodes.nodeList[i * maze_width: (i + 1) * maze_width]])
    for node in Nodes.nodeList:
        for rows in maze:
            for cell in rows:
                if cell == node:
                    y = maze.index(rows)
                    x = rows.index(cell)
                    node.assign_coordinate(x, y)

    def do_the_recursion(possible_spaces):
        if len(possible_spaces) > 0:
            space_index = random.randrange(0, len(possible_spaces))
            space_corners = possible_spaces[space_index]

            space_width = space_corners[1] - space_corners[0]
            space_height = space_corners[3] - space_corners[2]
            # For aesthetics:
            k = random.randrange(0, space_height + space_width)
            if k < space_width:
                vertical = True
            else:
                vertical = False

            # WE've got two problems, we can build in front of a gap; we can build two rows/columns next to e/o.
            if vertical:
                wall_column = random.randrange(space_corners[0] + 1, space_corners[1])
                height = space_corners[3] - space_corners[2]
                empty = [random.randrange(space_corners[2], space_corners[3] + 1)]
                y = space_corners[3]
                if y - height - 1 > - 1:
                    if not maze[y - height - 1][wall_column].is_Wall:
                        empty.append(y - height)
                if y + 1 < maze_height:
                    if not maze[y + 1][wall_column].is_Wall:
                        empty.append(y)
                for i in range(height + 1):
                    if y - i not in empty:
                        maze[y - i][wall_column].wall_Up = True
                        time.sleep(0.01)

            if not vertical:
                wall_row = random.randrange(space_corners[2], space_corners[3])
                width = space_corners[1] - space_corners[0]
                empty = [random.randrange(space_corners[0], space_corners[1] + 1)]
                x = space_corners[0]
                if x + width + 1 < maze_width:
                    if not maze[wall_row][x + width + 1].is_Wall:
                        empty.append(x + width)
                if x - 1 > - 1:
                    if not maze[wall_row][x - 1].is_Wall:
                        empty.append(x)
                for i in range(width + 1):
                    if x + i not in empty:
                        maze[wall_row][x + i].wall_Up = True
                        time.sleep(0.01)

            #time.sleep(30)
            find_the_space()

    def explore_direction(x, y, dx, dy):
        # Also need to check itself, otherwise we might pass over it. Is this a complete solution, might we get other problems?
        # Can only think that if it breaks on the first round, then we'd return a false value which is never good.
        x -= dx
        y -= dy

        has_run = False
        while -1 < x + dx < maze_width and -1 < y + dy < maze_height:
            # if at any point one cannot move right or left, then we should stop it there, returning what is already got

            # If next node is a wall we of course have to break because we have reached the edge of the space
            if maze[y + dy][x + dx].is_Wall:     # We have one problem here, we need to break if node is next to a wall and on the edge of the grid.
                break

            # If a node has a wall on either opposite side of itself, we also need to break, because we are reaching an
            # opening of another wall, which is the edge of the currently explored space.
            elif x + 1 < maze_width and x - 1 > -1:
                if maze[y + dy][x + 1].is_Wall and maze[y + dy][x - 1].is_Wall:
                    break
            elif y + 1 < maze_height and y - 1 > -1:  # Run this even if dx == 0??
                if maze[y + 1][x + dx].is_Wall and maze[y - 1][x + dx].is_Wall:
                    break

            #  If a node is on the edge of the grid and has a wall next to itself, on the far side of the edge, we are
            # also in an opening, so we've again reached the edge of our currently explored space.
            if (x - 1 == -1 and maze[y + dy][x + 1].is_Wall) or (x + 1 == maze_width and maze[y + dy][x - 1].is_Wall) or (y - 1 == -1 and maze[y + 1][x + dx].is_Wall) or (y + 1 == maze_height and maze[y - 1][x + dx].is_Wall):
                break

            x += dx
            y += dy
            has_run = True
        if not has_run:
            x += dx
            y += dy
        if dx == 0: return y
        if dy == 0: return x

    def find_the_space():
        # Can have a list containing the four corners of the space, and node is skipped if it's coordinate is within
        # the four corners. Should probably have a method which assigns each cell with an x and y coordinate.
        available_space = []    # Stores corners of all spaces [[xLeft, xRight, yTop, yBottom] for all spaces in grid]
        for row in maze:
            for node in row:
                if node.is_Wall:
                    continue
                # Checks if node is within any already found space, if so, there is no need to run that node.
                unexplored_space = True
                for spaces in available_space:
                    # For all spaces we need to check if our node is within that space, if so, no need to search it.
                    if spaces[0] <= node.x_grid <= spaces[1] and spaces[2] <= node.y_grid <= spaces[3]:
                        unexplored_space = False
                # If our node is in an unexplored space, we of course need to explore it.
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if unexplored_space:
                    corners = []
                    corners.append(explore_direction(node.x_grid, node.y_grid, directions[0][0], directions[0][1]))
                    corners.append(explore_direction(node.x_grid, node.y_grid, directions[1][0], directions[1][1]))
                    corners.append(explore_direction(node.x_grid, node.y_grid, directions[2][0], directions[2][1]))
                    corners.append(explore_direction(node.x_grid, node.y_grid, directions[3][0], directions[3][1]))
                    #print(corners)
                    #Then check if space is big enough
                    x_diff = abs(corners[0] - corners[1])
                    y_diff = abs(corners[2] - corners[3])
                    if x_diff > 1 and y_diff > 1:
                        available_space.append(corners)

        print(available_space)
        #time.sleep(30)
        do_the_recursion(available_space)


    find_the_space()
