import os
import re

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class TranslationService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )


    def translate_chunk(self, text: str):

        prompt = f"""
Translate this Hindi podcast transcript into two versions.

1. Natural English translation
2. Hinglish transliteration (Hindi written using Roman/English alphabet)

Rules:
- Preserve the original meaning.
- Do not summarize.
- Do not add information.
- Keep names and technical terms accurate.

Return in exactly this structure:

ENGLISH
<English translation>

HINGLISH
<Hinglish transliteration>

TRANSCRIPT:
{text}
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_completion_tokens=3000,
            reasoning_effort="low"
        )

        result = response.choices[0].message.content

        print("\nRAW RESPONSE:")
        print(repr(result))

        if not result or not result.strip():
            raise ValueError(
                "Groq returned an empty response."
            )

        # Remove markdown bold formatting
        cleaned_result = result.replace("**", "").strip()

        # Extract English text
        english_match = re.search(
            r"ENGLISH\s*:?\s*(.*?)\s*HINGLISH\s*:?",
            cleaned_result,
            re.DOTALL | re.IGNORECASE
        )

        # Extract Hinglish text
        hinglish_match = re.search(
            r"HINGLISH\s*:?\s*(.*)",
            cleaned_result,
            re.DOTALL | re.IGNORECASE
        )

        if not english_match or not hinglish_match:

            print("\nCLEANED RESPONSE:")
            print(cleaned_result)

            raise ValueError(
                "Could not parse translation response."
            )

        english = english_match.group(1).strip()
        hinglish = hinglish_match.group(1).strip()

        return {
            "english": english,
            "hinglish": hinglish
        }