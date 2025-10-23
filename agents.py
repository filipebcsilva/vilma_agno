from agno.agent import Agent
from agno.team import Team
from typing import List
from agno.models.google import Gemini
from agno.models.ollama import Ollama
from agno.agent import Agent
from agno.tools.calculator import CalculatorTools
import os
from pydantic import BaseModel,Field
from dotenv import load_dotenv 

load_dotenv()

##Define o estilo de saída do leitor##
class LeitorOutuput(BaseModel):
    answers: dict= Field(...,
                               description="A dictionary that has the name of the image as its key and each of the questions as its value, and within each question the corresponding answer",
                        )

##Define o estilo de saída do gerador de perguntas##   
class GeradorOutput(BaseModel):
    dados: List[str] = Field(...,
                             description= "A list of relevant information that should be extracted from the images")


# model = Gemini(id = "gemini-2.5-flash",provider= "gemini",api_key = os.getenv("GEMINI_API_KEY"))
model = Ollama(id = "mistral-small3.2:24b")


#Agente que recebe a lista de perguntas do usuario e faz uma analíse para descobrir quais|# 
#são as informações relevantes a serem extraídas da imagem.#
#O nome está ruim, vou trocar depois.#
gerador_perguntas = Agent(
    model = model,
    name = "Question generator",
    description= "You are an AI agent that specializes in deciding what to extract from an image based on a series of questions.",
    instructions= """
            Given a list of user questions, create a list of information to extract from each image.
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
    model = model,
    name = "Image reader",
    description= "You are an AI agent specialized in analyzing and extracting information from images",
    instructions= """
        Given a list of input images and a list of questions, perform the following action for all images:
        Answer the sequence of questions individually for each image directly, for example:
        Example:
        -Question: How many buildings are in the image?
        -Answer: 8
        Don't give ambiguous answers. If in doubt, choose only one direct answer.
        Instructions for output_schema:
        -Don't repeat the user's question more than once!
    """,
    output_schema= LeitorOutuput,
    use_json_mode= True,
    debug_mode= True,
)

#Agente que analisa o dicionario fornecido pelo leitor e responde as perguntas do usuario#
#Equipado com uma calculadora para calculos matematicos como média#
analista = Agent(
    model = model,
    name = "Data Analyst",
    description= "You are an AI agent specialized in analyzing and performing operations on data in dictionary format.",
    instructions= """
        Given the dictionary provided by the Image Reader, which contains keys with the image names and values ​​with the questions followed by the
        answers about each image, respond to the user's input according to the data provided.
        The dictionary will be, for example, in the form:
        'Image1': {'How many buildings are in the image': 2}
        'Image2': {'How many animals are in the image': 6}
        and so on...
        You will be equipped with a calculator for cases involving more complex mathematical operations such as mean, standard deviation, etc..
    """,
    tools = [CalculatorTools()],
    debug_mode= True,
)

#Time contendo os agentes e é basicamente o orquestrador de tudo#
#Ele é responsável por designar as tarefas, fazer as chamadas dos agentes e etc#
vilma = Team(
    name = "vilma",
    members=[gerador_perguntas,leitor,analista],
    model=model,
    description= """You are the head of an image data extraction and analysis system. 
    Your job is to use the Image Reader member to extract the data and then use the Data Analyst agent to answer user questions..
    """,
    instructions = """
        Follow these steps:
        1 - Read the user's questions and send them to the Question Generator to discover the relevant information to be extracted from the images.
        2 - Given the list generated by the Question Generator, send the generated list to the Image Reader so it can extract the information from the images and generate a dictionary with the information.
        3 - With the extracted data, send the dictionary generated by the Image Reader and the user's input questions to the Data Analyst.
        4 - Use the Data Analyst to answer the user's questions.
        Remember to send the images only to the Image Reader; it is not necessary for the other agents to receive them.
    """,
    debug_mode= True,
)
