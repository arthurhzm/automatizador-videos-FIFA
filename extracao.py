import cv2
video_path = r"C:\Users\arthu\Videos\partida.mp4"
video = cv2.VideoCapture(video_path)
fps = video.get(cv2.CAP_PROP_FPS) # Frames por segundo
success, frame = video.read() # Lê o primeiro frame do vídeo  
placar_region = (200, 50, 360, 118)  # (x1, y1, x2, y2)
frame_count = 0
success, frame = video.read()

while success:
    if frame_count % int(fps) == 0:  
        cropped = frame[placar_region[1]:placar_region[3], placar_region[0]:placar_region[2]]
        file_path = f"frames/frame_{frame_count}.jpg"
        cv2.imwrite(file_path, cropped)
        print(f"Salvou: {file_path}")

    success, frame = video.read()
    frame_count += 1

video.release()