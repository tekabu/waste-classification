from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
channel = 0

def loop():
	time.sleep(5)
	while True:
		single()
		time.sleep(5)

def single():
	kit.servo[channel].angle = 180
	time.sleep(3)
	kit.servo[channel].angle = 90

def set_position():
	kit.servo[channel].angle = 120
	time.sleep(0.3)
	kit.servo[channel].angle = 90

def x():
    for i in range(0, 5):
        kit.servo[i].angle = 180

    time.sleep(3)

    for i in range(0, 5):    
        kit.servo[i].angle = 100

def main():
	try:
		while True:
			loop()
	except KeyboardInterrupt:
		pass

	print('bye')

if __name__ == '__main__':
	x()