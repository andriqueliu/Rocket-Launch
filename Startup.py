'''
University of Washington Department of Electrical Engineering
ESS 472 Wireless Rocket Launch Research Project

Research Advisor: Professor John Sahr
Authors: Andrique Liu and Emraj Sidhu

Startup is intended to run on startup. 
'''

import Adafruit_BBIO.GPIO as GPIO

# Initialize GPIO pins
def init_GPIO():
	GPIO.setup("P8_8", GPIO.OUT)
	GPIO.setup("P8_10", GPIO.OUT)

# Code written for test purposes: drive both GPIOs low
def all_low():
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_10", GPIO.LOW)

# Disables all FETs
def disable_all_FETs():
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_10", GPIO.HIGH)


