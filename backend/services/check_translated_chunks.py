import json
from pathlib import Path


def main():

    # Path to translated chunks
    file_path = Path("translated_chunks.json")

    if not file_path.exists():
        print("❌ translated_chunks.json not found!")
        return

    # Load JSON
    with open(file_path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    print("=" * 60)
    print("TRANSLATED CHUNKS VALIDATION")
    print("=" * 60)

    print(f"\nTotal chunks: {len(chunks)}")

    # Check required fields
    required_fields = [
        "chunk_index",
        "original_text",
        "english_text",
        "hinglish_text",
        "start_time",
        "end_time"
    ]

    valid_chunks = 0
    invalid_chunks = []

    for chunk in chunks:

        missing_fields = []

        for field in required_fields:
            if field not in chunk:
                missing_fields.append(field)

        if missing_fields:
            invalid_chunks.append({
                "chunk_index": chunk.get("chunk_index", "Unknown"),
                "missing": missing_fields
            })
        else:
            valid_chunks += 1

    print(f"Valid chunks: {valid_chunks}")
    print(f"Invalid chunks: {len(invalid_chunks)}")

    # Check empty translations
    empty_english = []
    empty_hinglish = []

    for chunk in chunks:

        if not chunk.get("english_text", "").strip():
            empty_english.append(chunk["chunk_index"])

        if not chunk.get("hinglish_text", "").strip():
            empty_hinglish.append(chunk["chunk_index"])

    print("\nTranslation Checks:")
    print(f"Empty English translations: {len(empty_english)}")
    print(f"Empty Hinglish translations: {len(empty_hinglish)}")

    # Show sample
    print("\n" + "=" * 60)
    print("SAMPLE CHUNK")
    print("=" * 60)

    if chunks:

        sample = chunks[0]

        print(f"\nChunk Index: {sample['chunk_index']}")
        print(f"Timestamp: {sample['start_time']} - {sample['end_time']}")

        print("\nORIGINAL:")
        print(sample["original_text"][:300])

        print("\nENGLISH:")
        print(sample["english_text"][:300])

        print("\nHINGLISH:")
        print(sample["hinglish_text"][:300])

    # Final status
    print("\n" + "=" * 60)

    if valid_chunks == len(chunks) and not empty_english and not empty_hinglish:
        print("✅ ALL CHUNKS ARE VALID!")
        print("Ready for embedding and Qdrant storage.")
    else:
        print("⚠️ SOME ISSUES FOUND!")
        print("Review invalid or empty chunks.")

    print("=" * 60)


if __name__ == "__main__":
    main()