from simulator_hidden import *

mySimulator = Simulator()
myRobot = mySimulator.robot

def move_forward():
	if mySimulator.finished:
		return mySimulator.state
	myRobot.forward()
	mySimulator.update()
	return mySimulator.state

def turn_left():
	if mySimulator.finished:
		return mySimulator.state
	myRobot.left()
	mySimulator.update()
	return mySimulator.state

def turn_right():
	if mySimulator.finished:
		return mySimulator.state
	myRobot.right()
	mySimulator.update()
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