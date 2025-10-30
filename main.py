from agents import vilma
from workflow import vilma_workflow
from agno.media import Image
import os
from natsort import natsorted


caminho_da_pasta = 'imagens'

lista_de_imagens = []

nomes_dos_arquivos = natsorted([f for f in os.listdir(caminho_da_pasta) if f.endswith(('.png', '.jpg', '.jpeg'))])

for nome_do_arquivo in nomes_dos_arquivos:
    caminho_completo = os.path.join(caminho_da_pasta, nome_do_arquivo)
    imagem = Image(filepath=caminho_completo)
    if imagem is not None:
        lista_de_imagens.append(imagem)

questions = [
                "Quants pessoas tem por imagem"
            ]

vilma.print_response(input=questions,images=lista_de_imagens)
