#sprite.py
# https://www.pygame.org/docs/ref/sprite.html




import os

import sys
sys.path.insert(0, './../')
import gameengine
from gameengine import *

import pygame
from pygame import *

import spritesheet
from spritesheet import *

import spritestripanim
from spritestripanim import *

import spritesheetxml
from spritesheetxml import *

from enum import Enum

def get_sprites_directory():
    """
    Assuming current working directory is in \game folder
    """
    cwd = (os.getcwd())
    return cwd + "\\..\\sprites\\"


def get_rel_path(path):
    return os.path.join(os.path.dirname(__file__), path)


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, modelType):
        """
        """
        self.modelType = modelType
    
    def draw(self, surface):
        """
        """

class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, characterModelType):
        """
        Instantiate PlayerSprite object
        """
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Should we draw bounding box (around sprite Rect) ? 
        self.drawBoundingBox = False 
        #self.image = pygame.image.load(get_rel_path("./../sprites/house.png")).convert_alpha()

        spritesheet = SpritesheetXML(get_rel_path("./../sprites/character1ss.png"), get_rel_path("./../sprites/character1ss.xml"))
        self.images = [
            spritesheet.getImageByName("up1"), spritesheet.getImageByName("up2"), spritesheet.getImageByName("up3"),
            spritesheet.getImageByName("down1"), spritesheet.getImageByName("down2"), spritesheet.getImageByName("down3"),
            spritesheet.getImageByName("left1"), spritesheet.getImageByName("left2"), spritesheet.getImageByName("left3"),
            spritesheet.getImageByName("right1"), spritesheet.getImageByName("right2"), spritesheet.getImageByName("right3")          
        ]
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]

        self.direction = 0
        self.isWalking = False 
        self.current_time = 0
        self.animation_time = 0.3
        self.pixelsToMove = 0
        self.inc = 0

        #default direction / image = 'down1'

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.images[0].get_rect()

    def animateMove(self, direction, numOfSteps):
        """
        If we want to be precise about it, in turning we need to turn in order e.g
        Command : Up -> Down , we need to Up -> Right -> Down ? 
        """
        self.direction = direction
        self.isWalking = True
    
    def draw(self, surface, coords=(0,0)):
        """
        Draw the player sprite
        """
        # Based on the direction, we determine the index range and extract the array
        direction = self.direction
        index = 0
        if direction == gameengine.Direction.NORTH:
            index = 0
        elif direction == gameengine.Direction.SOUTH:
            index = 3
        elif direction == gameengine.Direction.WEST:
            index = 6
        elif direction == gameengine.Direction.EAST:
            index = 9


        if( self.isWalking == False ):
            inc = 0 # The first image is stationary
    
        dt = 0.01
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.imageIndex = index + self.inc % 3 #(self.index + 1) % len(self.images)
            self.inc += 1
            if( self.inc > 2 ):
                self.inc = 0
            
            self.image = self.images[self.imageIndex]
   
        if( self.image ):
            surface.blit(self.image, coords)
            #surface.blit(self.image, (rect[0], rect[1]))



class TileType(Enum):
    UNBLOCKED = 0 # Tile that can be walked across
    BLOCKED = 1
    START = 2
    DESTINATION = 3

class TileModel(Enum):
    GRASS = 1
    STUMP = 2
    TREE = 3
    HOUSE = 4

    

class TileSprite(pygame.sprite.Sprite):
    def __init__(self, tileSpriteSheet, rect, tileType):
        """
        Instantiate tile spirite ?
        """
        super().__init__()

        self.tileType = tileType
        self.rect = rect 
        self.tileSpriteSheet = tileSpriteSheet

        self.image = self.getTileByType( self.tileType )
        



    def getTileByType(self, tileType):
        tiles = {
            'plain': self.getTileAt(0, 0),
            'blocked': self.getTileAt(7, 2)
        }
        if self.tileType == TileType.UNBLOCKED:
            return tiles['plain']
        elif self.tileType == TileType.BLOCKED:
            return tiles['blocked']
        else: 
            return None
       

    def getTileRectInSpritesheet(self, rowNum, colNum):
        """
        Our tile sheet doesnt have an xml kind of thing so we can only do it hardcoded for now
        """
        sizeInPixels = [33, 33] # 32x32 with a 1px border?
        startingX = 74
        startingY = 0

        return (
            startingX + sizeInPixels[0]*colNum, 
            startingY + sizeInPixels[1]*rowNum,
            sizeInPixels[0], 
            sizeInPixels[1]
        )

    def getTileAt(self, rowNum, colNum):
        rect = self.getTileRectInSpritesheet(rowNum, colNum)
        image = self.tileSpriteSheet.image_at(rect)

        return image 

    def draw(self, surface, coordinates = (0,0)):
        if( coordinates == None ):
            surface.blit(self.image, (self.rect[0], self.rect[1]))
        else:
            surface.blit(self.image, coordinates)
    

class StarSprite(pygame.sprite.Sprite):
    def __init__(self):
        """
        """
        spritesheet = SpritesheetXML(get_rel_path("./../sprites/stars.png"), get_rel_path("./../sprites/stars.xml"))
        self.images = {}
        self.images['3stars'] =  spritesheet.getImageByName("3stars")
        self.images['2stars'] =  spritesheet.getImageByName("2stars")
        self.images['1stars'] =  spritesheet.getImageByName("1stars")
        self.images['0stars'] =  spritesheet.getImageByName("0stars")
        self.selectedImage = None

    def selectImage(self, imageName):
        self.selectedImage = self.images[imageName]

    def setNumOfStars(self, numOfStars):
        imageName = str(numOfStars) + "stars"
        self.selectImage(imageName)

    def draw(self, surface, coordinates = (0,0)):
        """
        """
        if( self.selectedImage ):
            surface.blit(self.selectedImage, coordinates)

    
    