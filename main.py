from agents import vilma
from agno.media import Image
import os
from natsort import natsorted


caminho_da_pasta = 'mnist_images'

lista_de_imagens = []

nomes_dos_arquivos = natsorted([f for f in os.listdir(caminho_da_pasta) if f.endswith(('.png', '.jpg', '.jpeg'))])
print(nomes_dos_arquivos)

for nome_do_arquivo in nomes_dos_arquivos:
    caminho_completo = os.path.join(caminho_da_pasta, nome_do_arquivo)
    imagem = Image(filepath=caminho_completo)
    if imagem is not None:
        lista_de_imagens.append(imagem)
print(len(lista_de_imagens))
questions = [
                "Each one of the images has a number. Count how many times each number appears"
            ]

vilma.print_response(input=questions, images=lista_de_imagens)
