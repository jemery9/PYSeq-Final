# game.py
# where our game runs

import gamewindow
from gamewindow import*

import gamemenu
from gamemenu import *

import gameworld
from gameworld import *

import gameengine
from gameengine import *


class Game:
    def __init__(self):
        self.gameWindow = None
        self.gameWorld = None

    def init(self):
        # init pygame
        pygame.init()

        # init game classes
        gameWindow   = GameWindow("Pyseq", 640, 400)
        gameMenu     = GameMenu(0, 0, 400, 300, gameWindow)
        inGameMenu   = InGameMenu((gameWindow.getWidth() - 250, 0, 400, 300)) 

        gameEngine   = GameEngine.getInstance()
        gameEngine.init(gameWindow)
        #gameEngine.startLevel(1)
        gameWindow.setGameEngine(gameEngine)

        gameLevelMenu = GameLevelMenu()

        gameWindow.setScene(gameMenu)
        gameWindow.run()
    
        self.gameWindow = gamewindow
        self.gameWorld = None

#################
#               #
#               #
#               #
#################
game = Game()
game.init()