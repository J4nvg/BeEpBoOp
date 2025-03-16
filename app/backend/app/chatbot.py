import os
from dotenv import load_dotenv
import openai
from openai import AssistantEventHandler
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI  as LLMOpenAI  # renamed for clarity
import sqlite3

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Create a new conversation thread (once)
thread = openai.beta.threads.create()

# Retrieve your assistant by its ID using retrieve()
assistant = openai.beta.assistants.retrieve("asst_N6pOdHNreq2yVJjJvR6JbNE9")

# ---------------------
# Define the Streaming Event Handler (printing version)
# ---------------------
class MyEventHandler(AssistantEventHandler):
    def on_text_created(self, text) -> None:
        print("\nassistant > ", end="", flush=True)
      
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
      
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant (tool call: {tool_call.type})", flush=True)
  
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print("\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

# ---------------------
# Define a Capturing Event Handler (for FastAPI responses)
# ---------------------
class CaptureEventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()  # Initialize the base class attributes
        self.result = ""
    
    def on_text_created(self, text) -> None:
        self.result += "\n "
      
    def on_text_delta(self, delta, snapshot):
        self.result += delta.value
      
    def on_tool_call_created(self, tool_call):
        self.result += f"\nassistant (tool call: {tool_call.type})"
  
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                self.result += delta.code_interpreter.input
            if delta.code_interpreter.outputs:
                self.result += "\n\noutput >"
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        self.result += f"\n{output.logs}"

# ---------------------
# Chatbot Functions
# ---------------------
def run_initial_welcome() -> str:
    """Run the initial welcome instructions and return the output captured."""
    handler = CaptureEventHandler()
    with openai.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=(
            "Please start the conversation by greeting the user. "
            "Introduce yourself as Tecco and explain that you are a technical assistant who helps users build personal computers "
            "by providing component recommendations. Make sure not to return Markdown language."
        ),
        event_handler=handler,
    ) as stream:
        stream.until_done()
    return handler.result

def get_last_assistant_message() -> str:
    """Retrieve the content of the latest assistant message from the thread."""
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    assistant_msgs = [msg for msg in messages if msg.role == "assistant"]
    if assistant_msgs:
        return assistant_msgs[-1].content or ""
    return ""

# ---------------------
# LangChain SQL Query Integration
# ---------------------
def sql_query_tool(query: str) -> str:
    try:
        conn = sqlite3.connect("components.db")
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        if rows:
            return "\n".join(str(row) for row in rows)
        else:
            return "No matching components found."
    except Exception as e:
        return f"Error executing query: {e}"

# Wrap the SQL query tool as a LangChain Tool
sql_tool = Tool(
    name="SQLQuery",
    func=sql_query_tool,
    description=(
        "Use this tool to query the SQL database for PC components from a table called 'components'. "
        "The table has columns such as 'type', 'model', and 'specs'. "
        "Input should be a valid SQL SELECT statement."
    )
)

llm = LLMOpenAI(temperature=0)
agent = initialize_agent([sql_tool], llm, agent="zero-shot-react-description", verbose=True)

def run_sql_query(requirements: str) -> str:
    prompt = (
        "Based on the following suggested components, generate a SQL query that selects all matching PC components "
        "from a table called 'components'. The table has columns such as 'type', 'model', and 'specs'. "
        f"Components: {requirements}"
    )
    sql_query = agent.run(prompt)
    return sql_query

def process_message(user_input: str) -> str:
    """
    Process a single user message and return the assistant's response as a string.
    Handles SQL queries if the message starts with 'query:'.
    """
    # Handle SQL query requests:
    if user_input.strip().lower().startswith("query:"):
        extra = user_input.strip()[len("query:"):].strip()
        if extra:
            requirements = extra
        else:
            requirements = get_last_assistant_message()
        generated_query = run_sql_query(requirements)
        query_result = sql_query_tool(generated_query)
        # Log the SQL query and its result in the conversation thread:
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="assistant",
            content=f"SQL Query: {generated_query}\nResults:\n{query_result}"
        )
        return f"SQL Query: {generated_query}\nResults:\n{query_result}"
    
    # Otherwise, treat as a normal chat message:
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )
    
    handler = CaptureEventHandler()
    with openai.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=(
            "You are a knowledgeable technical assistant that helps users build personal computers. "
            "Gather the user's requirements and provide helpful recommendations."
        ),
        event_handler=handler,
    ) as stream:
        stream.until_done()
    
    return handler.result