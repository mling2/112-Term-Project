import pygame, random
import mapGenerator
from cmu_112_graphics import *

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Tower, self).__init__()
        self.x = x
        self.y = y
        self.drag = False

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

    def getDims(self, scale):
        self.width = self.image.get_width()//scale
        self.height = self.image.get_height()//scale
        self.radiusX = self.width//2
        self.radiusY = self.height//2
        self.rect = pygame.Rect(self.x - self.radiusX, self.y - self.radiusY,
                                self.width, self.height)

class Dart(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("dartMonkey.png")
        self.getDims(6)
        self.name = "DART MONKEY"
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

class Boom(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("boomerangMonkey.png")
        self.getDims(5)
        self.name = "BOOMERANG MONKEY"
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

class Bomb(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("bombShooter.png")
        self.getDims(6)
        self.name = "BOMB SHOOTER"
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

class SuperM(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("superMonkey.png")
        self.getDims(5)
        self.name = "SUPER MONKEY"
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

class Wizard(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("wizardMonkey.png")
        self.getDims(6)
        self.name = "WIZARD MONKEY"
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

class Ninja(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("ninjaMonkey.png")
        self.getDims(5)
        self.name = "NINJA MONKEY"
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

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

class StoneTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("stoneTile.jpg")
        super().getDims(4)
        self.name = "Stone Tile"
        self.image = pygame.transform.scale(self.image, (self.side,self.side))

class BloonsTowerDefense(ModalApp):
    def appStarted(self):
        self.game = Game()
        self.setActiveMode(self.game)

class Game(Mode):
    def appStarted(self):
        # general pygame template copied from 
        # http://blog.lukasperaza.com/getting-started-with-pygame/
        # with modifications
        pygame.init()
        self.width=800
        self.height=600
        self.rows = 10
        self.cols = 10
        screen = pygame.display.set_mode((self.width,self.height))
        clock = pygame.time.Clock()

        # initializing the towers
        self.towers = pygame.sprite.Group()
        self.playing = True
        self.dart = Dart(650,100)
        self.boom = Boom(750,100)
        self.bomb = Bomb(650,180)
        self.wizard = Wizard(750,180)
        self.ninja = Ninja(650,260)
        self.superM = SuperM(750,260)
        self.towers.add(self.dart, self.boom, self.bomb, self.wizard, self.ninja, self.superM)

        # intializing the tiles and map
        self.mapStartX = 50
        self.mapStartY = 50
        self.tiles = pygame.sprite.Group()
        self.createTiles()

        # writing text
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial Bold', 20)
        textsurface = self.font.render('DART MONKEY', False, (0,0,0))
        self.textstart = 7*self.width/8 - textsurface.get_width()/2
        generateMapTextSurface = self.font.render('Generate New Map', False, (0,0,0))
        self.generateMapText = (650, 550)

        while self.playing:
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for tower in self.towers:
                        if event.button == 1:
                            if tower.checkBounds(event.pos):
                                textsurface = self.font.render(f'{tower.name}', False, (0,0,0))
                                self.textstart = 7*self.width/8 - textsurface.get_width()/2
                                tower.drag = True 
                elif event.type == pygame.MOUSEBUTTONUP:
                    for tower in self.towers:
                        if event.button == 1:
                            tower.drag = False
                elif event.type == pygame.MOUSEMOTION:
                    for tower in self.towers:
                        if tower.drag:
                            tower.x, tower.y = event.pos[0], event.pos[1]
                elif event.type == pygame.QUIT:
                    self.playing = False
            self.tiles.update(800, 600)
            self.towers.update(800, 600)
            screen.fill((255, 255, 255))
            screen.blit(textsurface, (self.textstart, self.height/13))
            screen.blit(generateMapTextSurface, (self.generateMapText))
            self.tiles.draw(screen)
            self.towers.draw(screen)
            pygame.display.flip()
        pygame.quit()

    def createTiles(self):
        tileList = mapGenerator.generateMap(10,10)
        print(tileList)
        for tile in tileList:
            row, col = tile[0], tile[1]
            sampleTile = StoneTile(0,0)
            x = self.mapStartX + col*sampleTile.side
            y = self.mapStartY + row*sampleTile.side
            newTile = StoneTile(x,y)
            self.tiles.add(newTile)

BloonsTowerDefense()