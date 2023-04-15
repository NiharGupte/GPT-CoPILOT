import os

os.environ["OPENAI_API_KEY"] = "" # Enter API
os.environ["SERPAPI_API_KEY"] = "" # Enter API
os.environ["LANGCHAIN_HANDLER"] = "langchain"

from langchain.agents import load_tools
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


tool_names = ["human", "python_repl", "serpapi", "requests_all", "terminal"]
tools = load_tools(tool_names)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm=ChatOpenAI(temperature=0)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

# template="You are a helpful assistant that generates python selenium scripts to automate the given task."
# system_message_prompt = SystemMessagePromptTemplate.from_template(template)
# human_template="{text}"
# human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
#
# chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
#
# # get a chat completion from the formatted messages
# chat_prompt.format_prompt(text="Find me a video of Virat Kohli playing a cover drive").to_messages()

Main_Prompt = "You are a helpful AI assistant that takes query from user and generates and executes python selenium script to automate the task in a Chrome Browser, but use this code to initialize the driver. (driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())))"
#Secondary_Prompt = "Now generate and execute a python selenium script for the following task in the same chrome browser that was opened just now. Task : "
x = input(">")
x = Main_Prompt + " Query : " + x
y = agent_chain.run(x)
print("Response : ", y)
while True:
    x = input(">")
    x = Main_Prompt + " Query : " + x
    agent_chain.run(input=x)