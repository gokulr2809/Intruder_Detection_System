import RPi.GPIO as GPIO
from mail import mail
from datetime import datetime,date
import requests
import base64
import time
import picamera
from time import sleep
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
from _thread import *
from _thread import start_new_thread
import http.server as SimpleHTTPServer


PIR_input = 29
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_input, GPIO.IN)
i=1

def camera():
        camera = picamera.PiCamera()
        #set resolution
        camera.resolution = (1024, 768)
        camera.brightness = 60
        camera.start_preview()
        sleep(3)
        #store image
        camera.capture('/home/pi/Desktop/image.png')
        camera.stop_preview()
        camera.close()
        
while True:
    URL = "http://192.168.150.105:8000/idsstate"
    x = requests.get(url = URL)
    data = x.json()
    print(data)
    if data['ids'] == True and data['stream'] == False:
        print('System On')
        if(GPIO.input(PIR_input)):
            #create object for PiCamera class
            print("Detected")
            camera()
            today = date.today()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            URL = "http://192.168.150.105:8000/rpi"
            #image encoding
            with open("/home/pi/Desktop/image.png", "rb") as original_file:
                encoded_string = base64.b64encode(original_file.read())
            #httpreq  
            data = {"ittime" : current_time, "itdate" : today, "media": encoded_string}
            r = requests.post(url = URL,data = data)
            data = r.text
            print(data)
            #mail
            #mail()
        else:
            print("Not Detected")
            
    elif data['stream'] == True:
        print('Streaming')
        PAGE="""\
        <html>
        <head>
        <title>Surveillance Camera</title>
        </head>
        <body style = "background-color: #182446;">
        <center style = "margin-top: 30px;"><h1 style = "color: white;">Surveillance Camera</h1></center>
        <center style = "margin-top: 50px;"><img src="stream.mjpg" width="852" height="480"></center>
        </body>
        </html>
        """

        class StreamingOutput(object):
            def __init__(self):
                self.frame = None
                self.buffer = io.BytesIO()
                self.condition = Condition()

            def write(self, buf):
                if buf.startswith(b'\xff\xd8'):
                    # New frame, copy the existing buffer's content and notify all
                    # clients it's available
                    self.buffer.truncate()
                    with self.condition:
                        self.frame = self.buffer.getvalue()
                        self.condition.notify_all()
                    self.buffer.seek(0)
                return self.buffer.write(buf)

        class StreamingHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(301)
                    self.send_header('Location', '/index.html')
                    self.end_headers()
                elif self.path == '/index.html':
                    content = PAGE.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Content-Length', len(content))
                    self.end_headers()
                    self.wfile.write(content)
                elif self.path == '/stream.mjpg':
                    self.send_response(200)
                    self.send_header('Age', 0)
                    self.send_header('Cache-Control', 'no-cache, private')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                    self.end_headers()
                    try:
                        while True:
                            with output.condition:
                                output.condition.wait()
                                frame = output.frame
                            self.wfile.write(b'--FRAME\r\n')
                            self.send_header('Content-Type', 'image/jpeg')
                            self.send_header('Content-Length', len(frame))
                            self.end_headers()
                            self.wfile.write(frame)
                            self.wfile.write(b'\r\n')
                    except Exception as e:
                        logging.warning(
                            'Removed streaming client %s: %s',
                            self.client_address, str(e))
                else:
                    self.send_error(404)
                    self.end_headers()
                    
            def do_POST(self):
                if self.path.startswith('/kill_server'):
                    print ("Server is going down, run it again manually!")
                    def kill_me_please(server):
                        server.shutdown()
                    start_new_thread(kill_me_please, (server,))
                    self.send_error(500)

        class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
            allow_reuse_address = True
            daemon_threads = True

        with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
            output = StreamingOutput()
            camera.start_recording(output, format='mjpeg')
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            try:
                server.serve_forever()
            finally:
                camera.stop_recording()
    else:
        print('System Off')
    sleep(2)
    
    
        


        
    






























