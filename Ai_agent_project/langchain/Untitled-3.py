# %%
pip install wikipedia

# %%
!pip install langchain langchain-google-genai wikipedia python-dotenv


# %%
GOOGLE_API_KEY="AIzaSyBu1D85e2RDIdk-7xl2I7ThYD0PBoKom3k"


# %%
pip install -U langchain-community


# %%
import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun
from langchain_google_genai import ChatGoogleGenerativeAI


# %%
# Step 1: Import packages (assume you've done this already)
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun
from langchain.agents import Tool

# Step 2: Create the Wikipedia tool
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Step 3: Define the tool for the agent
tools = [
    Tool(
        name="wikipedia",
        func=wiki.run,
        description="Use this tool to answer general questions about people, places, or things using Wikipedia."
    )
]


# %%
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Ali Jawad\\Downloads\\gen-lang-client-0495743012-e8ae6ca249ba.json"


# %%
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-pro",  # No need to say "models/"
    temperature=0
)


# %%
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools,
    model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


# %%
question = "What is machine learning?"
response = agent.run(question)
print(response)


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%



