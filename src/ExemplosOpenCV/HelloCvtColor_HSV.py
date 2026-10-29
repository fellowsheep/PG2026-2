import numpy as np
import cv2 as cv

imgColor = cv.imread('../../src/ExemplosOpenCV/baboon.png')

if imgColor is not None:
    imgHSV = cv.cvtColor(imgColor,cv.COLOR_BGR2HSV)
    h, s, v = cv.split(imgHSV)
    s_modificado = cv.multiply(s,1.5)
    imgSaturada = cv.merge([h,s_modificado,v])
    imgSaturada = cv.cvtColor(imgSaturada,cv.COLOR_HSV2BGR)
    v_escurecido = cv.multiply(v,0.5)
    imgEscurecida = cv.merge([h,s,v_escurecido])
    imgEscurecida = cv.cvtColor(imgEscurecida,cv.COLOR_HSV2BGR)
    #pseudo-sépia (explicação na aula):
    h.fill(0)
    h_modificado = cv.add(h,21/2)
    imgSepia = cv.merge([h_modificado,s,v])
    imgSepia = cv.cvtColor(imgSepia,cv.COLOR_HSV2BGR)

cv.imshow('Imagem original (colorida)',imgColor)
cv.imshow('Imagem saturada:',imgSaturada)
cv.imshow('Imagem escurecida:',imgEscurecida)
cv.imshow('Imagem sepia:',imgSepia)

cv.waitKey(0)
