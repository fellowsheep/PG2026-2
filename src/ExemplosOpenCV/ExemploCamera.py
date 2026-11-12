import cv2 as cv
import numpy as np

def main():
    # Inicializa a captura da webcam (0 é a câmera padrão)
    cap = cv.VideoCapture('../../src/ExemplosOpenCV/rossana.mp4')

    if not cap.isOpened():
        print("Erro: Não foi possível acessar a webcam.")
        return

    print("Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro na captura do frame.")
            break

        frame = cv.resize(frame, (800, 600), interpolation=cv.INTER_LINEAR)

        # Aplica o Gaussian Blur conforme mostrado no ExemploFiltrosConvolucao.py
        frame_blur = cv.GaussianBlur(frame, (5, 5), 1.5)
        
        # Aplica detecção de bordas de Canny
        frame_canny = cv.Canny(frame_blur, 100, 150)
        
        cv.imshow('Webcam Original (Modo Video)', frame)
        cv.imshow('Filtro Suavizacao (Blur)', frame_blur)
        cv.imshow('Filtro Realce (Canny)', frame_canny)

        # ATENÇÃO ALUNOS: Espera de 1ms vital para o OpenCV processar a renderização
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()