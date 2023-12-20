import os
import json
import yaml
from dotenv import load_dotenv
import aiohttp
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

load_dotenv()
browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serp_api_key = os.getenv("SERP_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

async def scrape_website(objective: str, url: str):
    #scrape website, and also will summarize the content based on objective if the content is too large
    #objective is the original objective & task that user give to the agent, url is the url of the website to be scraped

    print("Scraping website...")
    # Define the headers for the request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    # Define the data to be sent in the request
    data = {
        "url": url        
    }

    # Convert Python object to JSON string
    data_json = json.dumps(data)

    # Send the POST request
    response = requests.post(f"https://chrome.browserless.io/content?token={browserless_api_key}", headers=headers, data=data_json)
    
    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        # print("CONTENTTTTTT:", text)
        if len(text) > 10000:
            output = summary(objective,text)
            return output
        else:
            return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")        


def search_youtube(query, number_of_results=5):
    video_ids = []
    try:
        response = requests.get('https://serpapi.com/search.json', params={
            'engine': 'youtube',
            'search_query': query,
            'api_key': serp_api_key,
        })

        if response.status_code != 200:
            raise Exception(f"HTTP error occurred: {response.status_code}")

        data = response.json()
        # # Extract video IDs from the results
        # for result in data.get('movie_results', [])[:number_of_results]:
        #     video_url = result.get('link')
        #     video_id = video_url.split('watch?v=')[-1]
        #     video_ids.append(video_id)

    except Exception as err:
        print(f"An error occurred: {err}")

    return data

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join(segment['text'] for segment in transcript)
        return full_transcript
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None

def search_google(query):    
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print("RESPONSE:", response.text)
    return response.text

async def search_google_scholar(session, query):
    try:
        async with session.get('https://serpapi.com/search.json', params={
            'engine': 'google_scholar',
            'q': query,
            'api_key': serp_api_key,
        }) as response:

            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    response.status, message=f"HTTP error occurred: {response.status}")

            results = await response.json()
            organic_results = results.get("organic_results", [])
            return organic_results

    except aiohttp.ClientResponseError as err:
        print(err)
    except Exception as err:
        print(f"An error occurred: {err}")
        return []


#  Summary
def summary(objective, content):
    llm = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size = 10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "objective"])
    
    summary_chain = load_summarize_chain(
        llm=llm, 
        chain_type='map_reduce',
        map_prompt = map_prompt_template,
        combine_prompt = map_prompt_template,
        verbose = False
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output

if __name__ == "__main__":
    async def main():
        url = "https://scholar.google.com/citations?user=JCvWfDQAAAAJ&hl=en&oi=sra"
        objective = "find quantum computer components"
        async with aiohttp.ClientSession() as session:
            scraped_content = await scrape_website(objective, url)
            print(scraped_content)

    import asyncio
    asyncio.run(main())
