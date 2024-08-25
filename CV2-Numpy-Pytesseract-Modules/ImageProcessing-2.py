import cv2
import numpy as np
from PIL import Image
import pytesseract
import os

img=cv2.imread("image.jpg")

grayImg=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
noiseRemoval=cv2.bilateralFilter(grayImg, 9, 75, 75)
equalHistogram=cv2.equalizeHist(noiseRemoval)

kernel=cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
morphImg=cv2.morphologyEx(equalHistogram,cv2.MORPH_OPEN,kernel,iterations=15)
subMorphImg=cv2.subtract(equalHistogram, morphImg)

ret,threshImg=cv2.threshold(subMorphImg, 0, 255, cv2.THRESH_OTSU)
cannyImg=cv2.Canny(threshImg, 250, 255)
cannyImg=cv2.convertScaleAbs(cannyImg)
cv2.imwrite("result_1.jpg", cannyImg )
kernel=np.ones((3,3), np.uint8)
dilatedImg=cv2.dilate(cannyImg, kernel, iterations=1)

new, contours, hierarchy=cv2.findContours(dilatedImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:10]
screenCnt=None

for c in contours:
    peri=cv2.arcLength(c, True)
    approx=cv2.approxPolyDP(c, 0.06 * peri, True)
    if len(approx) == 4:
        screenCnt=approx
        break
final=cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.imwrite("result_2.jpg",  final)

mask=np.zeros(grayImg.shape,np.uint8)
new_image=cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
new_image=cv2.bitwise_and(img, img, mask=mask)
cv2.imwrite("result.jpg", new_image)

filename="result.jpg"
text=pytesseract.image_to_string(Image.open(filename))
print(text)