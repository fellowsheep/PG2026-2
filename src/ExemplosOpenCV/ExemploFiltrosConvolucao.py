import cv2 as cv
import numpy as np

img = cv.imread('../../src/ExemplosOpenCV/pikachu.jpg')
img_grayscale = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
img_grayscale = cv.resize(img, (500, 500), interpolation=cv.INTER_LINEAR)

img_blur = cv.blur(img_grayscale,(5,5))
img_gaussianBlur = cv.GaussianBlur(img_grayscale,(5,5),1.5)

# Filtro de sobel, aplicado horizontalmente 
sobel_horizontal = cv.Sobel(img_gaussianBlur, cv.CV_64F,1, 0,3)
sobel_vertical = cv.Sobel(img_gaussianBlur, cv.CV_64F,0, 1,3)

img_somada = cv.add(sobel_horizontal,sobel_vertical)

# Método de detecção de bordas de Canny
img_Canny = cv.Canny(img_gaussianBlur,100,150)

cv.imshow('Imagem original', img)
cv.imshow('Imagem suavizada', img_blur)
cv.imshow('Imagem suavizada (gaussian)', img_gaussianBlur)
cv.imshow('Imagem com filtro Sobel (horizontal)', sobel_horizontal)
cv.imshow('Imagem com filtro Sobel (vertical)', sobel_vertical)
cv.imshow('Sobel horizontal + vertical', img_somada)
cv.imshow('Detecção de bordas Canny',img_Canny)
cv.waitKey(0)