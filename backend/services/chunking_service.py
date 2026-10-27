class ChunkingService:

    def chunk_transcript(
        self,
        transcript_segments,
        max_words=150
    ):
        chunks = []

        current_chunk = []
        current_word_count = 0
        chunk_start = None
        chunk_end = None

        for segment in transcript_segments:

            text = segment["text"]
            words = text.split()

            # Set chunk start time
            if chunk_start is None:
                chunk_start = segment["start"]

            current_chunk.append(text)
            current_word_count += len(words)

            # Update chunk end time
            chunk_end = (
                segment["start"] +
                segment["duration"]
            )

            # Create chunk once word limit is reached
            if current_word_count >= max_words:

                chunks.append({
                    "text": " ".join(current_chunk),
                    "start_time": chunk_start,
                    "end_time": chunk_end
                })

                # Reset for next chunk
                current_chunk = []
                current_word_count = 0
                chunk_start = None
                chunk_end = None

        # Add remaining text as final chunk
        if current_chunk:
            chunks.append({
                "text": " ".join(current_chunk),
                "start_time": chunk_start,
                "end_time": chunk_end
            })

        return chunks