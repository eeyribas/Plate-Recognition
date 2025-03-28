import picamera
import time
from openalpr import Alpr

alpr=Alpr("eu", "/home/pi/openalpr/config/openalpr.conf", "/home/pi/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

def function():   
    with picamera.PiCamera() as camera:
        time.sleep(0.1)
        camera.capture('image.jpg')

    alpr.set_top_n(1)
    results=alpr.recognize_file("image.jpg")
    
    i=0
    for plate in results['results']:
        i+=1
        for candidate in plate['candidates']:
            prefix="-"
            if candidate['matches_template']:
                prefix="*"
            text=candidate['plate']
            length=len(text)
            if(length==7):
                print(text)              
            if(length==8):
                print(text)

function()