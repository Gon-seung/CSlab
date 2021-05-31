from simulator import move_forward, turn_left, turn_right, reset_map, set_speed, show_animation, test
# DO NOT MODIFY LINE 1
# You may import any libraries you want. But you may not import simulator_hidden

import numpy as np
import random
import time

#show_animation(True)
#set_speed(3)          # This line is only meaningful if animations are enabled.
 
#####################################
#### Implement steps 1 to 3 here ####
#####################################
grid_size   = (8, 8)             # Size of the map
goal        = (6, 6)             # Coordinates of the goal
orientation = ['N','E','S','W']  # List of orientations



# Hyperparameters: Feel free to change all of these!
actions = [move_forward(), turn_left(), turn_right()]
num_epochs = 500
alpha = 0.8
gamma = 0.9
epsilon = 0
q_table = np.zeros((8 * 17 * 8 * 4, 8 * 17 * 8 * 4))
qmax_table = np.zeros(8 * 17 * 8 * 4)
state = np.zeros((8 * 17 , 8 * 4))

# Define your reward function
def reward(x,y,check_blue):
	if((x % 8 == 6) and (y % 8 == 6)):
		return 1
	elif(check_blue):
		return -1
	return 0

def destination(x, y, ori, sensor, path):
	#sensor[0] is left
	answer = 1
	one = 0
	two = 0
	four = 0
	eight = 0
	if ori == 'S':
		if(sensor[1] == 1): one = 1
		if(sensor[0] == 1): two = 1
		if(sensor[2] == 1): eight = 1
	elif ori == 'E':
		if(sensor[2] == 1): one = 1
		if(sensor[1] == 1): two = 1
		if(sensor[0] == 1): four = 1
	elif ori == 'N':
		if(sensor[2] == 1): two = 1
		if(sensor[1] == 1): four = 1
		if(sensor[0] == 1): eight = 1
	elif ori == 'W':
		if(sensor[0] == 1): one = 1
		if(sensor[2] == 1): four = 1
		if(sensor[1] == 1): eight = 1
	
	if((x,y,x,y + 1) in path): 
		one = 1
	if((x,y,x + 1,y) in path): 
		two = 1
	if((x,y,x,y - 1) in path): 
		four = 1
	if((x,y,x - 1,y) in path): 
		eight = 1
	answer += 1 * one + 2 * two + 4 * four + 8 * eight
	answer *= 8
	answer += x
	return answer

def renew_q(ori_x,ori_y,des_x,des_y,check_blue):
	global q_table
	global qmax_table
	start = int(state[ori_x][ori_y])
	end = int(state[des_x][des_y])
	#print(ori_x % 8,ori_y % 8,des_x,des_y, start, end, check_blue)
	result = q_table[start][end] + alpha * (reward(des_x,des_y,check_blue) + gamma * qmax_table[end] - q_table[start][end])
	q_table[start][end] = result
	#if(0 < result and des_x % 8 != 6):
	#	print(1)
	if(result > qmax_table[start]):
		qmax_table[start] = result
	return result

#"""
for j in range(8 * 17):
	for k in range(8 * 4):
		state[j][k] = j + k * 8 * 17
for i in range(num_epochs):
	(x, y), ori, sensor, done = reset_map()
	path = []
	des_x = (1 + 1 * sensor[1] + 2 * sensor[0] + 4 + 8 * sensor[2]) * 8 + x
	des_y = y
	ori_x = x
	ori_y = y
	check_blue = False
	renew_q(ori_x,ori_y,des_x,des_y,check_blue)
	count = 0
	#print(i)
	while True:
		#time.sleep(1)
		count += 1
		if count > 500:
			break
		#print(i, (x, y), ori, sensor, done)
		
		ori_x = des_x
		ori_y = des_y

		des_x = ori_x % 8
		des_y = ori_y % 8
		if(ori == 'S'):
			des_y += 1
		elif(ori == 'E'):
			des_y += 8
			des_x += 1
		elif(ori == 'N'):
			des_y += -1 + 16
		elif(ori == 'W'):
			des_y += 24
			des_x += -1
		
		choose = []
		check_blue = False
		if(sensor[1] == 1 or (x,y,des_x % 8 , des_y % 8) in path): 
			check_blue = True
		check_pos = renew_q(ori_x,ori_y,des_x,des_y,check_blue)
		if(sensor[1] != 1):
			choose = [(0,des_x,des_y)]

		check_blue = False
		des_x = ori_x
		des_y = (ori_y + 8) % 32
		renew_q(ori_x,ori_y,des_x,des_y,check_blue)
		choose.append((1,des_x,des_y))
		
		des_x = ori_x
		des_y = (ori_y + 24) % 32
		renew_q(ori_x,ori_y,des_x,des_y,check_blue)
		choose.append((2,des_x,des_y))

		order = random.randint(0,len(choose) - 1)
		if choose[order][0] == 0:
			path.append((x,y,choose[order][1] % 8 , choose[order][2] % 8))
			(x, y), ori, sensor, done = move_forward()
		elif choose[order][0] == 1:
			(x, y), ori, sensor, done = turn_left()
		elif choose[order][0] == 2:
			(x, y), ori, sensor, done = turn_right()
		des_x = choose[order][1]
		des_y = choose[order][2]
		#print(des_x,des_y)

		if done:
			break
		if(des_x < 8):
			ori_x = des_x
			ori_y = des_y
			des_x = destination(x, y, ori, sensor, path)
			renew_q(ori_x,ori_y,des_x,des_y,check_blue)
#"""


#####################################

""""
import pygame
set_speed(5)
show_animation(True)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit("Closing...")
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT: print(turn_left())
			if event.key == pygame.K_RIGHT: print(turn_right())
			if event.key == pygame.K_UP: print(move_forward())
			if event.key == pygame.K_t: test()
			if event.key == pygame.K_r: print(reset_map())
			if event.key == pygame.K_q: exit("Closing...")
"""

np.save("q_table", q_table)
show_animation(True)
set_speed(3)
test()
(x, y), ori, sensor, done = reset_map()

###############################
#### Implement step 4 here ####
###############################

"""
count1 = 0
for i in range(8 * 17 * 8 * 5):
	for j in range(8 * 17 * 8 * 5):
		if q_table[i][j] > 0:
			count1 += 1
print(count1)
"""

state = np.zeros((8 * 17 , 8 * 4))
for j in range(8 * 17):
	for k in range(8 * 4):
		state[j][k] = j + k * 8 * 17

while not done:
	all_block = []
	path = []
	des_x = (1 + 1 * sensor[1] + 2 * sensor[0] + 4 + 8 * sensor[2]) * 8 + x
	des_y = y
	ori_x = x
	ori_y = y

	while True:
		#time.sleep(3)

		ori_x = des_x
		ori_y = des_y

		des_x = ori_x % 8
		des_y = ori_y % 8
		if(ori == 'S'):
			des_y += 1
		elif(ori == 'E'):
			des_y += 8
			des_x += 1
		elif(ori == 'N'):
			des_y += -1 + 16
		elif(ori == 'W'):
			des_y += 24
			des_x += -1
		
		#print("--------------------------------------")
		#print(ori_x,ori_y)
		start = int(state[ori_x][ori_y])
		end = int(state[des_x][des_y])
		best = q_table[start][end]
		#print(des_x,des_y,q_table[start][end])
		choose = [0,des_x,des_y]

		des_x = ori_x
		des_y = (ori_y + 8) % 32
		start = int(state[ori_x][ori_y])
		end = int(state[des_x][des_y])
		#print(des_x,des_y,q_table[start][end])
		if q_table[start][end] > best:
			best = q_table[start][end]
			choose = [1,des_x,des_y]
		
		des_x = ori_x
		des_y = (ori_y + 24) % 32
		start = int(state[ori_x][ori_y])
		end = int(state[des_x][des_y])
		#print(des_x,des_y,q_table[start][end])
		if q_table[start][end] > best:
			best = q_table[start][end]
			choose = [2,des_x,des_y]

		if choose[0] == 0:
			path.append((x,y,choose[1] % 8 , choose[2] % 8))
			(x, y), ori, sensor, done = move_forward()
		elif choose[0] == 1:
			(x, y), ori, sensor, done = turn_left()
		elif choose[0] == 2:
			(x, y), ori, sensor, done = turn_right()
		des_x = choose[1]
		des_y = choose[2]

		if done:
			break

		if(des_x < 8):
			ori_x = des_x
			ori_y = des_y
			des_x = destination(x,y, ori, sensor,path)

	done = True
#raise NotImplementedError
###############################

#### If you want to try moving around the map with your keyboard, uncomment the below lines 


