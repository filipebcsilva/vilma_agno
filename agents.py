from agno.agent import Agent  
from typing import List
import json
from agno.models.google import Gemini
from agno.media import Image
import os
from pydantic import BaseModel,Field
from natsort import natsorted
from dotenv import load_dotenv 

load_dotenv()

class dboutuput(BaseModel):
    answers: dict= Field(...,
                               description="Um dicionario que tem como key a o nome da Imagem e como value cada uma das perguntas,e dentro de cada pergunta a resposta correpondente",
                               )
    
    
model = Gemini(id = "gemini-2.5-flash",provider= "gemini",api_key = os.getenv("GEMINI_API_KEY"))

leitor = Agent(
    model = model,
    name = "Leitor de imagem",
    description= "Você é um agente IA especialista em analisar e extrair informações de imagens",
    instructions= """
            Dado uma lista de imagens de entrada e uma  lista de perguntas do usuario,realize a seguinte ação para todas as imagens:
            Responda a sequência de perguntas individualmente para cada imagem de maneira direta, por exemplo:
            Exemplo:
            -Pergunta: Quantas pessoas tem na imagem
            -Resposta: 3
            Se a pergunta for sobre o contexto ou tema do ambiente, analise e responde:
            -Urbano para imagens  em que o foco principal seja cidades com carros,ruas,estradas,prédios etc.
            -Natureza para imagens relacionadas a natureza, campo,vegetação etc
            Instruções para o output_schema:
            -Não repita a pergunta do usuario mais de uma vez!
            -O nome das imagens dever se algo do tipo "Imagem1"
    """,
    output_schema= dboutuput,
    use_json_mode=True,
    debug_mode= True,
    
)

caminho_da_pasta = 'imagens'

lista_de_imagens = []

nomes_dos_arquivos = natsorted([f for f in os.listdir(caminho_da_pasta) if f.endswith(('.png', '.jpg', '.jpeg'))])
print(nomes_dos_arquivos)
for nome_do_arquivo in nomes_dos_arquivos:
    caminho_completo = os.path.join(caminho_da_pasta, nome_do_arquivo)
    imagem = Image(filepath=caminho_completo)
    if imagem is not None:
        lista_de_imagens.append(imagem)

input = ["Quantos carros tem na imagem","Qual é o ambiente da imagem","Quantas pessoas tem na imagem"]


run_output = leitor.run(input=input,images=lista_de_imagens)
print(run_output.content)