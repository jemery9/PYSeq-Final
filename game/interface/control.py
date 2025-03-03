# control.py

from enum import * 
import collections
import pygame
from pygame import Rect
import os

def get_rel_path(path):
    return os.path.join(os.path.dirname(__file__), path)

class Control:
    
    def __init__(self, x, y, width, height, parentControl, controlId, controlName=None, controlValue=None):
        # Control properties
        self.bkgndColor     = (0,0,0)
        self.frgndColor     = (255,255,255)
        self.width          = width
        self.height         = height
        self.minWidth       = width  # 
        self.minHeight      = height #
        self.maxWidth       = width  #
        self.maxHeight      = height #
        self.isVisible      = True
        self.x              = x
        self.y              = y
        self.parentControl  = parentControl
        self.bkgndImage     = None #self.loadBkgndImage(os.path.join(os.path.dirname(__file__), 'button.png'))
        #self.setBkgndImage(os.path.join(os.path.dirname(__file__), 'button.png'))

        # Control identifiers
        self.controlId      = controlId
        self.controlName    = controlName
        self.controlValue   = controlValue
        # Event Handlers
        self.handlers       = collections.defaultdict(set)

    # Control functions
    def draw(self, surface):
        """
        This function must be overrided 
        """
        if( self.bkgndImage != None ):
            surface.blit(self.bkgndImage, (self.x, self.y))
        
    
    def hide(self):
        self.isVisible = False
    
    def show(self):
        self.isVisible = True

    def setWidth(self, newWidth):
        if( newWidth > self.maxWidth ):
            self.maxWidth = newWidth
        if( newWidth < self.minWidth ):
            self.minWidth = newWidth
        
        self.width = newWidth
    
    def setHeight(self, newHeight):
        if( newHeight > self.minHeight ):
            self.minHeight = newHeight
        if( newHeight < self.minHeight ):
            self.minHeight = newHeight
        
        self.height = newHeight       

    def setBkgndColor(self, color):
        self.bkgndColor = color

    def loadBkgndImage(self, imagePath):
        bkgndImage = pygame.image.load( imagePath ).convert_alpha()
        return bkgndImage

    def setBkgndImage(self, imagePath):
        self.bkgndImage = self.loadBkgndImage(imagePath)
    
        imageRect = self.bkgndImage.get_rect()
        self.setWidth(imageRect[2])
        self.setHeight(imageRect[3])
       

    def getRect(self):
        return (self.x, self.y, self.width, self.height)
        #return Rect(self.x, self.y, self.width, self.height)

    def centerXY(self, parentRect):
        """
        Center the XY relative to parentRect
        """
        #print("%d %d %d %d" % (parentRect[0], parentRect[1], parentRect[2], parentRect[3]) )
        x = parentRect[0] + (parentRect[2] // 2) - (self.width // 2)
        y = parentRect[1] + (parentRect[3] // 2) - (self.height // 2)

        self.x = x
        self.y = y
        #print("calc x:%d y:%d" % (x,y))
        return (x, y, self.width, self.height)

    def centerX(self, parentRect):
        """
        Center X relative to parentRect
        """
        x = parentRect[0] + (parentRect[2] // 2) - (self.width // 2)
        self.x = x

        return (x, self.y, self.width, self.height)

    def centerY(self, parentRect):
        """
        Center Y relative to parentRect
        """
        y = parentRect[1] + (parentRect[3] // 2) - (self.height // 2)
        self.y = y

        return (self.x, y, self.width, self.height)

    # Event Handlers
    def register(self, event, callback):
        self.handlers[event].add(callback)

    def fire(self, event, **kwargs):
        for handler in self.handlers.get(event, []):
            handler(**kwargs)

    def onMouseDownEvent(self, ):
        self.fire('onMouseDown')
    
    def onMouseUpEvent(self):
        self.fire('onMouseUp')

    def onHoverEvent(self):
        self.fire('onHoverEvent')

    def onDoubleMouseDownEvent(self):
        self.fire('onDoubleMouseDown')
    
    def onDoubleMouseUpEvent(self):
        self.fire('onDoubleMouseUp')

    def isDoubleMouseUp(self):
        """
        This function should be only called within onMouseUp callback
        """
        if( self.lastMouseUp == None ):
            return False

        timeNow     = time.time()
        timeDiff    = timeNow - self.lastMouseUp
        self.lastMouseUp = timeNow

        return (timeDiff < 0.5)

    def isDoubleMouseDown(self):
        """
        This function should be only called within onMouseUp callback
        """
        if( self.lastMouseDown == None ):
            return False

        timeNow     = time.time()
        timeDiff    = timeNow - self.lastMouseDown
        self.lastMouseDown = timeNow

        return (timeDiff < 0.5)

class Font:
    def __init__(self, fontName, fontSize, isCustomFont = False):
        """
        If isCustomFont is true, fontName becomes the path to the font file (.ttf)
        """
        pygame.font.init()
        self.fontName = fontName
        self.fontSize = fontSize
        self.isCustomFont = isCustomFont

    def getFont(self):
        if( self.isCustomFont == False ):
            return pygame.font.SysFont(self.fontName, self.fontSize)
        else:
            return pygame.font.Font(self.fontName, self.fontSize)

class FontManager:

    instance = None

    def __init__(self):
        """
        """
        self.fonts = {}
        self.loadFontsInDirectory('./') # ./ or . ?
        
    @staticmethod
    def getInstance():
        if( FontManager.instance != None ):
            FontManager.instance = FontManager()

        return FontManager.instance()
        
    def addFont(self, fontName, font):
        self.fonts[fontName] = font
    
    def removeFont(self, fontName):
        del self.fonts[fontName]

    def loadFontsInDirectory(self, directory):
        """
        Load all fonts in a given directory 
        """
        




class Label(Control):
    def __init__(self, x, y, font, parentControl, controlId, controlName=None, controlValue=None):
        if not (font):
            raise ValueError("Font cannot be empty")

        super(Label, self).__init__(x, y, 0, 0, parentControl, controlId, controlName, controlValue)  

        self.font       = font    
        self.surface    = font.render(controlValue, True, self.frgndColor)   
        self.isCenter   = False #True

        surfaceWidth    = self.surface.get_width()
        surfaceHeight   = self.surface.get_height()

        # Set the width and height
        self.setWidth(surfaceWidth)
        self.setHeight(surfaceHeight)

    def setFont(self, font):
        """
        Set a new font, and re-render it
        """
        self.font = font
        self.surface = font.render(self.controlValue, True, self.frgndColor)
    def getFont(self, font):
        return self.font

    def getSurface(self):
        return self.surface

    def getWidth(self):
        """
        Overwritten getWidth method
        """
        return self.surface.get_width()
    def getHeight(self):
        return self.surface.get_height()

    def draw(self, window):
        x = self.x
        y = self.y
        window.blit(self.surface, [x, y])



class EButtonType(Enum):
    NORMAL  = 0
    FLAT    = 1
    POPUP   = 2

class Button(Control):
    def __init__(self, x, y, width, height, parentControl, controlId, controlName=None, controlValue=None):
        super(Button, self).__init__(x, y, width, height, parentControl, controlId, controlName, controlValue)  
        self.fontSize   = 16
        #self.font       = Font("comicsansms", self.fontSize).getFont()
        #"C:\\Users\\L31405\\Desktop\\Python project\\pyseq\\game\\interface\\gamefont.ttf"
        self.font       = Font(get_rel_path('./gamefont.ttf'), self.fontSize, True).getFont()
        self.label      = Label(self.x, self.y, self.font, self, 10001, "ButtonLabels", self.controlValue)
        self.btnStyle   = EButtonType.FLAT
        self.isTextCentered = False

        labelWidth  = self.label.getWidth()
        labelHeight = self.label.getHeight()

        if( labelWidth >= self.minWidth ):
            self.width = labelWidth
        if( labelHeight >= self.minHeight  ):
            self.height = labelHeight

        #self.autoSize()

    def autoSize(self):
        """
        Automatically resize button width and height based on text width/height
        """
        textWidth, textHeight = self.font.size(self.controlValue)
        padding = 5
        self.width = textWidth + padding
        self.height = textHeight + padding

    def centerText(self):
        if( not self.isTextCentered ):
            oldWidth = self.width
            #self.x -= oldWidth / 2
            #self.width = oldWidth * 2 # Expand rectangle/button

            #self.label.x = self.x

            self.label.centerXY(self.getRect())
            self.isTextCentered = True 

    def uncenterText(self):
        """
        """

    def draw(self, window):
             
        width = 0
        if( self.btnStyle != EButtonType.NORMAL ):
            width = 1

        buttonRect = self.getRect()

        # Draw Border
        super(Button, self).draw(window)
        pygame.draw.rect(window, self.bkgndColor, buttonRect, width) # The last arg 'width' is the rect border thickness/width 

        # Draw Label
        self.centerText()
        self.label.draw(window)




class Textbox(Control):
    """
    This class is not ready yet.
    """
    def __init__(self, x, y, width, height, parentControl, controlId, controlName=None, controlValue=None):
        super(Textbox, self).__init__(x, y, width, height, controlId, controlName, controlValue)   


class ControlManager:
    def __init__(self):
        """
        """
        self.controls = []

    def count(self):
        return len(self.controls)
    def len(self):
        return len(self.controls)

    def add(self, control):
        """
        Add control
        """
        self.controls.append(control)

    def addList(self, controls):
        """
        Add a list of controls
        """
        for control in controls:
            self.controls.append(control)
    
    def removeAt(self, index):
        """
        Remove control at index
        """
        self.controls.pop(index)

    def removeAll(self):
        self.controls = []

    def getControlById(self, id):
        """
        """
        for control in self.controls:
            if( control.controlId == id ):
                return control
                
    def getControlByName(self, name):
        """
        """

    def getControlByValue(self, value):
        """
        """    

    def printControls(self):
        print("format = id | controlName : controlValue")
        for control in self.controls:
            print(str(control.controlId) + " | " + control.controlName + " : " + control.controlValue)