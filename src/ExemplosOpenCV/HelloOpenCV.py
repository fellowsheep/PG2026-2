import numpy as np
import cv2 as cv

# Imprime a versão do OpenCV
print(cv.__version__)

img = cv.imread('../../src/ExemplosOpenCV/baboon.png')

cv.imshow('Hello OpenCV', img)

k = cv.waitKey(0)

