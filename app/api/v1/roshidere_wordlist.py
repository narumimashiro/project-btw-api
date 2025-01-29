from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from api.core.firebase_config import get_firebase_client

DB_NAME = 'roshirede_word_list'

router = APIRouter()

class Word(BaseModel):
    word_native_lang: str
    word_foreign_lang: str

class WordInfo(BaseModel):
    word_native_lang: str
    word_foreign_lang: str
    registration_date: datetime

class WordListItem(BaseModel):
    id: str
    word_native_lang: str
    word_foreign_lang: str
    registration_date: datetime

@router.post('/wordRegistration/', response_model=WordInfo)
def word_registration(word: Word):
    db = get_firebase_client()
    try:
        now = datetime.now()
        db.collection(DB_NAME).add({
            "word_native_lang": word.word_native_lang,
            "word_foreign_lang": word.word_foreign_lang,
            "registration_date": now
        })
        return WordInfo(
            word_native_lang=word.word_native_lang,
            word_foreign_lang=word.word_foreign_lang,
            registration_date=now)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed wordlist API: Failed to register {str(e)}")
    
@router.get('/getWordlist/', response_model=List[WordListItem])
def get_word_list():
    db = get_firebase_client()
    try:
        docs = db.collection(DB_NAME).stream()

        res_data = []
        for doc in docs:
            data = doc.to_dict()
            id = str(doc.id)
            res_data.append({
                "id": id,
                "word_native_lang": data['word_native_lang'],
                "word_foreign_lang": data['word_foreign_lang'],
                "registration_date": data['registration_date']
            })
        return res_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed wordlist API: Failed to get wordlist {str(e)}")