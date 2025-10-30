from agno.agent import Agent
from agno.workflow import Workflow,Step
from agno.workflow.types import StepInput, StepOutput
from typing import List
from agno.models.google import Gemini
from agno.tools.python import PythonTools
from agno.models.ollama import Ollama
from agno.agent import Agent
from agno.media import Image
import os
import base64
from natsort import natsorted
from pydantic import BaseModel,Field
from dotenv import load_dotenv 

load_dotenv()


def analista_step(step_input: StepInput) -> StepOutput:
    questions = step_input.input
    image_data = step_input.get_last_step_content()
    answer = f"""
    {image_data}
    {questions}
    """
    return StepOutput(content=answer)
def leitor_step(step_input: StepInput) -> StepOutput:
    return step_input.get_last_step_content()
    
    

##Define o estilo de saída do leitor##
class LeitorOutuput(BaseModel):
    answers: dict= Field(...,
                               description="A dictionary that has the name of the image as its key and each of the questions as its value, and within each question the corresponding answer",
                        )

##Define o estilo de saída do gerador de perguntas##   
class GeradorOutput(BaseModel):
    dados: List[str] = Field(...,
                             description= "A list of relevant information that should be extracted from the images"
                             )


vision_model = Gemini(id = "gemini-2.5-flash",provider= "gemini",api_key = os.getenv("GEMINI_API_KEY"))
text_model = Ollama(id = "llama3.1:8b")

#Agente que recebe a lista de perguntas do usuario e faz uma analíse para descobrir quais|# 
#são as informações relevantes a serem extraídas da imagem.#
#O nome está ruim, vou trocar depois.#

gerador_perguntas = Agent(
    model = vision_model,
    name = "Question generator",
    description= "You are an AI agent that specializes in deciding what to extract from an image based on a series of questions.",
    instructions= """
            Given a list of user questions, create a list of information to extract from all the images.
            For each one of the question, you MUST give only one information.
            For example:
            INPUT: How many buildings are visible in the image.
            OUTPUT: Number of buildings.
    """,
    output_schema= GeradorOutput,
    debug_mode= True,
)

#Agente que le as imagens e gera um dicionario contendo as informações das imagens# 
#No estilo: "Imagem1": {                                                                                                                                                                    
#         "Quantidade de pessoas": 7,                                                                                                                                                   
#        "Ambiente de natureza": false,                                                                                                                                                
#        "Quantidade de carros": 3,                                                                                                                                                    
#       "Cor predominante": "Cinza"                                                                                                                                                   
#     },   

leitor = Agent(
    model = vision_model,
    name = "Image reader",
    description= "You are an AI agent specialized in analyzing and extracting information from images",
    instructions= """
        Given a list of input images and a list of information that must be extracted from the images, perform the following action for all images:
        Answer the sequence of questions individually for each image directly, for example:
        Example:
        -Question: How many buildings are in the image?
        -Answer: 8
        Don't give ambiguous answers. If in doubt, choose only one direct answer.
        Instructions for output_schema:
        -Don't repeat the user's question more than once!
        -The name of the image must be something like Image1, Image2...
    """,
    output_schema= LeitorOutuput,
    use_json_mode= True,
    debug_mode= True,
)

#Agente que analisa o dicionario fornecido pelo leitor e responde as perguntas do usuario#
#Equipado com uma calculadora para calculos matematicos como média#
analista = Agent(
    model = vision_model,
    name = "Data Analyst",
    description= "You are an AI agent specialized in analyzing and performing operations on data in dictionary format.",
    instructions= """
        Given the dictionary provided by the Image Reader, which contains keys with the image names and values ​​with the questions followed by the
        answers about each image, write a python code that can respond to the user's input according to the data provided.
        The dictionary will be, for example, in the form:
        'Image1': {'How many buildings are in the image': 2}
        'Image2': {'How many animals are in the image': 6}
        and so on...
        You must use the python tool to generate and run a code that can use the dictionary to answer the user's questions.
    """,
    tools = [PythonTools()],
    debug_mode= True,
)

vilma_workflow = Workflow(
    name = "vilma workflow",
    description= "Automated data extraction from images",
    steps=[
        Step(name = "gerador",agent = gerador_perguntas),
        Step(name = "get_images",executor = leitor_step),
        Step(name = "leitor",agent = leitor),
        Step(name = "retrive_information",executor = analista_step),
        Step(name = "analista",agent = analista)
        ],
    debug_mode = True,
)



caminho_da_pasta = 'imagens'

lista_de_imagens = []

nomes_dos_arquivos = natsorted([f for f in os.listdir(caminho_da_pasta) if f.endswith(('.png', '.jpg', '.jpeg'))])

for nome_do_arquivo in nomes_dos_arquivos:
    caminho_completo = os.path.join(caminho_da_pasta, nome_do_arquivo)
    with open(caminho_completo, 'rb') as f:
        image_bytes = f.read()
    
    # --- ESTA É A NOVA MUDANÇA ---
    
    # 2. Codificar os bytes brutos para Base64
    base64_bytes = base64.b64encode(image_bytes)
    
    # 3. Decodificar os bytes Base64 para uma string UTF-8 (texto)
    base64_string = base64_bytes.decode('utf-8')
    
    # 4. Passar a STRING Base64 para o argumento 'content'
    imagem = Image(content=base64_string)
    
    lista_de_imagens.append(imagem)
    break
lista_de_imagens = [Image(url= "https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg")]
questions = [
                "Quants pessoas tem por imagem"
            ]

    
vilma_workflow.run(
    input=questions,images=lista_de_imagens
)
