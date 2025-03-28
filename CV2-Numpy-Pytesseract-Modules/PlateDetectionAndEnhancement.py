import cv2
import numpy as np

img=cv2.imread("/home/pi/image.jpg")
cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
cv2.imshow("Original Image", img)

grayImg=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.namedWindow("Gray Converted Image", cv2.WINDOW_NORMAL)
cv2.imshow("Gray Converted Image", grayImg)

noiseRemoval=cv2.bilateralFilter(grayImg, 9, 75, 75)
cv2.namedWindow("Noise Removed Image", cv2.WINDOW_NORMAL)
cv2.imshow("Noise Removed Image", noiseRemoval)

equalHistogram=cv2.equalizeHist(noiseRemoval)
cv2.namedWindow("After Histogram equalisation", cv2.WINDOW_NORMAL)
cv2.imshow("After Histogram equalisation", equalHistogram)

kernel=cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
morphImg=cv2.morphologyEx(equalHistogram, cv2.MORPH_OPEN, kernel, iterations=15)
cv2.namedWindow("Morphological opening", cv2.WINDOW_NORMAL)
cv2.imshow("Morphological opening", morphImg)

subMorpImg=cv2.subtract(equalHistogram, morphImg)
cv2.namedWindow("Subtraction image", cv2.WINDOW_NORMAL)
cv2.imshow("Subtraction image", subMorpImg)

ret,threshImg=cv2.threshold(subMorpImg, 0, 255, cv2.THRESH_OTSU)
cv2.namedWindow("Image after Thresholding", cv2.WINDOW_NORMAL)
cv2.imshow("Image after Thresholding", threshImg)

cannyImg=cv2.Canny(threshImg, 250, 255)
cv2.namedWindow("Image after applying Canny", cv2.WINDOW_NORMAL)
cv2.imshow("Image after applying Canny", cannyImg)
cannyImg=cv2.convertScaleAbs(cannyImg)

kernel=np.ones((3,3), np.uint8)
dilatedImg=cv2.dilate(cannyImg, kernel, iterations=1)
cv2.namedWindow("Dilation", cv2.WINDOW_NORMAL)
cv2.imshow("Dilation", dilatedImg)

new, contours, hierarchy=cv2.findContours(dilatedImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key=cv2.contourArea, reverse=True)[:10]
screenCnt=None

for c in contours:
    peri=cv2.arcLength(c, True)
    approx=cv2.approxPolyDP(c, 0.06*peri, True)
    if len(approx)==4:
        screenCnt=approx
        break

final=cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.namedWindow("Image with Selected Contour", cv2.WINDOW_NORMAL)
cv2.imshow("Image with Selected Contour", final)

mask=np.zeros(grayImg.shape, np.uint8)
newImg=cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
newImg=cv2.bitwise_and(img, img, mask=mask)
cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
cv2.imshow("Final_image", newImg)

y,cr,cb=cv2.split(cv2.cvtColor(newImg, cv2.COLOR_RGB2YCrCb))
y=cv2.equalizeHist(y)
finalImg=cv2.cvtColor(cv2.merge([y,cr,cb]), cv2.COLOR_YCrCb2RGB)
cv2.namedWindow("Enhanced Number Plate", cv2.WINDOW_NORMAL)
cv2.imshow("Enhanced Number Plate", finalImg)
cv2.waitKey() 