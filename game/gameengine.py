#game engine class
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "physics"))
sys.path.append(os.path.join(os.path.dirname(__file__), "world"))
sys.path.append(os.path.join(os.path.dirname(__file__), "audio"))
#print(os.path.dirname(__file__))
#print(sys.path)
import threading
import configparser
from configparser import * 
import copy
from enum import Enum

import sprite
from sprite import *
from pygame.locals import Color, KEYUP, K_ESCAPE, K_RETURN
import spritesheet
from spritesheet import spritesheet
from spritestripanim import SpriteStripAnim

import random

import audio
from audio import Audio

def get_rel_path(path):
    return os.path.join(os.path.dirname(__file__), path)

# ENUMS
class Direction(Enum):
    NORTH   = 0
    SOUTH   = 1
    EAST    = 2
    WEST    = 3
    LOOP    = 4

class CommandType(Enum):
    BASIC = 0 # The 4 standard directions
    LOOP = 1  # Loop any other commands
# ENUMS


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def asList(self):
        return [self.x, self.y, self.z]

    def asXYList(self):
        return [self.x, self.y]

    def asString(self):
        return "{} {} {}".format(self.x, self.y, self.z)

    def asTuple(self):
        return (self.x, self.y, self.z)

    def asXYTuple(self):
        return (self.x, self.y)

    
    def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        """
        The implementation of math.isclose(a, b, rel_tol)
        """
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def isZero(self):
        """
        We can't be sure if the float will be exactly zero, so we can only do the next best -
        as close to zero as possible.
        """
        x = self.x
        y = self.y
        z = self.z
        if( self.isclose(x, 0.0, abs_tol=0.001) and
            self.isclose(y, 0.0, abs_tol=0.001) and 
            self.isclose(z, 0.0, abs_tol=0.001) ):
            return True
        return False
    
    def roundInt(self):
        """
        Perform normal integer-rounding operation on x, y, z
        """
        self.x = int(round(self.x))
        self.y = int(round(self.y))
        self.z = int(round(self.z))

# OVERLOAD OPERATORS
    def forceType(self, other):
        """
        This function is to allow e.g Vector3 * 7 
        """
        if isinstance(other, Vector3):
            return other
        if isinstance(other, int):
            return Vector3(other, other, other)
        if isinstance(other, float):
            return Vector3(other, other, other)

        raise ValueError("Vector3 type of variable other is not supported")

    # self + other
    def __add__(self, other):
        other = self.forceType(other)
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector3(x, y, z)
    
    # self += other
    def __iadd__(self, other):
        other = self.forceType(other)
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    # self - other
    def __sub__(self, other):
        other = self.forceType(other)
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector3(x, y, z)

    # self -= other
    def __isub__(self, other):
        other = self.forceType(other)
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    # self / other
    def __div__(self, other):
        other = self.forceType(other)
        x = self.x / other.x
        y = self.y / other.y
        z = self.z / other.z
        return Vector3(x, y, z)  

    def __truediv__(self, other):
        return self.__div__(other)

    # self /= other
    def __idiv__(self, other):
        other = self.forceType(other)
        self.x /= other.x
        self.y /= other.y
        self.z /= other.z
        return self

    def __eq__(self, other):
        if( self.x == other.x and
            self.y == other.y and
            self.z == other.z ):
            return True
        return False

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)
# OVERLOAD OPERATORS

    def calc2DDistanceTo(self, other):
        """
        Return  1 for > 
        Return  0 for == 
        Return -1 for <
        """
    
    def calc3DDistanceTo(self, other):
        """
        """


    def deepcopy(self):
        return Vector3(self.x, self.y, self.z)


class Tile:
    # Should these values be retrieved from the spritesheet instead of hardcoding?
    pixelSizeX = 33
    pixelSizeY = 33

    def __init__(self, tileType, tileModel, rect=None):
        # Type of tile 
        self.type       = tileType
        # Tile properties (sprite)
        self.model      = tileModel
        self.tileSprite = None
        self.rect       = rect 
        # Other objects (sprites) on this same tile
        self.objects    = []
                
        imgHouse = pygame.image.load( get_rel_path("./sprites/house.png") ).convert_alpha()

        tileSpriteSheet = spritesheet( get_rel_path('./sprites/tiles.png') )
        plainTileSprite = TileSprite(tileSpriteSheet, (0,0,32,32), TileType.UNBLOCKED)
        blockedTileSprite = TileSprite(tileSpriteSheet, (32,32,32,32), TileType.BLOCKED)

        self.tileSprite = plainTileSprite

        if( tileType == TileType.BLOCKED ):
            self.tileSprite = blockedTileSprite
        if( tileType == TileType.DESTINATION ):
            self.tileSprite = plainTileSprite
            self.objects.append(imgHouse)

    def isBlocked(self):
        return (self.type == TileType.BLOCKED)

    def isUnblocked(self):
        return (self.type == TileType.UNBLOCKED) # Check the enum TileType

    def draw(self, surface, coords=(0,0)):
        """
        """
        if( self.tileSprite ):
            self.tileSprite.draw(surface, coords)

        if( len(self.objects) > 0 ):
            for obj in self.objects:
                if( isinstance(obj, pygame.sprite.Sprite) ):
                    obj.draw(surface)
                else:
                    surface.blit(obj, coords)
                



class Board:
    def __init__(self, width, height, surface):
        self.setBoard(width, height, surface)
        # boardArray is an array of Tiles
        self.unit = 10 # not in use
        self.boardArray = []
        self.startPos = Vector3(0,0,0)
        self.endPos = Vector3(0,0,0)

    def getBoard(self):
        return self

    def setBoard(self, width, height, surface):
        self.height = height 
        self.width  = width 
        self.numOfTiles = self.height * self.width
        self.surface = surface
    
    def getSurface(self):
        return self.surface
    

    def convertIndexToCoordinates(self, index):
        """
        Given the boardArray index, determine the world coordinates based on
        the board width and height
        """        
        x = index % self.height
        y = (int)( (index - x) // self.height )

        return (x, y)

    def convertIndexToPixelCoordinates(self, index):
        row = int(index / self.width)
        col = index % self.width
        
        #print('%d , %d' % (col, row))

        return (0+col*Tile.pixelSizeX, 0+row*Tile.pixelSizeY)

    def convertCoordinatesToIndex(self, coordinates):
        """
        Given the coordinates on the board, determine the boardArray index based on
        the board width and height
        """
        y = coordinates[1]     
        x = coordinates[0] 
        #print ("cc %d %d" % (x, y))
        if( y == 0 ):
            return int(x)
        
        return int(y * self.width + x)

    def convertCoordinatesToPixelCoordinates(self, coords):
        return (coords[0] * Tile.pixelSizeX, coords[1] * Tile.pixelSizeY)


    def generateBoard(self, levelConfig):
        """
        Generate board based on config provided
        """

        # Loop through board
        for rowNum, row in enumerate(levelConfig.board):
            for colNum, tile in enumerate(row):
                # Perform lookup
                tileData = levelConfig.tileLookup(tile)
                tileType = TileType(int(tileData['type']))
                tileModel = int(tileData['model'])

                if( tileType == TileType.DESTINATION ):
                    # Change end point
                    self.endPos = Vector3(colNum, rowNum, 0)
                    print("endPos detected to be %d %d" % (colNum, rowNum))

                if ( tileType == TileType.START ):
                    self.startPos = Vector3(colNum, rowNum, 0)
                    GameEngine.getInstance().getPlayer().getCharacter().teleport(self.startPos) # Move character to starting pos
                    print("startPos detected to be %d %d" % (colNum, rowNum))

                # Create tile
                tile = Tile(tileType, tileModel)
                self.boardArray.append(tile)                

        return self.boardArray

    def generateEmptyBoard(self):
        """
        Based on the length and width, generate an array of Tile accordingly
        """    
        self.boardArray = [Tile(TileType.UNBLOCKED, 0)] * (self.width * self.height)
        return self.boardArray

    def generateRandomBoard(self):
        """
        Generate random Tile (s)
        """    
        for i in range(self.numOfTiles):
            tile = Tile( TileType(random.randint(0, 1)), 0)
            self.boardArray.append( tile )

    def printAsArray(self):
        """
        """

    def hasRouteToExit(self):
        """
        Determine if the character have at least 1 path from start till end
        """
        boardArray = self.boardArray
        

    def resetBoard(self):
        """
        If the player fails to succeed in completing a path, reset the board as an option
        """
    

    def canMoveTo(self, position):
        """
        Check if the position/coordinates specified is one where the character can move to \n
        @position : Vector3 object
        """
    
        index = self.convertCoordinatesToIndex( position.asList() )
        #print("index %d %d" % (index, len(self.boardArray)))
        
        if( index > len(self.boardArray) ):
            # Index out of bounds
            # Character is going outside the boundary of the board !!
            return False
        
        if( position.x > (self.width-1) or position.y > (self.height-1) ):
            # Out of X or Y boundary . 
            # -1 because x starts from 0 whereas width starts from 1
            return False

        print("canmoveto index : " + str(index))

        tile = self.boardArray[int(index)]
        #return tile.isUnblocked()
        return not tile.isBlocked() # by default tiles unblocked

    def isAtExit(self, playerPos):
        
        if( playerPos == self.endPos ):
            return True

        endPos = self.endPos
        # For floats, it's hard to get == due to how floats (and binary) work.
        # So we need to check if it's within the grid/square
        # *kind of checking of collision
        if( ( playerPos.x > endPos.x and playerPos.x < (endPos.x + 0.999) ) and
            ( playerPos.y > endPos.y and playerPos.y < (endPos.y + 0.999) )
        ):
            return True
         
        if( ( playerPos.x < endPos.x and playerPos.x > (endPos.x - 0.999) ) and
            ( playerPos.y < endPos.y and playerPos.y > (endPos.y - 0.999) )
        ):
            return True


        return False

    def tick(self):
        raise NotImplementedError

    def draw(self, surface, coords=(0,0)):
        """
        Draw the game board( which is basically all the tiles )
        """
        #surface.fill( (0,0,0) ) 

        for i in range(len(self.boardArray)):
            tile = self.boardArray[i]
            coords = self.convertIndexToPixelCoordinates(i)
            #print("Board coords {0}".format(coords))
            tile.draw(surface, coords)
        
        # Draw the endpos sprite (house)



# There may not be a need for this class but who knows...
class Physics:
    def __init__(self):
        """
        """
        self.acceleration = [0, 0]
        self.velocity = [0, 0]

    def canMove(self):
        """
        """
    def canJump(self):
        """
        """ 
    

# Player class 
# Holds various information about the current player

class Player:
    """
    Player class is the class that handles the player(user) information.
    It is different from the Character class in that the Character class is the in-game entity
    """
    def __init__(self):
        """
        """
        super(Player, self).__init__()
        self.character = Character("zelda", 1)
        self.previousMoves = []
        self.currentMove = []
        self.isMenu = True

    def getCharacter(self):
        return self.character
    
    def isAtMenu(self):
        return self.isMenu

    def startLevel(self, level):
        self.character.startLevel(level)

    def runCommand(self, commandQueue):
        self.character.runCommand(commandQueue)

    def tick(self):
        """
        On each player tick, we should 
        1. Update player information 
        2. Update character information 
        3. Redraw character & player related sprites
        """
        self.character.tick()


class Command:
    def __init__(self, direction, numOfSteps=1):
        self.commandType = 0 # 0 For normal, 1 for loop ?
        self.direction = direction
        self.numOfSteps = numOfSteps
    
class CommandQueue:
    def __init__(self, commands):
        self.queue      = commands
        self.loopsLeft  = 1 # -1 for infinite loop

    def peek(self, index=0):
        return self.queue[index]
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        self.queue.pop(0) # remove element at index 0 

    def removeAt(self, index):
        self.queue.pop(index)

    def count(self):
        return len(self.queue)
    
    def size(self):
        return self.count()

    def getQueue(self):
        return self.queue

    def extractQueue(self, indexFrom, indexTo):
        extractedCommands = []
        for i in range(indexFrom, indexTo):
            extractedCommands.append( self.queue[i] )
        
        return CommandQueue(extractedCommands)

    def getLoopsLeft(self):
        return self.loopsLeft

    def setInfiniteLoop(self):
        self.loopsLeft = 100 # 100 should be enough ba ?

    def clearQueue(self):
        self.queue = []



class Entity:
    def __init__(self):
        """
        """
class Actor:
    def __init__(self):
        """
        """

class Controller(Actor):
    """
    See unreal engine Pawn vs Controller
    If our player class gets too big this may be the only way
    """
    def possess(self, actor):
        """
        Possess a player
        """
    def unpossess(self):
        """
        Unpossess actor in possession
        """

class CharacterModel(Enum):
    GIRL    = 0,
    BOY     = 1,
    THIEF   = 2


class Character:
    """
    Character class. \n
    Character class holds information about the in-game character the player has chosen to use \n

    *If the Character class bubbles up, we may want to split it into Pawn and Controller (see Unreal Engine)
    """
    def __init__(self, characterName, characterModel):
        """
        """
        # Properties
        self.characterName  = characterName
        self.characterModel = 1
        self.characterSprite = CharacterSprite(self.characterModel)
        self.isInGame = False
        self.board = None

        # Character movement
        self.position = Vector3(0,0,0)
        self.isWalking = False
        self.deltas = []
        self.speed = 0.02 # not really speed also but like velocity? not sure how to describe this variable..
        self.facingDirection = Direction.NORTH
        self.canMove = True
        self.spritePosition = Vector3(0,0,0)
        self.spriteFacingDirection = Direction.NORTH

        self.displayDebugInformation = False # Display info such as character coordinates

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def startLevel(self, level):
        self.level = level
        self.board = level.board
        self.isInGame = True 


    def canMove(self):
        return self.canMove

    def toggleMovement(self, toggle):
        self.canMove = toggle



    def executeCommand(self, commandQueue, loopsLeft):
        """
        executeCommand does the actual command execution + handling of loops
        """
        if( loopsLeft <= 0 ):
            return 

        for i in range(commandQueue.size()):
            command = commandQueue.peek(i)
            direction = command.direction
            numOfSteps = command.numOfSteps

            if( direction == Direction.LOOP ):
                subCommandQueue = commandQueue.extractQueue(0, i) # Loop every other command thus far
                self.executeCommand(subCommandQueue, 1)
            else:
                self.move(direction, numOfSteps)        

        return self.executeCommand(commandQueue, loopsLeft - 1)

    def runCommand(self, commandQueue):
        # run commands
        if not isinstance(commandQueue, CommandQueue):
            raise ValueError("runCommand(self, commandQueue) : commandQueue must be of type CommandQueue")
            
        # reset deltas
        numOfCommands = commandQueue.count()
        numOfLoops = commandQueue.getLoopsLeft()
        self.executeCommand(commandQueue, numOfLoops)

        # check final position (we don't have to do that here anymore)
        """
        if( self.board.isAtExit(self.position) ):
            print("Player has reached the end in {0} commands".format(numOfCommands))
            self.toggleMovement(False)
            self.level.completeLevel()

            # Display completed level screen
            # - Display number of stars, points etc..
            # - Display buttons - retry level, next level.
        else:
            print("Player failed to complete this level. Try again?")
        """

    def loopMove(self, loopCommandQueue, numOfTimes):
        """
        Loop a command queue. 
        Note that a command queue can be a subset of another command queue ( This is where the loop forms )
        """
        if( numOfTimes <= 0 ):
            return 

        for _ in range(numOfTimes):
            self.runCommand(loopCommandQueue)

    def animateMove(self, direction, numOfSteps):
        """
        Animate the movement of the character
        """
        self.characterSprite.animateMove(direction, numOfSteps)

    def setPosition(self, position):
        """
        Only changes the character coordinates (not the sprite coordinates) \n
        To change both the character and sprite, use .teleport(coords)
        """
        if( self.canMove ):
            self.position = position

    def teleport(self, teleportTo):
        if( self.canMove ):
            self.position = teleportTo
            self.spritePosition = teleportTo

    def walkTo(self, delta):
        if( self.canMove ):
            self.deltas.append( delta )
            self.isWalking = True

    def startWalking(self, delta):
        if( self.canMove ):
            self.deltas.append( delta ) # i think the problem with multi-directional movement lies here? maybe my walking algorithm has a problem :x
            self.isWalking = True

    def stopWalking(self): 
        self.isWalking = False

    def getDirectionByDelta(self, delta):
        if delta.x < 0.0 : 
            return Direction.WEST
        if delta.x > 0.0 :
            return Direction.EAST
        if delta.y < 0.0 :
            return Direction.NORTH
        if delta.y > 0.0 :
            return Direction.SOUTH

    def walk(self):
        self.spriteFacingDirection = self.getDirectionByDelta(self.deltas[0]) 
        change = self.getDisplacement()

        # KINDA WORKS, BUT BUGGY 
        self.deltas[0] -= change
        self.spritePosition += change
     
        if( self.deltas[0].isZero() ):
            self.deltas.pop(0)

        if( len(self.deltas) == 0 ): #self.delta.isZero() or 
            self.stopWalking()

            # adjust coordinates (due to floating point being unprecise)
            # perform normal rounding
            # this kind of acts like 'animationWalkDelta' though i'm not too sure how to implement it so i will leave it ofr now
            self.spritePosition.roundInt()
    
    def getDisplacement(self):
        speed = self.speed
        if( self.spriteFacingDirection == Direction.NORTH ):
            change = Vector3(0, -speed, 0)
        elif( self.spriteFacingDirection == Direction.SOUTH ):
            change = Vector3(0, speed, 0)
        elif( self.spriteFacingDirection == Direction.EAST ):
            change = Vector3(speed, 0, 0)
        elif( self.spriteFacingDirection == Direction.WEST ) :
            change = Vector3(-speed, 0, 0)
        else:
            raise ValueError("Direction is not recognized")

        return change        

    def calculateDelta(self, newPosition, direction):
        """
        """

    def move(self, direction, numOfSteps):
        """

        Returns the final position (whether character moved or not)
        """
        # [Up, Down, Left, Right]
        # [North, South, West, East]
        
        # Turn character direction
        self.facingDirection = direction
        
        # **rewrite algorithm here?
        newPosition = self.position.deepcopy() # use a deepcopy otherwise we will end up copying the reference
        if( self.facingDirection == Direction.NORTH ):
            newPosition.y -= numOfSteps
            delta = Vector3(0, -numOfSteps, 0)
        elif( self.facingDirection == Direction.SOUTH ):
            newPosition.y += numOfSteps
            delta = Vector3(0, +numOfSteps, 0)
        elif( self.facingDirection == Direction.EAST ):
            newPosition.x += numOfSteps
            delta = Vector3(numOfSteps, 0, 0)
        elif( self.facingDirection == Direction.WEST ) :
            newPosition.x -= numOfSteps
            delta = Vector3(-numOfSteps, 0, 0)
        else:
            raise ValueError("Direction is not recognized")

        if( self.board.canMoveTo(newPosition) ):
            # Modify position 
            self.setPosition(newPosition)
            # Animate character movement
            self.walkTo(delta)
            self.animateMove(direction, numOfSteps)

        else: 
            print("Can't move to tile")
            
        return self.position

    def turn(self, direction):
        return self.move(direction, 0)

    def tick(self):
        if( self.isWalking ):
            self.walk()
        
        # We need to work on this. Because we want to detect if user is at end whether movement is walk or teleport
        if( not self.isWalking ):       
            if( self.board and self.board.isAtExit(self.position) ):
                self.toggleMovement(False)
                self.level.completeLevel()


        if( self.board and self.characterSprite ):
            # If has movement, then animate
            # else, just draw as normal? idk man 
            surface     = self.board.getSurface()
            pixelCoords = self.board.convertCoordinatesToPixelCoordinates(self.spritePosition.asTuple())

            self.characterSprite.draw(surface, pixelCoords)       



class Level:
    def __init__(self, levelNum):
        self.maxStars = 3
        self.levelNum = levelNum
        self.starSprite = StarSprite()        
        self.isCompleted = False

        self.allowedCommands = [CommandType.BASIC, CommandType.LOOP]
        self.board = None

    def getStars(self, numOfSteps, maxSteps):
        """
        Maximum of 3 stars.
        We need to inverse it because the lesser number of steps = better score, so we do 1-x

        or we could invert it to be min stars(the best score)
        """
        return (1 - (numOfSteps/maxSteps)) * self.maxStars


    def getLevelConfig(self, levelNum):
        """
        Get the config file for the specified levelNum
        """
        levelConfig = LevelConfig.loadFileByLevelNum( levelNum )
        return levelConfig
    
    def startLevel(self, levelNum, surface):
        """
        """
        self.levelNum = levelNum

        # Based on the level, find the level config file
        levelConfig = self.getLevelConfig(levelNum)
        boardWidth = levelConfig.boardWidth
        boardHeight = levelConfig.boardHeight

        # Create the game board
        #self.board = Board(10, 10, surface)
        self.board = Board(boardWidth, boardHeight, surface)
        self.board.generateBoard(levelConfig)

        #self.board.generateEmptyBoard()
        #self.board.generateRandomBoard()

        # Start Audio
        Audio.load('Pim Poy.wav')
        Audio.play(-1)
        


    def completeLevel(self):
        """
        Once the player complete the level, do action
        """
        self.isCompleted = True

        # Save level completion progres into settings/cfg
        # Show the stars
        # numOfStars = self.getStars(numOfSteps, maxSteps)
        self.starSprite.setNumOfStars(3)

        # End Audio
        Audio.stop()

    def resetLevel(self):
        """
        Reset the board and other necessary stuff
        """
        self.board.resetBoard()
        # reset character position to start
        GameEngine().getPlayer().getCharacter().teleport(self.startPos)

    @staticmethod
    def loadLevel(self, levelNum):
        """
        Load the level.
        1. Load the config file for the specified levelNum
        2. Parse the config and pass it to Level object

        *All filenames have the structure levelX.txt where X is levelNum
        """
        levelConfig = LevelConfig.loadFileByLevelNum(levelNum)

        level = Level(levelNum)
        level.allowedCommands = levelConfig.parseAllowedCommands( level.allowedCommands )
        level.board = levelConfig.parseBoard( levelConfig.board )

        return level

    def tick(self):
        if( self.board ):
            self.board.draw(self.board.getSurface())
        
        if( self.isCompleted ):
            starCoords = (50,50) # We should make it center and maybe resize it?
            self.starSprite.draw(self.board.getSurface(), starCoords)


def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print (k)
                dumpclean(v)
            else:
                print ('%s : %s' % (k, v))
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print (v)
    else:
        print (obj)




from os import listdir
from os.path import isfile, join

class LevelConfig:
    directory = '/levels/'
    extension = '.txt'
    def __init__(self):
        """
        """
        self.directory = '/levels/'

        # Level properties
        self.levelNum = None
        self.allowedCommands = None
        self.board = None
        self.boardWidth = 0
        self.boardHeight = 0
        self.key = {} # Initialize an empty dict() .

        # Other
    

    def parseTile(self, tile):
        """
        """
    def parseBoard(self, board):
        """

        """
    def tileLookup(self, char):
        """
        Look up tile information in config 

        char = symbol = section
        """    
        return self.key[char]

    def parseAllowedCommands(self, allowedCommands):
        """
        allowedCommands is an list of integer. reference CommandType(Enum) for more information on the values
        """
        allowedCommands = allowedCommands.split(",")
        # allowedCommands is a list of levels (in string). Map it to an integer list
        allowedCommands = list(map(int, allowedCommands))

        return allowedCommands

    def parseBoardWidth(self, boardWidth):
        return int(boardWidth)

    def parseBoardHeight(self, boardHeight):
        return int(boardHeight)

    @staticmethod
    def getAllFileNames():
        extension = LevelConfig.extension
        print(extension)
        path = LevelConfig.getDirectory()

        files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(extension)]
        fileNames = []
        levels = []
        for file in files:
            fileName = file    
            levelNum = fileName.replace('level', '')
            levelNum = fileName.replace(extension, '')

           
            fileNames.append(fileName)
            levels.append(levelNum)

        return levels

    @staticmethod
    def getDirectory():
        dirPath = os.path.dirname(os.path.realpath(__file__))
        return dirPath + LevelConfig.directory # maybe use relative directory


    @staticmethod
    def loadFile(fileName):
        """
        Load the specified file, and return an instance of a LevelConfig object
        
        *Warning : Exception/error handling is not done
        """
        # Initialize 
        filePath = LevelConfig.getDirectory() + fileName
        levelConfig = LevelConfig()

        configParser = ConfigParser()
        configParser.read(filePath)
        print("filepath : %s" % (filePath))

        # Push config values into object
        levelConfig.levelNum           = configParser.get("level", "levelNum")
        levelConfig.allowedCommands    = configParser.get("level", "allowedCommands")

        levelConfig.board              = configParser.get("level", "board").split("\n") 
        levelConfig.boardHeight        = len(levelConfig.board)
        levelConfig.boardWidth         = len(levelConfig.board[0])
        
        # Load subsequent sections which are the tile indicator/key mapping value
        # 1. Level (loaded)
        # 2. ...
        # 3. ... 
        # 
        for section in configParser.sections():
            if len(section) == 1:
                desc = dict(configParser.items(section))
                levelConfig.key[section] = desc

        print(levelConfig.board)
        print(levelConfig.boardWidth)
        print(levelConfig.boardHeight)

        print("levelconfigkey")
        #print(levelConfig.key['#']['type'])
        #print(levelConfig.key['#']['model'])

        dumpclean(levelConfig.key)

        # Parse config values in object

        return levelConfig

    @staticmethod
    def loadFileByLevelNum( levelNum ):
        levelFileName = "level" + str(levelNum) + LevelConfig.extension
        return LevelConfig.loadFile( levelFileName )


class Input:
    """
    Input class handles all mouse and keyboard inputs, before passing them down the GameEngine line(to all the entities)
    """
    def __init__(self):
        """
        """

class Singleton:
    """
    https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons/33201#33201

    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def getInstance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class GameEngine:
    
    def __init__(self):
        """
        drawer : class that handles the drawing of the ui. can be 2d/3d,
                as long as it follows the interface methods
        """

        self.gameSurface = None
        self.gameWindow = None

        # gameSurface refers to the window that is to be drawn on
        self.player = None

        # Clock Speed / Tick Rate / Frames per Second
        self.tickrate = 30

        # Only when the actual game start will this be filled
        self.isAtMenu = True 
        self.isInGame = False
        self.level = None

        # Game Control Constants
        self.GAMECONTROL_UP = 0
        self.GAMECONTROL_DOWN = 1
        self.GAMECONTROL_LEFT = 2
        self.GAMECONTROL_RIGHT = 3
        self.GAMECONTROL_LOOP = 4

        self.gameControls = {
            
        }

        self.hasInit = False

    def init(self, gameWindow):
        self.gameWindow = gameWindow # GameWindow class
        self.window = gameWindow.getWindow() 
        self.player = Player()

        self.hasInit = True
    
    def getGameWindow(self):
        return self.gameWindow

    def getWindow(self):
        return self.window

    def hasInit(self):
        return self.hasInit

    def getPlayer(self):
        return self.player

    def start(self):
        """
        Start the GameEngine. 
        1. Start GameMenu
        """

    def stop(self):
        """
        """

    def goHome(self):
        self.isAtMenu = True
        self.isInGame = False

        # Stop audio when home screen, or level completed
        Audio.stop() 
    
    def startLevel(self, levelNum): 
        """
        Instantiate a instance of Level class.
        """
        self.level = Level(levelNum)
        self.level.startLevel(levelNum, self.window)
        self.player.startLevel(self.level)

        self.isAtMenu = False
        self.isInGame = True
        
    def tick(self):
        """
        On each game tick, execute ...
        """
        if( self.isInGame ):
            if( self.level ):
                self.level.tick()
            
            if( self.player ):
                self.player.tick()
            