import numpy as np
import cv2 as cv

img = cv.imread('../../src/ExemplosOpenCV/baboon.png')
imgColorizada = img.copy()

corColorizadora = [0, 0, 255]

altura = img.shape[0]
largura = img.shape[1]

for i in range (altura):
    for j in range(largura):
        # obter os valores de R, G e B do pixel i j visitado
        b = img.item(i,j,0) # Canal Azul - B
        g = img.item(i,j,1) # Canal Verde - G
        r = img.item(i,j,2) # Canal Vermelho - R      

        imgColorizada[i,j] = imgColorizada[i,j] | corColorizadora
        
       


cv.imshow('Imagem Original', img)
cv.imshow('Imagem Colorizada',imgColorizada)
k = cv.waitKey(0)