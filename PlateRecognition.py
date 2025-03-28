import picamera
import time
from openalpr import Alpr
from Tkinter import *
from PIL import Image, ImageTk

alpr=Alpr("eu", "/home/pi/openalpr/config/openalpr.conf", "/home/pi/openalpr/runtime_data")
if not alpr.is_loaded():
	print("Error loading OpenALPR")
    sys.exit(1)

root=Tk() 
root.wm_title("PLATE RECOGNITION") 
root.config(background = "#FFFFFF")
root.geometry("1400x600")

leftFrame=Frame(root, width=900, height=600, background="Yellow")
leftFrame.grid(row=0, column=0)
rightFrame=Frame(root, width=500, height=600, background="Yellow")
rightFrame.grid(row=0, column=1)

text1=Label(rightFrame, text="READING PLATES", font=('times', 20, 'bold'))
text1.config(bg='yellow', fg='black')
text1.grid(row=0, column=0, padx=2, pady=2)
text2=Label(rightFrame, text="RECORD PLATES", font=('times', 20, 'bold'))
text2.config(bg='yellow', fg='black')
text2.grid(row=2, column=0, padx=2, pady=2)

colorLog1=Text(rightFrame, width=37, height=10, takefocus=0, font=('times', 18))
colorLog1.grid(row=1, column=0, padx=10, pady=10)
colorLog2=Text(rightFrame, width=37, height=5, takefocus=0, font=('times', 18))
colorLog2.grid(row=3, column=0, padx=10, pady=10)

fr=open("Plates.txt", "r")
str1=fr.read()
str2=str1.split('_')

colorLog2.insert(0.0, str2[0]+"\n")
colorLog2.insert(0.0, str2[1]+"\n")
colorLog2.insert(0.0, str2[2]+"\n")

def myMainloop():   
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
                colorLog1.insert(0.0, text+"\n")
    root.after(1000, myMainloop) 

image=Image.open("result.jpg")  
photo=ImageTk.PhotoImage(image)
l1=Label(leftFrame, image=photo, height=600, width=900).pack()

root.after(1000, myMainloop)
root.mainloop() 