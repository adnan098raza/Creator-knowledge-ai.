
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qdrant_client.http.exceptions import ResponseHandlingException

app = FastAPI(
    title="Podcast Knowledge AI",
    description="Ask questions about podcast content",
    version="1.0.0"
)


# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class QuestionRequest(BaseModel):
    question: str


@lru_cache(maxsize=1)
def get_answer_service():
    """Build the model and external service clients when the first answer is requested."""
    from backend.services.answer_service import AnswerService

    return AnswerService()


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "SIGNAL Podcast Intelligence API is running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        # Generate answer and retrieve relevant podcast chunks
        answer, search_results = get_answer_service().answer_question(
            request.question
        )

        # Build source references from retrieved chunks
        sources = []

        for result in search_results:
            payload = result.payload or {}

            sources.append({
                "chunk_index": payload.get("chunk_index"),
                "start_time": payload.get("start_time"),
                "end_time": payload.get("end_time"),
                "text": payload.get("english_text", "")
            })

        return {
            "answer": answer,
            "sources": sources
        }

    except HTTPException:
        # Preserve intentional HTTP errors
        raise

    except ResponseHandlingException as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Could not connect to Qdrant. Check QDRANT_URL, "
                "QDRANT_API_KEY, and access to the Qdrant Cloud endpoint."
            ),
        ) from exc

    except Exception as exc:
        # Temporary debugging: print the full traceback
        import traceback

        print(f"Error processing question: {exc}")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Failed to process the question. Check the backend terminal."
        ) from exc
