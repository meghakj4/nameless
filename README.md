
# nameless — PDF-based CLI Chatbot

A command-line chatbot that answers questions using content extracted from PDF(s).

## Repo layout (important files)
-  `script.py` — main CLI launcher; loads the latest trained model and starts the chat.

-  `one_timer/create_syllab_iq_model.py` — run once to build a model from PDFs and save to `models/` as `syllab_iq_{timestamp}.pkl`.

-  `model_loader.py` — helper used by `script.py` to load the latest model from `models/`.

-  `vector_store_manager.py` — vector store manager that handles PDF loading, chunking, embeddings and FAISS index.

-  `gemini_embeddings.py` / `gemini_free_embeddings.py` — custom embeddings wrappers (project uses existing embedding and LLM code; do not change models).

-  `chat_bot.py` — chat loop that composes prompts and queries the loaded vector store + LLM.

-  `models/` — directory for saved one-time trained models (created by `one_timer` script).

-  `pdfs/` — optional folder to place PDFs to be learned.

-  `.env` — environment variables (e.g. `GOOGLE_API_KEY`) — NOT committed (see `.gitignore`).

-  `.gitignore` — configured to ignore `venv`, `.env`, `models/*`, `pdfs/*`, build artifacts.

## Quickstart (Windows)

1. Create & activate virtual env

```powershell
python -m venv venv

venv\Scripts\activate
```

2. Install dependencies
```powershell
pip install -r requirements.txt
```
3. Add API key
Create a `.env` in project root with:
```text
GOOGLE_API_KEY=your_api_key_here
```

4. Place PDFs
Put PDFs you want the model to learn into the `pdfs/` folder OR rely on the configured specific path used by the create script.

5. Create the one-time model
Run:
```powershell
python one_timer/create_syllab_iq_model.py
```

This generates a model file in `models/` named like:
```text
models/syllab_iq_YYYYmmdd_HHMMSS.pkl
```
What the create script does:
- reads PDFs
- builds FAISS index with configured embeddings
- saves a pickled `VectorStoreManager` instance as the model snapshot

6. Run the chatbot
```powershell
python script.py
```
`script.py` automatically loads the latest `syllab_iq_*.pkl` from `models/`.

Inside the chat you can:
- ask questions normally
- use `add-pdf` to append a new PDF to the loaded vector store (which will save the updated store)
- use `info` to inspect store stats
- use `exit` or `quit` to end the session

## Behavior & Notes
- One-time learning: after you run the create script, `script.py` uses the saved model and does not re-learn PDFs on each run.
- Adding PDFs after model creation:
- Use `add-pdf` while the bot is running or re-run the create script to produce a fresh snapshot.
-  `VectorStoreManager` avoids re-indexing files already present (it uses metadata/hash).
- Embeddings/LLM:
- The project keeps the existing embedding and LLM configurations — do not change them unless you understand the consequences.
- Ensure `GOOGLE_API_KEY` is set in `.env`.
- If using local HuggingFace embeddings, the model will be downloaded on first run.