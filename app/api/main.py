from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .v1.bangdream_live_event import router as bangdream_event_router
from .v1.google_translation import router as google_translation_router
from .v1.roshidere_wordlist import router as roshidere_word_list_router
from .v1.todo_webapp import router as todo_webapp_router
from .v1.my_fav_game import router as my_fav_game_router

# for local
from dotenv import load_dotenv

env = os.environ.get('ENV', 'development')
if env == "development":
    load_dotenv('.env.local')

allow_origins = os.getenv('ALLOWED_ORIGINS', '').split(',')

app = FastAPI(docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Custom-Header", "Content-Type"]
)

app.include_router(bangdream_event_router, prefix="/api/v1", tags=['bangdream_events'])
app.include_router(google_translation_router, prefix="/api/v1", tags=['google_translation'])
app.include_router(roshidere_word_list_router, prefix="/api/v1", tags=['roshidere_wordlist'])
app.include_router(todo_webapp_router, prefix="/api/v1", tags=['todo_webapp'])
app.include_router(my_fav_game_router, prefix="/api/v1", tags=['my_fav_game'])