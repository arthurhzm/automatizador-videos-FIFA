import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = r'frames/frame_5400.jpg' 
image = cv2.imread(image_path)

# Desenhar um círculo no ponto (0, 0)
cv2.circle(image, (0, 0), 5, (0, 255, 0), -1)

# Pré-processamento
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
blur = cv2.GaussianBlur(gray, (5, 5), 0)  
_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  
resized = cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

config = r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ: '

# Extrair texto
texto = pytesseract.image_to_string(resized, config=config)

file_path = f"frames/teste.jpg"
cv2.imwrite(file_path, resized)

# Mostrar a imagem processada para conferência
cv2.imshow('Imagem Processada', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Resultado
print("Texto extraído:")
print(texto)