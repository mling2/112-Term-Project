# This contains the Bloon class, which is subclassed by the four colored bloons and Camo bloons
# Each bloon type has its own properties like health, reward, cost, and speed 
# This class also contains the method for moving bloons along the path

import pygame, random, copy
from tiles import * 

class Bloon(pygame.sprite.Sprite):
    def __init__(self, x, y, tiles):
        super(Bloon, self).__init__()
        self.x = x
        self.y = y
        self.tiles = copy.deepcopy(tiles)
        self.tileSide = StoneTile(0,0).side
        self.prev = (0,0)
        self.stopped = False
        self.tick = 0

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

    def move(self):
        if len(self.tiles) == 0:
            self.x = 600
            self.y = 600
        if len(self.tiles) >= 2:
            nexTileX = 50 + self.tiles[1][1]*self.tileSide
            nexTileY = 50 + self.tiles[1][0]*self.tileSide
            currTileX = 50 + self.tiles[0][1]*self.tileSide
            currTileY = 50 + self.tiles[0][0]*self.tileSide
            self.prev = (currTileX, currTileY)
            vecX = nexTileX - currTileX
            vecY = nexTileY - currTileY
            if (abs(nexTileX - self.x) < self.check) and (abs(nexTileY - self.y) < self.check):
                self.tiles.pop(0)
        if len(self.tiles) == 1:
            currTileX = 50 + self.tiles[0][1]*self.tileSide
            currTileY = 50 + self.tiles[0][0]*self.tileSide
            vecX = currTileX - self.prev[0]
            vecY = currTileX - self.prev[0]
            self.stopped = True
        if self.stopped:
            self.x = 600
            self.y = 600
        self.x += vecX//self.timerDelay
        self.y += vecY//self.timerDelay
        pygame.display.update()


    def checkBounds(self, obj):
        if ((obj.rect.left < self.rect.right) and (obj.rect.right > self.rect.left) and 
            (obj.rect.top < self.rect.bottom) and (obj.rect.bottom > self.rect.top)):
            return True
        return False


class Green(Bloon):
    def __init__(self, x, y, tiles):
        super().__init__(x,y,tiles)
        self.image = pygame.image.load('images/greenBloon.png').convert_alpha()
        self.health = 3
        self.reward = 3
        self.getDims(2)
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 6
        self.check = 13

class Blue(Bloon):
    def __init__(self, x, y, tiles):
        super().__init__(x,y,tiles)
        self.image = pygame.image.load('images/blueBloon.png').convert_alpha()
        self.health = 2
        self.reward = 2
        self.getDims(2)
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 7
        self.check = 10

class Yellow(Bloon):
    def __init__(self, x, y, tiles):
        super().__init__(x,y,tiles)
        self.image = pygame.image.load('images/yellowBloon.png').convert_alpha()
        self.health = 4
        self.reward = 4
        self.getDims(2)
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 4
        self.check = 20

class Red(Bloon):
    def __init__(self, x, y, tiles):
        super().__init__(x,y,tiles)
        self.image = pygame.image.load('images/red.png').convert_alpha()
        self.health = 1
        self.reward = 1
        self.getDims(6)
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 9
        self.check = 8

class Camo(Bloon):
    def __init__(self, x, y, tiles):
        super().__init__(x,y,tiles)
        self.colors = ['images/redCamo.png', 'images/blueCamo.png', 'images/greenCamo.png', 'images/yellowCamo.png']
        num = random.randint(0,3)
        self.image = pygame.image.load(self.colors[num]).convert_alpha()
        self.health = num
        self.reward = num
        if num == 0: self.getDims(2)
        elif num == 1: self.getDims(2)
        elif num == 2: self.getDims(3)
        elif num == 3: self.getDims(2)
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 8
        self.check = 10

class Popped(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Popped, self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/bloonPop.png').convert_alpha()
        self.width = self.image.get_width()//5
        self.height = self.image.get_height()//5
        self.radiusX = self.width//2
        self.radiusY = self.height//2
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.tick = 0
        self.rect = pygame.Rect(self.x - self.radiusX, self.y - self.radiusY,
                                self.width, self.height)

    def getRect(self): 
        self.rect = pygame.Rect(self.x - self.radiusX, self.y - self.radiusY,
                                self.width, self.height)

    def update(self, screenWidth, screenHeight):
        self.getRect()