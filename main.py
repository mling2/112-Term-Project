import pygame, random, math, copy
import mapGenerator
# Modal App framework from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
from cmu_112_graphics import *
from towers import *
from tiles import *
from misc import *
from bloons import * 
from weapons import * 

class BloonsTowerDefense(ModalApp):
    def appStarted(self):
        self.splashScreen = SplashScreen()
        self.game = Game()
        self.gameOver = GameOver()
        self.settings = Settings()
        self.instructions = Instructions()
        self.map = MapCreator()
        self.setActiveMode(self.splashScreen)

class Settings(Mode):
    def appStarted(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial Bold', 40)
        self.coolFont = pygame.font.SysFont('copperplate', 120)
        self.font2 = pygame.font.SysFont('copperplate', 40)
        self.font3 = pygame.font.SysFont('copperplate', 26)
        self.font4 = pygame.font.SysFont('copperplate', 42)
        self.width=800
        self.height=600
        screen = pygame.display.set_mode((self.width,self.height))
        clock = pygame.time.Clock()
        pygame.font.init()
        self.playing = True
        self.ownMap = False
        self.easyWidth, self.mediumWidth, self.hardWidth = 5, 5, 5
        self.level = None
        
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.app.setActiveMode(self.app.map)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.instructionsButton.checkBounds(event.pos):
                            self.app.setActiveMode(self.app.instructions)
                        elif self.mapButton.checkBounds(event.pos):
                            if self.level != None:
                                self.app.setActiveMode(self.app.map)
                        elif self.noMapButton.checkBounds(event.pos):
                            if self.level != None:
                                self.app.setActiveMode(self.app.game)
                        elif self.levelButton1.checkBounds(event.pos):
                            self.level = "easy"
                            self.easyWidth, self.mediumWidth, self.hardWidth = 10, 5, 5                     
                        elif self.levelButton2.checkBounds(event.pos):
                            self.level = "intermediate"
                            self.easyWidth, self.mediumWidth, self.hardWidth = 5, 10, 5
                        elif self.levelButton3.checkBounds(event.pos):
                            self.level = "hard"
                            self.easyWidth, self.mediumWidth, self.hardWidth = 5, 5, 10
                elif event.type == pygame.QUIT:
                    self.playing = False
            screen.fill((255, 254, 161))
            self.levelButton2 = Button(self.width//2, self.height//2+30, "MEDIUM", (255,255,0), self.font)
            self.levelButton3 = Button(3*self.width//4, self.height//2+30, "HARD", (220,20,60), self.font)
            self.levelButton1 = Button(self.width//4, self.height//2+30, "EASY", (57, 252, 3), self.font)
            pygame.draw.rect(screen, self.levelButton1.boxColor, self.levelButton1.boxRect, self.easyWidth)
            pygame.draw.rect(screen, self.levelButton2.boxColor, self.levelButton2.boxRect, self.mediumWidth)
            pygame.draw.rect(screen, self.levelButton3.boxColor, self.levelButton3.boxRect, self.hardWidth)
            screen.blit(self.levelButton1.textSurf, self.levelButton1.textRect)
            screen.blit(self.levelButton2.textSurf, self.levelButton2.textRect)
            screen.blit(self.levelButton3.textSurf, self.levelButton3.textRect)

            self.settingsText = self.coolFont.render('MAIN MENU', False, (0,0,200))
            self.settingsStart = self.width/2 - self.settingsText.get_width()/2
            screen.blit(self.settingsText, (self.settingsStart, 50))

            self.instructionsButton = Button(self.width//2, self.height//3+30, "INSTRUCTIONS", (0,0,0), self.font2)
            pygame.draw.rect(screen, self.instructionsButton.boxColor, self.instructionsButton.boxRect, 8)
            screen.blit(self.instructionsButton.textSurf, self.instructionsButton.textRect)

            self.mapButton = Button(self.width//2, 5*self.height//6+30, "CREATE YOUR OWN MAP", (0,0,0), self.font3)
            pygame.draw.rect(screen, self.mapButton.boxColor, self.mapButton.boxRect, 8)
            screen.blit(self.mapButton.textSurf, self.mapButton.textRect)

            self.noMapButton = Button(self.width//2, 2*self.height//3+30, "RANDOM MAP", (0,0,0), self.font4)
            pygame.draw.rect(screen, self.noMapButton.boxColor, self.noMapButton.boxRect, 8)
            screen.blit(self.noMapButton.textSurf, self.noMapButton.textRect)

            pygame.display.update()
        pygame.quit()


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
        self.totalBloonsDeployed = 0
        self.totalBloonsPopped = 0
        self.deployCamo = False
        self.startDeployment = False

        self.initializeFeatures()

        while self.playing:
            clock.tick(10**10)

            if self.score < 0:
                self.app.setActiveMode(self.app.gameOver)
            
            if self.startDeployment: 
                # deploying balloons
                self.bloonDeployment()
                self.levelingUp()
                if self.totalBloonsPopped >= self.total:
                    self.finishDeployment = True
            
            if not self.finishDeployment:
                self.blueTick += clock.tick(100)
                self.greenTick += clock.tick(100)
                self.yellowTick += clock.tick(100)
                self.redTick += clock.tick(100)
                self.camoLevelTick += clock.tick(100)
                self.camoTick += clock.tick(100)
                for pop in self.pops:
                    pop.tick += 100

            if self.score > 0:
                for tower in self.gameTowers:
                    tower.tick += clock.tick(100)

            # displaying name of tower
            for tower in self.towers:
                if tower.checkBounds(pygame.mouse.get_pos()):
                    self.textsurface = self.font.render(f'{tower.name}', False, (0,0,0))
                    self.textstart = 7*self.width/8 - self.textsurface.get_width()/2
                    self.costsurface = self.font.render(f'COST: {tower.cost}', False, (0,0,0))
                    self.coststart = 7*self.width/8 - self.costsurface.get_width()/2

            # displaying the score, coins, bloons left, and current level
            self.font2 = pygame.font.SysFont('Arial Bold', 30)
            scoreTextSurface = self.font2.render(f'Lives: {self.score}', False, (0,0,0))
            coinsTextSurface = self.font2.render(f'Coins: {self.coins}', False, (0,0,0))
            bloonsTextSurface = self.font2.render(f'Blewns Left: {self.total-self.totalBloonsPopped}', False, (0,0,0))

            levelTextSurface = self.font2.render(f'LEVEL: {self.currentLevel}/{self.levels}', False, (0,0,0))

            # move bloons
            for bloon in self.bloons:
                bloon.move()

            # check if bloons are on the map
            for bloon in self.bloons:
                if not self.inMap((bloon.x, bloon.y)): 
                    self.score -= bloon.reward
                    self.bloons.remove(bloon)

            if ((self.finishDeployment) and (len(self.bloons) == 0)):
                self.app.setActiveMode(self.app.gameOver)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.appStarted()
                    elif event.key == pygame.K_ESCAPE:
                        self.app.setActiveMode(self.app.settings)
                    elif event.key == pygame.K_RIGHT:
                        if self.speedPos < 3:
                            self.redLevel //= 2
                            self.blueLevel //= 2
                            self.greenLevel //= 2
                            self.yellowLevel //= 2
                            self.camoThreshold //= 2
                            for tower in self.gameTowers:
                                tower.tickLevel //= 2
                                for weapon in tower.weapons:
                                    weapon.speed *= 2
                            for bloon in self.bloons:
                                if bloon.timerDelay > 1:
                                    bloon.timerDelay -= 1
                                    if bloon.timerDelay <= 5:
                                        bloon.check += (5-bloon.timerDelay)
                            self.speedPos += 1
                        print(self.speedPos)
                    elif event.key == pygame.K_LEFT:
                        if self.speedPos > -3:
                            self.redLevel *= 2
                            self.blueLevel *= 2
                            self.greenLevel *= 2
                            self.yellowLevel *= 2
                            self.camoThreshold *= 2
                            for tower in self.gameTowers:
                                tower.tickLevel *= 2
                                for weapon in tower.weapons:
                                    weapon.speed //= 2
                            for bloon in self.bloons:
                                bloon.timerDelay += 1
                                if bloon.timerDelay <= 5:
                                        bloon.check += (5-bloon.timerDelay)
                            self.speedPos -= 1
                        print(self.speedPos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for tower in self.towers:
                        if event.button == 1:
                            if ((event.pos[0] < 675+60) and 
                                (event.pos[0] > 675-60) and 
                                (event.pos[1] < 525+50) and 
                                (event.pos[1] > 525-50)):
                                self.startDeployment = True
                            if tower.checkBounds(event.pos):
                                if type(tower) == Dart: newTower = Dart(event.pos[0], event.pos[1])
                                elif type(tower) == Boom: newTower = Boom(event.pos[0], event.pos[1])
                                elif type(tower) == Wizard: newTower = Wizard(event.pos[0], event.pos[1])
                                elif type(tower) == Ninja: newTower = Ninja(event.pos[0], event.pos[1])
                                elif type(tower) == SuperM: newTower = SuperM(event.pos[0], event.pos[1])
                                elif type(tower) == Bomb: newTower = Bomb(event.pos[0], event.pos[1])
                                self.gameTowers.add(newTower)
                                self.coins -= newTower.cost
                                newTower.initPos = (tower.x, tower.y)
                                newTower.drag = True
                                if self.inMap(event.pos):
                                    newTower.showRange = True
                    for tower in self.gameTowers:
                        if self.inMap(event.pos):
                            tower.showRange = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    for tower in self.gameTowers:
                        if event.button == 1 and tower.drag:
                            for block in self.blocks:
                                if block.checkBounds(event.pos) or not self.inMap(event.pos) or (self.coins < 0):
                                    self.gameTowers.remove(tower)
                                    self.coins += tower.cost
                                    tower.cost = 0
                                elif self.inMap(event.pos):
                                    tower.inMap = True
                                tower.drag = False
                        tower.showRange = False
                elif event.type == pygame.MOUSEMOTION:
                    red = False
                    for tower in self.gameTowers:
                        if tower.drag:
                            tower.x, tower.y = event.pos[0], event.pos[1]
                        for block in self.blocks:
                            if block.checkBounds((tower.x, tower.y)):
                                red = True
                elif event.type == pygame.QUIT:
                    self.playing = False

            # fire weapons
            for tower in self.gameTowers:
                if not tower.drag and self.inMap((tower.x, tower.y)):
                    if type(tower) == Bomb:
                        if tower.tick > tower.tickLevel:
                            tower.weapons.add(BombBomb(tower.x, tower.y))
                            tower.tick = 0
                    elif type(tower) == Ninja: 
                        if tower.tick > tower.tickLevel:
                            tower.weapons.add(NinjaStar(tower.x, tower.y))
                            tower.tick = 0
                    elif type(tower) == Dart:
                        if tower.tick > tower.tickLevel:
                            tower.weapons.add(DartDart(tower.x, tower.y))
                            tower.tick = 0
                    elif type(tower) == Boom: 
                        if tower.tick > tower.tickLevel:
                            tower.weapons.add(Rang(tower.x, tower.y))
                            tower.tick = 0
                    elif type(tower) == SuperM: 
                        if tower.tick > tower.tickLevel: 
                            tower.weapons.add(Plasma(tower.x, tower.y))
                            tower.tick = 0
                    elif type(tower) == Wizard: 
                        if tower.tick > tower.tickLevel:
                            tower.weapons.add(Fire(tower.x, tower.y))
                            tower.tick = 0

            # fire weapons
            for tower in self.gameTowers:
                self.bloonsInRange = pygame.sprite.Group()
                for weapon in tower.weapons:
                    for bloon in self.bloons:
                        if tower.checkRange((bloon.x, bloon.y)):
                            self.bloonsInRange.add(bloon)
                    if len(self.bloonsInRange) > 0:
                        if type(tower) == Wizard:
                            weapon.closestTile = tower.findClosestTile(self.tiles)
                        else:
                            weapon.angle = tower.fireWeapons(self.bloonsInRange)
                    else:
                        tower.weapons.remove(weapon)
                    self.bloonsInRange.empty()

            # move weapons
            for tower in self.gameTowers:
                for weapon in tower.weapons:
                    weapon.tick += 100
                    weapon.move()
            
            # check that weapons don't go off of the map or out of range
            for tower in self.gameTowers:
                if type(tower) == Wizard:
                    for weapon in tower.weapons:
                        if (not self.inMap((weapon.x, weapon.y))) or (weapon.tick > 500):
                            tower.weapons.remove(weapon)
                else:
                    for weapon in tower.weapons:
                        distance = math.sqrt((weapon.x - tower.x)**2 + (weapon.y - tower.y)**2)
                        if ((distance > weapon.range*math.sqrt(2)) or (not self.inMap((weapon.x, weapon.y)))):
                            tower.weapons.remove(weapon)

            # pop bloons when the weapons hit them
            self.bloonPopCheck()

            self.tiles.update(800, 600)
            self.grassTiles.update(800, 600)
            self.arrows.update(800, 600)
            self.towers.update(800, 600)
            self.gameTowers.update(800, 600)
            self.pops.update(800, 600)
            self.bloons.update(800, 600)
            for tower in self.gameTowers:
                tower.weapons.update(800,600)
            screen.fill((255, 255, 255))
            # map box
            pygame.draw.rect(screen, self.LIGHTRED, (0,0,585,600))
            pygame.draw.rect(screen, self.BLACK, (25,25,475,475), 10)
            pygame.draw.rect(screen, self.GREEN, (25,25,475,475))
            # sidebar
            pygame.draw.rect(screen, self.BLACK, (585,0,235,600), 10)
            pygame.draw.rect(screen, self.YELLOW, (585,0,235,600))
            # monkey and cost bar
            rec = (self.textstart-5, (self.height/15)-5, self.textsurface.get_width()+10, self.textsurface.get_height()+10)
            pygame.draw.rect(screen, (0,0,0), rec, 5)
            pygame.draw.rect(screen, (252, 252, 199), rec)
            rec2 = (self.coststart-5, (self.height/2)-5, self.costsurface.get_width()+10, self.costsurface.get_height()+10)
            pygame.draw.rect(screen, (0,0,0), rec2, 5)
            pygame.draw.rect(screen, (252, 252, 199), rec2)
            screen.blit(self.textsurface, (self.textstart, self.height/14))
            screen.blit(self.costsurface, (self.coststart, self.height/2))
            screen.blit(scoreTextSurface, (25, 550))
            screen.blit(coinsTextSurface, (175, 550))
            screen.blit(bloonsTextSurface, (325, 550))
            screen.blit(levelTextSurface, (640, 400))
            screen.blit(self.playButton, (675, 475))
            pygame.draw.rect(screen, self.rightArrow.boxColor, self.rightArrow.boxRect, 5)
            pygame.draw.rect(screen, self.leftArrow.boxColor, self.leftArrow.boxRect, 5)
            screen.blit(self.rightArrow.textSurf, self.rightArrow.textRect)
            screen.blit(self.leftArrow.textSurf, self.leftArrow.textRect)
            self.tiles.draw(screen)
            self.grassTiles.draw(screen)
            self.arrows.draw(screen)
            self.towers.draw(screen)
            self.gameTowers.draw(screen)
            self.pops.draw(screen)
            self.bloons.draw(screen)
            for tower in self.gameTowers:
                tower.weapons.draw(screen)
            for tower in self.gameTowers:
                if tower.drag and self.inMap((tower.x, tower.y)):
                        if red: 
                            pygame.draw.circle(screen, self.RED, (tower.x, tower.y), tower.firingRange, 2)
                        else:
                            pygame.draw.circle(screen, self.DARKGREEN, (tower.x, tower.y), tower.firingRange, 2)
                if tower.showRange:
                    pygame.draw.circle(screen, self.DARKGREEN, (tower.x, tower.y), tower.firingRange, 2)
            pygame.display.update()
        pygame.quit()

    def initializeFeatures(self):
        # play button
        self.playButton = pygame.image.load('playbutton.png').convert_alpha()
        self.playButton = pygame.transform.scale(self.playButton, (60,60))

        # fast forward and backwards buttons
        self.arrowFont = pygame.font.SysFont('Arial Bold', 20)
        self.rightArrow = Button(765, 505, ">>", (0,0,0), self.arrowFont)
        self.leftArrow = Button(645, 505, "<<", (0,0,0), self.arrowFont)
        self.speedPos = 0

        # initializing the scores and coins
        if self.app.settings.level == "easy": 
            self.score, self.coins, self.total, self.levels = 200, 650, 200, 5
            self.redLevel, self.blueLevel, self.greenLevel, self.yellowLevel = 600, 900, 1400, 2000
            self.camoThreshold, self.camoLevelThreshold = 10**6, 10**10
            self.levelUp = 25
            self.redMin, self.blueMin, self.greenMin, self.yellowMin = 300, 600, 900, 1200
        elif self.app.settings.level == "intermediate": 
            self.score, self.coins, self.total, self.levels = 150, 550, 400, 10
            self.redLevel, self.blueLevel, self.greenLevel, self.yellowLevel = 400, 700, 900, 1400
            self.camoThreshold, self.camoLevelThreshold = 400, 10000
            self.levelUp = 50
            self.redMin, self.blueMin, self.greenMin, self.yellowMin = 200, 400, 600, 800
        elif self.app.settings.level == "hard": 
            self.score, self.coins, self.total, self.levels = 100, 450, 600, 15
            self.redLevel, self.blueLevel, self.greenLevel, self.yellowLevel = 300, 500, 700, 1000
            self.camoThreshold, self.camoLevelThreshold = 300, 8000
            self.redMin, self.blueMin, self.greenMin, self.yellowMin = 100, 200, 300, 400
            self.levelUp = 100
        self.currentLevel = 1

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

        #initializing the towers used
        self.gameTowers = pygame.sprite.Group()

        # intializing the tiles and map
        self.mapStartX = 50
        self.mapStartY = 50
        self.tiles = pygame.sprite.Group()
        self.grassTiles = pygame.sprite.Group()
        self.grassList = []
        self.createTiles()
    
        # initializing the bloons
        self.bloons = pygame.sprite.Group()
        self.x = self.mapStartX + self.tileList[0][1]*StoneTile(0,0).side
        self.y = self.mapStartY + self.tileList[0][0]*StoneTile(0,0).side
        
        self.pops = pygame.sprite.Group()

        # writing text
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial Bold', 24)
        self.textsurface = self.font.render('DART MONKEY', False, (0,0,0))
        self.textstart = 7*self.width/8 - self.textsurface.get_width()/2
        self.costsurface = self.font.render('COST: 100', False, (0,0,0))
        self.coststart = 7*self.width/8 - self.costsurface.get_width()/2
        
        # initialize the group of weapons
        self.weapons = pygame.sprite.Group()

        # initialize bloon deployment variables
        self.blueTick, self.greenTick, self.yellowTick, self.redTick = 0, 0, 0, 0
        self.camoTick = 0
        self.camoLevelTick = 0
        self.BLACK = (0,0,0)
        self.LIGHTRED = (255, 152, 152)
        self.YELLOW = (255, 254, 161)
        self.GREEN = (71, 209, 71)
        self.BROWN = (153, 76, 0)
        self.DARKGREEN = (0,128,0)
        self.RED = (255,0,0)
        self.finishDeployment = False

    # create green arrows to indicate to the player how the path goes
    def createGuidingArrows(self):
        self.arrows = pygame.sprite.Group()
        num = len(self.tileList)//6
        sampleTile = StoneTile(0,0)
        side = sampleTile.side
        for i in range(6):
            (currx, curry) = self.tileList[i*num]
            (succx, succy) = self.tileList[i*num+1]
            if ((succx-currx) == 1) and ((succy-curry) == 0): # go down
                x = self.mapStartX + curry*side + 10
                y = self.mapStartY + succx*side - 10
                self.arrows.add(Arrow(x, y, -90))
            elif ((succx-currx) == -1) and ((succy-curry) == 0): # go up
                x = self.mapStartX + curry*side + 10
                y = self.mapStartY + succx*side + 10
                self.arrows.add(Arrow(x, y, 90))
            elif ((succx-currx) == 0) and ((succy-curry) == 1): # go right
                x = self.mapStartX + curry*side
                y = self.mapStartY + succx*side
                self.arrows.add(Arrow(x, y, 0))
            elif ((succx-currx) == 0) and ((succy-curry) == -1): # go left
                x = self.mapStartX + curry*side
                y = self.mapStartY + succx*side
                self.arrows.add(Arrow(x, y, 180))
            

    def createTiles(self):
        if self.app.settings.ownMap:
            self.tileList = self.app.map.orderedTiles
        else:
            self.tileList = mapGenerator.generateMap(10,10)
        for tile in self.tileList:
            row, col = tile[0], tile[1]
            sampleTile = StoneTile(0,0)
            x = self.mapStartX + col*sampleTile.side
            y = self.mapStartY + row*sampleTile.side
            newTile = StoneTile(x,y)
            self.tiles.add(newTile)
        self.createGuidingArrows()
        if (self.app.settings.level == "hard") or (self.app.settings.level == "intermediate"):
            if (self.app.settings.level == "hard"): x = 25
            else: x = 10
            for _ in range(x):
                temp = (random.randint(0, 9), random.randint(0, 9))
                while temp in self.tileList:
                    temp = (random.randint(0,9), random.randint(0,9))
                self.grassList += [temp]
            for (row,col) in self.grassList:
                sampleTile = StoneTile(0,0)
                x = self.mapStartX + col*sampleTile.side
                y = self.mapStartY + row*sampleTile.side
                self.grassTiles.add(Obstacle(x,y))
        self.blocks = pygame.sprite.Group()
        for tile in self.tiles: self.blocks.add(tile)
        for grass in self.grassTiles: self.blocks.add(grass)

    def inMap(self, position):
        if ((position[0] < 475) and (position[0] > 25) and 
            (position[1] < 475) and (position[1] > 25)): 
            return True
        return False

    def bloonPopCheck(self):
        for bloon in self.bloons:
            for tower in self.gameTowers:
                for weapon in tower.weapons:
                    if bloon.checkBounds(weapon):
                        bloon.health -= weapon.damage
                        if type(bloon) == Yellow:
                            if bloon.health <= 0:
                                pop = Popped(bloon.x, bloon.y)
                                self.pops.add(pop)
                                self.totalBloonsPopped += 1
                                self.bloons.add(Green(bloon.x,bloon.y,bloon.tiles))
                                self.coins += bloon.reward
                                self.bloons.remove(bloon)
                                tower.weapons.remove(weapon)
                        if type(bloon) == Green:
                            if bloon.health <= 0:
                                pop = Popped(bloon.x, bloon.y)
                                self.pops.add(pop)
                                self.totalBloonsPopped += 1
                                self.bloons.add(Blue(bloon.x,bloon.y,bloon.tiles))
                                self.coins += bloon.reward
                                self.bloons.remove(bloon)
                                tower.weapons.remove(weapon)
                        if type(bloon) == Blue:
                            if bloon.health <= 0:
                                pop = Popped(bloon.x, bloon.y)
                                self.pops.add(pop)
                                self.totalBloonsPopped += 1
                                self.bloons.add(Red(bloon.x,bloon.y,bloon.tiles))
                                self.coins += bloon.reward
                                self.bloons.remove(bloon)
                                tower.weapons.remove(weapon)
                        if type(bloon) == Red:
                            if bloon.health <= 0:
                                pop = Popped(bloon.x, bloon.y)
                                self.pops.add(pop)
                                self.totalBloonsPopped += 1
                                self.coins += bloon.reward
                                self.bloons.remove(bloon)
                                tower.weapons.remove(weapon)
                        if (type(bloon) == Camo) and (type(tower) == Ninja):
                            if bloon.health <= 0:
                                pop = Popped(bloon.x, bloon.y)
                                self.pops.add(pop)
                                self.totalBloonsPopped += 1
                                self.coins += bloon.reward
                                self.bloons.remove(bloon)
                                tower.weapons.remove(weapon)
        for pop in self.pops:
            if pop.tick > 100:
                self.pops.remove(pop)
    
    def bloonDeployment(self):
        if self.greenTick > self.greenLevel: 
            self.bloons.add(Green(self.x,self.y,self.tileList))
            self.totalBloonsDeployed += 1
            self.greenTick = 0
        if self.blueTick > self.blueLevel: 
            self.bloons.add(Blue(self.x,self.y,self.tileList))
            self.totalBloonsDeployed += 1
            self.blueTick = 0
        if self.yellowTick > self.yellowLevel:
            self.bloons.add(Yellow(self.x,self.y,self.tileList))
            self.totalBloonsDeployed += 1
            self.yellowTick = 0
        if self.redTick > self.redLevel:
            self.bloons.add(Red(self.x,self.y,self.tileList))
            self.totalBloonsDeployed += 1
            self.redTick = 0
        if self.deployCamo:
            if self.camoTick > self.camoThreshold:
                self.bloons.add(Camo(self.x, self.y, self.tileList))
                self.totalBloonsDeployed += 1
                self.camoTick = 0
        if self.camoLevelTick > self.camoLevelThreshold:
            self.deployCamo = True
    
    def levelingUp(self):
        if self.totalBloonsDeployed == 40:
            if self.redLevel > self.redMin: self.redLevel -= self.levelUp
            if self.blueLevel > self.blueMin: self.blueLevel -= self.levelUp
            if self.yellowLevel > self.yellowMin: self.yellowLevel -= self.levelUp
            if self.greenLevel > self.greenMin: self.greenLevel -= self.levelUp
            if self.currentLevel < self.levels:
                self.currentLevel += 1
            self.totalBloonsDeployed = 0

class SplashScreen(Mode):
    def appStarted(self):
        pygame.init()
        pygame.display.set_caption("BLEWNS TOWER DEFENSE")
        self.font = pygame.font.SysFont('Arial Bold', 40)
        self.width=800
        self.height=600
        screen = pygame.display.set_mode((self.width,self.height))
        clock = pygame.time.Clock()
        pygame.font.init()
        self.playing = True
        
        while self.playing:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.app.setActiveMode(self.app.settings)
                elif event.type == pygame.QUIT:
                    self.playing = False
            screen.fill((255, 255, 255))
            self.image = pygame.image.load('BTDtitle.png').convert()
            self.image = pygame.transform.scale(self.image, (800,600))
            screen.blit(self.image, (0,0))
            pygame.display.update()
        pygame.quit()

class Instructions(Mode):
    def appStarted(self):
        self.font = pygame.font.SysFont('copperplate', 50)
        self.font2 = pygame.font.SysFont('Arial bold', 24)
        self.width, self.height = 800, 600
        screen = pygame.display.set_mode((self.width,self.height))
        clock = pygame.time.Clock()
        pygame.font.init()
        self.playing = True
        self.slides = ['instruct1.png', 'instruct2.png', 'instruct3.png', 'instruct4.png']
        self.ind = 0
        
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.ind < len(self.slides)-1:
                            self.ind += 1
                    elif event.key == pygame.K_LEFT:
                        if self.ind > 0:
                            self.ind -= 1
                    elif event.key == pygame.K_ESCAPE:
                        self.app.setActiveMode(self.app.settings)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rightArrow.checkBounds(event.pos):
                        if self.ind < len(self.slides)-1:
                            self.ind += 1
                    elif self.leftArrow.checkBounds(event.pos):
                        if self.ind > 0:
                            self.ind -= 1
                if event.type == pygame.QUIT:
                    self.playing = False
            screen.fill((255, 255, 200))
            
            self.text = self.font.render('INSTRUCTIONS', False, (0,0,0))
            self.textStart = self.width/2 - self.text.get_width()/2
            screen.blit(self.text, (self.textStart, 50))

            self.back = self.font2.render('Press ESC to return to the Main Menu', False, (0,0,0))
            screen.blit(self.back, (self.width//2-self.back.get_width()//2, 575))

            self.rightArrow = Button(750, self.height//2, ">", (126, 255, 117), self.font)
            self.leftArrow = Button(50, self.height//2, "<", (126, 255, 117), self.font)
            pygame.draw.rect(screen, self.rightArrow.boxColor, self.rightArrow.boxRect, 5)
            pygame.draw.rect(screen, self.leftArrow.boxColor, self.leftArrow.boxRect, 5)
            screen.blit(self.rightArrow.textSurf, self.rightArrow.textRect)
            screen.blit(self.leftArrow.textSurf, self.leftArrow.textRect)

            self.image = pygame.image.load(self.slides[self.ind]).convert()
            screen.blit(self.image, (100,100))

            pygame.display.update()
        pygame.quit()

class GameOver(Mode):
    def appStarted(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial Bold', 40)
        self.width=800
        self.height=600
        screen = pygame.display.set_mode((self.width,self.height))
        clock = pygame.time.Clock()
        pygame.font.init()
        self.playing = True
        self.slides = ['win.png', 'lose.png']
        
        while self.playing:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.app.setActiveMode(self.app.settings)
                if event.type == pygame.QUIT:
                    self.playing = False
            screen.fill((255, 255, 255))
            if self.app.game.score <= 0:
                self.image = pygame.image.load(self.slides[1]).convert()
            else:
                self.image = pygame.image.load(self.slides[1]).convert()
            screen.blit(self.image, (0,0))
            pygame.display.update()
        pygame.quit()

class MapCreator(Mode):
    def appStarted(self):
        pygame.init()
        self.font = pygame.font.SysFont('copperplate', 25)
        self.width=800
        self.height=600
        screen = pygame.display.set_mode((self.width,self.height))
        clock = pygame.time.Clock()
        pygame.font.init()
        self.playing = True
        self.tiles = pygame.sprite.Group()
        self.sample = StoneTile(0,0)
        self.mapStartX = 25
        self.mapStartY = 25
        self.coords = set()
        self.board = [ ([0] * 10) for _ in range(10) ]
        self.orderedTiles = []
        self.BLACK = (0,0,0)
        self.LIGHTRED = (255, 152, 152)
        self.YELLOW = (255, 254, 161)
        self.GREEN = (71, 209, 71)
        self.BROWN = (153, 76, 0)
        self.textsurface = self.font.render(" ", False, (0,0,0))
        self.textstart = self.width//2 - self.textsurface.get_width()/2
        self.instruct = pygame.image.load('mapcreate.png').convert_alpha()
        
        while self.playing:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # convert view to model
                    col = (event.pos[0]-self.mapStartX)//self.sample.side
                    row = (event.pos[1]-self.mapStartY)//self.sample.side

                    # only applies to coordinates on the map
                    if (row < 10) and (row >= 0) and (col < 10) and (col >= 0):
                        if self.board[row][col] == 0:
                            self.coords.add((col,row))
                            self.board[row][col] = 1
                        elif self.board[row][col] == 1:
                            self.coords.remove((col,row))
                            self.board[row][col] = 0
                    self.textsurface = self.font.render('', False, (0,0,0))
                    self.textstart = self.width//3 - self.textsurface.get_width()/2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.findSolutionState() == None:
                            self.textsurface = self.font.render(f"Sorry, this map doesn't work. Try again!", False, (0,0,0))
                            self.textstart = self.width//3 - self.textsurface.get_width()/2
                        else:
                            self.app.settings.ownMap = True
                            self.app.setActiveMode(self.app.game)
                if event.type == pygame.QUIT:
                    self.playing = False
            self.tiles = pygame.sprite.Group()
            for row in range(10):
                for col in range(10):
                    if self.board[row][col] == 1:
                        x = self.mapStartX + col*self.sample.side
                        y = self.mapStartY + row*self.sample.side
                        self.tiles.add(StoneTile(x+self.sample.side/2,y+self.sample.side/2))
            screen.fill((255, 255, 255))
            # map box
            pygame.draw.rect(screen, self.LIGHTRED, (0,0,585,600))
            pygame.draw.rect(screen, self.BLACK, (25,25,475,475), 10)
            pygame.draw.rect(screen, self.GREEN, (25,25,475,475))
            # sidebar
            pygame.draw.rect(screen, self.BLACK, (585,0,235,600), 10)
            pygame.draw.rect(screen, self.YELLOW, (585,0,235,600))
            self.tiles.update(800, 600)
            self.tiles.draw(screen)
            screen.blit(self.textsurface, (self.textstart+15, 535))
            screen.blit(self.instruct, (600,25))
            pygame.display.update()
        pygame.quit()
        
    def findSolutionState(self):
        # find a starting coordinate 
        if len(self.coords) < 10:
            return None
        startCandidates = []
        for coord in self.coords:
            if coord[0] == 0 or coord[1] == 0:
                startCandidates += [coord]
        for cand in startCandidates:
            tilesLeft = copy.deepcopy(self.coords)
            tilesLeft.remove(cand)
            self.orderedTiles = [cand]
            while len(tilesLeft) > 0:
                nextTile = self.findAdjacentTile(self.orderedTiles[-1], tilesLeft)
                if nextTile != None:
                    self.orderedTiles.append(nextTile)
                    tilesLeft.remove(nextTile)
                elif nextTile == None:
                    tilesLeft = set()
            if len(self.orderedTiles) == len(self.coords):
                last = self.orderedTiles[-1]
                if last[0] == 9 or last[1] == 9:
                    swappedTiles = []
                    for (x,y) in self.orderedTiles:
                        swappedTiles.append((y,x))
                    self.orderedTiles = swappedTiles
                    return self.orderedTiles
        return None
    
    def findAdjacentTile(self, tile, tilesLeft):
        right = (tile[0]+1,tile[1])
        left = (tile[0]-1,tile[1])
        up = (tile[0],tile[1]-1)
        down = (tile[0],tile[1]+1)
        if right in tilesLeft: return right
        elif left in tilesLeft: return left
        elif up in tilesLeft: return up
        elif down in tilesLeft: return down
        else: return None

BloonsTowerDefense()