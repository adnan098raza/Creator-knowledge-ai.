# Podcast Knowledge AI

## Run the backend (Windows PowerShell)

From the repository root, create a fresh virtual environment if the existing one points to a missing Python installation:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Add `GROQ_API_KEY` to the root `.env` file. For vector storage, either set `QDRANT_PATH=qdrant_data` to use local on-disk Qdrant, or set `QDRANT_URL` and `QDRANT_API_KEY` for Qdrant Cloud (`QDRANT_PATH` takes precedence when set). With local storage, load the transcript chunks once with `python -m backend.services.ingestion_service`; stop the API first, since local Qdrant allows only one process to open the folder at a time. Start the API from the repository root so it can load `.env` and import the `backend` package:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/health` to check that the API is running and `http://127.0.0.1:8000/docs` for the interactive API. The embedding model loads on the first `/ask` request and may need to download once. The frontend expects the API at `http://127.0.0.1:8000`.
