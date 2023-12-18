import aiohttp
from agent_tools import search_youtube_video_ids, get_youtube_transcript
from gpt import generate_text

async def fetch_trending_videos(keyword):
    async with aiohttp.ClientSession() as session:
       video_ids =  search_youtube_video_ids(session, keyword)
    return video_ids

async def transcribe_videos(video_ids):
    # Transcribe videos and return transcripts
    transcripts = {}
    for video_id in video_ids:
        transcript = await get_youtube_transcript(video_id)
        transcripts[video_id] = transcript
    return transcripts

async def extract_insight(text):
    system_role = " you are an expert researcher... extract key insights from the text"
    prompt = f"Extract key insights from the following text: {text}"
    insight = await generate_text(prompt, system_role)
    return insight

async def extract_insights(transcripts):
    # Extract insights from transcripts
    insights = []
    for transcript in transcripts.items():
        insight = await extract_insight(transcript)
        insights.append(insight)
    return insights

async def analyze_common_themes(text):
    system_role = " you are an expert researcher... t"
    prompt = f"Analyze and describe common themes from the following text: {text}"
    common_themes = await generate_text(prompt, system_role)
    return common_themes

async def find_content_gap(common_themes):
    system_role = " you are an expert researcher... t"
    prompt = f"Find the gap in content from the following themes: {common_themes}"
    gap_in_content = await generate_text(prompt, system_role)
    return gap_in_content

def find_unique_angle(insights):
    # Analyze insights and determine a unique angle for a new video
    # Pass all insights as an array to analyze_common_themes
    common_themes = analyze_common_themes(insights)
    gap_in_content = find_content_gap(common_themes)
    
    return unique_angle

def create_video_script(unique_angle):
    # Create a script for the new video
    script = generate_script_based_on_angle(unique_angle)
    return script

def main():
    keyword = "your_keyword_here"
    video_ids = fetch_trending_videos(keyword)
    transcripts = transcribe_videos(video_ids)
    insights = extract_insights(transcripts)
    unique_angle = find_unique_angle(insights)
    new_video_script = create_video_script(unique_angle)
    # Additional steps to produce and publish the video

if __name__ == "__main__":
    main()
