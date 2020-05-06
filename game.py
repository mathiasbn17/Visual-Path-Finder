import pygame
import threading
from nodes import Nodes
from algorithms import dijkstra
from algorithms import method_dict
from menu_logic import Menu
from menu_logic import Button
from maze_generation import randomized_prims_algorithm
from maze_generation import recursive_division

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Visual Path Finder')

black = (40, 40, 40)
white = (255, 255, 255)
shadow = (192, 192, 192)
green = (0, 200, 0)
red = (255, 0, 0)
blue = (0, 220, 255)
yellow = (255, 255, 125)

Nodes.create_nodes()

clock = pygame.time.Clock()
gameExit = False

left_Mouse = False
right_Mouse = False
old_left_Mouse = False

# Maybe I should initialize the Menu with the first menu titles and then have it going by itself?
Menu.create_menu()

while not gameExit:
    old_left_Mouse = left_Mouse

    gameDisplay.fill(shadow)

    for event in pygame.event.get():
        # If user wants to exit the game
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameExit = True

        # if mouse clicking is happening, bool needed to let user keep buttons pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_Mouse = True
            elif event.button == 3:
                right_Mouse = True

        # if no mouse clicking is happening
        if event.type == pygame.MOUSEBUTTONUP:
            left_Mouse = False
            right_Mouse = False


    for node in Nodes.nodeList:
        node.draw_node()

    Button.clicking_logic(old_left_Mouse, left_Mouse)

#    print(Menu.bool_and_method_dict["GO!"])

    if left_Mouse:
        if Menu.bool_and_method_dict["Wall"]:
            for node in Nodes.nodeList:
                if node.mouse_intersection() and not node.is_Wall:
                    node.wall_Up = True
        elif Menu.bool_and_method_dict["Start"]:
            for node in Nodes.nodeList:
                if node.mouse_intersection(): node.create_start()
        elif Menu.bool_and_method_dict["End"]:
            for node in Nodes.nodeList:
                if node.mouse_intersection(): node.create_end()
        elif Menu.bool_and_method_dict["Erase"]:
            for node in Nodes.nodeList:
                if node.mouse_intersection() and node.is_Wall: node.erase()

            #t1 = threading.Thread(target=randomized_prims_algorithm, args=(Nodes.nodeList))

    if Menu.maze_generation_dict["Prim"]:
        t1 = threading.Thread(target=randomized_prims_algorithm, args=(Nodes.nodeList,))
        t1.start()
        Menu.maze_generation_dict["Prim"] = False
        Button.inactivate("Prim")

    elif Menu.maze_generation_dict["Recursive  Division"]:
        t1 = threading.Thread(target=recursive_division, args=(Nodes.nodeList,))
        t1.start()
        Menu.maze_generation_dict["Recursive  Division"] = False
        Button.inactivate("Recursive  Division")


    if Menu.bool_and_method_dict["GO!"]:
        Nodes.reset()
        k = 0
        for key in Menu.algorithms_dict:
            if Menu.algorithms_dict[key] is True:
                t1 = threading.Thread(target=method_dict[key], args=(Nodes.nodeList,))
                t1.start()
            else:
                k += 1
        if k == len(Menu.algorithms_dict):
            t1 = threading.Thread(target=dijkstra, args=(Nodes.nodeList,))
            t1.start()
        Menu.bool_and_method_dict["GO!"] = False
        Button.inactivate("GO!")



    for node in Nodes.nodeList:
        if node.wall_Up:
            node.make_wall()

    Button.display_buttons()

    pygame.display.update()
    clock.tick()


pygame.quit()
quit()
