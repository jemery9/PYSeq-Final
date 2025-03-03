# SpritesheetXML.py
# Spritesheet XML Parser

"""
Reference : https://stackoverflow.com/questions/45526988/does-anyone-have-an-example-of-using-sprite-sheets-in-tandem-with-xml-files
Example : 
img1 = sheet.get_image_name("walkRightIdle.png")
img2 = sheet.get_image_rect(0, 0, 22, 28)


Make XML of sprite : https://www.leshylabs.com/apps/sstool/


"""

import xml.etree.ElementTree as ET
import pygame 

class SpritesheetXML:
    # load an atlas image
    # can also pass an associated XML file (ref. Kenney art)
    def __init__(self, img_file, data_file=None):
        self.spritesheet = pygame.image.load(img_file).convert_alpha()
        if data_file:
            tree = ET.parse(data_file)
            self.map = {}
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['width'] = int(node.attrib.get('width'))
                    self.map[name]['height'] = int(node.attrib.get('height'))

    def getImageByRect(self, x, y, w, h):
        return self.spritesheet.subsurface(pygame.Rect(x, y, w, h))

    def getImageByName(self, name):
        rect = pygame.Rect(self.map[name]['x'], self.map[name]['y'],
                       self.map[name]['width'], self.map[name]['height'])
        return self.spritesheet.subsurface(rect)