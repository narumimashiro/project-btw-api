from fastapi import APIRouter
import httpx
from bs4 import BeautifulSoup

router = APIRouter()

@router.get('/bangdream_events_info/')
async def bang_dream_events():
    base_url = "https://bang-dream.com"
    bang_dream_event_base_url = f"{base_url}/events?page={{pageindex}}"
    event_all_info = []
    async with httpx.AsyncClient() as client:
        for page_index in range(1, 4):
            url = bang_dream_event_base_url.format(pageindex=page_index)
            response = await client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            event_info = soup.find('ul', class_='liveEventList')
            event_all_info.append(event_info)
        
    bang_dream_event_list = []
    for info in event_all_info:
        if info:
            info_html = info.find_all('li')
            for item in info_html:
                event_url = item.find('a').get('href')
                event_title = item.find('p', class_='liveEventListTitle')
                event_date_place = item.find_all('div', class_='itemInfoColumnData')
                event_date = event_date_place[0].get_text().strip() if len(event_date_place) > 0 else 'N/A'
                event_place = event_date_place[1].get_text().strip() if len(event_date_place) > 1 else 'N/A'
                event_title_text = event_title.get_text().strip() if event_title else 'N/A'

                bang_dream_event_list.append({
                    "event_url": f'{base_url}{event_url}' if event_url else 'N/A',
                    "event_title": event_title_text,
                    "event_date": event_date,
                    "event_place": event_place
                })
        else:
            return {"message": "Failed get event information"}
    return bang_dream_event_list