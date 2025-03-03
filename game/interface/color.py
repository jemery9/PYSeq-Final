# color.py
# but i think there is already a class that deals with color... so we might 
# not want to use this, otherwise we should rename it

class AColor:
    def __init__(self, color):
        self.color = color 
    
    def getLightestColor(self):
        """
        Get the lightest color possible based on the initial color given.
        For example, dark green #003500 becomes light green #00FF00
        """
        # First determine the largest value among R, G and B
        highest     = max(self.color)
        maxScale    = (float)( ((255 - highest) / 255) + 1 ) # think the decimal place might be bugged..
        
        return self.getLighterColor(maxScale)

    def getDarkestColor(self):
        """
        """
        lowest      = min(self.color)
        minScale    = (float)( ((lowest - 0) / 255) + 1 )

        return self.getDarkerColor(minScale)

    def getLighterColor(self, scale):
        # To make a color lighter, increase the RGB value
        if( scale < 1 ):
            return self.color 

        r = self.color[0] * scale
        g = self.color[1] * scale 
        b = self.color[2] * scale
    
        if( r > 255 or g > 255 or b > 255 ):
            return self.color
        
        return (r, g, b)
    
    def getDarkerColor(self, scale):
        if( scale > 1 ):
            return self.color 

        r = self.color[0] * scale
        g = self.color[1] * scale
        b = self.color[2] * scale

        if( r < 0 or g < 0 or b < 0 ):
            return self.color

        return (r, g, b)