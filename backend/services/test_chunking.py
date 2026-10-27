from backend.services.transcript_service import TranscriptService
from backend.services.chunking_service import ChunkingService


def main():

    video_id = "E3oG313_kps"

    # Get transcript
    transcript_service = TranscriptService()
    transcript = transcript_service.get_transcript(video_id)

    print(f"\nOriginal transcript segments: {len(transcript)}")

    # Chunk transcript
    chunking_service = ChunkingService()

    chunks = chunking_service.chunk_transcript(
        transcript,
        max_words=150
    )

    print(f"Generated chunks: {len(chunks)}")

    # Show first chunk
    first_chunk = chunks[0]

    print("\nFIRST CHUNK:")
    print("-" * 60)
    print("Start time:", first_chunk["start_time"])
    print("End time:", first_chunk["end_time"])
    print("\nText:")
    print(first_chunk["text"])
    print("-" * 60)

    # Show last chunk info
    last_chunk = chunks[-1]

    print("\nLAST CHUNK:")
    print("Start time:", last_chunk["start_time"])
    print("End time:", last_chunk["end_time"])


if __name__ == "__main__":
    main()