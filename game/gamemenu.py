#gamemenu.py

from enum import *
import pygame
from pygame import Rect
import sys
sys.path.insert(0, './interface')
sys.path.insert(0, './world') # spritesheetxml is inside
from interface.control import *

import world.spritesheetxml
from world.spritesheetxml import *

import interface.menu
from interface.menu import *


import gameengine
from gameengine import *


def get_rel_path(path):
    return os.path.join(os.path.dirname(__file__), path)

class InGameMenu(Menu):
    """
    The InGameMenu class handles the in-game-controls such as opening the menu,
    and also the selection of the command queue

    The layout of the menu is as follow :

    The left portion of the window will be the actual game, while \n
    the right portion of the window will be the in game menu
    """
    def __init__(self, rect):
        """
        """
        # Get the rect / coordinates
        # The startingX,Y of the menu is the ending of the board (considering our left-right layout)
        super(InGameMenu, self).__init__()
        self.rect = rect



        ssdir = get_rel_path(".//interface//spritesheet//")

        spritesheetxml = SpritesheetXML(ssdir + "greenSheet.png", ssdir + "greenSheet.xml")
        self.up     = spritesheetxml.getImageByName("green_sliderUp.png")
        self.down   = spritesheetxml.getImageByName("green_sliderDown.png")
        self.left   = spritesheetxml.getImageByName("green_sliderLeft.png")
        self.right  = spritesheetxml.getImageByName("green_sliderRight.png")
        self.circle = spritesheetxml.getImageByName("green_circle.png") # loop
        self.button6 = spritesheetxml.getImageByName("green_button06.png") # Popup, white / green
        self.imgPanel = spritesheetxml.getImageByName("green_panel.png")
        self.imgLargePanel = pygame.transform.rotozoom(self.imgPanel, 0, 2.5)

        greySpritesheetXML = SpritesheetXML(ssdir + "greySheet.png", ssdir + "greySheet.xml")
        self.greyImages = {}
        self.greyImages['grey_button06'] = greySpritesheetXML.getImageByName("grey_button06.png")
        self.greyImages['grey_button06_large'] = pygame.transform.smoothscale(self.greyImages['grey_button06'], (190, 190))

        gameIconSpritesheetXML = SpritesheetXML(ssdir + "sheet_white1x.png", ssdir + "sheet_white1x.xml")
        self.gameIcons = {}
        self.gameIcons['arrowDown'] = gameIconSpritesheetXML.getImageByName("arrowDown.png")
        self.gameIcons['arrowUp'] = gameIconSpritesheetXML.getImageByName("arrowUp.png")
        self.gameIcons['arrowLeft'] = gameIconSpritesheetXML.getImageByName("arrowLeft.png")
        self.gameIcons['arrowRight'] = gameIconSpritesheetXML.getImageByName("arrowRight.png")
        self.gameIcons['return'] = gameIconSpritesheetXML.getImageByName("return.png")
        self.gameIcons['loop'] = self.gameIcons['return']
        self.gameIcons['forward'] = gameIconSpritesheetXML.getImageByName("forward.png")
        self.gameIcons['run'] = self.gameIcons['forward']
        self.gameIcons['cross'] = gameIconSpritesheetXML.getImageByName("cross.png")
        self.gameIcons['clear'] = self.gameIcons['cross']
        self.gameIcons['door'] = gameIconSpritesheetXML.getImageByName("door.png")
        self.gameIcons['home'] = self.gameIcons['door']

        startingX = self.rect[0]
        startingY = self.rect[1]
        self.startingX = startingX
        self.startingY = startingY

        self.nextX = self.startingX
        self.nextY = self.startingY

        self.commandsStartingX = startingX
        self.commandsStartingY = 150


        self.commands = []
        self.commandQueue = CommandQueue(self.commands)
        self.btnCommands = ControlManager()

        iconWidth = 50
        iconHeight = 50


        self.addButton(None, 111, "btnHome", "home", self.gameIcons['home'], self.onHome)
        self.addButton(None, 111, "btnUp", "up", self.gameIcons['arrowUp'], self.onArrowUp)
        self.addButton(None, 111, "btnDown", "down", self.gameIcons['arrowDown'], self.onArrowDown)
        self.addButton(None, 111, "btnLeft", "left", self.gameIcons['arrowLeft'], self.onArrowLeft)
        self.addButton(None, 111, "btnRight", "right", self.gameIcons['arrowRight'], self.onArrowRight)
        self.addButton(None, 111, "btnLoop", "loop", self.gameIcons['loop'], self.onArrowLoop)
        self.addButton(None, 111, "btnRun", "run", self.gameIcons['run'], self.onRunCommands)
        self.addButton(None, 111, "btnClear", "clear", self.gameIcons['clear'], self.onClear)


    def addButton(self, parentControl, controlId, controlName, controlValue, bkgndImage, onMouseDownCallback):
        """
        This function automatically grids the control as necessary
        """
        # Maximum number of controls on the X,Y
        maxX = 4
        maxY = 3

        iconWidth = 50
        iconHeight = 50
        controlValue = "" # Let's empty the control value so no text is shown (temporarily)

        button = Button(self.nextX, self.nextY, iconWidth, iconHeight, None, controlId, controlName, controlValue)
        button.bkgndImage = bkgndImage
        button.register('onMouseDown', onMouseDownCallback)
        self.controlManager.add(button)

        if( self.controlManager.count() % maxX == 0 ):
            self.nextX = self.startingX
            self.nextY += iconHeight
        else:
            self.nextX += iconWidth
            #self.nextY remains the same

    def addCommand(self, parentControl, controlId, controlName, controlValue, bkgndImage, onMouseDownCallback):
        """
        This function automatically grids the control as necessary
        """
        # Maximum number of controls on the X,Y
        maxX = 4
        maxY = 3

        iconWidth = 50
        iconHeight = 50
        controlValue = "" # Let's empty the control value so no text is shown (temporarily)

        index = self.btnCommands.count()

        x = self.commandsStartingX + iconWidth * (index % maxX)
        y = self.commandsStartingY + iconHeight * (index // 4)

        #self.nextY remains the same
        button = Button(x, y, iconWidth, iconHeight, None, controlId, controlName, controlValue)
        button.bkgndImage = bkgndImage
        button.register('onMouseDown', onMouseDownCallback)
        self.btnCommands.add(button)


    def removeCommand(self, index):
        self.commandQueue.removeAt(index)
        self.btnCommands.removeAt(index)

    def clearCommandQueue(self):
        self.commandQueue.clearQueue()
        self.btnCommands.removeAll()

    def onHome(self):
        gameEngine = GameEngine.getInstance()

        gameEngine.goHome()
        gameWindow = gameEngine.getGameWindow()
        gameLevelMenu = GameLevelMenu()
        gameWindow.setScene(gameLevelMenu)

    def onArrowUp(self):
        command = Command(Direction.NORTH, 1)
        self.commandQueue.enqueue(command)
        index = self.commandQueue.size() - 1
        self.addCommand(None, 111, "btnCommandUp", "up", self.gameIcons['arrowUp'], lambda index=index: self.onRemoveCommand(index))

    def onArrowDown(self):
        command = Command(Direction.SOUTH, 1)
        self.commandQueue.enqueue(command)
        index = self.commandQueue.size() - 1
        self.addCommand(None, 111, "btnCommandDown", "down", self.gameIcons['arrowDown'], lambda index=index: self.onRemoveCommand(index))

    def onArrowLeft(self):
        command = Command(Direction.WEST, 1)
        self.commandQueue.enqueue(command)
        index = self.commandQueue.size() - 1
        self.addCommand(None, 111, "btnCommandLeft", "left", self.gameIcons['arrowLeft'], lambda index=index: self.onRemoveCommand(index))

    def onArrowRight(self):
        command = Command(Direction.EAST, 1)
        self.commandQueue.enqueue(command)
        index = self.commandQueue.size() - 1
        self.addCommand(None, 111, "btnCommandRight", "right", self.gameIcons['arrowRight'], lambda index=index: self.onRemoveCommand(index))

    def onArrowLoop(self):
        command = Command(Direction.LOOP, 1) # Every command before this loop, loop it once
        self.commandQueue.enqueue(command)
        index = self.commandQueue.size() - 1
        self.addCommand(None, 111, "btnLoop", "loop", self.gameIcons['loop'], lambda index=index: self.onRemoveCommand(index))

    def onRunCommands(self):
        if( len(self.commands) == 0 ):
            print("Command queue is empty")
            return

        GameEngine.getInstance().getPlayer().runCommand( self.commandQueue )
        self.clearCommandQueue()

    def onClear(self):
        self.clearCommandQueue()

    def onRemoveCommand(self, index):
        self.removeCommand(index)


# Handle events within our menu region/rect
    def onMouseDownEvent(self, mousePos):
        super(InGameMenu, self).onMouseDownEvent(mousePos)

        for i in range(len(self.btnCommands.controls)):
            print("clicked index : %d | %d" % (i, self.btnCommands.count()))
            control = self.btnCommands.controls[i]
            rect = Rect(control.getRect())
            print("%d %d" % (mousePos[0], mousePos[1])) #
            if rect.collidepoint(mousePos):
                control.onMouseDownEvent()

    def onMouseUpEvent(self, mousePos):
        super(InGameMenu, self).onMouseUpEvent(mousePos)

        for i in range(len(self.btnCommands.controls)):
            control = self.btnCommands.controls[i]
            rect = Rect(control.getRect())
            print("%d %d" % (mousePos[0], mousePos[1])) #
            if rect.collidepoint(mousePos):
                control.onMouseUpEvent()

    def draw(self, window):
        """
        Draw the in-game-menu
        """
        super(InGameMenu, self).draw(window)

        for i in range(len(self.btnCommands.controls)):
            control = self.btnCommands.controls[i]
            control.draw(window)


class GameLevelMenu(Menu):
    def __init__(self):
        """
        The game level menu will overtake the entire screen
        """
        super(GameLevelMenu, self).__init__()

        # Generate button for each level
        fileNames = self.getAllLevels()
        self.btnLevels = self.createAllLevelUI(fileNames)
        self.controlManager.addList(self.btnLevels)
        self.controlManager.printControls()


    def getAllLevels(self):
        """
        Get all the levels available by checking the file name
        """
        fileNames = LevelConfig.getAllFileNames()
        return fileNames

    def createAllLevelUI(self, levelNames):
        """
        Create all the user interface for each level e.g button
        """
        btnLevels = []
        index = 0

        btnWidth = 150
        btnHeight = 20
        padding = 20
        for levelName in levelNames:
            # adjust the x,y***
            x = (index % 3) * btnWidth + padding
            y = (index // 3) * btnHeight + padding

            levelNum = int(levelName.replace('level', ''))

            # create button
            button = Button(x, y, btnWidth, btnHeight, None, 1000, "controlName", levelName)
            button.setBkgndColor( (255,255,255) )
            button.register('onMouseDown', lambda levelNum=levelNum: self.startLevel(levelNum))

            btnLevels.append(button)
            index += 1

        return btnLevels

    def startLevel(self, levelNum):
        """
        Callback that is called when user has clicked a level to begin
        """
        #print("startLevel %d" % (levelNum))
        gameEngine = GameEngine.getInstance()
        gameEngine.startLevel(levelNum)

        gameWindow = gameEngine.getGameWindow()
        inGameMenu = InGameMenu((gameWindow.getWidth() - 250, 0, 400, 300))
        gameWindow.setScene(inGameMenu)


    def draw(self, window):
        """
        Draw our menu/scene for our level selection (after starting game)
        """
        #window.fill( (0,0,0) ) # window fill is necessary
        super(GameLevelMenu, self).draw(window)

class GameMenu(Menu):
    def __init__(self, x, y, width, height, gameWindow):
        """
        """
        super(GameMenu, self).__init__()
        window = gameWindow.getWindow()
        self.gameWindow = gameWindow

        # Controls
        btnStartGame = Button(0, 0, 150, 20, None, 1001, "controlName", "Start Game")

        #btnStartGame.register('onMouseDown', )
        btnStartGame.setBkgndColor( (255,255,255) )
        self.btnStartGame = btnStartGame
        self.btnStartGame.register('onMouseDown', self.onGameStart)
        self.controlManager.add(btnStartGame)

        # Fill white background
        self.btnStartGame.centerXY(window.get_rect())
        #self.btnStartGame.centerX(window.get_rect())

    def draw(self, window):
        #window.fill( (0,0,0) )
        super(GameMenu, self).draw(window)

    def onGameStart(self):
        #print("Start Game !! Please choose your level")
        gameLevelMenu = GameLevelMenu()
        self.gameWindow.setScene(gameLevelMenu)












