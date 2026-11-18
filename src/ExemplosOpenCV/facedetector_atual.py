"""
=============================================================================
Exemplo de Detecção Facial com Rede Neural Leve (YuNet / cv2.FaceDetectorYN)
=============================================================================

Este script demonstra a detecção de faces (com caixa delimitadora e 5 pontos
de referência faciais/landmarks) utilizando o modelo YuNet via módulo DNN do
OpenCV.

Diferente dos classificadores clássicos em cascata (Haar Cascades), abordagens
baseadas em redes neurais costumam lidar melhor com variações de pose,
iluminação e oclusões parciais.

ONDE OBTER O MODELO (.onnx) E EXEMPLOS DE REFERÊNCIA:
https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet

NOTA IMPORTANTE:
Certifique-se de que o arquivo do modelo (.onnx) esteja acessível no caminho
configurado no código (por exemplo, na mesma pasta do script).
=============================================================================
"""

import cv2 as cv

# Carrega o modelo ONNX (ex.: face_detection_yunet_2023mar.onnx)
detector = cv.FaceDetectorYN.create(
    model="../../src/ExemplosOpenCV/onnx/face_detection_yunet_2023mar.onnx",
    config="",
    input_size=(320, 320),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000
)

cap = cv.VideoCapture('../../src/ExemplosOpenCV/rossana.mp4') #pros testes sem camera na Unisinos
#cap = cv.VideoCapture(0)  # ou caminho de um vídeo

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    if faces is not None:
        for face in faces:
            x, y, bw, bh = face[:4].astype(int)
            cv.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

            # 5 landmarks: olho direito, olho esquerdo, nariz, canto direito e esquerdo da boca
            landmarks = face[4:14].astype(int).reshape((5, 2))
            for lx, ly in landmarks:
                cv.circle(frame, (lx, ly), 2, (255, 0, 0), -1)

    cv.imshow("YuNet Face Detection", frame)
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()