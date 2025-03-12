import os
from dotenv import load_dotenv

# Load environment variables from .env file
try:
    load_dotenv()

    # Access the keys
    serper_api_key = os.getenv("SERPER_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not serper_api_key or not openai_api_key:
        raise ValueError("API keys not found in .env file.")
except FileNotFoundError:
    print("Error: .env file not found.")
    # Handle the error, e.g., exit the program or use default values
except ValueError as e:
    print(f"Error: {e}")
    # handle the error.
except Exception as e:
    print(f"An unexpected error occured during api key loading: {e}")
    
    

from crewai import Agent,Task,Process,Crew
from crewai_tools import SerperDevTool

search_tool = SerperDevTool() #SerperDevTool is used to perform online searches by agents

# Agents

search_agent = Agent(
    role = "Senior Researcher",
    goal= "Uncover grounbreaking technologies in {topic}",
    verbose= True,
    memory = True,
    backstory=(
        "Driven by curiosity, you are at the forefront of innovation"
        "eager to explore and share knowledge that could change the world"
    ),
    tools=[search_tool],
    allow_delegation=True
)

writer_agent = Agent(
    role = "Blog Writer",
    goal= "Narate compelling stories on {topic}",
    verbose= True,
    memory = True,
    backstory=(
        "You are a talented educational writer with expertise in creating clear, engaging"
    "content. You have a gift for explaining complex concepts in accessible language"
    "and organizing information in a way that helps readers build their understanding."
    ),
    tools=[search_tool],
    allow_delegation=False
)

# Tasks

# Research Task
research_task = Task(
    description=(
    "Identify the video {topic}."
    "Get detailed information about the video from the channel."
    ),
    expected_output='A comprehensive 3 paragraphs long report based on the {topic} of video content.',
    tools=[search_tool],
    agent=search_agent,
)

# Writing task 
write_task = Task(
    description=(
    "get the info from the youtube channel on the topic {topic}."
        ),
    expected_output='Summarize the info from the youtube channel video on the topic{topic}',
    tool=[search_tool],
    agent=writer_agent,
    async_execution=False,
    output_file='new-blog-post.md'  # Example of output customization
)

# Crew 
crew = Crew(
    agents=[search_agent, writer_agent],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Optional: Sequential task execution is default ensures that the tasks are executed in a specific order.
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Starting the task execution process(crew kickoff with input parameters) with enhanced feedback
result = crew.kickoff(inputs={'topic': 'AI vs ML VS DL VS Data Science'})
print(result)

# we have our ouput printed as well as saved in file new-blog-post.md