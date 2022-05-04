from picamera import PiCamera
from gpiozero import Button
from time import sleep
import RPi.GPIO as GPIO
import datetime
from google.cloud import pubsub_v1

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)

button = Button(14)
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
time.sleep(2)
while True:
    try:
        button.wait_for_press()
        now = datetime.datetime.now().strftime('%m-%d-%Y_%H:%M:%S')
        camera.capture('/home/pi/Images/Image %s.jpg' % now)
        GPIO.output(15, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(15, GPIO.LOW)


    except KeyboardInterrupt:
        camera.stop_preview()
        break

camera.close()