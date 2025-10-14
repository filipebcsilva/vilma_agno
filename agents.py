from agno.agent import Agent
from agno.team import Team
from typing import List
from agno.models.google import Gemini
from agno.tools.calculator import CalculatorTools
import os
from pydantic import BaseModel,Field
from dotenv import load_dotenv 

load_dotenv()

class LeitorOutuput(BaseModel):
    answers: dict= Field(...,
                               description="Um dicionario que tem como key o nome da Imagem e como value cada uma das perguntas,e dentro de cada pergunta a resposta correpondente",
                        )
    
class GeradorOutput(BaseModel):
    dados: List[str] = Field(...,
                             description= "Uma lista de informações relevantes que devem ser extraidos das imagens")


model = Gemini(id = "gemini-2.5-flash",provider= "gemini",api_key = os.getenv("GEMINI_API_KEY"))

gerador_perguntas = Agent(
    model = model,
    name = "Gerador de perguntas",
    description= "Você é um agente IA especialista em decidir o que deve ser extraido de uma imagem baseado em uma série de perguntas",
    instructions= """
            Dado uma lista de perguntas do usuario, crie uma lista de informações que devem ser extraídas de cada uma das imagens.
            Por exemplo:
            INPUT: Quantas imagens tem mais de 5 pessoas.
            OUTPUT: Quantidade de pessoas.
    """,
    output_schema= GeradorOutput,
    debug_mode= True,
)
leitor = Agent(
    model = model,
    name = "Leitor de imagem",
    description= "Você é um agente IA especialista em analisar e extrair informações de imagens",
    instructions= """
            Dado uma lista de imagens de entrada e uma lista de perguntas ,realize a seguinte ação para todas as imagens:
            Responda a sequência de perguntas individualmente para cada imagem de maneira direta, por exemplo:
            Exemplo:
            -Pergunta: Quantas pessoas tem na imagem
            -Resposta: 3
            Não de respostas ambíguas, caso esteja em dúvida,escolha apenas uma resposta direta
            Se a pergunta for sobre o contexto ou tema do ambiente, analise e responde:
            -Urbano para imagens  em que o foco principal seja cidades com carros,ruas,estradas,prédios etc.
            -Natureza para imagens relacionadas a natureza, campo,vegetação etc
            Instruções para o output_schema:
            -Não repita a pergunta do usuario mais de uma vez!
            -O nome das imagens dever se algo do tipo "Imagem1"
    """,
    output_schema= LeitorOutuput,
    use_json_mode= True,
    debug_mode= True,
)

analista = Agent(
    model = model,
    name = "Analista de dados",
    description= "Você é um agente IA especialista em analisar e fazer operações em dados no formato de um dicionario",
    instructions= """
            Dado o dicionario fornecido pelo Leitor de Imagens que contém keys com o nome das imagens e values com as perguntas seguido das 
            respostas sobre cada imagem,responda o input do usuario de acordo com os dados fornecidos.
            O dicionario virá,por exemplo, na forma:
            'Imagem1': {'Quantos carros tem na imagem': '2', 'Qual é o ambiente da imagem': 'Urbano', 'Quantas pessoas tem na imagem': '8'}, 
            'Imagem2': {'Quantos carros tem na imagem': '5', 'Qual é o ambiente da imagem': 'Urbano', 'Quantas pessoas tem na imagem': '2'}
            e assim por diante...
            Você será equipado com uma calculadora para casos envolvendo operações matemáticas mais complexas como média, desvio padrão,etc.
    """,
    tools = [CalculatorTools()],
    debug_mode= True,
)

vilma = Team(
        name = "vilma",
        members=[gerador_perguntas,leitor,analista],
        model=model,
        description= """Você é o chefe de um sistema de extração e analíse de dados de imagens.Seu trabalho é utilizar o membro Leitor de Imagem para extrair 
        os dados e em seguida usar o agente Analista de dados para responder as perguntas do usúario.
        """,
        instructions = """
        Siga os seguintes passos:
        1 - Leia as perguntas do usuario e mande para o Gerador de perguntas para descobrir quais são as informaçẽos relevantes a serem extraídas das imagens.
        2 - Dado a lista gerada pelo Gerador de perguntas, envie a mesma lista para o Leitor de Imagem para ele extrair as informações das imagens
        3 - Com os dados extraídos, envie o dicionario gerado pelo Leitor de Imagem e as perguntas do input do usuario para o Analista de dados.
        4 - Use o Analista de dados para responder as perguntas do usuario.
        """,
        debug_mode= True,
)
