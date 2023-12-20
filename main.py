import json
import aiohttp
from agent_tools import search_google_scholar, scrape_website
from gpt import generate_text

system_role = " you are a helpful ai assistant"



async def generate_research_plan(objective):
    system_role = """
      you are an expert researcher who takes in an objective and generates a 5 step research plan.
      you will be passing this list to an research agent who can search and scrape the internet, scholarly articles, youtube, twitter, and many other sources to complete the research.
      your answers should be formatted like a numbered list of steps.

      """
    prompt = f"Generate a research plan for the following objective: {objective}"
    research_plan = await generate_text(system_role, prompt)
    return research_plan






async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Exiting chat...")
                break
            # response = await generate_text(system_role, user_input)
            research_plan = await generate_research_plan(user_input)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
