"""
=============================================================================
Exemplo de Detecção de Faces e Olhos usando Haar Cascades (OpenCV)
=============================================================================

Este script demonstra a detecção clássica de objetos utilizando Classificadores 
em Cascata de Haar (Haar Cascades). 

NOTA IMPORTANTE SOBRE O AMBIENTE (OpenCV 5+):
Nas versões mais recentes do OpenCV (OpenCV 5 e superiores), o pacote padrão 
('opencv-python') removeu o suporte nativo aos classificadores Haar e a classe 
'CascadeClassifier' do módulo principal. 

Para que este script funcione corretamente:
1. Certifique-se de instalar o pacote de contribuição:
   pip install opencv-contrib-python
   
2. Os arquivos XML dos classificadores (como 'haarcascade_frontalface_default.xml') 
   não vêm mais embutidos por padrão. Eles devem ser mantidos localmente na 
   pasta do seu projeto (ou baixados diretamente do repositório oficial do OpenCV).

USO:
    facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>]
=============================================================================
"""

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv

# local modules
from common import clock, draw_str


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv.rectangle(img, (x1, y1), (x2, y2), color, 2)

def main():

    print(cv.__version__)
    
    # coloquei os haarcascades em pasta local
    face_classifier = cv.CascadeClassifier("../../src/ExemplosOpenCV/haarcascades/haarcascade_frontalface_default.xml")
    eye_classifier = cv.CascadeClassifier("../../src/ExemplosOpenCV/haarcascades/haarcascade_eye.xml")   
    create_capture = cv.VideoCapture('../../src/ExemplosOpenCV/rossana.mp4')

    while True:
        _ret, img = create_capture.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)

        t = clock()
        rects = detect(gray, face_classifier)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        if not eye_classifier.empty():
            for x1, y1, x2, y2 in rects:
                roi = gray[y1:y2, x1:x2]
                vis_roi = vis[y1:y2, x1:x2]
                subrects = detect(roi.copy(), eye_classifier)
                draw_rects(vis_roi, subrects, (255, 0, 0))
        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv.imshow('facedetect', vis)

        if cv.waitKey(5) == 27:
            break

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()