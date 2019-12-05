import pygame, random, math

class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Weapon, self).__init__()
        self.x = x
        self.y = y
        self.angle = 0
        self.tick = 0
        self.speed = 20

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
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)
        self.rotate()
    
    def rotate(self):
        self.getRect()
        angle = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.originalImage, -angle).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        pygame.display.update()

class NinjaStar(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('ninjaStar.png').convert_alpha()
        self.damage = 2
        self.getDims(15)
        self.originalImage = pygame.transform.scale(self.image, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 50
        self.range = 100

class BombBomb(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('bomb.png').convert_alpha()
        self.damage = 4
        self.getDims(20)
        self.originalImage = pygame.transform.scale(self.image, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 100
        self.range = 100

class DartDart(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('dart.png').convert_alpha()
        self.damage = 1
        self.getDims(35)
        self.originalImage = pygame.transform.scale(self.image, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 200
        self.range = 100

class Rang(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('boomerang.png').convert_alpha()
        self.damage = 1
        self.getDims(16)
        self.originalImage = pygame.transform.scale(self.image, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 50
        self.range = 150

class Plasma(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('plasma.png').convert_alpha()
        self.damage = 5
        self.getDims(15)
        self.originalImage = pygame.transform.scale(self.image, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 25
        self.range = 200

class Fire(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('fire.png').convert_alpha()
        self.damage = 4
        self.getDims(15)
        self.originalImage = pygame.transform.scale(self.image, (self.width,self.height))
        self.image = pygame.transform.scale(self.image, (self.width,self.height))
        self.timerDelay = 50
        self.range = 100
        self.tick = 0

    def move(self):
        self.x = self.closestTile.x
        self.y = self.closestTile.y