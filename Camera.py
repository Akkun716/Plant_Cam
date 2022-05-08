from picamera import PiCamera
from gpiozero import Button
from time import sleep
import RPi.GPIO as GPIO
import datetime
import paho.mqtt.client as Client
import paho.mqtt.publish as publish
from PIL import Image
import base64
from io import BytesIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)

button = Button(14)
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

def on_connect(client, userdata, flags, rc):
    client.subscribe('projects/unfold-usf/topics/Camera_rig')

def publish_mqtt(image_date):
    mqttc.publish('projects/unfold-usf/topics/Camera_rig', image_date, qos=1)

def on_publish(unused_client, unused_userdata, unused_mid):
    print("on_publish")

mqttc = Client.Client('projects/unfold-usf/locations/us-central1/registries/Plant_Cam/devices/Main_Pi')
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.connect('mqtt.googleapis.com', 8883)
mqttc.loop_start()
while True:
    try:
        button.wait_for_press()
        now = datetime.datetime.now().strftime('%m-%d-%Y_%H:%M:%S')
        addr = ('/home/pi/Images/Image %s.jpg' % now)
        camera.capture(addr)
        img = Image.open(addr)
        img_file = BytesIO()
        img.save(img_file, format="JPEG")
        img_bytes = img_file.getvalue()
        img_b64 = base64.b64encode(img_bytes)
        publish_mqtt(img_b64)
        print('published')
        GPIO.output(15, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(15, GPIO.LOW)

    except KeyboardInterrupt:
        camera.stop_preview()
        mqttc.loop_stop()
        camera.close()
        break