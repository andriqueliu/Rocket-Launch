'''
University of Washington Department of Electrical Engineering
ESS 472 Wireless Rocket Launch Research Project

Research Advisor: Professor John Sahr
Authors: Andrique Liu and Emraj Sidhu

Launch.py enables the user to safely launch rockets using a series of redundant checks.

Note that this program 

Note that in the field, this code is designed to be operated from a safe distance. In
our case, this is accomplished by using EnGenius radio modules, allowing the user to
remotely SSH into the BeagleBone Black and operate this program.
'''

# Import libraries
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time

# Print welcome and safety message
def print_welcome():
	print("Welcome to the Launch Program.")
	print("Please make sure you have read the manual before operating this program.")
	print("If you haven\'t, please check it out and come back when you\'ve read it.")
	print("Remember, SAFETY FIRST!!!")

# Initialize GPIO pins
def init_GPIO():
	GPIO.setup("P8_8", GPIO.OUT)
	GPIO.setup("P8_10", GPIO.OUT)

# Initialize ADC pins
def init_ADC():
	ADC.setup()

# --------------------------------------------------------- #
# Testing code: drives LEDs

# Code written for test purposes: drive both GPIOs high
def all_high():
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_10", GPIO.HIGH)

# Code written for test purposes: drive both GPIOs low
def all_low():
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_10", GPIO.LOW)

# End LED testing codes
# --------------------------------------------------------- #

# Disables all FETs
def disable_all_FETs():
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_10", GPIO.HIGH)

# Enable FET A
def enable_FET_A():
	GPIO.output("P8_8", GPIO.LOW)

# Enable FET B
def enable_FET_B():
	GPIO.output("P8_10", GPIO.LOW)

# Read the ADC value and print out the read value.
# Prints out whether the system power is active or not.
# If active, return 1. Else, return 0
def read_ADC():
	value = ADC.read("AIN1")
	value = ADC.read("AIN1")
	value = value * 1.8
	print "Analog value:", value, "V"
	
	if value > 1.70: # This will need calibrating...
		print('Power is ACTIVE')
		return 1
	else:
		print('Power is NOT ACTIVE')
		return 0

# countdown controls a 5 second countdown to launch.
def countdown():
	print "5..."
	time.sleep(1)
	print "4..."
	time.sleep(1)
	print "3..."
	time.sleep(1)
	print "2..."
	time.sleep(1)
	print "1..."
	time.sleep(1)
	print "Launching!"

# launch_sequence begins the launch sequence.
# This function prompts the user whether they would like to enable FET A,
# then B, and if the user wishes to enable both, the user will be prompted
# with an additional redundant prompt.
# If launch is approved, FETs will be enabled briefly.
# Else, function exits
def launch_sequence():
	print "Initiating launch sequence."
	response_A = raw_input("Arm FET A? (Yes or No) ")
	response_B = raw_input("Arm FET B? (Yes or No) ")
	
	if (response_A == "Yes") and (response_B == "Yes"):
		response_final = raw_input("Final confirmation: Launch? ")
		if (response_final == "Yes"):
			# print "Launching!"
			countdown()
			
			enable_FET_A()
			enable_FET_B()
			time.sleep(2) # This will need to be calibrated depending on board tolerance!!!
		else:
			print "Abort"
	else:
		print "Abort"

# Shutdown procedure: ensure FETs are disabled, clean up GPIOs.
def shutdown():
	all_low()
	GPIO.cleanup()

# Program Execution
try:
	print_welcome()
	init_GPIO()
	init_ADC()
	disable_all_FETs() # CRITICAL
	
	while True:
		# Keep checking for power value until the power is ACTIVE.
		while not read_ADC():
			time.sleep(1)
		
		# Initiate launch sequence
		launch_sequence()
		
		break
		
except KeyboardInterrupt:
	shutdown()
	print "User KeyboardInterrupt"
	
else:
	shutdown()
	print "Some other exception..."
