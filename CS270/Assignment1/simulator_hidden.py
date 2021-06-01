import pygame
import os
import math
import time
from random import randint, uniform
from datetime import datetime

## Time
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

clock = pygame.time.Clock()

## Colors1
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
building = 30 * scale
padding = 5 * scale
robot_size = (int(block*0.4), int(block*0.6))
ir_range = block*5
ir_step = border

## Initial robot position
init_position = (block/2 + border, block/2 + border)
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
		self.move_step = uniform(1.0, 1.2) * scale
		a = randint(70, 90) * 2
		self.rotate_step = math.pi / a
		self.draw_robot()
		self.lll = []

	def get_pose(self):
		return self.cx, self.cy

	def reset(self):
		self.w, self.h = self.init[0]
		self.cx, self.cy = self.init[1]
		self.a = self.init[2]
		self.draw_robot()

	def draw_robot(self):
		self.set_colorkey(white)
		self.fill(red)
		# Center
		pygame.draw.rect(self, navy, pygame.Rect(self.w/2 - 1*scale, self.h/2 - 1*scale, 3*scale-1, 3*scale-1))
		# Color sensors
		pygame.draw.rect(self, yellow, pygame.Rect(scale, self.h-2*scale, 2*scale, 2*scale))
		pygame.draw.rect(self, yellow, pygame.Rect(self.w-3*scale, self.h-2*scale, 2*scale, 2*scale))
		# Design
		pygame.draw.rect(self, white, pygame.Rect(self.w/2 - 3*scale, self.h - 8*scale, 7*scale-1, 8*scale))

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
		if 0 <= new_x < self.map_size[0]:
			self.cx = new_x
		if 0 <= new_y < self.map_size[1]:
			self.cy = new_y
		self.update()

	def backward(self):
		new_x = self.cx - self.move_step * math.sin(self.a)
		new_y = self.cy - self.move_step * math.cos(self.a)
		if 0 <= new_x < self.map_size[0]:
			self.cx = new_x
		if 0 <= new_y < self.map_size[1]:
			self.cy = new_y
		self.update()

	def get_box(self):
		return self.parent.get_at((int(self.cx),int(self.cy)))[:3]

	def get_sensors(self):
		lc = rc = None
		ir = -1
		sin = math.sin(self.a)
		cos = math.cos(self.a)
		lx = self.cx + (self.w/2-scale) * cos + (self.h/2) * sin
		ly = self.cy - (self.w/2-scale) * sin + (self.h/2) * cos
		if 0 <= lx < self.map_size[0] and 0 <= ly < self.map_size[1]:
			lc = self.parent.get_at((int(lx),int(ly)))[:3]
		rx = self.cx - (self.w/2-scale) * cos + self.h/2 * sin
		ry = self.cy + (self.w/2-scale) * sin + self.h/2 * cos
		if 0 <= rx < self.map_size[0] and 0 <= ry < self.map_size[1]:
			rc = self.parent.get_at((int(rx),int(ry)))[:3]
		for i, l in enumerate(range(int(self.h/2), int(ir_range), int(ir_step))):
			mx = self.cx + l * sin
			my = self.cy + l * cos
			if 0 <= mx < self.map_size[0] and 0 <= my < self.map_size[1]:
				if self.parent.get_at((int(mx),int(my)))[:3] == brown:
					ir = i
					break
		self.lll = [(lx,ly), (rx,ry)]
		return (lc, rc), ir

	def get_corners(self):
		c = []
		sin = math.sin(self.a)
		cos = math.cos(self.a)
		for w in [-self.w/2, self.w/2]:
			for h in [-self.h/2, self.h/2]:
				x = self.cx + w * cos + h * sin
				y = self.cy - w * sin + h * cos
				if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
					c.append(self.parent.get_at((int(x),int(y)))[:3])
		
		return c


class Simulator():
	def __init__(self):
		# Set map sizes
		self.h_line = self.v_line = self.map_dim = self.map_size = self.screen = None
		self.set_map_size((10, 5))
		# Set blocks
		self.lake_blocks = []
		self.building_blocks = []
		self.set_random_blocks()
		# Set sensor variables
		self.color_sensor = self.ir_sensor = self.corners = self.current_col = None
		# Create robot
		self.robot = myRobot(self.screen, init_position, init_angle, robot_size, self.map_size)
		self.update()

		self.log()
		self.start_time = time.time()

	def set_map_size(self, map_dim_new):
		self.map_dim = map_dim_new
		self.h_line = self.map_dim[0]*(block+line) - line
		self.v_line = self.map_dim[1]*(block+line) - line
		self.map_size = (self.h_line + 2*border, self.v_line + 2*border)
		self.screen = pygame.display.set_mode(self.map_size)

	def draw_map(self):
		self.screen.fill(black)
		pygame.draw.rect(self.screen, white, pygame.Rect(border, border, self.map_size[0]-2*border, self.map_size[1]-2*border))

		for x in range(1, self.map_dim[0]):
			pygame.draw.rect(self.screen, gray, pygame.Rect(border + x*block + (x-1)*line, border, line, self.v_line))
		for y in range(1, self.map_dim[1]):
			pygame.draw.rect(self.screen, gray, pygame.Rect(border, border + y*block + (y-1)*line, self.h_line, line))

		for i,j in self.lake_blocks:
			pygame.draw.rect(self.screen, blue, pygame.Rect(border + i*(block+line), border + j*(block+line), block, block))
		for i,j in self.building_blocks:
			pygame.draw.rect(self.screen, brown, pygame.Rect(border + i*(block+line) + padding, border + j*(block+line) + padding, building, building))

	def set_random_blocks(self, num_lake = 5, num_building = 5):
		while len(self.lake_blocks) < num_lake:
			x = randint(0, self.map_dim[0]-1)
			y = randint(0, self.map_dim[1]-1)
			if (x,y) != (0,0) and (x,y) not in self.lake_blocks:
				self.lake_blocks.append((x,y))
		while len(self.building_blocks) < num_building:
			x = randint(0, self.map_dim[0]-1)
			y = randint(0, self.map_dim[1]-1)
			if (x,y) != (0,0) and (x,y) not in self.building_blocks and (x,y) not in self.lake_blocks:
				self.building_blocks.append((x,y))

	def set_blocks(self, lake_blocks_new, building_blocks_new):
		self.lake_blocks = lake_blocks_new
		self.building_blocks = building_blocks_new

	def update(self):
		self.draw_map()
		self.color_sensor, self.ir_sensor = self.robot.get_sensors()
		self.corners = self.robot.get_corners()
		self.current_col = self.robot.get_box()
		self.robot.update()
		pygame.display.flip()
		self.check_finished()
		clock.tick(60)

	def check_finished(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit("Closing...")
		if self.current_col == black:
			self.terminate("Wasted!")
		if brown in self.corners:
			self.terminate("Collision!")

	def terminate(self, message):
		text = font.render(message, True, red, black) 
		textRect = text.get_rect()
		textRect.center = (self.map_size[0] // 2, self.map_size[1] // 2)
		self.screen.blit(text, textRect) 
		pygame.display.flip()
		time.sleep(2)
		exit(message)

	def reset(self, map_dim_new, lake_blocks_new, building_blocks_new):
		self.set_map_size(map_dim_new)
		self.set_blocks(lake_blocks_new, building_blocks_new)
		self.robot.reset()
		self.update()
		self.start_time = time.time()


	def log(self):
		# read textfile into string
		with open('student.py', 'r') as txtfile:
			mytextstring = txtfile.read()
			date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

			# save the file
			with open('logs/'+date+".txt", 'w') as file:
				file.write(mytextstring)
