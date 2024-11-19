# Projeto de Detecção de Melhores Momentos em Partidas de FIFA

Este projeto tem como objetivo analisar um vídeo de uma partida de FIFA, detectar eventos importantes (como gols) e gerar trechos de vídeo com os melhores momentos da partida. É importante que o vídeo tenha sons do narrador e da torcida bem audíveis para uma melhor detecção dos eventos.

## Bibliotecas Necessárias

Para rodar este projeto, você precisará das seguintes bibliotecas:

- `cv2` (OpenCV): Utilizada para manipulação de imagens e vídeos.
- `pytesseract`: Utilizada para reconhecimento óptico de caracteres (OCR) a partir de imagens.
- `moviepy`: Utilizada para manipulação e edição de vídeos.
- `pydub`: Utilizada para manipulação de arquivos de áudio.
- `pydub.silence`: Utilizada para detecção de silêncio em arquivos de áudio.

## Configuração do Tesseract

Certifique-se de ter o Tesseract OCR instalado em seu sistema. Você pode baixar o Tesseract [aqui](https://github.com/tesseract-ocr/tesseract). Após a instalação, configure o caminho do executável do Tesseract no código:

```python
# Configuração do Tesseract
# Aqui você deve trocar pelo caminho onde o Tesseract está instalado
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Caminho do vídeo
# Aqui você deve trocar pelo caminho do vídeo que você quer analisar
video_path = r"C:\Users\arthu\Videos\2024-11-17 17-51-10.mp4"
```

As variáveis dos caminhos estão especificadas nas linhas 7 e 11 do arquivo integracao.py.
