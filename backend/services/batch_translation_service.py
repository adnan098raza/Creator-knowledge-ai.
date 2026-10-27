import json
import os
import time

from backend.services.transcript_service import TranscriptService
from backend.services.chunking_service import ChunkingService
from backend.services.translation_service import TranslationService


class BatchTranslationService:

    def __init__(self):
        self.transcript_service = TranscriptService()
        self.chunking_service = ChunkingService()
        self.translation_service = TranslationService()

        # Where translated chunks will be saved
        self.output_file = "translated_chunks.json"


    def load_existing_progress(self):
        """
        Load already translated chunks.
        This allows us to resume if the program stops.
        """

        if os.path.exists(self.output_file):
            with open(
                self.output_file,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        return []


    def save_progress(self, translated_chunks):
        """
        Save progress after every successful translation.
        """

        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                translated_chunks,
                file,
                ensure_ascii=False,
                indent=4
            )


    def process_video(self, video_id):

        print("\nFetching transcript...")

        transcript = self.transcript_service.get_transcript(
            video_id
        )

        print(
            f"Transcript segments found: {len(transcript)}"
        )

        # Create chunks
        chunks = self.chunking_service.chunk_transcript(
            transcript,
            max_words=150
        )

        print(f"Total chunks created: {len(chunks)}")

        # Load previous progress
        translated_chunks = self.load_existing_progress()

        start_index = len(translated_chunks)

        print(
            f"Already translated chunks: {start_index}"
        )

        print("\nStarting translation...\n")

        # Start from where we previously stopped
        for index in range(start_index, len(chunks)):

            chunk = chunks[index]

            print(
                f"Processing chunk "
                f"{index + 1}/{len(chunks)}"
            )

            try:

                translation = (
                    self.translation_service.translate_chunk(
                        chunk["text"]
                    )
                )

                translated_chunk = {
                    "chunk_index": index,
                    "original_text": chunk["text"],
                    "english_text": translation["english"],
                    "hinglish_text": translation["hinglish"],
                    "start_time": chunk["start_time"],
                    "end_time": chunk["end_time"]
                }

                translated_chunks.append(
                    translated_chunk
                )

                # Save immediately
                self.save_progress(
                    translated_chunks
                )

                print(
                    f"✓ Chunk {index + 1} completed"
                )

                # Small pause between API calls
                time.sleep(1)

            except Exception as error:

                print(
                    f"✗ Error processing chunk "
                    f"{index + 1}: {error}"
                )

                print(
                    "Stopping safely. "
                    "Run again to resume."
                )

                break

        print("\nProcessing finished!")
        print(
            f"Successfully translated: "
            f"{len(translated_chunks)} chunks"
        )

        return translated_chunks


if __name__ == "__main__":

    VIDEO_ID = "E3oG313_kps"

    batch_service = BatchTranslationService()

    batch_service.process_video(VIDEO_ID)