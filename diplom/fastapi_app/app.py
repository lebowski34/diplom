from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='your_secret_key')

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

tasks = []
users = []

class Task(BaseModel):
    title: str
    completed: bool = False

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    username = request.session.get("username", None)
    return templates.TemplateResponse("home.html", {"request": request, "username": username, "users": users})

@app.get("/register/", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register/")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    if any(user['username'] == username for user in users):
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует.")
    users.append({"username": username, "password": password})
    request.session["username"] = username  # Сохраняем имя пользователя в сессии
    return RedirectResponse(url="/", status_code=303)

@app.get("/tasks/add/", response_class=HTMLResponse)
async def get_add_task(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})

@app.post("/tasks/add/")
async def add_task(request: Request, title: str = Form(...)):
    tasks.append(Task(title=title))
    return RedirectResponse(url="/tasks", status_code=303)

@app.get("/tasks/", response_class=HTMLResponse)
async def task_list(request: Request):
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks})

@app.get("/tasks/edit/{task_id}/", response_class=HTMLResponse)
async def edit_task(request: Request, task_id: int):
    task = tasks[task_id]
    return templates.TemplateResponse("edit_task.html", {"request": request, "task": task, "task_id": task_id})

@app.post("/tasks/edit/{task_id}/")
async def update_task(request: Request, task_id: int, title: str = Form(...)):
    tasks[task_id].title = title
    return RedirectResponse(url="/tasks", status_code=303)

@app.post("/tasks/delete/{task_id}/")
async def delete_task(request: Request, task_id: int):
    if task_id < len(tasks):
        tasks.pop(task_id)
    return RedirectResponse(url="/tasks", status_code=303)
