# This contains the Tower class, which is subclassed by towers on the sidebar and towers in the game
# It includes information about the images, firing rate, firing angle, and firing algorithm for each type of tower

import pygame, random, math
from bloons import * 

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Tower, self).__init__()
        self.x = x
        self.y = y
        self.drag = False
        self.initPos = (x,y)
        self.inMap = False
        self.showRange = False
        self.tick = 0
        self.angle = 0
        self.weapons = pygame.sprite.Group()
        self.clicked = False
        self.upgraded = False

    def getRect(self): 
        self.rect = pygame.Rect(self.x - self.radiusX, self.y - self.radiusY,
                                self.width, self.height)

    def update(self, screenWidth, screenHeight):
        self.getRect()

    def checkBounds(self, position):
        if ((position[0] < self.rect.right) and (position[0] > self.rect.left) and 
            (position[1] < self.rect.bottom) and (position[1] > self.rect.top)):
            return True
        return False

    def checkRange(self, position):
        if ((position[0] < self.rect.right+self.firingRange) and (position[0] > self.rect.left-self.firingRange) and 
            (position[1] < self.rect.bottom+self.firingRange) and (position[1] > self.rect.top-self.firingRange)):
            return True
        return False

    def getDims(self, scale):
        self.width = self.image.get_width()//scale
        self.height = self.image.get_height()//scale
        self.radiusX = self.width//2
        self.radiusY = self.height//2
        self.rect = pygame.Rect(self.x - self.radiusX, self.y - self.radiusY,
                                self.width, self.height)

    def fireWeapons(self, bloons):
        shortest = None
        shortestBloon = None
        for bloon in bloons:
            if type(bloon) != Camo:
                current = len(bloon.tiles)
                if ((shortest == None) or (current <= shortest)):
                    shortest = current
                    shortestBloon = bloon
        if shortest == None: self.angle = 0
        else:
            vecX = shortestBloon.x - self.x
            vecY = shortestBloon.y - self.y 
            if vecX == 0:
                vecX = 0.01
            self.angle = math.atan2(vecY, vecX)
        self.rotate()
        return self.angle

    def rotate(self):
        self.getRect()
        angle = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.originalImage, -angle).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        pygame.display.update()

class Dart(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.originalImage = pygame.image.load('images/gameDart.png').convert_alpha()
        self.image = pygame.image.load("images/dartMonkey.png").convert_alpha()
        self.getDims(8)
        self.name = "DART MONKEY"
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width-20,self.height-20))
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.cost = 100
        self.firingRange = 100
        self.timerDelay = 2000
        self.tickLevel = 100
    
class Boom(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("images/boomerangMonkey.png").convert_alpha()
        self.getDims(6)
        self.name = "BOOMERANG MONKEY"
        self.originalImage = pygame.image.load('images/gameBoomer.png').convert_alpha()
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.cost = 300
        self.firingRange = 150
        self.timerDelay = 1000
        self.tickLevel = 50

class Bomb(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("images/bombShooter.png").convert_alpha()
        self.getDims(8)
        self.name = "BOMB SHOOTER"
        self.originalImage = pygame.image.load('images/gameBomb.png').convert_alpha()
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.cost = 500
        self.firingRange = 200
        self.timerDelay = 1000
        self.tickLevel = 100

    def fireWeapons(self, bloons):
        strongest = 0
        strongestBloon = None
        for bloon in bloons:
            current = bloon.health
            if (strongestBloon == None) or (current > strongest):
                strongest = current
                strongestBloon = bloon
        if strongestBloon == None:
            self.angle = 0
        else:
            vecX = strongestBloon.x - self.x
            vecY = strongestBloon.y - self.y
            if vecX == 0:
                vecX = 0.01
            self.angle = math.atan2(vecY,vecX)
        self.rotate()
        return self.angle


class SuperM(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("images/superMonkey.png").convert_alpha()
        self.getDims(6)
        self.name = "SUPER MONKEY"
        self.originalImage = pygame.image.load('images/gameSuper.png').convert_alpha()
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.cost = 1000
        self.firingRange = 300
        self.timerDelay = 1000
        self.tickLevel = 25

    def fireWeapons(self, bloons):
        strongest = 0
        strongestBloon = None
        for bloon in bloons:
            current = bloon.health
            if (strongestBloon == None) or (current > strongest):
                strongest = current
                strongestBloon = bloon
        if strongestBloon == None:
            self.angle = 0
        else:
            vecX = strongestBloon.x - self.x
            vecY = strongestBloon.y - self.y
            if vecX == 0:
                vecX = 0.01
            self.angle = math.atan2(vecY,vecX)
        self.rotate()
        return self.angle

class Wizard(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("images/wizardMonkey.png").convert_alpha()
        self.getDims(8)
        self.name = "WIZARD MONKEY"
        self.originalImage = pygame.image.load('images/gameWizard.png').convert_alpha()
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.originalImage = pygame.transform.scale(self.originalImage, (self.originalImage.get_width()-20, self.originalImage.get_height()-20))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.cost = 200
        self.firingRange = 100
        self.timerDelay = 1000
        self.tickLevel = 100

    def findClosestTile(self, tiles):
        min = None
        minTile = None
        for tile in tiles:
            dist = math.sqrt((tile.x-self.x)**2 + (tile.y-self.y)**2)
            if ((minTile == None) or (dist <= min)):
                min = dist
                minTile = tile
        vecX = tile.x - self.x
        vecY = tile.y - self.y 
        if vecX == 0:
            vecX = 0.01
        self.angle = math.atan2(vecY, vecX)+180
        self.rotate()
        return minTile

class Ninja(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("images/ninjaMonkey.png").convert_alpha()
        self.getDims(7)
        self.name = "NINJA MONKEY"
        self.originalImage = pygame.image.load('images/gameNinja.png').convert_alpha()
        self.originalImage = pygame.transform.rotate(self.originalImage, -90)
        self.originalImage = pygame.transform.scale(self.originalImage, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.cost = 500
        self.firingRange = 100
        self.timerDelay = 1000
        self.tickLevel = 50
    
    def fireWeapons(self, bloons):
        shortest = None
        shortestBloon = None
        for bloon in bloons:
            current = len(bloon.tiles)
            if ((shortestBloon == None) or (current <= shortest)):
                shortest = current
                shortestBloon = bloon
        vecX = shortestBloon.x - self.x
        vecY = shortestBloon.y - self.y 
        if vecX == 0:
            vecX = 0.01
        self.angle = math.atan2(vecY, vecX)
        self.rotate()
        return self.angle