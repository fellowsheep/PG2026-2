import numpy as np
import cv2 as cv

img = cv.imread('../../src/ExemplosOpenCV/baboon.png')
imgNegativo = img.copy()

altura = img.shape[0]
largura = img.shape[1]

for i in range (altura):
    for j in range(largura):
        # obter os valores de R, G e B do pixel i j visitado
        b = img.item(i,j,0) # Canal Azul - B
        g = img.item(i,j,1) # Canal Verde - G
        r = img.item(i,j,2) # Canal Vermelho - R      

        imgNegativo[i,j,0] = b ^ 255
        imgNegativo[i,j,1] = g ^ 255
        imgNegativo[i,j,2] = r ^ 255
        
       


cv.imshow('Imagem Original', img)
cv.imshow('Imagem Invertida',imgNegativo)
k = cv.waitKey(0)