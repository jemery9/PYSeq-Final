#audio.py

import pygame 
from pygame import *

import os

def get_rel_path(path):
    return os.path.join(os.path.dirname(__file__), path)

class Audio:
    """
    A wrapper around the pygame.mixer.music library
    """
    def __init__(self):
        """
        Instantiate an instance of the Audio class
        """


    @staticmethod
    def load(fileName):
        filePath = get_rel_path(fileName)
        pygame.mixer.music.load(filePath)
        pygame.mixer.music.set_volume(0.75)
    
    @staticmethod
    def play(numOfTimes):
        """
        -1 for infinite playing.
        """
        pygame.mixer.music.play(numOfTimes)

    @staticmethod
    def stop():
        pygame.mixer.music.stop()