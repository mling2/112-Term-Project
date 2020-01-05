# This contains the Button class, which contain all the properties for the buttons used in the game,
# including checkBounds and the graphics creation
# This also contains the Arrow class, which are drawn along the path to guide the player 

import pygame, random

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, font):
        self.font = font
        self.textSurf, self.textRect = self.text_objects(text, self.font)
        self.width = self.textSurf.get_width()
        self.height = self.textSurf.get_height()
        self.textRect.center = (x, y)
        self.boxRect = (self.textRect.center[0]-self.width, 
                        self.textRect.center[1]-self.height, 
                        self.width*2, self.height*2)
        self.boxColor = color

    # method copied from https://pythonprogramming.net/displaying-text-pygame-screen/
    # with modifications
    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def checkBounds(self, position):
        if ((position[0] < self.textRect.center[0]+self.width) and (position[0] > self.textRect.center[0]-self.width) and 
            (position[1] < self.textRect.center[1]+self.height) and (position[1] > self.textRect.center[1]-self.height)):
            return True
        return False

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super(Arrow, self).__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.image = pygame.image.load('greenArrow.png')
        self.getDims(13)
        self.originalImage = pygame.transform.scale(self.image, (self.width,self.height))
        self.image = pygame.transform.rotate(self.originalImage, self.angle).convert_alpha()

    def getRect(self): 
        self.rect = pygame.Rect(self.x - self.radiusX, self.y - self.radiusY,
                                self.width, self.height)

    def update(self, screenWidth, screenHeight):
        self.getRect()

    def getDims(self, scale):
        self.width = self.image.get_width()//scale
        self.height = self.image.get_height()//scale
        self.radiusX = self.width//2
        self.radiusY = self.height//2
        self.rect = pygame.Rect(self.x - self.radiusX, self.y - self.radiusY,
                                self.width, self.height)