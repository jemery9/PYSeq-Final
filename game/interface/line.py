# line.py
import pygame

class Line:
    """
 
    """
    def __init__(self, color, startpos, endpos, isAntialias = True):
        """
        Initialize a line object
        """
        self.color          = color
        self.startpos       = startpos
        self.endpos         = endpos
        self.isAntialias    = isAntialias

    def draw(self, window):
        """
        """
        if not ( self.isAntialias ):
            pygame.draw.line(window, self.color, self.startpos, self.endpos, 1)
        else:
            pygame.draw.aaline(window, self.color, self.startpos, self.endpos, True)

class HorizontalLine(Line):
    """
    Wrapper around the line class
    """
    def __init__(self, color, y, startX, endX, isAntialias = True):
        # Calculate the coordinate
        startpos = [startX, y]
        endpos   = [endX  , y]
        super(HorizontalLine, self).__init__(color, startpos, endpos, isAntialias)

class VerticalLine(Line):
    """
    Wrapper around the line class
    """
    def __init__(self, color, x, startY, endY, isAntialias = True):
        # Calculate the coordinate
        startpos = [x, startY]
        endpos   = [x, endY]
        super(VerticalLine, self).__init__(color, startpos, endpos, isAntialias)
