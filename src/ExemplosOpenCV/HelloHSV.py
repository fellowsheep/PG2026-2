import cv2 as cv
import numpy as np

# 1. Cria uma imagem em branco (150 pixels de altura por 360 de largura) com 3 canais
# Cada coluna representará um grau do sistema HSV (de 0 a 359)
altura = 150
largura = 360
img_hsv = np.zeros((altura, largura, 3), dtype=np.uint8)

# 2. Preenche a imagem coluna por coluna
for coluna in range(largura):
    # O OpenCV mapeia o Hue de 0 a 179 (dividindo o ângulo original por 2)
    hue_opencv = coluna // 2  
    
    # Define Saturação máxima (255) e Valor/Brilho máximo (255)
    img_hsv[:, coluna] = [hue_opencv, 255, 255]

# 3. Converte o espaço de cores de HSV para BGR (padrão de exibição do OpenCV)
img_bgr = cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR)

# 4. Exibe o resultado em uma janela
cv.imshow("Espectro HSV (0 a 359 graus)", img_bgr)

# Mantém a janela aberta até que qualquer tecla seja pressionada
cv.waitKey(0)

