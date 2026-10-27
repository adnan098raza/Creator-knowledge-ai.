from backend.services.transcript_service import TranscriptService
from backend.services.chunking_service import ChunkingService
from backend.services.translation_service import TranslationService


def main():

    video_id = "E3oG313_kps"

    transcript = TranscriptService().get_transcript(video_id)

    chunks = ChunkingService().chunk_transcript(
        transcript,
        max_words=150
    )

    first_chunk = chunks[0]

    print("\nORIGINAL HINDI:")
    print("=" * 60)
    print(first_chunk["text"])

    translation_service = TranslationService()

    result = translation_service.translate_chunk(
        first_chunk["text"]
    )

    print("\nENGLISH:")
    print("=" * 60)
    print(result["english"])

    print("\nHINGLISH:")
    print("=" * 60)
    print(result["hinglish"])


if __name__ == "__main__":
    main()