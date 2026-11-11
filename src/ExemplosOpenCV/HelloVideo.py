import cv2 as cv
import numpy as np

def main():
    # Caminho para o vídeo 
    cap = cv.VideoCapture('../../src/ExemplosOpenCV/Human_Kidney_Ultrasound_Scan.ogg')

    if not cap.isOpened():
        print("Erro: Não foi possível acessar o arquivo de vídeo.")
        return

    # Obtém o FPS do vídeo original para calcular o tempo de espera real
    fps = cap.get(cv.CAP_PROP_FPS)
    if fps == 0 or fps != fps: # Proteção caso o vídeo não informe o FPS
        fps = 30 
    
    # Calcula quantos milissegundos o waitKey deve esperar por frame (Ex: 1000ms / 30fps = ~33ms)
    delay_frame = int(1000 / fps)

    print("Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        
        # Se ret for falso, o vídeo acabou. (Para aula, você pode dar um cap.set(cv.CAP_PROP_POS_FRAMES, 0) para o vídeo ficar em loop).
        if not ret:
            print("Fim do vídeo.")
            break
            
        # 1. Converte para Grayscale (Ultrassom geralmente já é, mas o arquivo de vídeo pode estar salvo como BGR)
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # 2. Suavização (Blur) para reduzir o ruído de Speckle clássico de ultrassom
        frame_blur = cv.GaussianBlur(frame_gray, (3, 3), 0)
        
        # 3. Realce das bordas com Laplaciano (ajuda a ver contornos de tecidos)
        laplaciano = cv.Laplacian(frame_blur, cv.CV_64F)
        # Converte de volta para uint8 para exibição correta
        laplaciano_exibicao = cv.convertScaleAbs(laplaciano)

        cv.imshow('Exame Original (Modo Video)', frame_gray)
        cv.imshow('Exame Suavizado (Sem ruido)', frame_blur)
        cv.imshow('Realce de Bordas (Laplaciano)', laplaciano_exibicao)

        # Usa o delay calculado a partir do FPS do vídeo original
        if cv.waitKey(delay_frame) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()