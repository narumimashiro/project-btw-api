from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .v1.bangdream_live_event import router as bangdream_event_router
from .v1.google_translation import router as google_translation_router
from .v1.roshidere_wordlist import router as roshidere_word_list_router
from .v1.todo_webapp import router as todo_webapp_router

app = FastAPI(docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://next-project-btw.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Custom-Header", "Content-Type"]
)

app.include_router(bangdream_event_router, prefix="/api/v1", tags=['bangdream_events'])
app.include_router(google_translation_router, prefix="/api/v1", tags=['google_translation'])
app.include_router(roshidere_word_list_router, prefix="/api/v1", tags=['roshidere_wordlist'])
app.include_router(todo_webapp_router, prefix="/api/v1", tags=['todo_webapp'])
