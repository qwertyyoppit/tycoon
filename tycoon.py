import pygame
import math
import random
from sys import exit
import os

pygame.init()

class Structure(object):
    def __init__(self, sprite, rect):
        self.id = id
        self.sprite = sprite
        self.rect = rect

class Crop(Structure):
    def __init__(self, sprite, rect, stageSprites, type, growthrate, cropYields):
        super().__init__(sprite, rect)
        self.stageSprites = stageSprites
        self.stageSprites.append(pygame.Surface((self.sprite.get_width(), self.sprite.get_height())).convert_alpha())
        self.cropType = type
        self.baseGrowthRate = growthrate
        self.growthProgress = 0.0
        self.growthStage = 0
        self.harvestable = False
        self.planted = False
        self.cropYields = cropYields
    
    def update(self, dt):
        if self.planted == True:
            self.growthProgress += self.baseGrowthRate * dt * 10 if cropCheat == True else self.baseGrowthRate * dt
        else:
            self.sprite = self.stageSprites[3]
        if self.growthProgress >= 1.0:
            self.growthProgress = 1.0
            self.harvestable = True
        else:
            self.harvestable = False

        # sprite 0, 1, or 2 based on stage. if plantable == false, render no sprite
        if self.growthProgress == 1.0:
            self.growthStage = 2
        elif self.growthProgress >= 0.5:
            self.growthStage = 1
        elif self.growthProgress < 0.5:
            self.growthStage = 0

        if self.growthStage == 0:
            self.sprite = self.stageSprites[0]
        elif self.growthStage == 1:
            self.sprite = self.stageSprites[1]
        elif self.growthStage == 2:
            self.sprite = self.stageSprites[2]

    def interact(self):
        if self.harvestable == True:
            chance = random.randint(0, 1000) / 1000
            randomYield = 0
            for i in range(len(self.cropYields)):
                if chance <= self.cropYields[i][1]:
                    randomYield = self.cropYields[i][0]
                    break
            produce[self.cropType][1] += randomYield
            self.growthProgress = 0.0
            self.planted = False
        elif self.planted == False:
            if seeds[self.cropType][1] > 0:
                self.planted = True
                seeds[self.cropType][1] -= 1
    
    def get_interactable(self):
        if self.harvestable == True or (self.planted == False and seeds[self.cropType][1] > 0) == True:
            return True
        else:
            return False

class uiButton(object):
    def __init__(self, rect, color, colorHover=None, colorActive=None, colorActiveHover=None):
        self.rect = rect
        self.color = color
        if colorHover != None:
            self.colorHover = colorHover
        if colorActive != None:
            self.colorActive = colorActive
        if colorActiveHover != None:
            self.colorActiveHover = colorActiveHover
        self.active = False

    def get_color(self):
        if self.active == False:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and mousePressed[0] == False:
                return self.colorHover
            else:
                return self.color
        elif self.active == True:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return self.colorActiveHover
            else:
                return self.colorActive

    def set_active(self, state=None):
        self.active = not self.active if state == None else state

sw = 600
sh = 600

window = pygame.display.set_mode((sw,sh), pygame.SCALED | pygame.RESIZABLE)

gxscale = 6
gyscale = 2
gx = float(sw*gxscale)
gy = float(sh*gyscale)
tilew = gx / 50

offset = pygame.Vector2(gx / 2 - sw / 2, gy / 2 - sh / 2)
offsetp = pygame.Vector2(0, 0)

SmallThin = pygame.font.SysFont('helvetica', 20, bold=False)
SmallThick = pygame.font.SysFont('helvetica', 20, bold=True)
LargeThin = pygame.font.SysFont('helvetica', 40, bold=False)
LargeThick = pygame.font.SysFont('helvetica', 40, bold=True)

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
carrotRect = pygame.Rect(0, 0, carrotSprite[0].get_width(), carrotSprite[0].get_height())
cornRect = pygame.Rect(0, 0, cornSprite[0].get_width(), cornSprite[0].get_height())
potatoRect = pygame.Rect(0, 0, potatoSprite[0].get_width(), potatoSprite[0].get_height())
tomatoRect = pygame.Rect(0, 0, tomatoSprite[0].get_width(), tomatoSprite[0].get_height())
watermelonRect = pygame.Rect(0, 0, watermelonSprite[0].get_width(), watermelonSprite[0].get_height())
wheatRect = pygame.Rect(0, 0, wheatSprite[0].get_width(), wheatSprite[0].get_height())

ground = pygame.transform.scale(sprites[0], (gx, gy))
tiles = [pygame.Surface((tilew, tilew))]
trailsheet = pygame.image.load("sprites/testspritesheet.png", "testspritesheet.png")
trailsheet = pygame.transform.scale(trailsheet, (trailsheet.get_width() / 5 * tilew, tilew))
for i in range(math.floor(trailsheet.get_width() / tilew)):
    tiles.append(trailsheet.subsurface(tilew * i, 0, tilew, tilew))

objList = []
typeIdList = []

barnRect = pygame.Rect(0, 0, 19 * gxscale, 15 * gxscale)
barnSprite = pygame.image.load("sprites/barn2.png", "barn2.png")
barn = Structure(pygame.transform.scale(barnSprite, (barnSprite.get_width() * gxscale, barnSprite.get_height() * gxscale)), barnRect)
typeIdList.append(barn)

carrotCrop = Crop(carrotSprite[0], carrotRect, carrotSprite, 'carrot', 0.5, [(2, 0.5), (3, 1.0)])
typeIdList.append(carrotCrop)
cornCrop = Crop(cornSprite[0], cornRect, cornSprite, 'corn', 0.05, [(2, 0.5), (3, 1.0)])
typeIdList.append(cornCrop)
potatoCrop = Crop(potatoSprite[0], potatoRect, potatoSprite, 'potato', 0.05, [(2, 0.5), (3, 1.0)])
typeIdList.append(potatoCrop)
tomatoCrop = Crop(tomatoSprite[0], tomatoRect, tomatoSprite, 'tomato', 0.05, [(2, 0.5), (3, 1.0)])
typeIdList.append(tomatoCrop)
watermelonCrop = Crop(watermelonSprite[0], watermelonRect, watermelonSprite, 'watermelon', 0.05, [(1, 19/20), (2, 1.0)])
typeIdList.append(watermelonCrop)
wheatCrop = Crop(wheatSprite[0], wheatRect, wheatSprite, 'wheat', 0.05, [(3, 1/3), (4, 2/3), (5, 1.0)])
typeIdList.append(wheatCrop)

objectmap = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 7, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 4, 0, 0, 5, 0, 0, 6, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

for i in range(len(objectmap)):
    if objectmap[i] != 0:
        index = typeIdList[objectmap[i]-1]
        tempStructure = Structure(index.sprite, pygame.Rect((i * tilew - gx * (math.floor(i / (50))), tilew * (math.floor(i / (50)) + 1)), (index.rect.width, index.rect.height)))
        if type(index) == Crop:
            objList.append(Crop(tempStructure.sprite, tempStructure.rect, index.stageSprites, index.cropType, index.baseGrowthRate, index.cropYields))
        else:
            objList.append(tempStructure)

testgroundmap = [
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

groundmap = [
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 0, 0, 0, 0, 0,
 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
 0, 2, 0, 0, 0, 9, 1, 1, 8, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 4, 1, 1, 1, 8, 0,
 0, 6, 1, 1, 1, 5, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 2, 0, 0, 0, 2, 0, 0, 2, 0,11, 3, 1, 1, 1, 1, 3, 8, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 2, 0, 0, 0,11, 3, 1,10, 0, 0, 2, 0, 0, 0, 0, 6, 4, 1, 1, 1, 7, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 6, 1, 1, 1, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 9,10, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 2, 0, 0, 9, 1, 4, 1, 3, 1, 1, 4, 1, 3, 1, 5, 0, 0, 0, 0, 0, 6, 1, 3, 1, 1, 5, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 6, 1, 1, 3, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 5, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 6, 1, 1, 5, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0,11, 3, 1, 1, 1, 1,10, 0,11, 1, 3,10, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 2, 0, 0,11, 1, 1, 1,10, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0,
 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 4, 1, 1, 4, 8, 0, 0, 0, 0, 0, 0, 0, 6, 3, 1, 1,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 1, 1, 1, 1, 1, 1, 1,10, 0,
 0,11, 1, 1, 1, 1, 1, 1, 1, 1,10, 0, 0, 0, 0, 0, 0,11, 1, 1, 1, 1, 1, 1, 1, 4,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

path = pygame.Surface((gx, gy))
path.fill((0, 0, 0, 255))
for i in range(len(groundmap)):
    if groundmap[i] != 0:
        ground.blit(tiles[groundmap[i]], (i * tilew - gx * (math.floor(i / (50))), tilew * (math.floor(i / (50)) + 1)))

game_time = 480.0
baseTimeSpeed = 1.0

game_time = 480.0
baseTimeRate = 2
dayLength = 1440.0
dayPeriods = ['midnight', 'morning', 'noon', 'evening']
time_of_day = dayPeriods[0]

bob = pygame.Rect(300.0, 100.0, 50.0, 50.0)
bob.x, bob.y = sw / 2 - bob.width / 2, sh / 2 - bob.height / 2
bob_basespeed = 4.0
bob_effectspeed = bob_basespeed
bobp = pygame.math.Vector2(0.0, 0.0)
bobc = pygame.math.Vector2(0.0, 0.0)
movement = pygame.math.Vector2(1, 1)

money = 0

itemIds = ['carrot', 'corn', 'potato', 'tomato', 'watermelon', 'wheat']

produce = {
    'carrot': ['carrot', 0],
    'corn': ['corn', 0],
    'potato': ['potato', 0],
    'tomato': ['tomato', 0],
    'watermelon': ['watermelon', 0],
    'wheat': ['wheat', 0]
}

seeds = {
    'carrot': ['carrot', 0],
    'corn': ['corn', 0],
    'potato': ['potato', 0],
    'tomato': ['tomato', 0],
    'watermelon': ['watermelon', 0],
    'wheat': ['wheat', 3]
}

buyValue = {
    'carrot': 15,
    'corn': 60,
    'potato': 25,
    'tomato': 40,
    'watermelon': 80,
    'wheat': 10
}

sellValue = {
    'carrot': 10, # 10 * 2-3
    'corn': 40, # 40 * 2-3
    'potato': 20, # 20 * 2-4
    'tomato': 25, # 25 * 2-4
    'watermelon': 100, # 100 * 1-2 (2 rare)
    'wheat': 5 # 10 * 3-5
}

quadbool = 0
yes = False
interact = None
inventory = False
shop = False
invCat = 'produce'
invItemSelected = 0

invBackground = pygame.Rect(sw / 2 - 500 / 2, sh / 2 - 400 / 2, 500, 400)
invItemPos = pygame.Vector2(invBackground.x + 50 * 3, invBackground.y + 50 * 3)
invItemRect = pygame.Rect(invBackground.x + 75, invItemPos.y, 100, 50)
invItemUpRect = uiButton(pygame.Rect(invBackground.x + 30, invItemPos.y - 40, 200, 40), (117, 117, 117), (158, 158, 158))
invItemDownRect = uiButton(pygame.Rect(invBackground.x + 30, invItemPos.y + invItemRect.height, 200, 40), (117, 117, 117), (158, 158, 158))
invProdTab = uiButton(pygame.Rect(invBackground.x + 25, invBackground.y + 25, 100, 30), (35, 35, 35), (177, 171, 207), (100,90,150), (127, 118, 173))
invProdTab.set_active(True)
invSeedTab = uiButton(pygame.Rect(invBackground.x + 50 * 3, invBackground.y + 25, 100, 30), (35, 35, 35), (177, 171, 207), (100,90,150), (127, 118, 173))
invMoneyRect = pygame.Rect(invBackground.x + invBackground.width - 100, invBackground.y + 25, 75, 30)
invBuyRect = uiButton(pygame.Rect(invBackground.x + 50 * 6, invItemPos.y + invItemRect.height / 2 - 25, 50, 50), (211, 47, 47), (237, 49, 49))
invSellRect = uiButton(pygame.Rect(invBackground.x + 50 * 7.5, invItemPos.y + invItemRect.height / 2 - 25, 50, 50), (67, 160, 71), (76, 175, 80))

mouseHandled = True
events = []

controlsText = SmallThick.render("WASD or Arrows: Move | E: Plant/harvest | TAB: inventory", True, "white", "black")

# debug tools
condRes = 'Else'
cropCheat = False
debugMode = False
debugList = ''
renderRects = False

Clock = pygame.time.Clock()
while True:
    dt = Clock.tick(60)/1000.0
    game_time += dt * baseTimeRate

    mousePressed = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()
    left = keys[pygame.K_a] or keys[pygame.K_LEFT]
    right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
    up = keys[pygame.K_w] or keys[pygame.K_UP]
    down = keys[pygame.K_s] or keys[pygame.K_DOWN]
    
    movement = pygame.math.Vector2(right - left, down - up)

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
            if event.key == pygame.K_F5:
                cropCheat = not cropCheat
            if event.key == pygame.K_e:
                interacting = None
                for i in objList:
                    if bob.colliderect(i.rect) and i.get_interactable() == True:
                        interacting = i
                        break
                if type(interacting) == Crop:
                    interacting.interact()
            if event.key == pygame.K_x:
                print(objList[bob.collidelist(objList)])
            if event.key == pygame.K_TAB:
                inventory = not inventory
            if event.key == pygame.K_o:
                shop = not shop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if invBuyRect.rect.collidepoint(mousePos) and inventory == True and shop == True:
                    events.append('invBuy')
                if invSellRect.rect.collidepoint(mousePos) and inventory == True and shop == True:
                    events.append('invSell')
                if invItemUpRect.rect.collidepoint(mousePos) and inventory == True:
                    events.append('invItemUp')
                if invItemDownRect.rect.collidepoint(mousePos) and inventory == True:
                    events.append('invItemDown')
                if invProdTab.rect.collidepoint(mousePos) and inventory == True:
                    events.append('invCatProd')
                if invSeedTab.rect.collidepoint(mousePos) and inventory == True:
                    events.append('invCatSeeds')


    if quadbool <= 0:
        yes = False
    elif quadbool >= 3:
        yes = True
    
    bobc.xy = (0.0, 0.0)
    bob_effectspeed = bob_basespeed

    if keys[pygame.K_LSHIFT] == 1:
        bob_effectspeed *= 5
    bobc.xy = bob.x + bob_effectspeed * movement.x, bob.y + bob_effectspeed * movement.y

    if math.dist((bobp), (bobc)) > bob_effectspeed:
        bobc.xy = (bob.x + (bob_effectspeed / math.sqrt(2) * movement.x), bob.y + (bob_effectspeed / math.sqrt(2) * movement.y))
    
    # Player center right of horizontal center, offset.x is min: take distance past center, swap it to offset.x
    if bobc.x > sw / 2 - bob.width / 2 and (offset.x == 0.0 and offset.x != gx - sw):
        offset.x += bobc.x - sw / 2 + bob.width
        bobc.x = sw / 2 - bob.width
    # Player center left of horizontal center, offset.x is max: take distance past center, swap to offset.x
    elif bobc.x < sw / 2 - bob.width / 2 and (offset.x != 0.0 and offset.x == gx - sw):
        offset.x += bobc.x - sw / 2 + bob.width
        bobc.x = sw / 2 - bob.width
    # 
    elif offset.x > gx - sw:
        bobc.x += offset.x - gx + sw
        offset.x = gx - sw
    elif offset.x < 0.0:
        bobc.x += offset.x
        offset.x = 0.0

    if bobc.y > sh / 2 - bob.height / 2 and (offset.y == 0.0 and offset.y != gy - sh):
        offset.y += bobc.y - sh / 2 + bob.height
        bobc.y = sh / 2 - bob.height
    elif bobc.y < sh / 2 - bob.height / 2 and (offset.y != 0.0 and offset.y == gy - sh):
        offset.y += bobc.y - sh / 2 + bob.height
        bobc.y = sh / 2 - bob.height
    elif offset.y > gy - sh:
        bobc.y += offset.y - gy + sh
        offset.y = gy - sh
    elif offset.y < 0.0:
        bobc.y += offset.y
        offset.y = 0.0

    if offset.x == 0.0 or offset.x == gx - sw:
        bob.x = bobc.x
    else:
        offset.x = bobc.x - bob.x + offset.x
    if offset.y == 0.0 or offset.y == gy - sh:
        bob.y = bobc.y
    else:
        offset.y = bobc.y - bob.y + offset.y

    if bob.x < 0:
        bob.x = 0
        movement.x = movement.x * -1
    if bob.x + bob.width > sw:
        bob.x += sw - bob.x - bob.width
        movement.x = movement.x * -1
    if bob.y < 0:
        bob.y = 0
        movement.y = movement.y * -1
    if bob.y + bob.height > sh:
        bob.y += sh - bob.y - bob.height
        movement.y = movement.y * -1

    if keys[pygame.K_SPACE]:
        if yes == False:
            quadbool += 1
        elif yes == True:
            quadbool -= 1


    window.blit(ground, (- offset.x, - offset.y))
    for i in objList:
        if bob.contains(i.rect):
            interact = objList.index(i)

    for i in objList:
        if type(i) == Crop:
            i.update(dt)

    for i in objList:
        i.rect.x -= (offset.x - offsetp.x)
        i.rect.y -= (offset.y - offsetp.y)
        
    for i in objList:
        window.blit(i.sprite, i.rect)

    if renderRects == True:
        for i in objList:
            window.fill('red', i.rect)

    window.fill('blue', bob)

    time_hour = math.floor(math.floor(game_time) / 60)
    time_minute = math.floor(game_time) - 60 * time_hour
    time_text = SmallThin.render(str(time_hour) + ':' + ('0' + str(time_minute) if len(str(time_minute)) == 1 else str(time_minute)) + ' (' + time_of_day + ')', True, 'white', (25, 25, 25, 25))

    if inventory == True:
        window.fill((25,25,25), invBackground)
        window.fill(invProdTab.get_color(), invProdTab)
        window.fill(invSeedTab.get_color(), invSeedTab)
        window.fill(invItemUpRect.get_color(), invItemUpRect)
        window.fill(invItemDownRect.get_color(), invItemDownRect)
        moneyText = SmallThick.render("$" + str(money), True, 'white', (30,30,30))
        window.blit(moneyText, (invMoneyRect.x, invMoneyRect.y + invMoneyRect.height / 2 - moneyText.get_height() / 2))
        produceText = SmallThick.render("Produce", True, "white")
        window.blit(produceText, (invProdTab.rect.x + invProdTab.rect.width / 2 - produceText.get_width() / 2, invProdTab.rect.y + invProdTab.rect.height / 2 - produceText.get_height() / 2))
        seedText = SmallThick.render("Seeds", True, "white")
        window.blit(seedText, (invSeedTab.rect.x + invSeedTab.rect.width / 2 - seedText.get_width() / 2, invSeedTab.rect.y + invSeedTab.rect.height / 2 - seedText.get_height() / 2))
        itemText = LargeThin.render(eval(invCat)[itemIds[invItemSelected]][0], True, 'white')
        window.blit(itemText, (invItemRect.x + invItemRect.width / 2 - itemText.get_width() / 2, invItemPos.y + invItemRect.height / 2 - itemText.get_height() / 2))
        itemCount = LargeThick.render(str(eval(invCat)[itemIds[invItemSelected]][1]), True, 'white')
        window.blit(itemCount, (invItemPos.x + invItemRect.width, invItemPos.y + invItemRect.height / 2 - itemCount.get_height() / 2))
        
        if 'invItemUp' in events:
            events.remove('invItemUp')
            invItemSelected = invItemSelected - 1 if invItemSelected - 1 >= 0 else len(itemIds) - 1
        if 'invItemDown' in events:
            events.remove('invItemDown')
            invItemSelected = invItemSelected + 1 if invItemSelected + 1 < len(itemIds) else 0
        if 'invCatProd' in events:
            events.remove('invCatProd')
            invCat = 'produce'
            invProdTab.set_active(True)
            invSeedTab.set_active(False)
        if 'invCatSeeds' in events:
            events.remove('invCatSeeds')
            invCat = 'seeds'
            invSeedTab.set_active(True)
            invProdTab.set_active(False)
    
        if shop == True:
            window.fill(invBuyRect.get_color(), invBuyRect)
            window.fill(invSellRect.get_color(), invSellRect)
            priceText = SmallThin.render(str(buyValue[itemIds[invItemSelected]]), True, 'white')
            window.blit(priceText, (invBuyRect.rect.x + invBuyRect.rect.width / 2 - priceText.get_width() / 2, invBuyRect.rect.y + invBuyRect.rect.height / 2 - priceText.get_height() / 2))
            sellText = SmallThin.render(str(sellValue[itemIds[invItemSelected]]), True, 'white')
            window.blit(sellText, (invSellRect.rect.x + invSellRect.rect.width / 2 - sellText.get_width() / 2, invSellRect.rect.y + invSellRect.rect.height / 2 - sellText.get_height() / 2))
            
            if 'invBuy' in events:
                events.remove('invBuy')
                if money - buyValue[itemIds[invItemSelected]] >= 0:
                    money -= buyValue[itemIds[invItemSelected]]
                    eval(invCat)[itemIds[invItemSelected]][1] += 1
            if 'invSell' in events:
                events.remove('invSell')
                if produce[itemIds[invItemSelected]][1] > 0:
                    money += sellValue[itemIds[invItemSelected]]
                    produce[itemIds[invItemSelected]][1] -= 1

    window.blit(time_text, (window.get_width() - time_text.get_width(), 0))
    if debugMode == True:
        debugList = [offset.x, offset.y, pygame.Vector2((sw, sh)), pygame.Vector2((gx, gy)), pygame.Vector2((bob.x, bob.y)), bobc.xy, condRes]
        debugLineOffset = 0
        debugOffsets = SmallThin.render("{}, {}".format(debugList[0], debugList[1]), True, 'white')
        window.blit(debugOffsets, (0, debugLineOffset))
        debugLineOffset += debugOffsets.get_height()
        debugLengths = SmallThin.render("{}, {}".format(debugList[2], debugList[3]), True, 'white')
        window.blit(debugLengths, (0, debugLineOffset))
        debugLineOffset += debugLengths.get_height()
        debugCoords = SmallThin.render("{}, {}".format(debugList[4], debugList[5]), True, 'white')
        window.blit(debugCoords, (0, debugLineOffset))
        debugLineOffset += debugCoords.get_height()
        debugCondRes = SmallThin.render(str(debugList[6]), True, 'white')
        window.blit(debugCondRes, (0, debugLineOffset))
        debugLineOffset += debugCondRes.get_height()
    
    window.blit(controlsText, (5, sh - controlsText.get_height()))
    
    pygame.display.update()

    bobp.xy = bob
    offsetp.xy = (offset.x, offset.y)