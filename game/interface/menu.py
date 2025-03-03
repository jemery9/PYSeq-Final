# menu 

import scene
from scene import *

import control
from control import *

class Menu(Scene):
    """
    Menu will be inherited by classes such as GameMenu, GameLevelMenu ..
    """
    def __init__(self):
        """
        Instantiate a menu object
        """
        # Control Manager
        super(Scene, self).__init__()
        self.controlManager = ControlManager()
    
    def draw(self, window):
        for i in range(len(self.controlManager.controls)):
            control = self.controlManager.controls[i]
            control.draw(window)  

# Handle events within our menu region/rect
    def onMouseDownEvent(self, mousePos):
        for i in range(len(self.controlManager.controls)):
            control = self.controlManager.controls[i]
            rect = Rect(control.getRect())
            print("%d %d" % (mousePos[0], mousePos[1])) #
            if rect.collidepoint(mousePos):
                control.onMouseDownEvent()
    
    def onMouseUpEvent(self, mousePos):
        for i in range(len(self.controlManager.controls)):
            control = self.controlManager.controls[i]
            rect = Rect(control.getRect())
            print("%d %d" % (mousePos[0], mousePos[1])) #
            if rect.collidepoint(mousePos):
                control.onMouseUpEvent()

