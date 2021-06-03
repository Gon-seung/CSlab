from simulator import move_forward, turn_left, turn_right, reset_map, set_speed, show_animation, test
# DO NOT MODIFY LINE 1
# You may import any libraries you want. But you may not import simulator_hidden
import random
import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import math

show_animation(True)
set_speed(500)          # This line is only meaningful if animations are enabled.
 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

grid_size = (12, 12)
goal1 = (10, 10)
goal2 = (1, 10)
orientation = ['N','E','S','W']
actions = [move_forward, turn_left, turn_right]
num_epochs = 2000

def reward(coor, done):
	"""
	Task 6 (optional) - design your own reward function
	"""

	x, y = coor
	if coor == goal:
		return 10
	elif done:
		return -100
	
	return 0


class ReplayMemory(object):
	def __init__(self, capacity):
		self.capacity = capacity
		self.memory = []
		self.position = 0

	def push(self, transition):

		"""
		Task 3 - 
		push input: "transition" into replay meory
		"""

		return

	def sample(self, batch_size):
		"""
		Task 3 - 
		give a batch size, pull out batch_sized samples from the memory
		"""
		return

	def __len__(self):
		return len(self.memory)

class DQN(nn.Module):
	def __init__(self):
		super(DQN, self).__init__()
		"""
		Task 1 -
		generate your own deep neural network
		"""

	def forward(self, x):
		"""
		Task 1 - 
		generate your own deep neural network
		"""
		return 

def optimize_model():
	if len(memory) < BATCH_SIZE:
		return
	transition = memory.sample(BATCH_SIZE)
	"""
	Task 4: optimize model
	"""


policy_net = DQN().to(device)
target_net = DQN().to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.RMSprop(policy_net.parameters())
memory = ReplayMemory(1000)


def select_action(state):
	"""
	Task 2: select action
	"""
	return
	

TARGET_UPDATE = 5
for i in range(num_epochs):
	print(i)
	(x, y), ori, sensor, done = reset_map()
	while not done:
		o_i = orientation.index(ori)

		cur_state = #create your own state

		idx_action = select_action(cur_state).item()
		action = actions[idx_action]
		(new_x, new_y), new_ori, new_sensor, done = action()
		new_o_i = orientation.index(new_ori)

		reward_val = reward((new_x,new_y),done)


		transition = # generate your own transition form


		memory.push(transition)
		(x, y), ori, sensor = (new_x, new_y), new_ori, new_sensor
		optimize_model()



"""
Task 5 - save your policy net
"""



def test_network():
	"""
	Task 5: test your network
	"""
	set_speed(3)
	test()
	(x, y), ori, sensor, done = reset_map()
	
	policy_net = # load policy net

	policy_net.eval()

	while True:
		o_i = orientation.index(ori)
		"""
		fill this section to test your network
		"""
test_network()

###############################

#### If you want to try moving around the map with your keyboard, uncomment the below lines 
# import pygame
# set_speed(5)
# show_animation(True)
# while True:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			exit("Closing...")
# 		if event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_LEFT: print(turn_left())
# 			if event.key == pygame.K_RIGHT: print(turn_right())
# 			if event.key == pygame.K_UP: print(move_forward())
# 			if event.key == pygame.K_t: test()
# 			if event.key == pygame.K_r: print(reset_map())
# 			if event.key == pygame.K_q: exit("Closing...")