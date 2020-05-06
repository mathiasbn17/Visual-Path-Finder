from math import inf
import time
import pygame
import math
# Maybe import display height and width from game

display_width = 800
display_height = 600

black = (40, 40, 40)
white = (255, 255, 255)
shadow = (192, 192, 192)
green = (0, 200, 0)
red = (255, 0, 0)
blue = (0, 220, 255)
yellow = (255, 255, 125)
star = (255, 255, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))


class Nodes:
    block_size = 18
    space = 2
    blank = 3
    nodeList = []
    connected = []
    popCounter = 0
    color = white
    width = 0
    height = 0

    # initializes an instance of class Nodes, which is part of the grid
    def __init__(self, pos):
        self.X = pos[0] * (self.block_size + Nodes.space)
        self.Y = pos[1] * (self.block_size + Nodes.space) + Nodes.blank / int(display_height / (Nodes.block_size + Nodes.space )) * display_height
        self.origin = pos
        self.f = inf
        self.prev = None
        self.pop = True
        self.is_Open = True
        self.is_Wall = False
        self.is_startNode = False
        self.is_endNode = False
        self.wall_Up = False # Not needed, could return False to main
        self.path_Up = False # Not needed, could return False to main
        self.visit_Up = False

    def make_pop(self):
        if self.pop:
            self.X -= 2
            self.Y -= 2
        else:
            self.X += 2
            self.Y += 2

        self.popCounter += 1
        if self.popCounter == 5:
            self.pop = False
        if self.popCounter == 10:
            self.pop = True
            self.popCounter = 0
            return False
        return True

    def visit(self):
        self.is_Open = False
        self.visit_Up = True
        # Sigmoid function asymptotic to 255 to create gradient.
        gradient = 255/(1 + math.exp(-0.06*self.f + 4))
        grad = (gradient, 255 - gradient, 255 - gradient)
        if not self.is_endNode and not self.is_startNode:
            self.color = star
        time.sleep(0.002)
        if not self.is_endNode and not self.is_startNode:
            self.color = grad

    def make_path(self):
        self.color = yellow
        if not self.make_pop():
            self.path_Up = False
        time.sleep(0.000001)

    def draw_node(self):
        rect = pygame.Rect(self.X, self.Y, self.block_size, self.block_size)
        pygame.draw.rect(gameDisplay, self.color, rect)

    def mouse_intersection(self):
        mouse_xy = pygame.mouse.get_pos()
        if self.X <= mouse_xy[0] <= self.X + self.block_size:
            if self.Y <= mouse_xy[1] <= self.Y + self.block_size:
                return True

    def make_wall(self):
        self.color = black
        self.is_Wall = True

        if not self.make_pop():
            self.wall_Up = False

    def create_start(self):
        for nodes in Nodes.nodeList:
            if nodes.is_startNode and not nodes == self:
                Nodes.nodeList[Nodes.nodeList.index(nodes)] = Nodes(nodes.origin)
        self.is_startNode = True
        self.f = 0
        self.color = green
        self.is_Wall = False
        self.is_endNode = False
        for nodes in Nodes.connected:
            nodes.color = blue

    def create_end(self):
        for nodes in Nodes.nodeList:
            if nodes.is_endNode and not nodes == self:
                Nodes.nodeList[Nodes.nodeList.index(nodes)] = Nodes(nodes.origin)
        self.is_endNode = True
        self.f = inf
        self.color = red
        self.is_Wall = False
        self.is_startNode = False
        for node in Nodes.connected:
            node.color = blue

    def erase(self):
        Nodes.nodeList[Nodes.nodeList.index(self)] = Nodes(self.origin)

    def assign_coordinate(self, x, y):
        self.x_grid = x
        self.y_grid = y

    @classmethod
    def clear_grid(cls):
        cls.nodeList.clear()
        cls.create_nodes()

    @classmethod
    def reset(cls):
        cls.connected.clear()
        for node in cls.nodeList:
            node.is_Open = True
            node.prev = None
            if not node.is_Wall and not node.is_endNode and not node.is_startNode:
                node.color = white
            if not node.is_startNode:
                node.f = inf

    @staticmethod
    def create_nodes():
        for y in range(int(display_height / (Nodes.block_size + Nodes.space )) - Nodes.blank):
            for x in range(int(display_width / (Nodes.block_size + Nodes.space))):
                Nodes.nodeList.append(Nodes((x, y)))
        Nodes.width = int(display_width / (Nodes.block_size + Nodes.space))
        Nodes.height = int(display_height / (Nodes.block_size + Nodes.space) - Nodes.blank)

