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
epsilon = 0.8
BATCH_SIZE = 64

def reward(coor, done):
	"""
	Task 6 (optional) - design your own reward function
	"""

	x, y = coor
	if coor == goal1 or coor == goal2:
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
		if len(self.memory) < self.capacity:
			self.memory.append(None)
		self.memory[self.position] = transition
		self.position = (self.position+1)%self.capacity

		return

	def sample(self, batch_size):
		"""
		Task 3 - 
		give a batch size, pull out batch_sized samples from the memory
		"""
		random_sample = random.sample(self.memory, batch_size)
		return random_sample

	def __len__(self):
		return len(self.memory)

class DQN(nn.Module):
	def __init__(self):
		super(DQN, self).__init__()
		"""
		Task 1 -
		generate your own deep neural network
		"""
		self.linear1 = nn.Linear(8, 256)
		self.relu = nn.ReLU()
		self.linear2 = nn.Linear(256, 512)
		self.linear3 = nn.Linear(512, 256)
		self.linear4 = nn.Linear(256, 3)
	def forward(self, x):
		"""
		Task 1 - 
		generate your own deep neural network
		"""
		x = self.linear1(x)
		x = self.relu(x)
		x = self.linear2(x)
		x = self.relu(x)
		x = self.linear3(x)
		x = self.relu(x)
		x = self.linear4(x)
		return x

def optimize_model():
	if len(memory) < BATCH_SIZE:
		return
	transition = memory.sample(BATCH_SIZE)
	"""
	Task 4: optimize model
	"""
	state = []
	action = []
	reward = []
	new_state = []
	for t in transition:
		state.append(t[0])
		action.append(t[1])
		reward.append(t[2])
		new_state.append(t[3])

	state = torch.stack(state)
	action = torch.stack(action)
	reward = torch.stack(reward)
	new_state = torch.stack(new_state)


	state_action_values = policy_net(state).gather(1, action)
	state_values = target_net(new_state)

	y_values = []
	for i in range(len(transition)):
		if transition[i][4]==True:
			y_value = reward[i]
		else:
			y_value = reward[i] + 0.999 * torch.max(state_values[i])
		y_values.append(y_value.type(torch.FloatTensor).unsqueeze(0))
	expected_state_action_values = torch.stack(y_values)

	expected_state_action_values = expected_state_action_values.detach()


	loss = F.mse_loss(state_action_values, expected_state_action_values)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()


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
	global epsilon
	if random.uniform(0, 1) < epsilon:
		action = random.choices([0, 1, 2])
		action = torch.from_numpy(np.array(action))
		if epsilon>0.003:
			epsilon-=0.0001
	else:
		with torch.no_grad():
			q_values = policy_net(state)
			action = torch.argmax(q_values)
	return action
	

TARGET_UPDATE = 5
for i in range(num_epochs):
	print(i)
	visited = np.zeros((8, 8))
	steps = 0
	(x, y), ori, sensor, done = reset_map()
	while not done:
		o_i = orientation.index(ori)

		#create your own state
		cur_state = np.array((x, y, sensor[0], sensor[1], sensor[2], o_i, same, visited[x][y]), dtype=np.float32) 
		cur_state = torch.from_numpy(cur_state)
		idx_action = select_action(cur_state).item()

		action = actions[idx_action]
		(new_x, new_y), new_ori, new_sensor, done = action(1)
		steps+=1
		if visited[new_x][new_y]<4:
			visited[new_x][new_y]+=1
		if (new_x, new_y) == (x, y):
			if same<3:
				same+=1
		else:
			same=0
		new_o_i = orientation.index(new_ori)
		visited_val = visited[new_x][new_y]
		action_val = torch.tensor([idx_action], device=device)
		reward_val = reward((x, y), (new_x,new_y),done, steps, visited_val)
		reward_val = torch.tensor(reward_val, device=device)
		new_state = np.array((new_x, new_y, new_sensor[0], new_sensor[1], new_sensor[2], new_o_i, same, visited_val), dtype=np.float32)
		new_state = torch.from_numpy(new_state)
		transition = (cur_state, action_val, reward_val, new_state, done)# generate your own transition form


		memory.push(transition)
		(x, y), ori, sensor = (new_x, new_y), new_ori, new_sensor
		optimize_model()
		
		if steps>600:
			break




"""
Task 5 - save your policy net
"""
def select_action_testing(state, policy_net):
	with torch.no_grad():
		q_values = policy_net(state)
		action = torch.argmax(q_values)
	return action


def test_network():
	"""
	Task 5: test your network
	"""
	set_speed(3)
	test()
	(x, y), ori, sensor, done = reset_map()
	
	policy_net = 1 # load policy net

	policy_net.eval()
	visited = np.zeros((8, 8))
	while not done:
		o_i = orientation.index(ori)
		"""
		fill this section to test your network
		"""
		cur_state = np.array((x, y, sensor[0], sensor[1], sensor[2], o_i, same, visited[x][y]), dtype=np.float32)#create your own state
		cur_state = torch.from_numpy(cur_state)

		idx_action = select_action_testing(cur_state, policy_net).item()
		action = actions[idx_action]
		(new_x, new_y), ori, sensor, done = action()

		if visited[new_x][new_y]<3:
			visited[new_x][new_y]+=1
		if (new_x, new_y) == (x, y):
			if same<3:
				same+=1
		else:
			same=0
		(x, y) = (new_x, new_y)
		if done == True:
			break
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