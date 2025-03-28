import numpy as np
import cv2
from openalpr import Alpr

alpr=Alpr("eu", "/home/pi/openalpr/config/openalpr.conf", "/home/pi/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(1)
cap=cv2.VideoCapture("video.mpg")

while(True):    
    ret, frame=cap.read() 

    if ret:        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cv2.imwrite("image.jpg", frame)
        results=alpr.recognize_file("image.jpg")

        i=0
        for plate in results['results']:
            i+=1
            print("Plate : #%d" % i)
            for candidate in plate['candidates']:
                prefix="-"
                if candidate['matches_template']:
                    prefix="*"

                print("%12s" % (candidate['plate']))       
    else:
        break;

cap.release()
alpr.unload()
cv2.destroyAllWindows()