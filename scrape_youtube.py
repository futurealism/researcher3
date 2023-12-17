from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

video_id = 'FWO9OJUeouE'
# retrieve the available transcripts
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Concatenate all the text entries into one transcript
full_transcript = ' '.join(segment['text'] for segment in transcript)

# If you still want to format the transcript as JSON and save it, you can do so
formatter = JSONFormatter()
json_formatted = formatter.format_transcript(transcript)

# Now you have the full transcript as a single string in full_transcript
# And you also have the JSON formatted transcript in json_formatted

# You can print the full transcript
print(full_transcript)

# And if you want to write the JSON formatted transcript to a file named after the video_id, you can do that as well
with open(f'{video_id}.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_formatted)