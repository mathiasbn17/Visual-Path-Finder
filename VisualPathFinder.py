import pygame as pg
import inspect
import threading
import random
import time
from math import inf
import math

black = (40, 40, 40)
white = (255, 255, 255)
shadow = (192, 192, 192)
green = (0, 200, 0)
red = (255, 0, 0)
blue = (0, 220, 255)
yellow = (255, 255, 125)
star = (255, 255, 0)


class Solver:
    """
    Solver is a class which instances are capable of finding and drawing a path through a maze, from
    start node to end node. The algorithms used are Dijkstra, A*, BFS and DFS. All algorithms except DFS
    guarantee shortest path.
    """

    def __init__(self, grid):
        self.grid = grid
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x].is_start:
                    self.start_y = y
                    self.start_x = x
                if grid[y][x].is_end:
                    self.end_y = y
                    self.end_x = x
        self.end_node = self.grid[self.end_y][self.end_x]
        self.start_node = self.grid[self.start_y][self.start_x]
        self.visited = []

        self.solution = []

    def dijkstra(self, use_heuristic=False):
        while not self.end_node.visited:
            curr_coord = self.lowest_aggregate(use_heuristic)
            # The below condition will be true if we have no more accessible, unvisited nodes.
            if curr_coord == ():
                return False
            x = curr_coord[0]
            y = curr_coord[1]

            self.grid[y][x].visit()
            self.visited.append(self.grid[y][x])

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                if -1 < x + dx < len(self.grid[0]) and - 1 < y + dy < len(self.grid):
                    if self.grid[y][x].step_sum + self.grid[y][x].weight < self.grid[y + dy][x + dx].step_sum \
                            and not self.grid[y + dy][x + dx].visited:
                        self.grid[y + dy][x + dx].step_sum = self.grid[y][x].step_sum + self.grid[y][x].weight
                        self.grid[y + dy][x + dx].prev = self.grid[y][x]

        self.connect_dots()
        self.draw_shortest_path()

    def a_star(self):
        self.dijkstra(use_heuristic=True)

    def BFS(self):
        q = [self.start_node]
        while not self.end_node.visited:
            if len(q) < 1:
                return False
            curr_node = q.pop(0)
            curr_node.visit()
            x, y = curr_node.coord[0], curr_node.coord[1]

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                if - 1 < x + dx < len(self.grid[0]) and -1 < y + dy < len(self.grid):
                    if not self.grid[y + dy][x + dx].visited and not self.grid[y + dy][x + dx].is_wall and not self.grid[y + dy][x + dx] in q:
                        q.append(self.grid[y + dy][x + dx])
                        self.grid[y + dy][x + dx].prev = self.grid[y][x]
                        self.grid[y + dy][x + dx].step_sum = self.grid[y][x].step_sum + 1

        self.connect_dots()
        self.draw_shortest_path()

    def DFS(self):
        stack = [self.start_node]

        while not self.end_node.visited:
            if len(stack) < 1:
                return False
            curr_node = stack.pop()
            curr_node.visit()
            x, y = curr_node.coord[0], curr_node.coord[1]

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                if x + dx < len(self.grid[0]) and not x + dx < 0 and y + dy < len(self.grid) and not y + dy < 0:
                    if not self.grid[y + dy][x + dx].visited and not self.grid[y + dy][x + dx].is_wall and not \
                            self.grid[y + dy][x + dx] in stack:
                        stack.append(self.grid[y + dy][x + dx])
                        self.grid[y + dy][x + dx].prev = self.grid[y][x]
                        self.grid[y + dy][x + dx].step_sum = self.grid[y][x].step_sum + 1

        self.connect_dots()
        self.draw_shortest_path()

    def manhattan_distance(self, x, y):
        return abs(self.end_x - x) + abs(self.end_y - y)

    def lowest_aggregate(self, use_heuristic):
        smallest = inf
        xy_coord = ()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                h = self.manhattan_distance(x, y) if use_heuristic else 0
                if self.grid[y][x].step_sum + h < smallest and not self.grid[y][x].visited and not self.grid[y][x].is_wall:
                    smallest = self.grid[y][x].step_sum + h
                    xy_coord = (x, y)
        return xy_coord

    def backtrack(self, node):
        if node.prev is not None:
            self.solution.append(node)
            self.backtrack(node.prev)

    def connect_dots(self):
        self.backtrack(self.end_node.prev)  # We don't want the end node to be shown as part of the path.
        self.solution.reverse()

    def draw_shortest_path(self):
        for node in self.solution:
            node.make_path()


class MazeBuilder:
    """
    MazeBuilder is a class which instances operates on a grid with the aim of creating a maze. Each instance
    has a grid and can perform certain wall generating algorithms.
    """

    def __init__(self, grid):
        self.grid = grid
        self.height = len(self.grid)
        self.width = len(self.grid[0])

        # This list will keep track of what walls are connected to previously erased walls.
        self.erased = []
        self.connected_nodes = []
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def prims(self):
        self.make_wall_grid()
        self.initialize_prims()

        while len(self.connected_nodes) > 0:
            index = random.randrange(0, len(self.connected_nodes))
            xy_coord = self.connected_nodes.pop(index)
            x, y = xy_coord[0], xy_coord[1]

            # Erases (makes non-wall) the node at the given coordinate, and adds it to the erased list.
            self.grid[y][x].erase(is_popping=False)
            self.erased.append((x, y))

            for dx, dy in self.directions:
                if -1 < x + dx < self.width and -1 < y + dy < self.height:
                    if (x + dx, y + dy) not in self.erased and not (x + dx, y + dy) in self.connected_nodes:
                        self.connected_nodes.append((x + dx, y + dy))

                    # If it already is in the connected_walls list, this means that it should never be erased, since
                    # that would connect two different parts of the maze. Therefore, if that is the case, it is removed
                    # and added to the erased list, so that if it is encountered again it gives False for the above if-
                    # - statement, making sure that it will never again be added to the connected_walls list.
                    elif (x + dx, y + dy) in self.connected_nodes:
                        self.connected_nodes.remove((x + dx, y + dy))
                        self.erased.append((x + dx, y + dy))

            # Pauses the algorithm so that the user interface is cleaner.
            time.sleep(0.01)

    def initialize_prims(self):
        y = random.randrange(0, self.height)
        x = random.randrange(0, self.width)

        erased = []
        self.grid[y][x].erase(is_popping=False)
        erased.append((x, y))

        for dx, dy in self.directions:
            if -1 < x + dx < self.width and -1 < y + dy < self.height:
                self.connected_nodes.append((x + dx, y + dy))

    def recursive_division(self):
        axis_index = random.randrange(0, 2)
        self.divide(axis_index)

    # Divide is a recursive function where we split the grid parameter into two sub grids along an axis
    # (vertical/horizontal) with an opening so one can get from grid #1 to grid #2. The recursive step
    # consists of calling divide on each of the two sub grids until they can no longer be divided.
    def divide(self, axis_index):
        if self.height > 4 and self.width > 4:
            # We randomize which node in the grid we're dividing from.
            x = random.randrange(2, self.width - 2)
            y = random.randrange(2, self.height - 2)

            self.build_dividing_wall(x, y, axis_index)

            # Then we do the recursive step which is doing the same for the newly created sub grids.
            if axis_index == 0:
                MazeBuilder(self.grid[:y + 1]).divide((axis_index + 1) % 2)
                MazeBuilder(self.grid[y:]).divide((axis_index + 1) % 2)
            else:
                MazeBuilder([row[:x+1] for row in self.grid]).divide((axis_index + 1) % 2)
                MazeBuilder([row[x:] for row in self.grid]).divide((axis_index + 1) % 2)

    def build_dividing_wall(self, x, y, axis_index):
        axis_directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)]]

        # We set what axis we want to divide the grid by.
        axis_direction = axis_directions[axis_index]
        perpendicular_axis_direction = axis_directions[(axis_index + 1) % 2]

        # We move to the outer boundary of our axis by selecting one of two possible ways to
        # move up and down the axis.
        dx, dy = axis_direction[0][0], axis_direction[0][1]
        while 0 < x < self.width - 1 and 0 < y < self.height - 1:
            x += dx
            y += dy

        # Now, we want to move successively towards the other boundary of our axis in the grid, so we
        # select the other way to move across the axis.
        dx, dy = axis_direction[1][0], axis_direction[1][1]

        # Now, we every node on our axis will be made a wall, however, some nodes need to remain open
        # so that the two sub grids are connected. We store these nodes in gaps.
        walls = []
        gaps = []
        while -1 < x < self.width and -1 < y < self.height:
            # As we traverse along the axis, we need to make sure that we are not clogging a previous
            # gap, thus disconnecting two sub grids. Thus, we must also iterate over our perpendicular
            # directions, if the node on our axis is not a wall, but its perpendicular "siblings" are,
            # we would be clogging a connection by making our node a wall.
            for dx_perp, dy_perp in perpendicular_axis_direction:
                if -1 < x + dx_perp < self.width and -1 < y + dy_perp < self.height:
                    if self.grid[y + dy_perp][x + dx_perp].is_wall and not self.grid[y][x].is_wall:
                        gaps.append((x, y))
                        # Since the algorithms for solving the maze do not allow for diagonal movement
                        # we must also make sure the node before the one we're currently looking at is
                        # open.
                        if -1 < x - dx < self.width and -1 < y - dy < self.height:
                            gaps.append((x - dx, y - dy))
                        elif -1 < x + dx < self.width and -1 < y + dy < self.height:
                            gaps.append((x + dx, y + dy))
                        break
            time.sleep(0.01)

            self.grid[y][x].make_wall(is_popping=False)
            walls.append(self.grid[y][x])
            x += dx
            y += dy

        self.spawn_gaps(walls, gaps)

    def spawn_gaps(self, walls, gaps):
        # If there are zero cases where a gap is required to maintain a connected maze then we randomize
        # a gap.
        if len(gaps) == 0:
            gap_index = random.randrange(1, len(walls) - 1)
            walls[gap_index].erase(is_popping=False)
        # in other cases, we erase the nodes that need to be open.
        else:
            for x, y in gaps:
                self.grid[y][x].erase(is_popping=False)

    def make_wall_grid(self):
        for row in self.grid:
            for node in row:
                node.make_wall(is_popping=False)


class Menu:
    """
    The purpose of the Menu class is pretty self explanatory. However the menu logic resembles a NodeList
    class, an instance of class Menu holds the "active button" which is then linked to other buttons. Class
    Menu offers methods to navigate the button tree.

    Menu takes a dictionary and dissects it into linked instances of class Button.
    """

    def __init__(self, hierarchy, height):
        self.hierarchy = hierarchy
        self.height = height

        self.active_button = self.create_active_button()

    # Now we want to extract values of parameters that go into our active_button (Button)
    def create_active_button(self):
        text = list(self.hierarchy.keys())[0]
        parent = None
        children = self.hierarchy[text]

        # right_siblings should be exactly the entire menu structure to the right excluding our current node &
        # it's children tree.
        right_siblings = {}
        for key in self.hierarchy.keys():
            if key != text:
                right_siblings[key] = self.hierarchy[key]
        left_sibling = None

        width = int(display_width / len(self.hierarchy.keys()))
        center = (width / 2, self.height / 2)
        return Button(text, parent, children, right_siblings, left_sibling, center, width)

    def get_active_buttons(self):
        head = self.active_button
        active_buttons = []
        while head is not None:
            active_buttons.append(head)
            head = head.right_sibling
        return active_buttons

    def set_active_button(self, button):
        if button.parent is not None:
            self.active_button = button.parent
            while self.active_button.left_sibling is not None:
                self.active_button = self.active_button.left_sibling
        elif button.child is not None:
            self.active_button = button.child


class Button:
    """
    The most important attribute of an instance of class Button is its child. This will either be a method
    or another Button object. If it is a method, we want to call it, in other cases we want to change
    the active button in the Menu instance.

    Button objects are created recursively by dissecting the menu structure which is passed to Menu
    upon creation.
    """

    def __init__(self, text, parent, children, right_siblings, left_sibling, center, width):
        # Setting how button should be displayed on screen.
        self.text = text
        self.font = pg.font.Font('ARCADECLASSIC.TTF', 16)
        self.display_text = self.font.render(self.text, True, black, None)
        self.text_rect = self.display_text.get_rect()
        self.center = center
        self.text_rect.center = self.center
        self.x, self.y = center[0] - width / 2, 0
        self.width, self.height = width, center[1] * 2
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.color = white

        # parent and left sibling are either None, or another Button object since we are linking Button
        # objects recursively from the 'top left' in the menu hierarchy.
        self.parent = parent
        self.left_sibling = left_sibling

        # Now, we need to make sure that we pass on the correct parts of right_siblings and children to
        # the self.right_sibling and self.child Button object!
        # To do this, we need to create 2 new Button objects:
        self.right_sibling = self.set_right_sibling(right_siblings)
        self.child = self.set_child(children)

    def set_right_sibling(self, right_siblings):
        if right_siblings != {}:
            # The right sibling text corresponds to the first key in the right siblings structure
            rs_text = list(right_siblings)[0]
            # The children are accessed with the right sibling text
            rs_children = right_siblings[rs_text]

            # This step is a bit tricky, but we're essentially passing on everything in the right sibling
            # structure _except_ the right sibling and it's children.
            rs_right_siblings_keys = [list(right_siblings)[i] for i in range(1, len(right_siblings))]

            rs_right_siblings = {}
            for key in rs_right_siblings_keys:
                rs_right_siblings[key] = right_siblings[key]

            return Button(rs_text, None, rs_children, rs_right_siblings, self,
                          (self.center[0] + self.width, self.center[1]), self.width)

        else:
            return None

    def set_child(self, children):
        if children is not None and not callable(children):
            child_right_siblings = {}
            for key in children.keys():
                if key != self.text:
                    child_right_siblings[key] = children[key]

            # Now, when we create a child button we also need to decide what the size of the children buttons
            # will be:

            width = int(display_width / len(children))  # This is an integer because it makes sure any
            # left over space is put out on the right.
            center = (width / 2, self.height / 2)

            return Button(self.text, self, children[self.text], child_right_siblings, None, center, width)
        else:
            return children

    def click(self):
        if callable(self.child):
            if len(inspect.getfullargspec(self.child).args) > 1:
                self.child(self.text)
            else:
                self.child()
        else:
            return False


class Grid:
    def __init__(self, display_width, display_height, y, space_sz, node_sz):
        self.y = y

        grid_height = display_height - self.y
        self.no_columns = int(display_width / (node_sz + space_sz))
        self.no_rows = int(grid_height / (node_sz + space_sz))

        self.space_sz = space_sz
        self.node_sz = node_sz

        # This is the space left over around the grid, and it is needed to get the nodes centered on the display.
        lr_space = int((display_width - self.no_columns * (self.node_sz + self.space_sz) + self.space_sz) / 2)
        tb_space = int((grid_height - self.no_rows*(self.node_sz + self.space_sz) + self.space_sz) / 2)

        self.nodes = [[] for i in range(self.no_rows)]
        for v_i in range(self.no_rows):
            for h_i in range(self.no_columns):
                node_x = h_i*(self.space_sz + self.node_sz) + lr_space
                node_y = self.y + v_i*(self.space_sz + self.node_sz) + tb_space
                self.nodes[v_i].append(Node(node_x, node_y, (h_i, v_i), node_sz))

    # This is a function of grid because we need to make sure that we never have more than one start node.
    def change_start_node(self, node):
        for row in self.nodes:
            for other_node in row:
                if other_node.is_start:
                    other_node.reset()
        node.make_start()

    # This is a function of grid because we need to make sure that we never have more than one end node.
    def change_end_node(self, node):
        for row in self.nodes:
            for other_node in row:
                if other_node.is_end:
                    other_node.reset()
        node.make_end()

    # This methods takes every node and creates a new node object, with similar
    def prepare_to_solve(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                node = self.nodes[i][j]
                if not node.is_wall:
                    node.unvisit()

    def is_runnable(self):
        start_exists = False
        end_exists = False
        for row in self.nodes:
            for node in row:
                if node.is_start:
                    start_exists = True
                if node.is_end:
                    end_exists = True
        if start_exists and end_exists:
            return True
        else:
            return False


class Node:
    def __init__(self, x, y, coord, size):
        # Setting variables needed for visual representation
        self.x = x
        self.y = y
        self.coord = coord  # this is the nodes actual coordinate in the grid.
        self.origin_x, self.origin_y = self.x, self.y
        self.size = size

        # Some visually pleasing attributes
        self.is_popping = False
        self.is_returning = False
        self.pop_counter = 0

        self.color = white

        # Setting variables needed for path finding algorithm
        self.step_sum = inf
        self.weight = 1
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_weighted = False
        self.is_path = False
        self.prev = None
        self.visited = False

    def reset(self):
        self.weight = 1
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.is_path = False
        self.is_weighted = False
        self.color = white

    def make_start(self):
        self.reset()
        self.is_start = True
        self.color = green
        self.step_sum = 0

    def make_end(self):
        self.reset()
        self.is_end = True
        self.color = red

    def make_wall(self, is_popping=True):
        self.reset()
        self.is_popping = is_popping
        self.is_wall = True
        self.color = black

    def add_weight(self, weight):
        self.reset()
        self.is_popping = True
        self.weight = weight
        self.color = star
        self.is_weighted = True

    def make_path(self):
        self.color = yellow
        self.is_popping = True
        time.sleep(0.05)

    def erase(self, is_popping=True):
        self.reset()
        self.is_popping = is_popping

    def pop(self):
        self.x -= 2
        self.y -= 2

        if self.x < self.origin_x - 16:
            self.is_popping = not self.is_popping
            self.is_returning = not self.is_returning

    def return_to_origin(self):
        self.x += 2
        self.y += 2

        if self.x == self.origin_x:
            self.is_returning = not self.is_returning

    def visit(self):
        self.visited = True

        # Sigmoid function asymptotic to 255 to create gradient.
        gradient = 255 / (1 + math.exp(-0.06 * self.step_sum + 4))
        grad = (gradient, 255 - gradient, 255 - gradient)

        if not self.is_end and not self.is_start:
            self.color = star
        time.sleep(0.001)
        if not self.is_end and not self.is_start and not self.is_weighted:
            self.color = grad

    def unvisit(self):
        self.visited = False
        self.step_sum = inf if not self.is_start else 0
        self.is_path = False
        self.prev = None
        self.visited = False

        if self.is_start:
            self.color = green
        elif self.is_end:
            self.color = red
        elif self.is_weighted:
            self.color = star
        else:
            self.color = white


class VPF:
    """
    VPF is a GUI/game class which interacts with the user and also coordinates how the program responds
    to user input.
    """

    def __init__(self, window_width, window_height):
        # Setting up a pygame session
        pg.init()

        """
        We are actually going to hardcode some info for how we want the GUI to work here. This makes
        sure that if we plan on scaling the project and have a lot of optionality for the user, we will
        only ever have to make changes right here.

        The reason why I have the menu hardcoded here is because we cannot create it outside of our VPF
        class, because the buttons will correspond to a Method in our GUI. Some buttons will immediately
        execute some method which changes the GUI, while others will simply change the state of the GUI,
        and how we interpret user events. 

        For instance, the button for clearing the grid will immediately reset the nodes, whereas clicking
        the button which sets the start node simply tells us that the user _later on_ wants to perform this
        action. Meaning the VPF instance must be ready to interpret the next mouse click, if it intersects
        with a node, as the user setting that node to the start node.
        """
        self.main_menu_height = 60
        self.mouse_states = {
            "Start": False,
            "End": False,
            "Wall": False,
            "Weight": False,
            "Erase": False
        }
        self.algo_states = {
            "Dijkstra": True,
            "A star": False,
            "BFS": False,
            "DFS": False
        }
        sub_menu_algos = {
            "Algorithms": None
        }
        for state in self.algo_states:
            sub_menu_algos[state] = self.set_algo_state

        self.main_menu_hierarchy = {
            "Algorithms": sub_menu_algos,
            "Mazes": {"Mazes": None, "Prims algorithm": self.generate_maze, "Recursive division": self.generate_maze},
            "Clear": self.clear_grid,
            "GO!": self.go
        }
        for state in self.mouse_states:
            self.main_menu_hierarchy[state] = self.set_mouse_state

        # Now we create the Menu object
        self.menu = Menu(self.main_menu_hierarchy, self.main_menu_height)

        # We set some standard GUI attributes
        self.window_width = window_width
        self.window_height = window_height

        # We initiate the game display onto which we will draw our objects.
        self.display = pg.display.set_mode((window_width, window_height))
        pg.display.set_caption("Visual Path Finder")

        # Setting initial game necessities
        self.exit = False
        self.clock = pg.time.Clock()
        self.left_mouse = False
        self.old_left_mouse = False
        self.mouse_xy = pg.mouse.get_pos()

        # We have multiple methods where we require multithreading, but we only ever want one thread running
        # in parallell per instance of VPF.
        self.thread = None

        # Setting up a Grid instance which handles the creation of nodes (Node).
        self.node_size = 18
        self.space_between_nodes = 2
        self.grid = Grid(self.window_width, self.window_height, self.main_menu_height, self.space_between_nodes,
                         self.node_size)

    # Checks for exit event, and sets relevant instance variable if there was any.
    def check_exit(self, event):
        if event.type == pg.QUIT:
            self.exit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.exit = True

    # Checks for mouse click events, and sets relevant instance variable if there was any.
    def check_mouse_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_mouse = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.left_mouse = False

    # Handles pygame events, for instance if a key is pressed or a mouse button clicked.
    # One could say it sets the boolean values which the user can affect, which then
    # control the visual state of the GUI.
    def handle_user_events(self):
        for event in pg.event.get():
            self.check_exit(event)
            self.check_mouse_click(event)

    def display_grid(self):
        for row in self.grid.nodes:
            for node in row:
                rect = pg.Rect(node.x, node.y, node.size, node.size)
                pg.draw.rect(self.display, node.color, rect)

    def display_menu(self):
        active_buttons = self.menu.get_active_buttons()
        for button in active_buttons:
            pg.draw.rect(self.display, button.color, button.rect)
            self.display.blit(button.display_text, button.text_rect)

    def update_exterior(self):
        # Sets background color
        self.display.fill(shadow)
        self.display_grid()
        self.display_menu()

    def generate_maze(self, key):
        if self.thread is not None and self.thread.is_alive():
            return False
        self.clear_grid()
        mb = MazeBuilder(self.grid.nodes)

        if key == "Prims algorithm":
            self.thread = threading.Thread(target=mb.prims)
        elif key == "Recursive division":
            self.thread = threading.Thread(target=mb.recursive_division)
        self.thread.start()

    def solve(self):
        if not self.grid.is_runnable():
            return False
        self.grid.prepare_to_solve()
        solver = Solver(self.grid.nodes)
        if self.algo_states["Dijkstra"]:
            self.thread = threading.Thread(target=solver.dijkstra)
        elif self.algo_states["A star"]:
            self.thread = threading.Thread(target=solver.a_star)
        elif self.algo_states["BFS"]:
            self.thread = threading.Thread(target=solver.BFS)
        elif self.algo_states["DFS"]:
            self.thread = threading.Thread(target=solver.DFS)

        self.thread.start()

    def go(self):
        if self.thread is None or not self.thread.is_alive():
            self.solve()

    def set_mouse_state(self, key):
        for state in self.mouse_states:
            if state != key:
                self.mouse_states[state] = False
            else:
                self.mouse_states[key] = True

    def set_algo_state(self, key):
        for state in self.algo_states:
            if state != key:
                self.algo_states[state] = False
            else:
                self.algo_states[key] = True

    def click_node(self, node):
        for mouse_state in self.mouse_states:
            if self.mouse_states[mouse_state]:
                if mouse_state == 'Start':
                    self.grid.change_start_node(node)
                elif mouse_state == 'End':
                    self.grid.change_end_node(node)
                elif mouse_state == "Erase":
                    if node.is_wall or node.is_weighted:
                        node = node.erase()
                elif mouse_state == "Wall":
                    if not node.is_wall:
                        node.make_wall()
                elif mouse_state == "Weight":
                    if node.weight == 1:
                        node.add_weight(5)

    def clear_grid(self):
        if self.thread is not None:
            self.thread.join()
        self.grid = Grid(self.window_width, self.window_height, self.main_menu_height, self.space_between_nodes,
                         self.node_size)

    def update_grid(self):
        for row in self.grid.nodes:
            for node in row:
                if self.left_mouse:
                    if self.mouse_intersection(node.x, node.y, node.size, node.size):
                        self.click_node(node)
                if node.is_popping:
                    node.pop()
                elif node.is_returning:
                    node.return_to_origin()

    def update_menu(self):
        active_buttons = self.menu.get_active_buttons()
        for button in active_buttons:
            button.color = white
            if self.mouse_intersection(button.x, button.y, button.width, button.height):
                if self.left_mouse and not self.old_left_mouse:
                    if button.click() is False:
                        self.menu.set_active_button(button)
                button.color = shadow

    def update_interior(self):
        self.update_grid()
        self.update_menu()

    def mouse_intersection(self, x, y, width, height):
        return x <= self.mouse_xy[0] <= x + width and y <= self.mouse_xy[1] <= y + height

    def update_state(self):
        # We update our basic game necessities.
        self.old_left_mouse = self.left_mouse
        self.mouse_xy = pg.mouse.get_pos()

        # Changes booleans which control the main parts of the game
        self.handle_user_events()

        self.update_interior()

        self.update_exterior()

        pg.display.update()
        self.clock.tick()

    def run(self):
        while not self.exit:
            self.update_state()

        # Should always join thread before we end program
        if self.thread is not None:
            self.thread.join()
        pg.quit()
        quit()


if __name__ == "__main__":
    display_width = 800
    display_height = 600
    vpf = VPF(display_width, display_height)
    vpf.run()
