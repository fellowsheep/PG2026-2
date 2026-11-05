import cv2 as cv
import numpy as np

img = cv.imread('../../src/ExemplosOpenCV/baboon.png')

# Criando um kernel (filtro de média)
kernel3x3 = np.ones((3,3),np.float32) / 9.0
kernel5x5 = np.ones((5,5), np.float32) / 25.0

img_correlated3x3 = cv.filter2D(img,-1,kernel3x3)
img_correlated5x5 = cv.filter2D(img,-1,kernel5x5)

cv.imshow('Imagem original', img)
cv.imshow('Imagem com filtro de correlacao 3x3',img_correlated3x3)
cv.imshow('Imagem com filtro de correlacao 5x5',img_correlated5x5)

cv.waitKey(0)