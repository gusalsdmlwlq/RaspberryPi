# 카메라로 찍은 사진 server에 전달
# client.py

from picamera import PiCamera
import time
from PIL import Image
import socket
import base64
import requests
from io import BytesIO

IP = '172.29.148.137'
PORT = 5001
#IMAGE_SIZE = (1920, 1080)
#IMAGE_SIZE = (1366, 768)
#time.sleep(5)

#with PiCamera(resolution=IMAGE_SIZE) as camera:
with PiCamera() as camera:
        stream = BytesIO()
        for i in camera.capture_continuous(stream, format='jpeg', use_video_port = True):
                stream.truncate()
                stream.seek(0)
                barray = stream.read(stream.getbuffer().nbytes)
                requests.post('http://{}:{}/api/calculateEmptySeats'.format(IP, PORT), files={'file': barray})
                time.sleep(10)
                stream.seek(0)