from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from doucment_summarizer.rag_tool import RAGTool

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

@CrewBase
class DocumentSummarizer():
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def chunking_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chunking_agent'],
            tools=[RAGTool()],
            verbose=True
        )

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_agent'],
            verbose=True
        )

    @task
    def extract_chunks(self) -> Task:
        return Task(
            config=self.tasks_config['extract_chunks'],
        )

    @task
    def answer_query(self) -> Task:
        return Task(
            config=self.tasks_config['answer_query']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
