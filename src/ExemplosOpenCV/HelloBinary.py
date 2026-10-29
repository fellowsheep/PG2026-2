import numpy as np
import cv2 as cv

img = cv.imread('../../src/ExemplosOpenCV/bolinhas.png')
imgGrayscale = img.copy()

altura = img.shape[0]
largura = img.shape[1]

limiar = 200

for i in range (altura):
    for j in range(largura):
        # obter os valores de R, G e B do pixel i j visitado
        b = img.item(i,j,0) # Canal Azul - B
        g = img.item(i,j,1) # Canal Verde - G
        r = img.item(i,j,2) # Canal Vermelho - R      

        #mediaPonderada = r * 0.2125 + g * 0.7154 + b * 0.0721
        mediaPonderada = g
        valorBin = 0
        if mediaPonderada >= limiar:
            valorBin = 255

        imgGrayscale[i,j,0] = valorBin 
        imgGrayscale[i,j,1] = valorBin 
        imgGrayscale[i,j,2] = valorBin 


cv.imshow('Imagem Original', img)
cv.imshow('Imagem binaria',imgGrayscale)
k = cv.waitKey(0)