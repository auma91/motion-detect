import RPi.GPIO as GPIO
import time, urllib.request, json
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)  # Define pin 8 as an output pin
base_link = "https://aurangzeblight.herokuapp.com/"
endpoint = "summary"
secret_query = "?psw=Aurangzebiscool123@"
def get_JSON(link):
	with urllib.request.urlopen() as url:
		data = json.loads(url.read().decode())
		return data
def adjust_LED():
	fail_count = 0
	while True:
		data = None
		try:
			data = get_JSON(base_link+endpoint+secret_query)
			fail_count = 0
		except:
			fail_count+=1
			print("Error Reaching Endpoint, trying again ...")
			if fail_count == 10:
				print("10 exceptions raised, check internet connection\nShutting program down.")
				break
			else:
				continue
		if data['On']:
			GPIO.output(8, 1)  # Outputs digital HIGH signal (5V) on pin 8
			time.sleep(5)  # Time delay of 1 second
		else:
			GPIO.output(8, 0)  # Outputs digital LOW signal (0V) on pin 8
			time.sleep(1)  # Time delay of 1 second