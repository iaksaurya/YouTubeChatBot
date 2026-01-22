from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled,NoTranscriptFound

def fetch_and_save_transcripts(video_id, file_path="transcripts.txt"):
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id,languages=['en'])

        # Convert transcript to plain text
        transcripts = " ".join(chunk.text for chunk in transcript_list)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(transcripts)

        return transcripts  # return text for Streamlit UI

    except TranscriptsDisabled:
        print(f"Transcript disabled for video {video_id}.")
        return None
    except NoTranscriptFound:
        print(f"No transcript found for video {video_id}.")
        return None
    except Exception as e:
        print(f"Error fetching transcript for video {video_id}: {e}")
        return None