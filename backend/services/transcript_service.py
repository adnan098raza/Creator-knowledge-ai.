from youtube_transcript_api import YouTubeTranscriptApi


class TranscriptService:

    def get_transcript(self, video_id: str):

        transcript = YouTubeTranscriptApi().fetch(
    video_id,
    languages=["hi"]
)

        transcript_data = []

        for item in transcript:
            transcript_data.append({
                "text": item.text,
                "start": item.start,
                "duration": item.duration
            })

        return transcript_data


if __name__ == "__main__":

    transcript_service = TranscriptService()

    video_id = "E3oG313_kps"

    transcript = transcript_service.get_transcript(video_id)

    print(f"\nTranscript segments: {len(transcript)}\n")

    print("First 5 segments:\n")

    for segment in transcript[:5]:
        print(segment)