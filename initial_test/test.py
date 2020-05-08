import RPi.GPIO as GPIO
import time, urllib.request, json
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)  # Define pin 8 as an output pin
while True:
	with urllib.request.urlopen("https://aurangzeblight.herokuapp.com/summary?psw=Aurangzebiscool123@") as url:
		data = json.loads(url.read().decode())
		print(data)
	if data['On']:
		GPIO.output(8, 1)  # Outputs digital HIGH signal (5V) on pin 8
		time.sleep(5)  # Time delay of 1 second
	else:
		GPIO.output(8, 0)  # Outputs digital LOW signal (0V) on pin 8
		time.sleep(1)  # Time delay of 1 second

