from simulator import get_sensors, move_forward, move_backward, turn_left, turn_right, submit, set_map
# DO NOT MODIFY LINE 1
# You may import any libraries you want. But you may not import "simulator_hidden" or any other functions from "simulator"
import time
# Colors
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
blue = (0,180,255)

##############################
#### Write your code here ####
##############################

# How to use the functions:
# (left_color, right_color), ir_sensor = get_sensors()
# move_forward(how_much)
# submit(lake_list=[(x1,y1),(x2,y2)...], building_list=[(x1,y1),(x2,y2)...])
# set_map(new_map_dim=(width, heigth), new_lake_list=[(x1,y1),(x2,y2)...], new_building_list=[(x1,y1),(x2,y2)...])




##############################


#### If you want to try moving around the map with your keyboard, uncomment the below lines 
import pygame
lake = []
wall = []
trip = [(0,0)]
dire = 0
# 0 down 1 right 2 up 3 left
pos_x = 0
pos_y = 0
width = -2
height = -2

def Color():
	infor = get_sensors()
	left = infor[0][0]
	right = infor[0][1]
	return left, right

def Move_block():
	global pos_x
	global pos_y
	answer = False
	for i in range(60):
			move_forward()
			left, right = Color()
			
			if((left == black or right == black) and ((dire == 0 and pos_y != 0) or (dire == 1 and pos_x != 0) or (dire == 2 and pos_y == 1) or (dire == 3 and pos_x == 1))):
				move_backward(5)
				answer = True
				break
				
			if((left == gray or left == black) and not (right == gray or right == black)):
				move_forward()
				left,right = Color()
				if(right == gray or right == black):
					turn_left()
				else:
					turn_right()
				move_backward()
			if(not (left == gray or left == black) and (right == gray or right == black)):
				move_forward()
				left,right = Color()
				if(left == gray or left == black):
					turn_right()
				else:
					turn_left()
				move_backward()
			if(i > 20 and (left == gray or right == gray)):
				move_backward()
				break
	if (dire == 0):
		pos_y += 1
	elif(dire == 2):
		pos_y -= 1
	elif(dire == 1):
		pos_x += 1
	elif(dire == 3):
		pos_x -= 1
	return answer

def Wall_check():
	global wall
	infor = get_sensors()
	if(0 <= infor[1] <= 4):
		if (dire == 0):
			if (not (pos_x, pos_y + 1) in wall):
				wall.append((pos_x,pos_y + 1))
		elif(dire == 2):
			if (not (pos_x, pos_y - 1) in wall):
				wall.append((pos_x,pos_y - 1))
		elif(dire == 1):
			if (not (pos_x + 1, pos_y) in wall):
				wall.append((pos_x + 1,pos_y))
		elif(dire == 3):
			if (not (pos_x - 1, pos_y) in wall):
				wall.append((pos_x - 1,pos_y))
		return True
	return False

def Real_dir(turn):
	#"""
	left,right = Color()
	if(turn == "left"):
		turn_left(60)
	else:
		turn_right(60)
	move_backward(5)
	while not ((right == gray or right == black) and (left == gray or left == black)):
		if((left == white or left == blue) and (right == white or right == blue)):
			move_forward()
		if((left == gray or left == black) or (right == gray or right == black)):
			if(turn == "left"):
				turn_left()
			else:
				turn_right()
			move_backward()
		left,right = Color()
	move_backward(3)
	
	if(turn == "left"):
		turn_left(10)
	else:
		turn_right(10)

	left,right = Color()
	while not ((right == gray or right == black) and (left == gray or left == black)):
		if((left == white or left == blue) and (right == white or right == blue)):
			move_forward()
		
		if(left == gray or left == black):
			turn_left()
			move_backward()
		elif(right == gray or right == black):
			turn_right()
			move_backward()
		left,right = Color()
		
	move_backward(5)
	"""
	while(True):
		left,right = Color()
		if((left == gray or left == black) and (right != gray and right != black)):
			turn_left()
			move_backward()
		elif((right == gray or right == black) and (left != gray and left != black)):
			turn_right()
			move_backward()
		elif((right == gray or right == black) and (left == gray or left == black)):
			break
		move_forward()
	#move_backward(2)
	"""


def Find_dir():
	global dire
	global trip
	pos_dir = [(pos_x,pos_y + 1),(pos_x + 1,pos_y),(pos_x,pos_y - 1),(pos_x - 1,pos_y)]
	ori_dir = dire
	dire = (dire + 3) % 4
	x,y = pos_dir[dire]
	count = 0
	while ((x,y) in trip or ((x,y) in wall) or x == -1 or y == -1 or x == width or y == height):
		dire = (dire + 1) % 4
		x,y = pos_dir[dire]
		count += 1
		if(count >= 3):
			if(len(trip) > 1):
				trip.pop()
				count = -999
	
	if(count < 0):
		trip = [(pos_x,pos_y)] + trip
	if((dire - ori_dir + 4) % 4 == 1):
		move_backward(5)
		Real_dir("left")
	elif((dire - ori_dir + 4) % 4 == 2):
		move_backward(5)
		Real_dir("left")
		move_backward(3)
		Real_dir("left")
	elif((dire - ori_dir + 4) % 4 == 3):
		move_backward(5)
		Real_dir("right")

def Check_in(x,y):
	if (not (x,y) in wall) and 0 <= x < width and 0 <= y < height:
		return True
	return False

def Go_home():
	root = [[(pos_x,pos_y)]]
	travel = [(pos_x, pos_y)]
	find = False
	while True:
		new_root = []
		for i in range(len(root)):
			new = root[i]
			new_x, new_y = new[-1]
			if (Check_in(new_x,new_y - 1) and not (new_x,new_y - 1) in travel):
				new_root.append(new + [(new_x, new_y - 1)])
				travel += [(new_x,new_y - 1)]
				if (new_x == 0 and new_y - 1 == 0): 
					find = True 
					break
			if (Check_in(new_x - 1,new_y) and not (new_x - 1,new_y) in travel):
				new_root.append(new + [(new_x - 1, new_y)])
				travel += [(new_x - 1,new_y)]
				if (new_x - 1 == 0 and new_y == 0): 
					find = True
					break
			if (Check_in(new_x,new_y + 1) and not (new_x,new_y + 1) in travel):
				new_root.append(new + [(new_x, new_y + 1)])
				travel += [(new_x,new_y + 1)]
				if (new_x == 0 and new_y + 1 == 0): 
					find = True
					break
			if (Check_in(new_x + 1,new_y) and not (new_x + 1,new_y) in travel):
				new_root.append(new + [(new_x + 1, new_y)])
				travel += [(new_x,new_y)]
				if (new_x + 1 == 0 and new_y == 0): 
					find = True
					break
		root = new_root
		if find: break
	return root[-1]


# set_map((10,5), [(8,0), (4,9), (2,0), (3,3), (4,1)], [(7,2), (0,1), (2,3)])
while True:
	#"""
	while True:
		infor = get_sensors()
		dis = infor[1]
		
		Wall_check()
		Find_dir()
		while Wall_check():
			Find_dir()
		#time.sleep(0.5)

		if(Move_block()):
			if (dire == 0 and height < pos_y + 1):
				height = pos_y + 1
			elif(dire == 1 and width < pos_x + 1):
				width = pos_x + 1
			trip = trip + [(pos_x,pos_y)]
			left,right = Color()
			if((left == blue or right == blue) and not (pos_x, pos_y) in lake):
				lake.append((pos_x,pos_y))
			continue
		
		
		trip = trip + [(pos_x,pos_y)]
		left,right = Color()

		
		if((left == blue and right == blue) and not (pos_x, pos_y) in lake):
			lake.append((pos_x,pos_y))
			
		#print(len(trip) , len(lake), len(wall) , width , height)
		if(len(trip) + len(wall) == width * height and width > 0 and height > 0):
			#print(lake)
			#print(wall)
			break


	root = Go_home()
	#print(root)
	for i in range(len(root)):
		if i == 0: continue
		trip.remove(root[i])
	while True:
		Find_dir()
		Move_block()
		if(pos_x == 0 and pos_y == 0):
			submit(lake,wall)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit("Closing...")

	"""
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP]: move_forward()
	if pressed[pygame.K_DOWN]: move_backward()
	if pressed[pygame.K_LEFT]: turn_left()
	if pressed[pygame.K_RIGHT]: turn_right()
	if pressed[pygame.K_n]: set_map((10,5), [(8,0), (4,9), (2,0), (3,3), (4,1)], [(7,2), (0,1), (2,3)])
	if pressed[pygame.K_c]: print(get_sensors())
	if pressed[pygame.K_b]: submit({},{})
	"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit("Closing...")