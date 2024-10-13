from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

class TaskCreate(BaseModel):
    task_title: str
    task_desc: str
    is_finished: Optional[bool] = False

class TaskUpdate(BaseModel):
    task_title: Optional[str]
    task_desc: Optional[str]
    is_finished: Optional[bool]

class TaskReplace(BaseModel):
    task_title: str
    task_desc: str
    is_finished: bool

def find_task_by_id(task_id: int):
    for task in task_db:
        if task["task_id"] == task_id:
            return task
    return None

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task_by_id(task_id)
    if task:
        return {"status": "ok", "data": task}
    raise HTTPException(status_code=404, detail={"error": "Task not found"})

@app.post("/tasks")
def create_task(task: TaskCreate):
    if not task.task_title.strip() or not task.task_desc.strip():
        raise HTTPException(status_code=400, detail={"error": "Task title and description cannot be empty"})
    
    new_task_id = max([task["task_id"] for task in task_db]) + 1 if task_db else 1
    new_task = {
        "task_id": new_task_id,
        "task_title": task.task_title,
        "task_desc": task.task_desc,
        "is_finished": task.is_finished,
    }
    task_db.append(new_task)
    return {"status": "ok", "data": new_task}

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    existing_task = find_task_by_id(task_id)
    
    if not existing_task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    if task.task_title is not None:
        if not task.task_title.strip():
            raise HTTPException(status_code=400, detail={"error": "Task title cannot be empty"})
        existing_task["task_title"] = task.task_title
    if task.task_desc is not None:
        if not task.task_desc.strip():
            raise HTTPException(status_code=400, detail={"error": "Task description cannot be empty"})
        existing_task["task_desc"] = task.task_desc
    if task.is_finished is not None:
        existing_task["is_finished"] = task.is_finished

    return {"status": "ok", "data": existing_task}

@app.put("/tasks/{task_id}")
def replace_task(task_id: int, task: TaskReplace):
    existing_task = find_task_by_id(task_id)
    
    if not existing_task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    existing_task["task_title"] = task.task_title
    existing_task["task_desc"] = task.task_desc
    existing_task["is_finished"] = task.is_finished
    
    return {"status": "ok", "data": existing_task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = find_task_by_id(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    task_db.remove(task)
    return {"status": "ok", "message": f"Task {task_id} deleted successfully"}