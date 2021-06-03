from simulator_hidden import *

mySimulator = Simulator()
myRobot_1 = mySimulator.robot_1
myRobot_2 = mySimulator.robot_2

def move_forward(robot_idx):
	if mySimulator.finished1 and mySimulator.finished2:
		return mySimulator.state
	if robot_idx == 1:
		myRobot_1.forward()
	else:
		myRobot_2.forward()
	mySimulator.update()
	return mySimulator.state

def turn_left(robot_idx):
	if mySimulator.finished1 and mySimulator.finished2:
		return mySimulator.state
	if robot_idx == 1:
		myRobot_1.left()
	else:
		myRobot_2.left()
	mySimulator.update()
	return mySimulator.state

def turn_right(robot_idx):
	if mySimulator.finished1 and mySimulator.finished2:
		return mySimulator.state
	if robot_idx == 1:
		myRobot_1.right()
	else:
		myRobot_2.right()
	mySimulator.update()
	return mySimulator.state

def stay(robot_idx):
	return mySimulator.state

def reset_map():
	return mySimulator.reset()

def set_speed(spd):
	mySimulator.clock_rate = spd

def show_animation(show):
	mySimulator.show_animation = show

def test():
	mySimulator.training = False
	mySimulator.reset()
	time.sleep(2)

def set_map(thin_ice_blocks):
	return mySimulator.set_map(thin_ice_blocks)