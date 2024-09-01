import pygame
import random
import math
from pygame.locals import *
import time

class Game:
    width, height = 640, 480
    background = (250, 250, 250)
    running = True

    def __init__(self):
        pygame.init()
        width, height = 640, 480
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('FollowRun')
        self.background = (250, 250, 250)
        self.running = True
        self.reset()

    def reset(self):
        pass

    def pollInputs(self, agent):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    agent.left = True
                if event.key == pygame.K_RIGHT:
                    agent.right = True
                if event.key == pygame.K_UP:
                    agent.up = True
                if event.key == pygame.K_DOWN:
                    agent.down = True
                if event.key == pygame.K_q:
                    self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    agent.left = False
                if event.key == pygame.K_RIGHT:
                    agent.right = False
                if event.key == pygame.K_UP:
                    agent.up = False
                if event.key == pygame.K_DOWN:
                    agent.down = False

    def update(self):
        agent.update()
        follower.update()

    def draw(self):
        self.screen.fill(self.background)
        agent.draw()
        follower.draw()
        pygame.display.flip()

    def get_distance(self):
        return math.sqrt((agent.x - follower.x) ** 2 + (agent.y - follower.y) ** 2)

    def loop(self):
        while self.running:
            self.pollInputs(agent)
            self.update()
            self.draw()
            time.sleep(0.016)  # ~60fps

class Player:
    x, y, vx, vy, drag = 0, 0, 0, 0, 0
    color = (20, 20, 20)

    def __init__(self, x, y, drag, color):
        self.x = x
        self.y = y
        self.drag = drag
        self.color = color
    
    def update(self):
        self.vx *= self.drag
        self.vy *= self.drag
        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.vx *= -1
            self.x += 1
        if self.x > game.width:
            self.vx *= -1
            self.x -= 1
        if self.y < 0:
            self.vy *= -1
            self.y += 1
        if self.y > game.height:
            self.y *= -1
            self.y -= 1
    
    def draw(self):
        pygame.draw.circle(game.screen, self.color, (self.x, self.y), 20)

class Agent(Player):
    speed = 6
    left = False
    right = False
    up = False
    down = False

    def __init__(self, x, y, drag, color):
        super().__init__(x, y, drag, color)

    def update(self):
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

        super().update()

class Follower(Player):
    def __init__(self, x, y, drag, color):
        super().__init__(x, y, drag, color)

    def update(self):
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

        super().update()

if __name__ == "__main__":
    game = Game()
    agent = Agent(300, 200, 1, (10, 10, 250))
    follower = Follower(50, 50, 0.975, (250, 10, 10))
    game.loop()
