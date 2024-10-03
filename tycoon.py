import pygame
import math
#from sympy import solve, Poly, Eq, Matrix, Symbol
#from sympy.abc import x, y, z, a, b
from sys import exit

pygame.init()

sw = 600
sh = 600

window = pygame.display.set_mode((sw,sh), pygame.SCALED | pygame.RESIZABLE)

gxscale = 6
gyscale = 2
gx = float(sw*gxscale)
gy = float(sh*gyscale)

offsetx = sw * gxscale / 2
offsety = sh * gyscale / 2

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
            if event.key == pygame.K_o:
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
    elif bobc.x < sw / 2 - bob.width / 2 and offsetx == gx:
        offsetx += bobc.x - sw / 2 + bob.width
        bobc.x = sw / 2 - bob.width
    # 
    elif offsetx > gx:
        bobc.x += offsetx-gx
        offsetx = gx
    elif offsetx < 0.0:
        bobc.x += offsetx
        offsetx = 0.0

    if bobc.y > sh / 2 - bob.height / 2 and offsety == 0.0:
        offsety += bobc.y - sh / 2 + bob.height
        bobc.y = sh / 2 - bob.height
    elif bobc.y < sh / 2 - bob.height / 2 and offsety == gy:
        offsety += bobc.y - sh / 2 + bob.height
        bobc.y = sh / 2 - bob.height
    elif offsety > gy:
        bobc.y += offsety-gy
        offsety = gy
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

    if offsetx == 0.0 or offsetx == gx:
        bob.x = bobc.x
    else:
        offsetx = bobc.x-bob.x+offsetx
    if offsety == 0.0 or offsety == gy:
        bob.y = bobc.y
    else:
        offsety = bobc.y-bob.y+offsety

    bob_pos = pygame.math.Vector2(bob.x + offsetx, bob.y + offsety)
    bob_cpos = pygame.math.Vector2(bobc.x + offsetx, bobc.y + offsety)

    if keys[pygame.K_SPACE]:
        if yes == False:
            quadbool += 1
        elif yes == True:
            quadbool -= 1

    window.fill('blue', bob)
    if debugMode == True:
        debugList = []
        debugList.append(offsetx); debugList.append(offsety); debugList.append(pygame.Vector2((bob.x, bob.y)), bobc.xy, condRes)
        debugOffsets = yay.render(debugList[0] + debugList[1], True, 'white')
        window.blit(debugOffsets, (0, 0))
        debugCoords = yay.render(debugList[2] + debugList[3], True, 'white')
        window.blit(debugCoords, (0, 0))
        debugCondRes = yay.render(debugList[4], True, 'white')
        window.blit(debugCondRes, (0, 0))
    pygame.display.update()

    bobp.xy = bob