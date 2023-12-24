import os
import json
from openai import AsyncOpenAI
import time
from dotenv import load_dotenv
import tiktoken
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import BaseTool

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_TEMP = 0
OPENAI_FUNCTION_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_FUNCTION_TEMP = 0

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
#  CORE Open AI Abstracted Methods
encoding_name = "cl100k_base"

# Helper functions

async def get_ada_embedding(text):
    text = text.replace("\n", " ")
    response = await client.embeddings.create(input=[text], model="text-embedding-ada-002")
    embedding = response.data[0].embedding
    return embedding


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


async def generate_text(system_role, prompt):
    print("runing generate text... in GPT.PY")

    start_time = time.time()

    new_message = [{"role": "system", "content": system_role},
                   {"role": "user", "content": prompt}]

    try:
        completion = await client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMP,
            messages=new_message
        )

        text = completion.choices[0].message.content

        end_time = time.time()
        print("Time taken to generate text in gpt function: ",
              end_time - start_time)
        return text
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return "An error occurred while generating a response."


async def generate_text_function(system_role, prompt, functions, function_name=None):
    print("running generate text function...")

    function_call = {
        "name": f"{function_name}"} if function_name is not None else "auto"

    new_message = [{"role": "system", "content": system_role},
                   {"role": "user", "content": prompt}]

    try:
        completion = await client.chat.completions.create(
            model=OPENAI_FUNCTION_MODEL,
            temperature=OPENAI_FUNCTION_TEMP,
            messages=new_message,
            functions=functions,
            function_call=function_call
        )

        completion_message = completion.choices[0].message

        function_call = getattr(completion_message, 'function_call', None)
        if function_call:
            function_name = getattr(function_call, 'name', None)
            function_args = json.loads(
                getattr(function_call, 'arguments', '{}'))

        return function_args
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None

#  SUMMARIZERS

def summary_with_objective(objective, content):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    extract specifics of the most pertinent information in extreme detail for the objectve: ' {objective} ' :
    "{text}"
    INFO:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=False
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output

