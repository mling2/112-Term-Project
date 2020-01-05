# This contains the Tile class, 
# which is subclassed by the StoneTiles that mark the paths and Obstacle, which are the trees
# using the checkBounds method, this ensures that towers and tiles/trees do not collide 

import pygame, random

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Tile, self).__init__()
        self.x = x
        self.y = y

    def getRect(self): 
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.side, self.side)

    def update(self, screenWidth, screenHeight):
        self.getRect()

    def getDims(self, scale):
        self.side = self.image.get_width()//scale
        self.radius = self.side//2
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.side, self.side)

    def checkBounds(self, position):
        if ((position[0] < self.rect.right+10) and (position[0] > self.rect.left-10) and 
            (position[1] < self.rect.bottom+10) and (position[1] > self.rect.top-10)):
            return True
        return False

class StoneTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("stoneTile.jpg").convert_alpha()
        super().getDims(5)
        self.name = "Stone Tile"
        self.image = pygame.transform.scale(self.image, (self.side,self.side))

class Obstacle(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('christmasTree.png').convert_alpha()
        super().getDims(9)
        self.name = 'Grass Tile'
        self.image = pygame.transform.scale(self.image, (self.side,self.side))