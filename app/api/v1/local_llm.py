from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import StreamingResponse
import json

class Message(BaseModel):
    role: str
    content: str
    
class ReqLocalLLM(BaseModel):
    prompt: str
    history: list[Message] = []
    model: str = "llama3.2"
    temperature: float = 0.3

router = APIRouter()

@router.post('/ollama_chat/')
def ollama_chat(req: ReqLocalLLM):
    
    client = OpenAI(
        api_key="ollama",
        base_url="http://localhost:11434/v1"
    )

    # 履歴をmessages配列に変換
    messages = [
        {"role": msg.role, "content": msg.content} 
        for msg in req.history
    ]
    
    # 現在のユーザーの質問を追加
    messages.append({"role": "user", "content": req.prompt})

    response = client.chat.completions.create(
        model=req.model,
        messages=messages,
        temperature=req.temperature
    )
    llm_response_text = response.choices[0].message.content
    
    return {"response": llm_response_text}

@router.post('/ollama_stream_chat/')
def ollama_steam_chat(req: ReqLocalLLM):
    
    client = OpenAI(
        api_key="ollama",
        base_url="http://localhost:11434/v1"
    )

    # 履歴をmessages配列に変換
    messages = [
        {"role": msg.role, "content": msg.content} 
        for msg in req.history
    ]
    
    # 現在のユーザーの質問を追加
    messages.append({"role": "user", "content": req.prompt})

    def generate():
        response = client.chat.completions.create(
            model=req.model,
            messages=messages,  # 修正: 履歴を含めたmessagesを使用
            temperature=req.temperature,
            stream=True
        )
        
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                # Server-Sent Events (SSE) 形式で送信
                yield f"data: {json.dumps({'content': content})}\n\n"
        
        # ストリーム終了を通知
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )