import os
import json
import yaml
from dotenv import load_dotenv
import aiohttp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

load_dotenv()

serp_api_key = os.getenv("SERP_API_KEY")

async def search_youtube_video_ids(session, query, number_of_results=5):
    video_ids = []
    try:
        async with session.get('https://serpapi.com/search.json', params={
            'engine': 'youtube',
            'search_query': query,
            'api_key': serp_api_key,
        }) as response:

            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    response.status, message=f"HTTP error occurred: {response.status}")

            data = await response.json()
            # Extract video IDs from the results
            for result in data.get('movie_results', [])[:number_of_results]:
                video_url = result.get('link')
                video_id = video_url.split('watch?v=')[-1]
                video_ids.append(video_id)

    except aiohttp.ClientResponseError as err:
        print(err)
    except Exception as err:
        print(f"An error occurred: {err}")

    return video_ids


async def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join(segment['text'] for segment in transcript)
        return full_transcript
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None
