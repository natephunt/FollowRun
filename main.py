import pygame
import random
import math
from pygame.locals import *
import time

playeraction = [0, 0, 0, 0]  # left, right, up, down
WALL_DISLIKE = 0.04


class Player:
    x, y, vx, vy, drag = 0, 0, 0, 0, 0
    color = (20, 20, 20)

    def __init__(self, x, y, drag, color):
        self.x = x
        self.y = y
        self.drag = drag
        self.color = color
    
    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def update(self, game):
        if self.x < 0:
            self.vx *= -1
            self.x = 1
        if self.x > game.width:
            self.vx *= -1
            self.x = game.width-1
        if self.y < 0:
            self.vy *= -1
            self.y = 1
        if self.y > game.height:
            self.vy *= -1
            self.y = game.height-1

        self.vx *= self.drag
        self.vy *= self.drag
        self.x += self.vx
        self.y += self.vy
    
    def reset(self, x, y):
        self.x, self.y, self.vx, self.vy = x,y,0,0
    
    def draw(self, game):
        pygame.draw.circle(game.screen, self.color, (self.x, self.y), 20)

class Agent(Player):
    speed = 6
    left = False
    right = False
    up = False
    down = False

    def __init__(self, x, y, drag, color):
        super().__init__(x, y, drag, color)

    def update(self, game):
        self.vx = 0
        self.vy = 0

        if self.left:
            self.vx = -self.speed
        if self.right:
            self.vx = self.speed
        if self.up:
            self.vy = -self.speed
        if self.down:
            self.vy = self.speed
        
        super().update(game)
    
    def setLeft(self, t):
        self.left = t
    def setRight(self, t):
        self.right = t
    def setUp(self, t):
        self.up = t
    def setDown(self, t):
        self.down = t

    def reset(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        super().reset(300, 200)
    

class Follower(Player):
    def __init__(self, x, y, drag, color):
        super().__init__(x, y, drag, color)

    def update(self, agent, game):
        #home follower
        if self.x < agent.x:
            self.vx += 0.3
        if self.x > agent.x:
            self.vx -= 0.3
        if self.y < agent.y:
            self.vy += 0.3
        if self.y > agent.y:
            self.vy -= 0.3

        # Random velocity changes for the follower
        if random.random() > 0.97:
            self.vx += random.random() * 7
        if random.random() > 0.97:
            self.vx -= random.random() * 7
        if random.random() > 0.97:
            self.vy += random.random() * 7
        if random.random() > 0.97:
            self.vy -= random.random() * 7

        # Collision detection with the agent
        #if game.getDistance(self, agent) < 50:
        #    self.vx *= -1
        #    self.vy *= -1

        super().update(game)

# ---------------------------------------------------------------------------------------------------------

class Game:
    width, height = 640, 480
    background = (250, 250, 250)
    running = True
    frame = 0
    agent = Agent(0, 0, 0, (0, 0, 0))
    follower = Follower(0, 0, 0, (0, 0, 0))
    score = 0


    def __init__(self):
        pygame.init()
        width, height = 640, 480
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('FollowRun')
        self.background = (250, 250, 250)
        self.running = True
        self.agent = Agent(320, 240, 1, (10, 10, 250))
        self.follower = Follower(0, 0, 0.975, (250, 10, 10))
        self.reset()

    def reset(self):
        self.frame = 0
        self.score = 0
        self.running = True
        self.agent.reset()
        x, y = random.randint(10, 630), random.randint(10, 470)
        self.follower.reset(x, y)

    def update(self):
        self.agent.update(self)
        self.follower.update(self.agent, self)

    def draw(self):
        self.screen.fill(self.background)
        self.agent.draw(self)
        self.follower.draw(self)
        pygame.display.flip()

    def getDistance(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
    
    def getFrame(self):
        return self.frame
    
    def convertAction(self, action):
        if action [0] > 0.5:
            self.agent.left = True
        else:
            self.agent.left = False
        if action [1] > 0.5:
            self.agent.right = True
        else:
            self.agent.right = False
        if action [2] > 0.5:
            self.agent.up = True
        else:
            self.agent.up = False
        if action [3] > 0.5:
            self.agent.down = True
        else:
            self.agent.down = False

    def playStep(self, action):
        self.convertAction(action)
        self.update()
        self.draw()
        self.frame += 1
        dist = self.getDistance(self.agent, self.follower)
        antiwall = (WALL_DISLIKE*(self.agent.get_x() - self.width/2))**2 - (WALL_DISLIKE*(self.agent.get_y() - self.height/2))**2
        reward = (dist - 50) - antiwall
        reward = reward / 100
        self.score += reward
        #print(reward)
        return reward, self.score, self.getDistance(self.agent, self.follower) < 50
    
    def getState(self):
        return [self.agent.get_x(), self.agent.get_y(), self.follower.get_x(), self.follower.get_y()]
        

def pollInputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playeraction[0] = 1
            if event.key == pygame.K_RIGHT:
                playeraction[1] = 1
            if event.key == pygame.K_UP:
                playeraction[2] = 1
            if event.key == pygame.K_DOWN:
                playeraction[3] = 1
            if event.key == pygame.K_ESCAPE:
                game.running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playeraction[0] = 0
            if event.key == pygame.K_RIGHT:
                playeraction[1] = 0
            if event.key == pygame.K_UP:
                playeraction[2] = 0
            if event.key == pygame.K_DOWN:
                playeraction[3] = 0
    return playeraction

if __name__ == "__main__":
    game = Game()

    while game.running:
        game.playStep(pollInputs())
        time.sleep(0.016)  # ~60fps