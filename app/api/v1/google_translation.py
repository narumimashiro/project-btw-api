import os
from fastapi import APIRouter, HTTPException
import requests
from typing import Optional
from pydantic import BaseModel

# for local
from dotenv import load_dotenv

router = APIRouter()

class Context(BaseModel):
    text: str
    lang: Optional[str] = 'en'

class TranslationResponse(BaseModel):
    translated_text: str

@router.post('/translation/', response_model=TranslationResponse)
def google_translation(context: Context):
    url = 'https://translation.googleapis.com/language/translate/v2'
    
    env = os.environ.get('ENV', 'development')
    if env == "development":
        load_dotenv('.env.local')

    API_KEY = os.environ.get('GOOGLE_TRANSLATION_API_KEY')

    if API_KEY is None:
        raise HTTPException(status_code=400, detail="Failed translation API: API key not found")

    params = {
        'q': context.text,
        'target': context.lang,
        'key': API_KEY
    }
    response = requests.post(url, params=params)

    if response.status_code == 200:
        result = response.json()
        translated_text = result['data']['translations'][0]['translatedText']
        return TranslationResponse(translated_text=translated_text)
    else:
        raise HTTPException(status_code=400, detail="Failed translation API: Failed google translation api")