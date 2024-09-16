import os
from fastapi import APIRouter
import requests
from typing import Optional
from pydantic import BaseModel

# for local
from dotenv import load_dotenv

router = APIRouter()

class Context(BaseModel):
    text: str
    lang: Optional[str] = 'en'

@router.post('/translation/', tags=['google_translation'])
def google_translation(context: Context):
    url = 'https://translation.googleapis.com/language/translate/v2'
    if os.getenv("VERCEL_ENV") is None:
        load_dotenv('.env.local')

    API_KEY = os.environ.get('GOOGLE_TRANSLATION_API_KEY')
    params = {
        'q': context.text,
        'target': context.lang,
        'key': API_KEY
    }
    response = requests.post(url, params=params)

    if response.status_code == 200:
        result = response.json()
        translated_text = result['data']['translations'][0]['translatedText']
        return {"translated_text": translated_text}
    else:
        return {"message": "failed translation api"}