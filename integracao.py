import cv2
import pytesseract
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Caminho do vídeo
video_path = r"C:\Users\arthu\Videos\2024-11-17 18-15-05.mp4"
output_folder = r"highlights"  # Pasta para salvar os cortes
placar_region = (330, 50, 360, 118)  # Região do placar no frame
fps = None  # Inicializa o FPS do vídeo
timestamps = []  # Lista para salvar os momentos dos gols
placar_anterior = None  # Placar da última análise

# Função para validar o formato do placar
def validar_placar(placar):
    import re
    return bool(re.match(r'^\d+:\d+$', placar))  # Exemplo: "2:1", "0:0", etc.

# Função para processar um frame e detectar gols (placar vertical)
def detectar_gol(frame):
    global placar_anterior
    # Recorta a região do placar
    cropped = frame[placar_region[1]:placar_region[3], placar_region[0]:placar_region[2]]

    # Divide a região do placar em duas partes (time 1 e time 2)
    height = cropped.shape[0]
    time1_region = cropped[0:height // 2, :]  # Metade superior (time 1)
    time2_region = cropped[height // 2:, :]   # Metade inferior (time 2)

    # Pré-processamento para OCR
    def preprocess(region):
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        resized = cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        return resized

    # Extrai os números para cada time
    config = r'--psm 7 -c tessedit_char_whitelist=0123456789'
    time1_text = pytesseract.image_to_string(preprocess(time1_region), config=config).strip()
    time2_text = pytesseract.image_to_string(preprocess(time2_region), config=config).strip()

    # Verifica se os números são válidos
    if time1_text.isdigit() and time2_text.isdigit():
        placar_atual = f"{time1_text}:{time2_text}"
        if validar_placar(placar_atual) and placar_atual != placar_anterior:
            placar_anterior = placar_atual
            return placar_atual
    return None

# Extração de frames e detecção de gols
def extrair_frames_e_detectar_gols(video_path):
    global fps
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    success, frame = video.read()
    frame_count = 0
    
    print("Processando frames e detectando gols...")
    
    while success:
        # Processa 1 frame por segundo
        if frame_count % int(fps) == 0:
            texto_placar = detectar_gol(frame)
            if texto_placar:
                timestamp = frame_count / fps
                print(f"Gol detectado no tempo {timestamp}s: {texto_placar}")
                timestamps.append((timestamp, texto_placar))  # Salva o tempo em segundos
            
        success, frame = video.read()
        frame_count += 1
    
    video.release()
    print("Processamento concluído!")
    return timestamps

# Detecção de eventos importantes no áudio
def detectar_eventos_audio(video_path):
    print(video_path)
    audio = AudioSegment.from_file(video_path, format="mp4")
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-27)
    audio_timestamps = [(start / 1000, end / 1000) for start, end in nonsilent_ranges]
    return audio_timestamps

# Cortar trechos do vídeo
def cortar_trechos(video_path, timestamps, output_folder):
    print("Cortando trechos do vídeo...")
    clip = VideoFileClip(video_path)
    
    for i, (timestamp, placar) in enumerate(timestamps):
        start = max(0, timestamp - 5)  # 5 segundos antes do gol
        end = min(clip.duration, timestamp + 5)  # 5 segundos depois do gol
        highlight = clip.subclip(start, end)
        highlight = highlight.set_audio(clip.audio.subclip(start, end))
        
        output_path = f"{output_folder}/highlight_{i + 1}.mp4"
        highlight.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"Trecho salvo: {output_path}")
    
    clip.close()

# Execução principal
if __name__ == "__main__":
    import os
    
    # Cria a pasta de highlights, se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 1. Extrair frames e detectar gols
    gols_detectados = extrair_frames_e_detectar_gols(video_path)
    print(f"Gols detectados: {gols_detectados}")
    

    # 2. Detectar eventos importantes no áudio
    eventos_audio = detectar_eventos_audio(video_path)
    print(f"Eventos de áudio detectados: {eventos_audio}")
    
    # 3. Combinar timestamps de gols e eventos de áudio
    todos_eventos = sorted(set(gols_detectados + eventos_audio))
    
    # 4. Cortar os trechos de vídeo
    if todos_eventos:
        cortar_trechos(video_path, todos_eventos, output_folder)
    else:
        print("Nenhum evento detectado.")
