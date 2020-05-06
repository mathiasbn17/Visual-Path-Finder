import pygame
from nodes import Nodes

black = (40, 40, 40)
white = (255, 255, 255)
shadow = (192, 192, 192)
red = (255, 0, 0)

display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))


"""The menu logic for this program is recursive. Meaning that a first menu is created, using strings in a list.
Each of the strings also exist in either another list or in a dictionairy. If, the string is found in another list
it means we should create a new menu, connecting the sub-menu to its "parent" as a characteristic of an object of type
Button. Else, if the string is found in a dictionairy, it means it's either the key to a boolean or method type, which
is activated through clicking."""


class Menu:
    menu_start_x, menu_start_y, menu_end, menu_height = 2, 2, 796, 56

    # If time, add weighted nodes to the menu, and also more maze generating algorithms.
    list_0 = ["Algorithms", "Start", "End", "Wall", "Erase", "Maze", "Clear", "GO!"]
    algorithms = ["Algorithms", "dijkstra", "A*", "Breadth  first"]
    mazes = ["Maze", "Prim", "Recursive  Division"]


    # Dijkstras = ["Dijkstra", "Testing", "Testing2", "Testing3"]
    bool_and_method_dict = {
        "Start": False,
        "End": False,
        "Wall": False,
        "Erase": False,
        "Weight": False,
        "Maze": False,
        "Clear": Nodes.clear_grid,
        "GO!": False,
    }
    algorithms_dict = {
        "dijkstra": False,
        "A*": False,
        "Breadth  first": False
    }

    maze_generation_dict = {
        "Prim": False,
        "Recursive  Division": False
    }

    menu_lists = [list_0, algorithms, mazes]

    @classmethod
    def create_menu(cls, menu_strings=list_0, parent=[]):
        space = 2 * (len(menu_strings) + 1)
        button_width = (display_width - space) / len(menu_strings)
        center_coord = [(2 * (i + 1) + button_width * i + button_width / 2, 28) for i in range(len(menu_strings))]

        for i in range(len(menu_strings)):
            Button.button_list.append(Button(menu_strings[i], center_coord[i], button_width, menu_strings, parent))


class Button:
    button_list = []

    def __init__(self, string, center, width, neighbours, parent):
        self.parent = parent
        self.string = string
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', 16)
        self.text = self.font.render(string, True, black, None)
        self.clicked = False
        self.hover = False
        self.textRect = self.text.get_rect()
        self.textRect.center = center
        self.width, self.height = width, center[1] * 2
        self.X, self.Y = center[0] - width / 2, 2
        self.rect = pygame.Rect(self.X, self.Y, self.width, self.height)
        self.neighbours = neighbours
        self.latent = False if self.parent == [] else True
        self.function = None
        # A characteristic of type list or None
        self.successor = self.find_successor()
        if self.successor is not None:
            Menu.create_menu(self.successor, self.neighbours)
        elif self.string not in self.parent:
            self.function = self.find_function()

    def find_successor(self):
        for lists in Menu.menu_lists:
            for string in lists:
                if self.string == string and self.neighbours != lists and self.parent != lists:
                    return lists
        return None

    def find_function(self):
        for key in Menu.bool_and_method_dict:
            if key is self.string:
                return Menu.bool_and_method_dict[self.string]
        for key in Menu.algorithms_dict:
            if key is self.string:
                return Menu.algorithms_dict[self.string]
        for key in Menu.maze_generation_dict:
            if key is self.string:
                return Menu.maze_generation_dict[self.string]

        # for key in Menu.bool...
        # if key == button.string, return Menu.bool_and_method_class[key]

    @classmethod
    def display_buttons(cls):
        for button in cls.button_list:
            if button.latent is False:
                pygame.draw.rect(gameDisplay, shadow if button.clicked else white, button.rect)
                gameDisplay.blit(button.text, button.textRect)


    @classmethod
    def clicking_logic(cls, old_left_mouse, left_mouse):
        mouse_xy = pygame.mouse.get_pos()
        for button in cls.button_list:
            if not button.latent:
                if button.X <= mouse_xy[0] <= button.X + button.width and button.Y <= mouse_xy[1] <= button.Y + button.height:
                    button.text = button.font.render(button.string, True, red, None)
                    if left_mouse:
                        pass
                    elif not left_mouse and old_left_mouse:
                        if button.successor is not None:
                            Button.switch_menu_downwards(button.successor)
                        elif button.function is not None:
                            function_type = type(button.function)
                            if function_type is bool:
                                for other_buttons in Button.button_list:
                                    if not other_buttons == button and not other_buttons.latent:
                                        other_buttons.clicked = False
                                button.clicked = not button.clicked

                                # Checks if usual boolean value
                                if button.string in Menu.bool_and_method_dict:
                                    for key in Menu.bool_and_method_dict:
                                        if not key is button.string:
                                            Menu.bool_and_method_dict[key] = False
                                    Menu.bool_and_method_dict[button.string] = not Menu.bool_and_method_dict[button.string]

                                # Checks if path finding algorithm
                                if button.string in Menu.algorithms_dict:
                                    Menu.algorithms_dict[button.string] = not Menu.algorithms_dict[button.string]
                                    for key in Menu.algorithms_dict:
                                        if not key is button.string:
                                            Menu.algorithms_dict[key] = False

                                # Checks if maze generating algorithm
                                if button.string in Menu.maze_generation_dict:
                                    Menu.maze_generation_dict[button.string] = not Menu.maze_generation_dict[button.string]
                                    for key in Menu.maze_generation_dict:
                                        if not key is button.string:
                                            Menu.maze_generation_dict[key] = False

                            else:
                                button.function()
                        else:
                            Button.switch_menu_upwards(button, button.parent)  # Remove downwards.
                            break
                else:
                    button.text = button.font.render(button.string, True, black, None)

    @classmethod
    def switch_menu_upwards(cls, curr_button, successors):                 # Defo needs to be readjusted
        for button in Button.button_list:
            if button.string in successors and button.latent:
                if button.string is not curr_button.string and button.string in button.parent:
                    pass
                else:
                    button.latent = False
            else:
                button.latent = True


    @classmethod
    def switch_menu_downwards(cls, successors):
        for button in Button.button_list:
            if button.string in successors and button.latent:
                button.latent = False
            else:
                button.latent = True

    @classmethod
    def inactivate(cls, string):
        for button in cls.button_list:
            if button.string == string:
                button.clicked = False

