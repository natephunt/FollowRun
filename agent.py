# TODO: find optimal network structure, add colision detection

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
        self.model = Linear_QNet(4, 64, 8)
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
        #print(f"q_values: {q_values}")
        if random.random() < self.epsilon:
            act = [0, 0, 0, 0, 0, 0, 0, 0] # left, right, up, down, leftup, rightup, leftdown, rightdown
            act[random.randint(0, q_values.size(dim=0) - 1)] = 1
            out = self.handleAction(act)
            print(f"random action {out}")
            return torch.tensor(out)  # Random action
        else:
            act = q_values.size(dim=0) * [0]
            act[torch.argmax(q_values).item()] = 1
            out = self.handleAction(act)
            print(f"action: {out}")
            return torch.tensor(out)

    def handleAction(self, action):
        out = [0, 0, 0, 0]
        if action[4] == 1 or action[5] == 1:
            out[2] = 1 # up
        if action[6] == 1 or action[7] == 1:
            out[3] = 1 # down
        if action[4] == 1 or action[6] == 1:
            out[0] = 1 # left
        if action[5] == 1 or action[7] == 1:
            out[1] = 1 # right
        if action[0] == 1:
            out[0] = 1
        if action[1] == 1:
            out[1] = 1
        if action[2] == 1:
            out[2] = 1
        if action[3] == 1:
            out[3] = 1
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
        reward, score, done = game.playStep(final_move.tolist())
        done = True if game.getFrame() > 1000 else done

        state_new = agent.get_state(game)

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if game.getFrame() > 1000 or done: 
            if score > record:
                record = score
                agent.model.save()
                print('Game', agent.n_games, 'Score', score, 'Record:', record)
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