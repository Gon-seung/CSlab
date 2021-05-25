from simulator import move_forward, turn_left, turn_right, reset_map, set_speed, show_animation, test, set_map
import numpy as np
import time
q_table = np.load("q_table.npy")

orientation = ['N','E','S','W']
actions = [move_forward, turn_left, turn_right]

thin_ice_blocks = [(1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6)]

set_speed(3)
test()
#(x, y), ori, sensor, done = set_map(thin_ice_blocks)
(x, y), ori, sensor, done = reset_map()
##############################################
#### Copy and paste your step 4 code here ####
##############################################

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

def check_sensor(ori, all_block, x , y, sensor):
	dir_4 = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]
	if(ori == 'S'):
		if((dir_4[1] in all_block or sensor[0]) and (dir_4[0] in all_block or sensor[1]) and (dir_4[3] in all_block or sensor[2])):
			return True
	elif(ori == 'E'):
		if((dir_4[2] in all_block or sensor[0]) and (dir_4[1] in all_block or sensor[1]) and (dir_4[0] in all_block or sensor[2])):
			return True
	elif(ori == 'N'):
		if((dir_4[3] in all_block or sensor[0]) and (dir_4[2] in all_block or sensor[1]) and (dir_4[1] in all_block or sensor[2])):
			return True
	elif(ori == 'W'):
		if((dir_4[0] in all_block or sensor[0]) and (dir_4[3] in all_block or sensor[1]) and (dir_4[2] in all_block or sensor[2])):
			return True
	return False


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