import eel
import os

os.environ["OPENAI_API_KEY"] = "" # Enter your api key for openai
os.environ["SERPAPI_API_KEY"] = "" # Enter your api key for serpapi
os.environ["LANGCHAIN_HANDLER"] = "langchain"

from langchain.agents import load_tools
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType

tool_names = ["human", "python_repl", "serpapi", "requests_all", "terminal"]
tools = load_tools(tool_names)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm=ChatOpenAI(temperature=0)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

Main_Prompt = "You are a helpful AI assistant that takes query from user and generates and executes python selenium script to automate the task in a Chrome Browser, but use this code to initialize the driver. (driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())))"
Secondary_Prompt = "Now generate and execute a python selenium script for the following task in the same chrome browser that was opened just now. Task : "
idx = 0
# Set web files folder and optionally specify which file types to check for
eel.init('.', allowed_extensions=['.js', '.html', '.css'])

@eel.expose  # Expose this function to Javascript
def process_input(input_string):
    global idx
    if idx==0:
        x = Main_Prompt + " Query : " + input_string
        y = agent_chain.run(x)
        idx += 1
    else:
        x = Secondary_Prompt + input_string
        y = agent_chain.run(x)
    input_string = y
    return input_string

# Start the app with a size and title
eel.start('index.html', size=(400, 400), title='Chat GUI')
