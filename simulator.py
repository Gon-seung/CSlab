from simulator_hidden import *

mySimulator = Simulator()
myRobot = mySimulator.robot

def get_sensors():
	return mySimulator.color_sensor, mySimulator.ir_sensor

def move_forward(n=1):
	for i in range(n):
		myRobot.forward()
		mySimulator.update()

def move_backward(n=1):
	for i in range(n):
		myRobot.backward()
		mySimulator.update()

def turn_left(n=1):
	for i in range(n):
		myRobot.left()
		mySimulator.update()

def turn_right(n=1):
	for i in range(n):
		myRobot.right()
		mySimulator.update()

def submit(lake, building):
	success = True
	x, y = myRobot.get_pose()
	if not (border < x < border+block and border < y < border+block):
		print("You must return to the starting block!")
		success = False
	if set(lake) != set(mySimulator.lake_blocks):
		print("Incorrect lake position!")
		success = False
	if set(building) != set(mySimulator.building_blocks):
		print("Incorrect building position!")
		success = False
	if success:
		mySimulator.terminate("Success! Time: {:.2f}".format(time.time() - mySimulator.start_time))

	time.sleep(1)
	return success

def set_map(map_dim_new, lake_blocks_new, building_blocks_new):
	mySimulator.reset(map_dim_new, lake_blocks_new, building_blocks_new)
	time.sleep(1)