import pygame
import sys
import threading
from time import sleep

axis_name = ["LX", "LY", "RX", "RY"]
trig_name = ["L_TRIG", "R_TRIG"]
imuData_name = ["AX", "AY", "AZ", "GX", "GY", "GZ"]
buttons_name = ["TRIANGLE", "CROSS", "SQUARE", "CIRCLE", "L1", "L2", "R1", "R2", "LB", "RB", "SHARE", "OPTION", "PS", "TOUCHPAD"]
hatButtons_name = ["UP", "DOWN", "LEFT", "RIGHT"]

axis_index = [0, 1, 2, 5]
trig_index = [3, 4]
imuData_index = [7, 6, 8, 11, 9, 10]
buttons_index = [3, 1, 0, 2, 4, 6, 5, 7, 10, 11, 8, 9, 12, 13]

axis_val = [0]*len(axis_index)
trig_val = [-1.0, -1.0]
imuData_val =[0.0]*len(imuData_index) 
buttons_val = [0]*len(buttons_index)
hatButtons_val = [0]*len(hatButtons_name)

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
	print("Unable to connect. Please check Connection")
	sys.exit(0)

controller_name = 'Sony Computer Entertainment Wireless Controller'
ds4 = pygame.joystick.Joystick(0)
ds4.init()
if not(ds4.get_name() == controller_name):
	print("Wrong Controller Connected")
	exit()
print("Sony DualShock 4 Connected")
sleep(.8) 

def grab_data(val_list, index_list, dataHandler):
	for i in range(len(index_list)):
				val_list[i] = dataHandler( index_list[i] )
 
def calc_hat():
	tup = ds4.get_hat(0)
	hatButtons_val[0] = tup[1]
	hatButtons_val[1] = tup[1] * -1
	hatButtons_val[2] = tup[0] * -1
	hatButtons_val[3] = tup[0]
	for i in range(4):
		if hatButtons_val[i] < 0:
			hatButtons_val[i] = 0

def print_data(val_list):
	for val in val_list:
		if isinstance(val, float):
			print("%.3f   " % val, end='')
		elif isinstance(val, int):
			print("%d  " % val, end='')

def read_ds4():
	while(True):
		event = len(pygame.event.get())
		if  event > 1:
			grab_data(axis_val, axis_index, ds4.get_axis)
			grab_data(imuData_val, imuData_index, ds4.get_axis)
			grab_data(trig_val, trig_index, ds4.get_axis)
			grab_data(buttons_val, buttons_index, ds4.get_button)
			calc_hat()

grab_data(trig_val, trig_index, ds4.get_axis)
if trig_val[0] != -1.0 or trig_val[1] != -1.0:
	print("Press Left and Right Triggers once to start.")
	while(not(trig_val[0] == -1.0 and trig_val[1] == -1.0)):
		event = len(pygame.event.get())
		if  event > 1:
			grab_data(trig_val, trig_index, ds4.get_axis)

def print_all():
	while True:
		print_data(axis_val)
		print_data(trig_val)
		print_data(hatButtons_val)
		print_data(buttons_val)
		print_data(imuData_val)
		print()

Thread1 = threading.Thread(target=read_ds4)
Thread2 = threading.Thread(target=print_all)

Thread1.start()
Thread2.start()
