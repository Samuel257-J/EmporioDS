import os
import sys
from pathlib import Path
from PIL import Image, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Caminho temporário no executável PyInstaller
    except AttributeError:
        base_path = Path(__file__).parent  # Caminho local no VSCode
    return os.path.join(base_path, relative_path)

def carregar_imagem_tk(nome_arquivo, tamanho=None):
    caminho = resource_path(os.path.join("ImagensProjeto", nome_arquivo))
    imagem = Image.open(caminho)
    if tamanho:
        imagem = imagem.resize(tamanho)
    return ImageTk.PhotoImage(imagem)