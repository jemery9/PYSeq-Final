#gameworld.py

import gameengine
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "world"))

import sprite
from sprite import *


class GameWorld:
    def __init__(self, gameEngine, drawEngine):
        self.gameEngine = gameEngine
        self.drawEngine = drawEngine     
        self.sprites    = pygame.sprite.Group()

        characterSprite = CharacterSprite(1)
        characterSprite.rect.x = 0
        characterSprite.rect.y = 0
        rect = characterSprite.rect

        nextX = rect[0] + rect[2]
        nextY = rect[1]

        characterSprite1 = CharacterSprite(1)
        characterSprite1.rect.x = nextX
        characterSprite1.rect.y = nextY

        self.sprites.add(characterSprite)
        self.sprites.add(characterSprite1)
        self.clock = pygame.time.Clock()

    def draw(self, screen):
        """
        Draw the game world 
        """

        self.sprites.update()
        screen.fill( (20,255,140) )
        #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        self.sprites.draw(screen)
 
        #Refresh Screen
        #pygame.display.flip()
 
        #Number of frames per secong e.g. 60
        #clock.tick(60)