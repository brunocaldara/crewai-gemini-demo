import os

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose=True,
                             temperature=0.5,
                             google_api_key=os.getenv("GOOGLE_API_KEY"))

search_tool = DuckDuckGoSearchRun()

search_agent = Agent(
    role="Pesquisador",
    goal="Pesquisar sobre as melhores matérias sobre o assunto {topic} no Brasil em 2024",
    backstory="Você é um pesquisador senior responsável por elaborar uma pesquisa sobre o tema abordado",
    allow_delegation=False,
    cache=True,
    verbose=True,
    tool=[search_tool],
    llm=llm
)

search_task = Task(
    description="Buscar as matérias mais importantes sobre {topic} no Brasil em 2024",
    expected_output="Uma lista enumerada com as matérias e o link mais relevantes matérias sobre o assunto pesquisado",
    agent=search_agent
)

crew = Crew(
    tasks=[search_task],
    agents=[search_agent],
    verbose=True,
    cache=True,
    process=Process.sequential
)

result = crew.kickoff(inputs={"topic": "Mercado de trabalho com Python"})
print(result)
