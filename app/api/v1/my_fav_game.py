from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from api.core.firebase_config import get_firebase_client

router = APIRouter()

class MyFavGame(BaseModel):
    game_id: int
    uid: str
    game_title: str
    game_link: Optional[str] = None
    play_style: List[str]
    favorite_characters: List[str]
    favorite_points: List[str]

@router.get('/my-fav-game-list/', response_model=List[MyFavGame])
def get_my_fav_game_list():
    db = get_firebase_client()
    try:
        docs = db.collection('my-fav-games').stream()
        my_fav_game_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            my_fav_game_list.append({
                "game_id": doc_dict['game_id'],
                "uid": doc_dict['uid'],
                "game_title": doc_dict['game_title'] or '',
                "game_link": '',
                "play_style": doc_dict['play_style'] or [''],
                "favorite_characters": doc_dict['favorite_characters'] or [''],
                "favorite_points": doc_dict['favorite_points']
            })
        return my_fav_game_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed my fav game API: Failed to get my fav game list {str(e)}")