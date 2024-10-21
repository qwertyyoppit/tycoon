import pygame
import math
from sys import exit
import os

pygame.init()

sw = 600
sh = 600

window = pygame.display.set_mode((sw,sh), pygame.SCALED | pygame.RESIZABLE)

gxscale = 6
gyscale = 2
gx = float(sw*gxscale)
gy = float(sh*gyscale)

offsetx = gx / 2 - sw / 2
offsety = gy / 2 - sh / 2

def load_sprites(directory):
    sprites = []
    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):  # Adjust file extensions as needed
            image = pygame.image.load(os.path.join(directory, filename)).convert_alpha()
            sprites.append(image)
    return sprites

sprites = load_sprites("sprites")
background = pygame.transform.scale(sprites[0], (gx, gy))
path = pygame.transform.scale(sprites[11], (gx, gy))
tiles = []
trailsheet = pygame.image.load("sprites/testspritesheet", "testspritesheet.png")

for i in range(trailsheet.get_width()/5):
    tiles.append(trailsheet.subsurface((5 * i, 5, 5, 5)))
trailsheet = pygame.transform.scale(trailsheet, (gx, gy))

groundmap = [
     9, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 8,
     2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
     6, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 1, 1, 1, 7, 1, 5,
     2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2,
    11, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 4, 1,10
]

path = pygame.Surface((gx, gy))
for i in range(len(groundmap)-1):
    path.blit(tiles[i-1], ((gx / 25 * i - gx * math.floor((i) / 25), ) if (i + 1) % 25 == 0 else ()))

def toCenter(width, height, *args):
    return (width / 2 - args[0].width / 2, height / 2 - args[0].height / 2)

bob = pygame.Rect(300.0, 100.0, 50.0, 50.0)
bob.x, bob.y = toCenter(sw, sh, bob)
bob_basespeed = 4.0
bob_effectspeed = bob_basespeed
bobp = pygame.math.Vector2(0.0, 0.0)
bobc = pygame.math.Vector2(0.0, 0.0)
movement = pygame.math.Vector2(1, 1)

yay = pygame.font.SysFont('calibri', 20, bold=True)
text = yay.render("HELP ME", True, 'white')

def tran(x, y, addx, addy):
    translated = (x + addx, y + addy)
    return translated

quadbool = 0
yes = False

condRes = 'Else'
debugMode = False
debugList = ''

Clock = pygame.time.Clock()
while True:
    dt = Clock.tick(60)/1000.0
    window.fill('black')
    text = yay.render(str(offsetx), True, 'white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                break
            if event.key == pygame.K_F3:
                debugMode = not debugMode
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
    if bobc.x > sw / 2 - bob.width / 2 and offsetx == 0.0:
        offsetx += bobc.x - sw / 2 + bob.width
        bobc.x = sw / 2 - bob.width
    # Player center left of horizontal center, offsetx is max: take distance past center, swap to offsetx
    elif bobc.x < sw / 2 - bob.width / 2 and offsetx == gx - sw:
        offsetx += bobc.x - sw / 2 + bob.width
        bobc.x = sw / 2 - bob.width
    # 
    elif offsetx > gx - sw:
        bobc.x += offsetx - gx + sw
        offsetx = gx - sw
    elif offsetx < 0.0:
        bobc.x += offsetx
        offsetx = 0.0

    if bobc.y > sh / 2 - bob.height / 2 and offsety == 0.0:
        offsety += bobc.y - sh / 2 + bob.height
        bobc.y = sh / 2 - bob.height
    elif bobc.y < sh / 2 - bob.height / 2 and offsety == gy - sh:
        offsety += bobc.y - sh / 2 + bob.height
        bobc.y = sh / 2 - bob.height
    elif offsety > gy - sh:
        bobc.y += offsety - gy + sh
        offsety = gy - sh
    elif offsety < 0.0:
        bobc.y += offsety
        offsety = 0.0

    if bobc.x < 0:
        bobc.x += -bobc.x
        movement.x = movement.x * -1
    if bobc.x + bob.width > sw:
        bobc.x += sw - bobc.x - bob.width
        movement.x = movement.x * -1
    if bobc.y < 0:
        bobc.y += -bobc.y
        movement.y = movement.y * -1
    if bobc.y + bob.height > sh:
        bobc.y += sh - bobc.y - bob.height
        movement.y = movement.y * -1

    if offsetx == 0.0 or offsetx == gx - sw:
        bob.x = bobc.x
    else:
        offsetx = bobc.x - bob.x + offsetx
    if offsety == 0.0 or offsety == gy - sh:
        bob.y = bobc.y
    else:
        offsety = bobc.y - bob.y + offsety

    bob_pos = pygame.math.Vector2(bob.x + offsetx, bob.y + offsety)
    bob_cpos = pygame.math.Vector2(bobc.x + offsetx, bobc.y + offsety)

    if keys[pygame.K_SPACE]:
        if yes == False:
            quadbool += 1
        elif yes == True:
            quadbool -= 1

    window.blit(background, (-offsetx, -offsety))
    window.blit(path, (-offsetx, -offsety))
    window.fill('blue', bob)
    if debugMode == True:
        debugList = []
        debugLineOffset = 0
        debugList.append(offsetx); debugList.append(offsety); debugList.append(pygame.Vector2((sw, sh))); debugList.append(pygame.Vector2((gx, gy))); debugList.append(pygame.Vector2((bob.x, bob.y))); debugList.append(bobc.xy); debugList.append(condRes)
        debugOffsets = yay.render("{}, {}".format(debugList[0], debugList[1]), True, 'white')
        window.blit(debugOffsets, (0, debugLineOffset))
        debugLineOffset += debugOffsets.get_height()
        debugLengths = yay.render("{}, {}".format(debugList[2], debugList[3]), True, 'white')
        window.blit(debugLengths, (0, debugLineOffset))
        debugLineOffset += debugLengths.get_height()
        debugCoords = yay.render("{}, {}".format(debugList[4], debugList[5]), True, 'white')
        window.blit(debugCoords, (0, debugLineOffset))
        debugLineOffset += debugCoords.get_height()
        debugCondRes = yay.render(debugList[6], True, 'white')
        window.blit(debugCondRes, (0, debugLineOffset))
        debugLineOffset += debugCondRes.get_height()
    pygame.display.update()

    bobp.xy = bob