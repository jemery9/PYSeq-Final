#gamewindow.py

import os, sys
import pygame
from enum import Enum

class ButtonEvent(Enum):
    LEFT_CLICK = 1,
    MIDDLE_CLICK = 2,
    RIGHT_CLICK = 3,
    SCROLL_UP = 4,
    SCROLL_DOWN = 5


class GameWindow:
    """
    GameWindow class
    """
    def __init__(self, caption, width=400, height=300, bkgndColor=(255,255,255),):
        self.width = width
        self.height = height 
        self.scene = None 
        self.menu = None
        self.bkgndColor = bkgndColor
        self.gameEngine = None

        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.RESIZABLE)     
        pygame.display.set_caption(caption)

        self.key_to_function = {
            """
            pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
            pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
            pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
            pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
            pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
            pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
            pygame.K_q: (lambda x: x.rotateAll('X',  0.1)),
            pygame.K_w: (lambda x: x.rotateAll('X', -0.1)),
            pygame.K_a: (lambda x: x.rotateAll('Y',  0.1)),
            pygame.K_s: (lambda x: x.rotateAll('Y', -0.1)),
            pygame.K_z: (lambda x: x.rotateAll('Z',  0.1)),
            pygame.K_x: (lambda x: x.rotateAll('Z', -0.1))
            """
        }

    def setGameEngine(self, gameEngine):
        self.gameEngine = gameEngine
        
    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
    
    def setScene(self, scene):
        self.scene = scene

    def getScene(self):
        return self.scene

    def setMenu(self, menu):
        self.menu = menu
    
    def getMenu(self):
        return self.menu

    def getWindow(self):
        return self.screen
    
    def run(self):
        """ Create a pygame screen until it is closed. """

        LEFT = 1
        RIGHT = 3

        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.key_to_function:
                        self.key_to_function[event.key](self)
                elif event.type == self.REFRESH:
                    self.scale()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    # Left click , mouse down
                    # This is used when the player
                    # 1. Clicks stuff on the menu / control (e.g start game, exit, level ..)
                    # 2. Add command to queue

                    mouse = pygame.mouse.get_pos()
                    self.scene.onMouseDownEvent(mouse)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    # Right click , mouse down
                    # This is used when the player wants to remove a command from queue
                    """
                    """

            self.screen.fill( (0,0,0) )
            if( self.gameEngine ):
                self.gameEngine.tick()

            if( self.scene ):
                self.scene.draw(self.screen)

            if( self.menu ):
                self.menu.draw(self.screen)

            #loop through our controls and call each event handle where appropriate

            # Draw the controls in order 
            # 1. GameMenu
            # 2. Other Controls 
            BLACK =   (  0,   0,   0)
            WHITE =   (255, 255, 255)
            BLUE =    (  0,   0, 255)
            GREEN =   (  0, 255,   0)
            RED =     (255,   0,   0)
            CONTROL = (240, 240, 240)
            GRAYISH_BLUE = (55, 64, 67)
            #pygame.draw.line(self.screen, GREEN, [0, 0], [50,30], 5)
            #pygame.draw.aaline(self.screen, GRAYISH_BLUE, [0, 100],[640, 100], True)
            #pygame.draw.lines(self.screen, BLACK, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)
            pygame.display.flip()

    def scale(self):
        """
        """

    def clearScreen(self):
        """
        Draw over a colored background
        https://www.reddit.com/r/pygame/comments/3pot4c/how_to_remove_an_object_from_the_screen_in_pygame/
        """
        self.screen.fill( (0,0,0) )

