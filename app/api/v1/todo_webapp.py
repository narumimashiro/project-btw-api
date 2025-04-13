from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from api.core.firebase_config import get_firebase_client

router = APIRouter()

# AppType List
APPTYPE_LIST = {"collaboration"}

# Database Name
DB_NAME_COLLABORATION = 'collaboration_todo_task'

class TodoTask(BaseModel):
    task_summary: str
    task_description: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[datetime] = None

class ReqRegisterTodoTask(BaseModel):
    app_type: str
    task_info: TodoTask

class ResRegisterTodoTask(BaseModel):
    unique_task_id: str
    task_summary: str
    task_description: str
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    registration_date: datetime
    update_date: datetime
    task_status: int

@router.post('/register-todo-task/', response_model=ResRegisterTodoTask)
def register_todo_task(req: ReqRegisterTodoTask):
    if req.app_type not in APPTYPE_LIST:
        raise HTTPException(status_code=400, detail=f'No such app type: {req.app_type}')
    
    db = get_firebase_client()
        
    try:
        now = datetime.now()
        _, doc_ref = db.collection(DB_NAME_COLLABORATION).add({
            "task_summary": req.task_info.task_summary,
            "task_description": req.task_info.task_description or '',
            "priority": req.task_info.priority,
            "due_date": req.task_info.due_date,
            "registration_date": now,
            "update_date": now,
            "task_status": 0
        })

        doc_id = doc_ref.id

        return ResRegisterTodoTask(
            unique_task_id=doc_id,
            task_summary=req.task_info.task_summary,
            task_description=req.task_info.task_description or '',
            priority=req.task_info.priority,
            due_date=req.task_info.due_date,
            registration_date=now,
            update_date=now,
            task_status=0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: Failed to register {str(e)}")
    
@router.get('/get-todo-task-list/', response_model=List[ResRegisterTodoTask])
def get_todo_task():
    db = get_firebase_client()

    try:
        docs = db.collection(DB_NAME_COLLABORATION).stream()

        res_data = []
        for doc in docs:
            data = doc.to_dict()
            id = str(doc.id)
            res_data.append({
                "unique_task_id": id,
                "task_summary": data['task_summary'],
                "task_description": data['task_description'],
                "priority": data['priority'],
                "due_date": data['due_date'],
                "registration_date": data['registration_date'],
                "update_date": data['update_date'],
                "task_status": data['task_status']
            })
        return res_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: Failed to get task list {str(e)}")

class ReqDeleteTodoTask(BaseModel):
    unique_task_id: List[str]

class ResDeleteTodoTask(BaseModel):
    success: List[str]
    failed: List[str]

@router.post('/delete-todo-task', response_model=List[ResDeleteTodoTask])
def delete_todo_task(req: ReqDeleteTodoTask):

    if not req.unique_task_id:
        raise HTTPException(status_code=400, detail='No task id provided')

    db = get_firebase_client()

    success_task_ids = []
    failed_task_ids = []

    for task_id in req.unique_task_id:
        try:
            doc_ref = db.collection(DB_NAME_COLLABORATION).document(task_id)
            doc_ref.delete()
            success_task_ids.append(task_id)
        except Exception as e:
            failed_task_ids.append(task_id)

    return ResDeleteTodoTask(
        success=success_task_ids,
        failed=failed_task_ids
    )