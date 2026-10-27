import yt_dlp


class YouTubeService:

    def get_video_metadata(self, video_url: str):

        ydl_options = {
            "quiet": True,
            "no_warnings": True
        }

        with yt_dlp.YoutubeDL(ydl_options) as ydl:

            info = ydl.extract_info(
                video_url,
                download=False
            )

        return {
            "title": info.get("title"),
            "video_url": video_url,
            "duration_seconds": info.get("duration"),
            "channel": info.get("channel"),
            "channel_url": info.get("channel_url")
        }


if __name__ == "__main__":

    youtube_service = YouTubeService()

    video_url = "https://www.youtube.com/watch?v=E3oG313_kps"

    metadata = youtube_service.get_video_metadata(video_url)

    print("\nVIDEO METADATA:\n")

    for key, value in metadata.items():
        print(f"{key}: {value}")