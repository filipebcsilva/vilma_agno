from agents import analista,leitor,AnalistaInput,vilma
from agno.media import Image
import os
from natsort import natsorted


caminho_da_pasta = 'imagens'

lista_de_imagens = []

nomes_dos_arquivos = natsorted([f for f in os.listdir(caminho_da_pasta) if f.endswith(('.png', '.jpg', '.jpeg'))])
print(nomes_dos_arquivos)
for nome_do_arquivo in nomes_dos_arquivos:
    caminho_completo = os.path.join(caminho_da_pasta, nome_do_arquivo)
    imagem = Image(filepath=caminho_completo)
    if imagem is not None:
        lista_de_imagens.append(imagem)

questions = ["Quantas imagens tem mais de pessoas 5 e me diga quais são",
                 "Quantas imagens estão em um ambiente de natureza",
                 "Qual é a média de pessoas por imagem",
                 "Qual é a média de carros por imagem"
            ]

vilma.print_response(input=questions, images=lista_de_imagens)
