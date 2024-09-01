import pygame
import random
import math
from pygame.locals import*
import time

# variables
background = (250,250,250)
red = (250, 10, 10)
blue = (10, 10, 250)
running = True

# agent variables
left, right, up, down = False, False, False, False
px, py = 100, 100
pSpeed = 6

# follower variables
fx, fy = 300, 100
fvx, fvy = 2, 2
fSpeed = 4

# make screen
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('FollowRun')
screen.fill(background)

# functions
def draw():
    #fill over last frame
    screen.fill(background)

    #draw the player
    pygame.draw.circle(screen, blue, (px,py), 20)
    pygame.draw.circle(screen, red, (fx,fy), 20)

    #display
    pygame.display.flip()

def inputs():
    global left, right, up, down, running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_DOWN:
                down = True
            if event.key == pygame.K_q:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = False

def update():
    #handle agent stuff
    global px,py
    if left:
        px-=pSpeed
    if right:
        px+=pSpeed
    if up:
        py-=pSpeed
    if down:
        py+=pSpeed

    #handle follower stuff
    global fx, fy, fvx, fvy
    fvx *= 0.975
    fvy *= 0.975
    fx += fvx
    fy += fvy
    if fx < px:
        fvx += 0.3
    if fx > px:
        fvx -= 0.3
    if fy < py:
        fvy += 0.3
    if fy > py:
        fvy -= 0.3
    if fx<0:
        fvx *=-1
        fx+=1
    if fx>width:
        fvx *=-1
        fx-=1
    if fy<0:
        fvy *=-1
        fy+=1
    if fy>height:
        fvy *=-1
        fy-=1
    if(random.random()>0.97):
        fvx += random.random()*7
    if(random.random()>0.97):
        fvx -= random.random()*7
    if(random.random()>0.97):
        fvy += random.random()*7
    if(random.random()>0.97):
        fvy -= random.random()*7

def getDist(): # returns a double value of the distance between dots
    return math.sqrt((px-fx)(px-fx) + (py-fy)(py-fy))

# main game loop
def loop():
    while running:
        inputs()
        update()

        draw()
        time.sleep(0.016) # ~60fps
        

# run
if __name__ == "__main__":
    loop()