import pygame
import os
import math
import time
import numpy as np
from random import randint, uniform
from datetime import datetime

## Time
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

clock = pygame.time.Clock()

## Colors
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
blue = (0,180,255)
red = (255,0,0)
brown = (120,70,0)
green = (90,170,50)
navy = (10,30,120)
yellow = (255,230,0)
pink = (222, 11, 211)

## Map size
scale = 2
border = 10 * scale
line = 5 * scale
block = 40 * scale
padding = 5 * scale
robot_size = (int(block*0.4), int(block*0.6))
ir_range = block + line

## Initial robot position
init_position = (block/2 + border + block + line, block/2 + border + block + line)
init_angle = 0

class myRobot(pygame.Surface):
	def __init__(self, parent, pos, a, size, map_size):
		pygame.Surface.__init__(self, size)
		self.init = [size, pos, a]
		self.parent = parent
		self.cx, self.cy = pos
		self.a = a
		self.w, self.h = size
		self.map_size = map_size
		self.move_step =  block + line
		self.rotate_step = math.pi / 2
		self.draw_robot()

	def get_pose(self):
		return self.cx, self.cy, self.a

	def reset(self, map_size):
		self.w, self.h = self.init[0]
		self.cx, self.cy = self.init[1]
		self.a = self.init[2]
		self.map_size = map_size
		self.draw_robot()

	def draw_robot(self):
		self.set_colorkey(white)
		self.fill(red)
		# Center
		pygame.draw.rect(self, navy, pygame.Rect(self.w/2 - 1*scale, self.h/2 - 1*scale, 3*scale-1, 3*scale-1))
		# Color sensors
		pygame.draw.rect(self, yellow, pygame.Rect(scale, self.h-2*scale, 2*scale, 2*scale))
		pygame.draw.rect(self, yellow, pygame.Rect(self.w-3*scale, self.h-2*scale, 2*scale, 2*scale))

	def update(self):
		rotated_surf = pygame.transform.rotate(self, math.degrees(self.a))
		rotated_rect = rotated_surf.get_rect()
		rotated_rect.center = (self.cx, self.cy)
		self.parent.blit(rotated_surf, rotated_rect)

	def left(self):
		self.a += self.rotate_step
		if self.a >= 2*math.pi:
			self.a -= 2*math.pi
		self.update()

	def right(self):
		self.a -= self.rotate_step
		if self.a < 0:
			self.a += 2*math.pi
		self.update()

	def forward(self):
		new_x = self.cx + self.move_step * math.sin(self.a)
		new_y = self.cy + self.move_step * math.cos(self.a)
		self.cx = min(max(0, new_x), self.map_size[0]-1)
		self.cy = min(max(0, new_y), self.map_size[1]-1)
		self.update()

	def backward(self):
		new_x = self.cx - self.move_step * math.sin(self.a)
		new_y = self.cy - self.move_step * math.cos(self.a)
		self.cx = min(max(0, new_x), self.map_size[0]-1)
		self.cy = min(max(0, new_y), self.map_size[1]-1)
		self.update()

	def get_box(self):
		return self.parent.get_at((int(self.cx),int(self.cy)))[:3]

	def get_ir(self):
		sin = math.sin(self.a)
		cos = math.cos(self.a)
		mx = self.cx + ir_range * sin
		my = self.cy + ir_range * cos
		if 0 <= mx < self.map_size[0] and 0 <= my < self.map_size[1]:
			if self.parent.get_at((int(mx),int(my)))[:3] == blue:
				return 1
		return 0

	def get_ir_4(self):
		ir_4d = []
		ang = self.a
		for i in range(4):
			sin = math.sin(ang)
			cos = math.cos(ang)
			mx = self.cx + ir_range * sin
			my = self.cy + ir_range * cos
			if 0 <= mx < self.map_size[0] and 0 <= my < self.map_size[1]:
				if self.parent.get_at((int(mx),int(my)))[:3] == blue:
					ir_4d.append(1)
				else:
					ir_4d.append(0)
			else:
				ir_4d.append(0)
			ang -= self.rotate_step

		return ir_4d

	def get_ir_3(self):
		ir_4d = []
		ang = self.a
		for i in [ang+self.rotate_step, ang, ang-self.rotate_step]:
			sin = math.sin(i)
			cos = math.cos(i)
			mx = self.cx + ir_range * sin
			my = self.cy + ir_range * cos
			if 0 <= mx < self.map_size[0] and 0 <= my < self.map_size[1]:
				if self.parent.get_at((int(mx),int(my)))[:3] == blue:
					ir_4d.append(1)
				else:
					ir_4d.append(0)
			else:
				ir_4d.append(0)

		return ir_4d


class Simulator():
	def __init__(self):
		# Set map sizes
		self.h_line = self.v_line = self.map_dim = self.map_size = self.screen = self.goal = self.state = None
		self.training = True
		self.num_actions = 0
		self.clock_rate = 5
		self.finished = False
		self.set_map_size((8, 8))
		self.show_animation = False
		# Set blocks
		self.lake_blocks = []
		self.lake_border = []
		for i in range(self.map_dim[0]):
			self.lake_border.append((i,0))
			self.lake_border.append((i,self.map_dim[1]-1))
		for i in range(self.map_dim[1]):
			self.lake_border.append((0,i))
			self.lake_border.append((self.map_dim[0]-1,i))
		self.set_random_blocks()
		# Set sensor variables
		self.ir_sensor = self.current_col = None
		# Create robot
		self.robot = myRobot(self.screen, init_position, init_angle, robot_size, self.map_size)
		self.update()
		pygame.display.flip()

		self.log()
		self.start_time = time.time()

	def set_map_size(self, map_dim_new):
		self.map_dim = map_dim_new
		self.h_line = self.map_dim[0]*(block+line) - line
		self.v_line = self.map_dim[1]*(block+line) - line
		self.map_size = (self.h_line + 2*border, self.v_line + 2*border)
		self.screen = pygame.display.set_mode(self.map_size)
		self.goal = (self.map_dim[0]-2, self.map_dim[1]-2)

	def draw_map(self):
		self.screen.fill(black)
		pygame.draw.rect(self.screen, white, pygame.Rect(border, border, self.map_size[0]-2*border, self.map_size[1]-2*border))

		# Starting block
		pygame.draw.rect(self.screen, green, pygame.Rect(border + block+line, border + block+line, block, block))

		for x in range(1, self.map_dim[0]):
			pygame.draw.rect(self.screen, gray, pygame.Rect(border + x*block + (x-1)*line, border, line, self.v_line))
		for y in range(1, self.map_dim[1]):
			pygame.draw.rect(self.screen, gray, pygame.Rect(border, border + y*block + (y-1)*line, self.h_line, line))

		for i,j in self.lake_blocks:
			pygame.draw.rect(self.screen, blue, pygame.Rect(border + i*(block+line), border + j*(block+line), block, block))

		for i,j in self.lake_border:
			pygame.draw.rect(self.screen, blue, pygame.Rect(border + i*(block+line), border + j*(block+line), block, block))

		# Goal block1
		pygame.draw.rect(self.screen, yellow, pygame.Rect(border + self.goal[0]*(block+line), border + self.goal[1]*(block+line), block, block))

	def set_random_blocks(self, num_lake = 8):
		done = False
		while not done:
			self.lake_blocks = []
			while len(self.lake_blocks) < num_lake:
				x = randint(1, self.map_dim[0]-2)
				y = randint(1, self.map_dim[1]-2)
				if (x,y) != (1,1) and (x,y) not in self.lake_blocks and (x,y) != self.goal:
					self.lake_blocks.append((x,y))

			white = [(i,j) for i in range(1, self.map_dim[0]-1) for j in range(1, self.map_dim[1]-1)]
			for lake in self.lake_blocks:
				white.remove(lake)

			size = len(white)
			adj = np.zeros((size,size))
			for i in range(size):
				for j in range(i+1, size):
					x1, y1 = white[i]
					x2, y2 = white[j]
					if math.fabs(x1 - x2) + math.fabs(y1 - y2) == 1:
						adj[i][j] = 1
						adj[j][i] = 1

			visited = [False] * size
			queue = []

			queue.append((1,1))
			visited[0] = True

			while queue:
				block = queue.pop(0)
				if block == self.goal:
					done = True
					break
				idx = white.index(block)
				for i in np.where(adj[idx, :] == 1)[0]:
					if visited[i] == False:
						queue.append(white[i])
						visited[i] = True

	def set_blocks(self, lake_blocks_new):
		self.lake_blocks = lake_blocks_new

	def update(self):
		self.num_actions += 1
		self.draw_map()
		self.ir_sensor = self.robot.get_ir_3()
		self.current_col = self.robot.get_box()
		self.robot.update()
		if not self.training or self.show_animation:
			pygame.display.flip()

		x,y,a = self.robot.get_pose()
		coord = int((x-border)/(block+line)), int((y-border)/(block+line))
		orien = ['S','E','N','W'][int(a/(math.pi/2))]
		done = self.check_finished()
		self.state = (coord, orien, self.ir_sensor, done)
		if not self.training or self.show_animation:
			clock.tick(self.clock_rate)

	def check_finished(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit("Closing...")
		if self.training:
			if self.current_col == black or self.current_col == blue or self.current_col == yellow:
				self.finished = True
		else:
			if self.current_col == black or self.current_col == blue:
				self.terminate("Wasted!")
			elif self.current_col == yellow:
				# self.terminate("Success! ({:.2f})".format(time.time()-self.start_time))
				self.terminate("Success! ({} moves)".format(self.num_actions))
		return self.finished

	def terminate(self, message):
		text = font.render(message, True, red, black) 
		textRect = text.get_rect()
		textRect.center = (self.map_size[0] // 2, self.map_size[1] // 2)
		self.screen.blit(text, textRect) 
		pygame.display.flip()
		time.sleep(2)
		exit(message)

	def reset(self):
		self.finished = False
		self.set_random_blocks()
		self.robot.reset(self.map_size)
		self.update()
		self.start_time = time.time()
		self.num_actions = 0
		return self.state

	def set_map(self, lake_blocks_new):
		self.finished = False
		self.set_blocks(lake_blocks_new)
		self.robot.reset(self.map_size)
		self.update()
		self.start_time = time.time()
		self.num_actions = 0
		return self.state

	def log(self):
		# read textfile into string
		with open('student.py', 'r') as txtfile:
			mytextstring = txtfile.read()
			date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

			# save the file
			#with open('logs/'+date+".txt", 'w') as file:
			#	file.write(mytextstring)
