from PIL import Image
import pytesseract
import os

filename="image.jpg"
text=pytesseract.image_to_string(Image.open(filename))
print(text)