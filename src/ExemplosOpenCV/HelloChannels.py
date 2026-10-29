import numpy as np
import cv2 as cv

img = cv.imread('../../src/ExemplosOpenCV/baboon.png')
imgR = img.copy()
imgG = img.copy()
imgB = img.copy()

altura = img.shape[0]
largura = img.shape[1]

for i in range (altura):
    for j in range(largura):
        # obter os valores de R, G e B do pixel i j visitado
        b = img.item(i,j,0) # Canal Azul - B
        g = img.item(i,j,1) # Canal Verde - G
        r = img.item(i,j,2) # Canal Vermelho - R

        imgR[i,j,0] = r 
        imgR[i,j,1] = r
        imgR[i,j,2] = r

        imgG[i,j,0] = g 
        imgG[i,j,1] = g
        imgG[i,j,2] = g

        imgB[i,j,0] = b 
        imgB[i,j,1] = b
        imgB[i,j,2] = b


cv.imshow('Imagem Original', img)
cv.imshow('Canal R',imgR)
cv.imshow('Canal G',imgG)
cv.imshow('Canal B',imgB)

k = cv.waitKey(0)