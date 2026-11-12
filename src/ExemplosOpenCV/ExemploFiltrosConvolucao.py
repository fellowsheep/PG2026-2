import cv2 as cv
import numpy as np

img = cv.imread('../../src/ExemplosOpenCV/baboon.png')
#img = cv.imread('../../src/ExemplosOpenCV/pikachu.jpg')

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

# Método de detecção de bordas/realce Laplaciano
img_laplacian = cv.Laplacian(img_grayscale,cv.CV_64F)
img_laplacian_final = cv.convertScaleAbs(img_laplacian)

# Filtro para aumento de nitidez (sharpening)
kernel = np.array([[ 0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

img_sharpen = cv.filter2D(img_grayscale,-1,kernel)

# Filtro ne mínimo e de máximo 

kernel = np.ones((3,3), np.uint8)

#filtro de máximo (Dilatação)
img_dilated = cv.dilate(img_Canny,kernel)

#filtro de mínimo (Erosão)
img_erosion = cv.erode(img_dilated,kernel)

cv.imshow('Imagem original', img)
cv.imshow('Imagem suavizada', img_blur)
cv.imshow('Imagem suavizada (gaussian)', img_gaussianBlur)
cv.imshow('Imagem com filtro Sobel (horizontal)', sobel_horizontal)
cv.imshow('Imagem com filtro Sobel (vertical)', sobel_vertical)
cv.imshow('Sobel horizontal + vertical', img_somada)
cv.imshow('Detecção de bordas Canny',img_Canny)
cv.imshow('Detecção com filtro laplaciano', img_laplacian_final)
cv.imshow('Filtro de nitidez', img_sharpen)
cv.imshow('Filtro de máximo (dilatação)',img_dilated)
cv.imshow('Filtro de mínimo (erosão)',img_erosion)

cv.waitKey(0)