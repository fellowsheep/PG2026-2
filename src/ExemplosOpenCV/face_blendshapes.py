"""
=============================================================================
Extração de Blendshapes e Landmarks Faciais com MediaPipe Face Landmarker
=============================================================================

Este script lê um vídeo ou fluxo de webcam, detecta 478 landmarks faciais 3D
e extrai 52 blendshapes (padrão ARKit) por frame, salvando os resultados
em um arquivo de texto separado por ponto e vírgula (;).

1. INSTALAÇÃO DAS DEPENDÊNCIAS (Python 3.9 a 3.12):
   pip install mediapipe opencv-python

2. BAIXAR O MODELO (face_landmarker.task):
   - Linux/macOS:
     curl -o face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task
   - Windows (PowerShell):
     Invoke-WebRequest -Uri https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task -OutFile face_landmarker.task

   Coloque o arquivo 'face_landmarker.task' no diretório esperado pelo script
   (ou ajuste a variável MODEL_PATH conforme a estrutura da sua pasta).

3. DOCUMENTAÇÃO OFICIAL:
   https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/python
=============================================================================
"""

import argparse
import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = "../../src/ExemplosOpenCV/mediapipe_landmarks/face_landmarker.task"


def draw_landmarks_on_image(rgb_image, detection_result):
    annotated_image = rgb_image.copy()
    if not detection_result.face_landmarks:
        return annotated_image

    h, w, _ = annotated_image.shape

    # Tenta usar o desenhador oficial do MediaPipe (com malha/contornos)
    try:
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh
        from mediapipe.framework.formats import landmark_pb2

        for face_landmarks in detection_result.face_landmarks:
            proto_list = landmark_pb2.NormalizedLandmarkList()
            proto_list.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
                for lm in face_landmarks
            ])

            # Desenha a tesselação (malha)
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=proto_list,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            # Desenha os contornos (olhos, sobrancelhas, lábios, rosto)
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=proto_list,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
            )
    except AttributeError:
        # Fallback caso mp.solutions não esteja disponível na versão instalada
        for face_landmarks in detection_result.face_landmarks:
            for lm in face_landmarks:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(annotated_image, (cx, cy), 1, (0, 255, 0), -1)

    return annotated_image


def main():
    ap = argparse.ArgumentParser(description="Extrai blendshapes do MediaPipe Face Landmarker")
    ap.add_argument("--source", default="0",
                    help="Caminho do vídeo (ex.: video.mp4) ou índice da webcam (0, 1, ...)")
    ap.add_argument("--out", default="blendshapes.txt", help="Arquivo de saída")
    ap.add_argument("--no-show", action="store_true", help="Ocultar a janela com o vídeo")
    args = ap.parse_args()

    is_camera = args.source.isdigit()
    src = int(args.source) if is_camera else args.source

    # cap = cv2.VideoCapture(src)
    cap = cv2.VideoCapture('../../src/ExemplosOpenCV/rossana.mp4')  # pros testes sem camera na Unisinos
    if not cap.isOpened():
        raise SystemExit(f"Não consegui abrir a fonte: {args.source}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    options = vision.FaceLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,   # modo de vídeo: timestamps monotônicos
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        output_face_blendshapes=True,            # ativa os 52 blendshapes
    )
    landmarker = vision.FaceLandmarker.create_from_options(options)

    header_written = False
    frame_idx = 0
    last_ts = -1
    t0 = time.monotonic()

    with open(args.out, "w", encoding="utf-8") as f:
        while True:
            ok, frame_bgr = cap.read()
            if not ok:
                break  # fim do vídeo ou webcam desconectada

            # Timestamp em ms: real para webcam, pelo FPS para arquivo
            if is_camera:
                ts = int((time.monotonic() - t0) * 1000)
            else:
                ts = int(frame_idx * 1000 / fps)
            ts = max(ts, last_ts + 1)  # garante que seja estritamente crescente
            last_ts = ts

            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            result = landmarker.detect_for_video(mp_image, ts)

            if result.face_blendshapes:
                cats = result.face_blendshapes[0]  # primeiro rosto
                if not header_written:
                    names = [c.category_name for c in cats]
                    f.write("frame;timestamp_ms;" + ";".join(names) + "\n")
                    header_written = True
                scores = [f"{c.score:.4f}" for c in cats]
                f.write(f"{frame_idx};{ts};" + ";".join(scores) + "\n")
            else:
                f.write(f"{frame_idx};{ts};NO_FACE\n")

            if not args.no_show:
                # Desenha os landmarks na imagem RGB e converte de volta para BGR
                annotated_rgb = draw_landmarks_on_image(frame_rgb, result)
                vis_bgr = cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)

                # Mostra os top 5 blendshapes ativos no canto superior esquerdo
                if result.face_blendshapes:
                    top_cats = sorted(
                        result.face_blendshapes[0],
                        key=lambda c: c.score,
                        reverse=True
                    )[:5]
                    for i, c in enumerate(top_cats):
                        text = f"{c.category_name}: {c.score:.2f}"
                        cv2.putText(vis_bgr, text, (15, 30 + i * 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                cv2.imshow("Face Landmarker", vis_bgr)
                if cv2.waitKey(1) & 0xFF in (27, ord("q")):  # ESC ou 'q' para sair
                    break

            frame_idx += 1

    cap.release()
    landmarker.close()
    cv2.destroyAllWindows()
    print(f"Concluído: {frame_idx} frames salvos em {args.out}")


if __name__ == "__main__":
    main()