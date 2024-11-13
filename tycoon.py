import pygame
import math
from sys import exit
import os

pygame.init()
class Structure(object):
    def __init__(self, sprite, rect):
        self.id = id
        self.sprite = sprite
        self.rect = rect

class Crop(Structure):
    def __init__(self, sprite, rect, stageSprites, type, growthrate):
        super().__init__(sprite, rect)
        self.stageSprites = stageSprites
        self.cropType = type
        self.baseGrowthRate = growthrate
        self.growthProgress = 0.0
        self.growthStage = 0
        self.harvestable = False
        self.planted = True
    
    def update(self):
        if self.planted == True:
            self.growthProgress += self.baseGrowthRate
        if self.growthProgress >= 1.0:
            self.harvestable == True
            self.growthProgress = 0.0
        else:
            self.harvestable == False

        # sprite 0, 1, or 2 based on stage. if plantable == false, render no sprite
        if self.growthProgress >= 1.0:
            self.growthStage = 2
            self.harvest()
        elif self.growthProgress >= 0.5:
            self.growthStage = 1
        elif self.growthProgress < 0.5:
            self.growthStage = 0

        if self.growthStage == 0:
            self.sprite = self.stageSprites[0]
            print('{} {}'.format(self.growthProgress, self.baseGrowthRate))
        elif self.growthStage == 1:
            self.sprite = self.stageSprites[1]
            print('sprite 2')
        elif self.growthStage == 2:
            self.sprite = self.stageSprites[2]
            print('sprite 3')

    def harvest(self):
        self.growthProgress = 0.0
        self.planted = False

def main():
    sw = 600
    sh = 600

    window = pygame.display.set_mode((sw,sh), pygame.SCALED | pygame.RESIZABLE)

    gxscale = 6
    gyscale = 2
    gx = float(sw*gxscale)
    gy = float(sh*gyscale)
    tilew = gx / 50

    offsetx = gx / 2 - sw / 2
    offsety = gy / 2 - sh / 2

    def load_sprites(directory, *args):
        sprites = []
        filenames = []
        for filename in os.listdir(directory):
            filenames.append(str(filename))
            if filename.endswith(".png") or filename.endswith(".jpg"):  # Adjust file extensions as needed
                image = pygame.image.load(os.path.join(directory, filename)).convert_alpha()
                sprites.append(pygame.transform.scale(image, (image.get_width() * gxscale, image.get_height() * gxscale)))
        return filenames if args[0] == 'filenames' else sprites

    sprites = load_sprites("sprites", "sprites")
    cropSprites = load_sprites("sprites/newsprites/crops", "sprites")
    cropSpriteNames = load_sprites("sprites/newsprites/crops", "filenames")
    carrotSprite = []
    cornSprite = []
    potatoSprite = []
    tomatoSprite = []
    watermelonSprite = []
    wheatSprite = []
    for i in range(len(cropSpriteNames)):
        if 'carrot' in cropSpriteNames[i]:
            carrotSprite.append(cropSprites[i])
        elif 'corn' in cropSpriteNames[i]:
            cornSprite.append(cropSprites[i])
        elif 'potato' in cropSpriteNames[i]:
            potatoSprite.append(cropSprites[i])
        elif 'tomato' in cropSpriteNames[i]:
            tomatoSprite.append(cropSprites[i])
        elif 'watermelon' in cropSpriteNames[i]:
            watermelonSprite.append(cropSprites[i])
        elif 'wheat' in cropSpriteNames[i]:
            wheatSprite.append(cropSprites[i])
    carrotRect = pygame.Rect(0, 0, carrotSprite[0].get_width() * gxscale, carrotSprite[0].get_height() * gyscale)
    cornRect = pygame.Rect(0, 0, cornSprite[0].get_width() * gxscale, cornSprite[0].get_height() * gyscale)
    potatoRect = pygame.Rect(0, 0, potatoSprite[0].get_width() * gxscale, potatoSprite[0].get_height() * gyscale)
    tomatoRect = pygame.Rect(0, 0, tomatoSprite[0].get_width() * gxscale, tomatoSprite[0].get_height() * gyscale)
    watermelonRect = pygame.Rect(0, 0, watermelonSprite[0].get_width() * gxscale, watermelonSprite[0].get_height() * gyscale)
    wheatRect = pygame.Rect(0, 0, wheatSprite[0].get_width() * gxscale, wheatSprite[0].get_height() * gyscale)

    ground = pygame.transform.scale(sprites[0], (gx, gy))
    tiles = [pygame.Surface((tilew, tilew))]
    trailsheet = pygame.image.load("sprites/testspritesheet.png", "testspritesheet.png")
    trailsheet = pygame.transform.scale(trailsheet, (trailsheet.get_width() / 5 * tilew, tilew))
    for i in range(math.floor(trailsheet.get_width() / tilew)):
        tiles.append(trailsheet.subsurface(tilew * i, 0, tilew, tilew))

    objList = []
    typeIdList = []

    barnRect = pygame.Rect(0, 0, 19 * gxscale, 15 * gyscale)
    barnSprite = pygame.image.load("sprites/barn2.png", "barn2.png")
    barn = Structure(pygame.transform.scale(barnSprite, (barnSprite.get_width() * gxscale, barnSprite.get_height() * gxscale)), barnRect)
    typeIdList.append(barn)

    wheatCrop = Crop(wheatSprite[0], wheatRect, wheatSprite, 'wheat', 0.05)
    typeIdList.append(wheatCrop)

    objectmap = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]

    for i in range(len(objectmap)):
        if objectmap[i] != 0:
            index = typeIdList[objectmap[i]-1]
            tempStructure = Structure(index.sprite, pygame.Rect((i * tilew - gx * (math.floor(i / (50))), tilew * (math.floor(i / (50)) + 1)), (index.rect.width, index.rect.height)))
            if type(index) == Crop:
                objList.append(Crop(tempStructure.sprite, tempStructure.rect, index.stageSprites, index.cropType, index.baseGrowthRate))
            else:
                objList.append(tempStructure)

    groundmap = [
        9, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 8,
        2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
        6, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 5,
        2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
        6, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 5,
        2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
        6, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 5,
        2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
        6, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 5,
        2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
        6, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 5,
        2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
        6, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 5,
        2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
        11, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1,10
    ]

    path = pygame.Surface((gx, gy))
    path.fill((0, 0, 0, 255))
    for i in range(len(groundmap)):
        if groundmap[i] != 0:
            ground.blit(tiles[groundmap[i]], (i * tilew - gx * (math.floor(i / (50))), tilew * (math.floor(i / (50)) + 1)))

    def toCenter(width, height, *args):
        return (width / 2 - args[0].width / 2, height / 2 - args[0].height / 2)
    
    game_time = 480.0
    baseTimeSpeed = 1.0

    game_time = 480.0
    baseTimeRate = 2
    dayLength = 1440.0
    dayPeriods = ['midnight', 'morning', 'noon', 'evening']
    time_of_day = dayPeriods[0]

    bob = pygame.Rect(300.0, 100.0, 50.0, 50.0)
    bob.x, bob.y = toCenter(sw, sh, bob)
    bob_basespeed = 4.0
    bob_effectspeed = bob_basespeed
    bobp = pygame.math.Vector2(0.0, 0.0)
    bobc = pygame.math.Vector2(0.0, 0.0)
    movement = pygame.math.Vector2(1, 1)

    yay = pygame.font.SysFont('calibri', 20, bold=True)

    def tran(x, y, addx, addy):
        translated = (x + addx, y + addy)
        return translated

    quadbool = 0
    yes = False

    # debug tools
    condRes = 'Else'
    debugMode = False
    debugList = ''
    renderRects = False

    Clock = pygame.time.Clock()
    while True:
        dt = Clock.tick(60)/1000.0
        game_time += dt * baseTimeRate
        if game_time > dayLength:
            game_time = game_time - dayLength
        if game_time >= dayLength/4 * 3:
            time_of_day = dayPeriods[3]
        elif game_time >= dayLength/4 * 2:
            time_of_day = dayPeriods[2]
        elif game_time >= dayLength/4:
            time_of_day = dayPeriods[1]
        else:
            time_of_day = dayPeriods[0] 
        window.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break
                if event.key == pygame.K_F3:
                    debugMode = not debugMode
                if event.key == pygame.K_F4:
                    renderRects = not renderRects
                #if event.key == pygame.K_e and interact != None:

        if quadbool <= 0:
            yes = False
        elif quadbool >= 3:
            yes = True
        
        bobc.xy = (0.0, 0.0)
        bob_effectspeed = bob_basespeed

        keys = pygame.key.get_pressed()
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        
        movement = pygame.math.Vector2(right - left, down - up)
        if keys[pygame.K_LSHIFT] == 1:
            bob_effectspeed *= 5
        bobc.xy = bob.x + bob_effectspeed * movement.x, bob.y + bob_effectspeed * movement.y

        if math.dist((bobp), (bobc)) > bob_effectspeed:
            bobc.xy = tran(bob.x, bob.y, bob_effectspeed / math.sqrt(2) * movement.x , bob_effectspeed / math.sqrt(2) * movement.y)
        
        # Player center right of horizontal center, offsetx is min: take distance past center, swap it to offsetx
        if bobc.x > sw / 2 - bob.width / 2 and (offsetx == 0.0 and offsetx != gx - sw):
            offsetx += bobc.x - sw / 2 + bob.width
            bobc.x = sw / 2 - bob.width
        # Player center left of horizontal center, offsetx is max: take distance past center, swap to offsetx
        elif bobc.x < sw / 2 - bob.width / 2 and (offsetx != 0.0 and offsetx == gx - sw):
            offsetx += bobc.x - sw / 2 + bob.width
            bobc.x = sw / 2 - bob.width
        # 
        elif offsetx > gx - sw:
            bobc.x += offsetx - gx + sw
            offsetx = gx - sw
        elif offsetx < 0.0:
            bobc.x += offsetx
            offsetx = 0.0

        if bobc.y > sh / 2 - bob.height / 2 and (offsety == 0.0 and offsety != gy - sh):
            offsety += bobc.y - sh / 2 + bob.height
            bobc.y = sh / 2 - bob.height
        elif bobc.y < sh / 2 - bob.height / 2 and (offsety != 0.0 and offsety == gy - sh):
            offsety += bobc.y - sh / 2 + bob.height
            bobc.y = sh / 2 - bob.height
        elif offsety > gy - sh:
            bobc.y += offsety - gy + sh
            offsety = gy - sh
        elif offsety < 0.0:
            bobc.y += offsety
            offsety = 0.0

        if offsetx == 0.0 or offsetx == gx - sw:
            bob.x = bobc.x
        else:
            offsetx = bobc.x - bob.x + offsetx
        if offsety == 0.0 or offsety == gy - sh:
            bob.y = bobc.y
        else:
            offsety = bobc.y - bob.y + offsety

        if bob.x < 0:
            bob.x += -bob.x
            movement.x = movement.x * -1
        if bob.x + bob.width > sw:
            bob.x += sw - bob.x - bob.width
            movement.x = movement.x * -1
        if bob.y < 0:
            bob.y += -bob.y
            movement.y = movement.y * -1
        if bob.y + bob.height > sh:
            bob.y += sh - bob.y - bob.height
            movement.y = movement.y * -1

        bob_pos = pygame.math.Vector2(bob.x + offsetx, bob.y + offsety)
        bob_cpos = pygame.math.Vector2(bobc.x + offsetx, bobc.y + offsety)

        if keys[pygame.K_SPACE]:
            if yes == False:
                quadbool += 1
            elif yes == True:
                quadbool -= 1

        for i in objList:
            if type(i) == Crop:
                i.update()

        window.blit(ground, (- offsetx, - offsety))
        for i in objList:
            window.blit(i.sprite, (i.rect.x - offsetx, i.rect.y - offsety))
            if renderRects == True:
                pygame.draw.rect(window, 'white', i.rect)
        time_hour = math.floor(math.floor(game_time) / 60)
        time_minute = math.floor(game_time) - 60 * time_hour
        time_text = yay.render(str(time_hour) + ':' + ('0' + str(time_minute) if len(str(time_minute)) == 1 else str(time_minute)) + ' (' + time_of_day + ')', True, 'white')
        window.blit(time_text, (window.get_width() - time_text.get_width(), 0))
        window.fill('blue', bob)
        if debugMode == True:
            debugList = [offsetx, offsety, pygame.Vector2((sw, sh)), pygame.Vector2((gx, gy)), pygame.Vector2((bob.x, bob.y)), bobc.xy, condRes]
            debugLineOffset = 0
            debugOffsets = yay.render("{}, {}".format(debugList[0], debugList[1]), True, 'white')
            window.blit(debugOffsets, (0, debugLineOffset))
            debugLineOffset += debugOffsets.get_height()
            debugLengths = yay.render("{}, {}".format(debugList[2], debugList[3]), True, 'white')
            window.blit(debugLengths, (0, debugLineOffset))
            debugLineOffset += debugLengths.get_height()
            debugCoords = yay.render("{}, {}".format(debugList[4], debugList[5]), True, 'white')
            window.blit(debugCoords, (0, debugLineOffset))
            debugLineOffset += debugCoords.get_height()
            debugCondRes = yay.render(str(debugList[6]), True, 'white')
            window.blit(debugCondRes, (0, debugLineOffset))
            debugLineOffset += debugCondRes.get_height()
        
        pygame.display.update()

        bobp.xy = bob

main()