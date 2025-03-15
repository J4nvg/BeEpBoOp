from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)


# Initialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant that translates Dutch PC-component specifications to their commonly used English words.
            I need to clean my dataset from a Dutch PC Hardware store. Try to keep the text short.
            Return the result as a single string with the translations separated by '||' (in the order: col1, col2).
            """,
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm

def translate(col1, col2):
    input_data = (
        f"col1: {col1}\n"
        f"col2: {col2}\n"
    )
    response = chain.invoke({"input": input_data})
    return response.content

output = translate("Koeling", "TBW-classificatie")
print("Single String Translation Output:")
print(output)

translations = output.split("||")
print("\nExtracted Translations:")
print("Column 1:", translations[0].strip())
print("Column 2:", translations[1].strip())
