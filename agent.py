# TODO: find optimal network structure, creat 8 channel output, add colision detection

import torch
import torch.nn as nn
import torch.nn.functional as F

import random
import numpy as np
from collections import deque
from main import Game, Player, Agent, Follower
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Aigent:

    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0.1 #randomness
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(4, 64, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        state = game.getState()
        #print(state)
        return torch.tensor(state, dtype=torch.float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        #states, actions, rewards, next_states, dones = zip(*mini_sample)
        #self.trainer.train_step(states, actions, rewards, next_states, dones)

        for state, action, reward, next_state, done in mini_sample:
            self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        q_values = self.model(state)
        if random.random() < self.epsilon:
            out = [0, 0, 0, 0]
            out[random.randint(0, 3)] = 1
            print("random action")
            return torch.tensor(out)  # Random action
        else:
            out = [0, 0, 0, 0]
            out[torch.argmax(q_values).item()] = 1
            print(f"action: {out}")
            return torch.tensor(out)


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Aigent()
    game = Game()

    while True:
        #get old state
        state_old = agent.get_state(game)

        #get move
        final_move = agent.get_action(state_old)

        #perform move + step

        #print(f"Final move: {final_move}")
        reward, score = game.playStep(final_move.tolist())
        done = game.getFrame() > 700

        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if game.getFrame() > 700:
            #train long memory, plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

            

if __name__ == '__main__':
    train()


''' david wu code -- was in train short memory
        pred_q = self.q(state)
        action_q = pred_q[action]
        target_q = reward + self.gamma * torch.max(self.q(next_state).detach())

        loss = F.mse_loss(acion_q, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        print(f"Loss: {loss.item():.3f}")
'''