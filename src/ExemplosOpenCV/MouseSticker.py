# Leitura sugerida: https://docs.opencv.org/4.13.0/d0/d86/tutorial_py_image_arithmetics.html

import cv2 as cv
import numpy as np

# Variável global para armazenar as posições onde o usuário clicou
posicoes_stickers = []

def aplicar_sticker(fundo, sticker, x, y):
    h_fundo, w_fundo = fundo.shape[:2]
    h_sticker, w_sticker = sticker.shape[:2]

    # Prevenção de erro: ignora se o clique for muito perto da borda direita/inferior
    # (Evita que o slice do array tente acessar um índice que não existe)
    if y + h_sticker > h_fundo or x + w_sticker > w_fundo:
        return fundo

    # 1. Separa os canais do sticker (Azul, Verde, Vermelho e Alfa)
    b, g, r, a = cv.split(sticker)
    sticker_bgr = cv.merge([b, g, r])

    # 2. Normaliza o canal alfa (de 0-255 para 0.0-1.0) e replica para 3 canais
    alpha = a / 255.0
    alpha_3c = cv.merge([alpha, alpha, alpha])

    # 3. Define a Região de Interesse (ROI) na imagem de fundo
    roi = fundo[y:y+h_sticker, x:x+w_sticker]

    # 4. Operação Matemática de Blending
    # Equação: (Fundo * (1 - Alpha)) + (Sticker * Alpha)
    fundo_suavizado = roi * (1 - alpha_3c)
    sticker_suavizado = sticker_bgr * alpha_3c
    
    # Soma as duas matrizes para compor o resultado
    resultado = cv.add(fundo_suavizado, sticker_suavizado).astype(np.uint8)

    # Substitui os pixels originais da ROI pelo resultado do cálculo
    fundo[y:y+h_sticker, x:x+w_sticker] = resultado
    
    return fundo

def mouse_callback(event, x, y, flags, param):
    # Quando o botão esquerdo for clicado, salva a coordenada atual do mouse
    if event == cv.EVENT_LBUTTONDOWN:
        posicoes_stickers.append((x, y))

def main():
    # Carrega a imagem de base
    img = cv.imread('../../src/ExemplosOpenCV/baboon.png')
    
    # ATENÇÃO ALUNOS: A flag IMREAD_UNCHANGED é obrigatória para não perder o canal Alfa (4º canal)
    sticker_img = cv.imread('../../src/ExemplosOpenCV/sticker.png', cv.IMREAD_UNCHANGED)
    # sticker_img = cv.imread('../../src/ExemplosOpenCV/eyeglasses.png', cv.IMREAD_UNCHANGED)
    #sticker_img = cv.resize(sticker_img, (250, 100), interpolation=cv.INTER_LINEAR)
   
    if img is None or sticker_img is None:
        print("Erro: Imagem de fundo ou sticker não encontrados.")
        return

    # IMPORTANTE: A janela precisa ser criada e nomeada antes de associar o callback
    nome_janela = 'Modo Foto - Aplicacao de Stickers'
    cv.namedWindow(nome_janela)
    cv.setMouseCallback(nome_janela, mouse_callback)

    print("Clique na imagem para adicionar o sticker.")
    print("Pressione 'c' para limpar todos os stickers (Reset).")
    print("Pressione 'q' para sair.")

    while True:
        # Trabalhamos sempre em uma cópia para que os stickers não se fundam permanentemente
        # no array original, permitindo "limpar a tela" depois.
        img_display = img.copy()

        # Varre a lista global e aplica a função de blending em cada coordenada salva
        for (pos_x, pos_y) in posicoes_stickers:
            img_display = aplicar_sticker(img_display, sticker_img, pos_x, pos_y)

        cv.imshow(nome_janela, img_display)

        tecla = cv.waitKey(1)
        
        # Lógica para limpar a tela
        if tecla == ord('c'):
            posicoes_stickers.clear()
        elif tecla == ord('q'):
            break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()